
import streamlit as st
import sqlite3
import csv
import io
import os
import uuid
from collections import Counter

# =========================================
# 1. 페이지 설정
# =========================================

st.set_page_config(
    page_title="학생 디저트 선호도 분석",
    page_icon="🍰",
    layout="wide"
)

st.title("🍰 학생 디저트 선호도 분석")
st.write(
    "보성군 차 음식 및 디저트 공공데이터를 활용하여 "
    "학생들의 디저트 선호도를 조사합니다."
)

st.divider()

# =========================================
# 2. 데이터베이스 생성
# =========================================

DB_NAME = "dessert_survey.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT UNIQUE,
            dessert TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

create_table()

# =========================================
# 3. 공공데이터 CSV 불러오기
# =========================================

st.header("📂 1. 공공데이터 불러오기")

st.write(
    "공공데이터포털에서 다운로드한 "
    "보성군 차 음식 및 디저트 CSV 파일을 사용합니다."
)

st.markdown(
    "[공공데이터 원본 다운로드 페이지](https://www.data.go.kr/data/15111850/fileData.do)"
)

uploaded_file = st.file_uploader(
    "다운로드한 CSV 파일을 업로드하세요.",
    type=["csv"]
)

def read_csv_file(file_content):

    # UTF-8 또는 한글 CSV 인코딩 처리
    try:
        content = file_content.decode("utf-8-sig")
    except UnicodeDecodeError:
        content = file_content.decode("cp949")

    reader = csv.DictReader(io.StringIO(content))

    rows = []

    for row in reader:
        # 컬럼명 앞뒤 공백 제거
        cleaned = {
            str(key).strip(): (
                value.strip() if value else ""
            )
            for key, value in row.items()
            if key is not None
        }

        rows.append(cleaned)

    return rows


dataset = []

if uploaded_file is not None:

    try:
        dataset = read_csv_file(uploaded_file.getvalue())

        st.success("공공데이터 CSV를 불러왔습니다!")

    except Exception as e:

        st.error("CSV 파일을 읽지 못했습니다.")
        st.code(str(e))

elif os.path.exists("desserts.csv"):

    try:
        with open("desserts.csv", "rb") as file:
            dataset = read_csv_file(file.read())

        st.success("프로젝트 폴더의 desserts.csv를 불러왔습니다!")

    except Exception as e:

        st.error("CSV 파일을 읽지 못했습니다.")
        st.code(str(e))

else:

    st.warning(
        "아직 CSV 파일이 없습니다. "
        "공공데이터포털에서 파일을 다운로드한 뒤 업로드해주세요."
    )

# =========================================
# 4. 실제 데이터 컬럼 확인
# =========================================

required_columns = [
    "요리명",
    "주재료",
    "부재료",
    "조리법",
    "상세설명",
    "데이터기준일자"
]

data_valid = False

if dataset:

    missing_columns = [
        column
        for column in required_columns
        if column not in dataset[0]
    ]

    if missing_columns:

        st.error(
            "CSV 파일의 컬럼명이 공공데이터 원본과 다릅니다."
        )

        st.write("확인되지 않은 컬럼:", missing_columns)

    else:

        data_valid = True

        st.subheader("공공데이터 미리보기")

        st.dataframe(
            dataset,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "불러온 데이터 개수",
            str(len(dataset)) + "개"
        )

# =========================================
# 5. 디저트 목록 자동 생성
# =========================================

dessert_data = {}

if data_valid:

    for row in dataset:

        name = row["요리명"].strip()

        if name:

            dessert_data[name] = {
                "주재료": row["주재료"],
                "부재료": row["부재료"],
                "조리법": row["조리법"],
                "상세설명": row["상세설명"],
                "데이터기준일자": row["데이터기준일자"]
            }

dessert_list = list(dessert_data.keys())

st.divider()

# =========================================
# 6. 디저트 정보 확인
# =========================================

st.header("🍵 2. 공공데이터 디저트 정보")

if data_valid and dessert_list:

    selected_info = st.selectbox(
        "자세히 알아볼 디저트를 선택하세요.",
        dessert_list
    )

    info = dessert_data[selected_info]

    st.subheader("🍰 " + selected_info)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**주재료**")
        st.write(info["주재료"] or "정보 없음")

        st.markdown("**부재료**")
        st.write(info["부재료"] or "정보 없음")

    with col2:

        st.markdown("**상세설명**")
        st.write(info["상세설명"] or "정보 없음")

        st.markdown("**데이터기준일자**")
        st.write(info["데이터기준일자"] or "정보 없음")

    with st.expander("조리법 확인하기"):

        st.write(info["조리법"] or "조리법 정보 없음")

else:

    st.info("먼저 공공데이터 CSV 파일을 불러와주세요.")

st.divider()

# =========================================
# 7. 익명 투표 준비
# =========================================

st.header("🗳️ 3. 학생 익명 선호도 투표")

st.write(
    "공공데이터에 등록된 디저트 중 "
    "가장 선호하는 메뉴를 선택해주세요."
)

# 브라우저 세션별 익명 식별자
if "voter_id" not in st.session_state:

    st.session_state.voter_id = str(uuid.uuid4())


def has_voted(voter_id):

    conn = connect_db()

    result = conn.execute(
        """
        SELECT id
        FROM votes
        WHERE voter_id = ?
        """,
        (voter_id,)
    ).fetchone()

    conn.close()

    return result is not None


# =========================================
# 8. 투표 입력
# =========================================

if data_valid and dessert_list:

    if has_voted(st.session_state.voter_id):

        st.success("현재 브라우저 세션에서는 이미 투표했습니다.")

    else:

        with st.form("vote_form"):

            vote_dessert = st.selectbox(
                "가장 좋아하는 디저트는 무엇인가요?",
                dessert_list
            )

            vote_rating = st.slider(
                "선택한 디저트를 얼마나 좋아하나요?",
                min_value=1,
                max_value=5,
                value=5
            )

            vote_submit = st.form_submit_button(
                "익명 투표 제출하기",
                use_container_width=True
            )

            if vote_submit:

                conn = connect_db()

                try:

                    conn.execute(
                        """
                        INSERT INTO votes
                        (voter_id, dessert, rating)
                        VALUES (?, ?, ?)
                        """,
                        (
                            st.session_state.voter_id,
                            vote_dessert,
                            vote_rating
                        )
                    )

                    conn.commit()

                    st.success("투표가 저장되었습니다!")

                    st.rerun()

                except sqlite3.IntegrityError:

                    st.warning("이미 투표한 세션입니다.")

                finally:

                    conn.close()

else:

    st.info(
        "공공데이터 CSV를 불러오면 "
        "학생 투표 기능이 활성화됩니다."
    )

st.divider()

# =========================================
# 9. 투표 결과 불러오기
# =========================================

def get_votes():

    conn = connect_db()

    rows = conn.execute(
        """
        SELECT dessert, rating
        FROM votes
        """
    ).fetchall()

    conn.close()

    return rows


votes = get_votes()

total_votes = len(votes)

vote_counts = Counter(
    dessert for dessert, rating in votes
)

# =========================================
# 10. 전체 투표 현황
# =========================================

st.header("📊 4. 전체 투표 현황")

col1, col2, col3 = st.columns(3)

col1.metric(
    "총 투표 수",
    str(total_votes) + "명"
)

col2.metric(
    "조사 디저트 수",
    str(len(dessert_list)) + "종"
)

if vote_counts:

    popular_dessert = vote_counts.most_common(1)[0][0]

else:

    popular_dessert = "아직 없음"

col3.metric(
    "현재 인기 디저트",
    popular_dessert
)

st.divider()

# =========================================
# 11. 디저트별 득표수 그래프
# =========================================

st.header("🏆 5. 디저트별 선호도 순위")

if total_votes > 0:

    dessert_counts = {
        name: vote_counts.get(name, 0)
        for name in dessert_list
    }

    sorted_counts = dict(
        sorted(
            dessert_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    st.subheader("디저트별 투표 수")

    st.bar_chart(sorted_counts)

    st.caption(
        "막대가 길수록 해당 디저트를 선택한 학생이 많습니다."
    )

    st.subheader("디저트별 선호 비율")

    percentages = {
        name: round(count / total_votes * 100, 1)
        for name, count in sorted_counts.items()
    }

    st.bar_chart(percentages)

    st.caption(
        "각 디저트의 득표수를 전체 투표 수로 나눈 비율입니다."
    )

else:

    st.info(
        "아직 투표 결과가 없습니다. "
        "학생들이 투표하면 그래프가 자동으로 생성됩니다."
    )

st.divider()

# =========================================
# 12. 평균 선호도 그래프
# =========================================

st.header("⭐ 6. 디저트별 평균 선호도")

if total_votes > 0:

    rating_data = {}

    for dessert, rating in votes:

        if dessert not in rating_data:

            rating_data[dessert] = []

        rating_data[dessert].append(rating)

    average_ratings = {}

    for dessert, ratings in rating_data.items():

        average_ratings[dessert] = round(
            sum(ratings) / len(ratings),
            2
        )

    sorted_ratings = dict(
        sorted(
            average_ratings.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    st.bar_chart(sorted_ratings)

    best_dessert = max(
        average_ratings,
        key=average_ratings.get
    )

    st.success(
        "평균 선호도 1위: " + best_dessert
    )

else:

    st.info("아직 평균 선호도를 계산할 수 없습니다.")

st.divider()

# =========================================
# 13. 상세 조사 결과
# =========================================

st.header("📋 7. 조사 결과 상세표")

if total_votes > 0:

    result_rows = []

    for dessert in dessert_list:

        count = vote_counts.get(dessert, 0)

        ratings = rating_data.get(dessert, [])

        average = (
            round(sum(ratings) / len(ratings), 2)
            if ratings else 0
        )

        percentage = round(
            count / total_votes * 100,
            1
        )

        result_rows.append({
            "디저트": dessert,
            "투표 수": count,
            "선호 비율(%)": percentage,
            "평균 선호도": average
        })

    result_rows.sort(
        key=lambda row: row["투표 수"],
        reverse=True
    )

    st.dataframe(
        result_rows,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("투표가 모이면 상세 결과가 나타납니다.")

st.divider()

# =========================================
# 14. CSV 다운로드
# =========================================

st.header("💾 8. 조사 결과 다운로드")

if total_votes > 0:

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=[
            "디저트",
            "투표 수",
            "선호 비율(%)",
            "평균 선호도"
        ]
    )

    writer.writeheader()
    writer.writerows(result_rows)

    st.download_button(
        label="📥 전체 조사 결과 다운로드",
        data=output.getvalue().encode("utf-8-sig"),
        file_name="학생_디저트_선호도_결과.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info("아직 다운로드할 조사 결과가 없습니다.")

st.divider()

# =========================================
# 15. 데이터 출처
# =========================================

st.header("📚 데이터 출처 및 분석 방법")

st.markdown(
    """
    **데이터 출처:** 전남광주통합특별시 보성군

    **데이터명:** 차 음식 및 디저트 정보

    **활용 항목:**
    - 요리명
    - 주재료
    - 부재료
    - 조리법
    - 상세설명
    - 데이터기준일자

    **분석 방법:**
    - 실제 학생 익명 투표 수집
    - 디저트별 득표수 계산
    - 전체 투표 대비 선호 비율 계산
    - 평균 선호도 계산
    """
)

st.caption(
    "※ 이 결과는 실제 투표된 응답만을 분석합니다. "
    "투표하지 않은 학생의 의견은 포함되지 않습니다."
)

