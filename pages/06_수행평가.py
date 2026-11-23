
import streamlit as st
import sqlite3
import csv
import io
import os
import uuid
from collections import Counter

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="학생 디저트 선호도 조사",
    page_icon="🍰",
    layout="wide"
)

st.title("🍰 학생 디저트 선호도 조사")
st.write(
    "학생들이 직접 익명으로 투표하면 "
    "결과를 자동으로 수집하고 그래프로 분석합니다."
)

st.divider()

# ==========================================
# 2. 데이터베이스 설정
# ==========================================

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

# ==========================================
# 3. 디저트 목록 불러오기
# ==========================================

def load_desserts():

    desserts = []

    # 프로젝트 폴더에 CSV가 있으면 자동으로 읽기
    if os.path.exists("desserts.csv"):

        try:
            with open(
                "desserts.csv",
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:
                    name = row.get("요리명", "").strip()

                    if name:
                        desserts.append(name)

        except UnicodeDecodeError:
            with open(
                "desserts.csv",
                "r",
                encoding="cp949",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:
                    name = row.get("요리명", "").strip()

                    if name:
                        desserts.append(name)

        except Exception:
            desserts = []

    # CSV가 없으면 기본 목록 사용
    if not desserts:
        desserts = [
            "고구마녹차케이크",
            "그린티 스무디",
            "홍차 에이드",
            "녹차 쿠키",
            "녹차 라떼"
        ]

    return sorted(set(desserts))


dessert_list = load_desserts()

# ==========================================
# 4. 학생별 익명 투표
# ==========================================

st.header("🗳️ 1. 디저트 선호도 투표")

st.info(
    "가장 좋아하는 디저트 하나를 선택하고 "
    "선호도 점수를 남겨주세요. 투표는 익명으로 저장됩니다."
)

# 브라우저 세션별 투표 식별자
if "voter_id" not in st.session_state:
    st.session_state.voter_id = str(uuid.uuid4())

# 이미 투표했는지 확인
def has_voted(voter_id):

    conn = connect_db()

    result = conn.execute(
        "SELECT id FROM votes WHERE voter_id = ?",
        (voter_id,)
    ).fetchone()

    conn.close()

    return result is not None


already_voted = has_voted(st.session_state.voter_id)

if already_voted:

    st.success("이미 투표가 완료되었습니다!")

    st.write(
        "현재 브라우저 세션에서는 중복 투표할 수 없습니다."
    )

else:

    with st.form("dessert_vote_form"):

        selected_dessert = st.selectbox(
            "가장 좋아하는 디저트는 무엇인가요?",
            dessert_list
        )

        selected_rating = st.slider(
            "이 디저트를 얼마나 좋아하나요?",
            min_value=1,
            max_value=5,
            value=5
        )

        submitted = st.form_submit_button(
            "익명 투표하기",
            use_container_width=True
        )

        if submitted:

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
                        selected_dessert,
                        selected_rating
                    )
                )

                conn.commit()

                st.success("투표가 정상적으로 저장되었습니다!")

                st.rerun()

            except sqlite3.IntegrityError:
                st.warning("이미 투표한 세션입니다.")

            finally:
                conn.close()

st.divider()

# ==========================================
# 5. 투표 결과 불러오기
# ==========================================

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

# ==========================================
# 6. 전체 투표 현황
# ==========================================

st.header("📊 2. 전체 투표 현황")

total_votes = len(votes)

vote_counts = Counter(
    dessert for dessert, rating in votes
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "총 투표 수",
    f"{total_votes}명"
)

col2.metric(
    "조사 대상 디저트",
    f"{len(dessert_list)}종"
)

if vote_counts:

    popular_dessert = vote_counts.most_common(1)[0][0]

else:

    popular_dessert = "아직 없음"

col3.metric(
    "현재 인기 1위",
    popular_dessert
)

st.divider()

# ==========================================
# 7. 디저트별 선호도 그래프
# ==========================================

st.header("🏆 3. 디저트별 선호도 순위")

if total_votes > 0:

    dessert_counts = {}

    for dessert in dessert_list:
        dessert_counts[dessert] = vote_counts.get(
            dessert, 0
        )

    # 득표수가 많은 순서로 정렬
    sorted_counts = dict(
        sorted(
            dessert_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    st.subheader("디저트별 투표 수")

    st.bar_chart(sorted_counts)

    st.subheader("디저트별 선호 비율")

    percentages = {}

    for dessert, count in sorted_counts.items():

        percentages[dessert] = round(
            count / total_votes * 100,
            1
        )

    st.bar_chart(percentages)

    st.caption(
        "선호 비율은 전체 투표 수에서 "
        "각 디저트가 차지하는 비율입니다."
    )

else:

    st.info(
        "아직 투표 결과가 없습니다. "
        "학생들이 투표하면 그래프가 자동으로 나타납니다."
    )

st.divider()

# ==========================================
# 8. 디저트별 평균 선호도
# ==========================================

st.header("⭐ 4. 디저트별 평균 선호도")

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

    best_rating_dessert = max(
        average_ratings,
        key=average_ratings.get
    )

    st.success(
        "평균 선호도 1위: "
        + best_rating_dessert
    )

else:

    st.info("아직 분석할 선호도 자료가 없습니다.")

st.divider()

# ==========================================
# 9. 상세 조사 결과
# ==========================================

st.header("📋 5. 조사 결과 상세 분석")

if total_votes > 0:

    st.write("디저트별 조사 결과")

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

    st.info("투표가 시작되면 상세 결과가 표시됩니다.")

st.divider()

# ==========================================
# 10. 조사 결과 CSV 다운로드
# ==========================================

st.header("💾 6. 조사 결과 다운로드")

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
        label="📥 조사 결과 CSV 다운로드",
        data=output.getvalue().encode("utf-8-sig"),
        file_name="학생_디저트_선호도_결과.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info("투표 결과가 생기면 다운로드할 수 있습니다.")

st.divider()

# ==========================================
# 11. 데이터 출처 및 안내
# ==========================================

st.header("📚 데이터 출처")

st.write(
    "디저트 목록 참고 자료: "
    "공공데이터포털 보성군 차 음식 및 디저트 정보"
)

st.markdown(
    "[공공데이터 원본 페이지](https://www.data.go.kr/data/15111850/fileData.do)"
)

st.caption(
    "※ 디저트 목록은 공공데이터를 참고하며, "
    "선호도 결과는 실제 학생들의 익명 투표로 수집합니다."
)

st.caption(
    "※ 이 프로그램은 브라우저 세션 기준으로 중복 투표를 제한합니다. "
    "다른 브라우저나 기기에서의 중복 투표까지 막는 기능은 아닙니다."
)
