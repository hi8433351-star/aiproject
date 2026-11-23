
import streamlit as st
import csv
import io

# =====================================
# 1. 페이지 설정
# =====================================

st.set_page_config(
    page_title="학생별 디저트 선호도 분석",
    page_icon="🍰",
    layout="wide"
)

# =====================================
# 2. 프로그램 제목
# =====================================

st.title("🍰 학생별 디저트 선호도 분석")
st.write("공공데이터를 활용한 학생별 디저트 선호도 조사")

st.divider()

# =====================================
# 3. 공공데이터 CSV 업로드
# =====================================

st.header("📁 1. 디저트 데이터 불러오기")

uploaded_file = st.file_uploader(
    "공공데이터 CSV 파일을 업로드하세요.",
    type=["csv"]
)

# 기본 디저트 목록
dessert_list = [
    "녹차 케이크",
    "그린티 스무디",
    "홍차 에이드",
    "녹차 쿠키",
    "녹차 라떼"
]

if uploaded_file is not None:
    try:
        raw_data = uploaded_file.getvalue()

        try:
            content = raw_data.decode("utf-8-sig")
        except UnicodeDecodeError:
            content = raw_data.decode("cp949")

        reader = csv.DictReader(io.StringIO(content))
        csv_data = list(reader)

        # CSV에서 요리명 가져오기
        if csv_data and "요리명" in csv_data[0]:
            dessert_list = list(dict.fromkeys(
                row["요리명"].strip()
                for row in csv_data
                if row.get("요리명", "").strip()
            ))

            st.success("공공데이터를 성공적으로 불러왔습니다.")
            st.dataframe(csv_data, use_container_width=True)

        else:
            st.warning(
                "CSV 파일에 '요리명' 항목이 없습니다. "
                "기본 디저트 목록을 사용합니다."
            )

    except Exception as e:
        st.error("CSV 파일을 읽는 중 오류가 발생했습니다.")
        st.write(str(e))

else:
    st.info("CSV를 업로드하지 않으면 기본 디저트 목록을 사용합니다.")

st.divider()

# =====================================
# 4. 학생별 선호도 입력
# =====================================

st.header("📝 2. 학생별 디저트 선호도 조사")

# 세션 상태 저장
if "preferences" not in st.session_state:
    st.session_state.preferences = []

student = st.text_input(
    "학생 이름",
    placeholder="예: 학생1"
)

dessert = st.selectbox(
    "좋아하는 디저트를 선택하세요.",
    dessert_list
)

rating = st.slider(
    "디저트 선호도 점수",
    min_value=1,
    max_value=5,
    value=3,
    help="1점은 낮은 선호도, 5점은 높은 선호도입니다."
)

if st.button("선호도 저장하기", use_container_width=True):

    if student.strip() == "":
        st.warning("학생 이름을 입력해주세요.")

    else:
        st.session_state.preferences.append({
            "학생": student.strip(),
            "디저트": dessert,
            "선호도": rating
        })

        st.success("학생 선호도가 저장되었습니다!")

st.divider()

# =====================================
# 5. 입력 데이터 확인
# =====================================

st.header("📋 3. 학생별 조사 결과")

data = st.session_state.preferences

if data:

    st.dataframe(
        data,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "참여 학생 수",
            len(set(row["학생"] for row in data))
        )

    with col2:
        st.metric(
            "총 응답 수",
            len(data)
        )

    if st.button("전체 조사 결과 초기화"):
        st.session_state.preferences = []
        st.rerun()

else:
    st.info("아직 입력된 조사 결과가 없습니다.")

st.divider()

# =====================================
# 6. 학생별 선호도 그래프
# =====================================

st.header("📊 4. 학생별 디저트 선호도 그래프")

if data:

    students = list(dict.fromkeys(
        row["학생"] for row in data
    ))

    selected_student = st.selectbox(
        "그래프를 확인할 학생을 선택하세요.",
        students
    )

    student_scores = {}

    for row in data:

        if row["학생"] == selected_student:

            name = row["디저트"]
            score = row["선호도"]

            if name not in student_scores:
                student_scores[name] = []

            student_scores[name].append(score)

    # 같은 학생이 같은 디저트에 여러 번 응답한 경우 평균
    chart_data = {}

    for name, scores in student_scores.items():
        chart_data[name] = sum(scores) / len(scores)

    st.subheader(selected_student + "의 디저트 선호도")

    st.bar_chart(chart_data)

    st.caption("선호도 점수는 1점부터 5점까지입니다.")

else:
    st.info("학생 데이터를 입력하면 그래프가 표시됩니다.")

st.divider()

# =====================================
# 7. 전체 학생 평균 비교
# =====================================

st.header("👥 5. 전체 학생 선호도 비교")

if data:

    student_scores = {}

    for row in data:

        name = row["학생"]

        if name not in student_scores:
            student_scores[name] = []

        student_scores[name].append(row["선호도"])

    average_students = {}

    for name, scores in student_scores.items():
        average_students[name] = round(
            sum(scores) / len(scores), 2
        )

    st.bar_chart(average_students)

    st.write("학생별 평균 선호도")

    for name, score in average_students.items():
        st.write(name + ":", score, "점")

else:
    st.info("학생 데이터를 입력해주세요.")

st.divider()

# =====================================
# 8. 디저트 종류별 평균 선호도
# =====================================

st.header("🍮 6. 디저트 종류별 평균 선호도")

if data:

    dessert_scores = {}

    for row in data:

        name = row["디저트"]

        if name not in dessert_scores:
            dessert_scores[name] = []

        dessert_scores[name].append(row["선호도"])

    average_desserts = {}

    for name, scores in dessert_scores.items():

        average_desserts[name] = round(
            sum(scores) / len(scores), 2
        )

    st.bar_chart(average_desserts)

    # 가장 인기 있는 디저트
    best_dessert = max(
        average_desserts,
        key=average_desserts.get
    )

    st.success(
        "🏆 가장 선호도가 높은 디저트: "
        + best_dessert
    )

    st.metric(
        "평균 선호도",
        str(average_desserts[best_dessert]) + "점"
    )

else:
    st.info("학생 데이터를 입력해주세요.")

st.divider()

# =====================================
# 9. 조사 결과 CSV 다운로드
# =====================================

st.header("💾 7. 조사 결과 다운로드")

if data:

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=["학생", "디저트", "선호도"]
    )

    writer.writeheader()
    writer.writerows(data)

    st.download_button(
        label="📥 조사 결과 CSV 다운로드",
        data=output.getvalue().encode("utf-8-sig"),
        file_name="학생별_디저트_선호도.csv",
        mime="text/csv",
        use_container_width=True
    )

else:
    st.info("다운로드할 조사 결과가 없습니다.")

# =====================================
# 10. 마무리
# =====================================

st.divider()

st.caption(
    "데이터 출처: 공공데이터포털 "
    "- 보성군 차 음식 및 디저트 정보"
)

st.caption(
    "학생별 선호도는 직접 입력한 설문 결과를 활용합니다."
)
