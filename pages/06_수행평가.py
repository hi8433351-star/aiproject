st.set_page_config(
    page_title="학생 디저트 선호도 분석",
    page_icon="🍰",
    layout="wide"
)

st.title("🍰 학생별 디저트 선호도 분석")
st.write("공공데이터를 활용한 디저트 선호도 조사 및 시각화")

# -------------------------
# 1. 디저트 데이터 불러오기
# -------------------------

st.header("1. 디저트 데이터")

uploaded_file = st.file_uploader(
    "공공데이터 CSV 파일을 업로드하세요",
    type=["csv"]
)

dessert_list = [
    "고구마녹차케이크",
    "그린티 스무디",
    "홍차 에이드",
    "녹차 쿠키",
    "녹차 라떼"
]

if uploaded_file is not None:
    try:
        raw = uploaded_file.getvalue()

        try:
            content = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            content = raw.decode("cp949")

        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)

        if rows and "요리명" in rows[0]:
            dessert_list = list(dict.fromkeys(
                row["요리명"].strip()
                for row in rows
                if row.get("요리명", "").strip()
            ))
            st.success("공공데이터를 불러왔습니다.")
            st.dataframe(rows)
        else:
            st.warning("요리명 컬럼을 찾을 수 없습니다.")

    except Exception as e:
        st.error("CSV 파일을 읽을 수 없습니다.")
        st.write(str(e))

else:
    st.info("CSV를 업로드하지 않으면 예시 디저트가 표시됩니다.")

# -------------------------
# 2. 학생 선호도 입력
# -------------------------

st.header("2. 학생별 선호도 입력")

if "preferences" not in st.session_state:
    st.session_state.preferences = []

student = st.text_input(
    "학생 이름",
    placeholder="예: 학생1"
)

dessert = st.selectbox(
    "선호하는 디저트",
    dessert_list
)

rating = st.slider(
    "선호도 점수",
    min_value=1,
    max_value=5,
    value=3
)

if st.button("선호도 저장"):
    if student.strip():
        st.session_state.preferences.append({
            "학생": student.strip(),
            "디저트": dessert,
            "선호도": rating
        })
        st.success("선호도가 저장되었습니다!")
    else:
        st.warning("학생 이름을 입력해주세요.")

# -------------------------
# 3. 입력 데이터 확인
# -------------------------

st.header("3. 학생별 선호도 데이터")

data = st.session_state.preferences

if data:
    st.dataframe(data, use_container_width=True)

    if st.button("입력 데이터 초기화"):
        st.session_state.preferences = []
        st.rerun()
else:
    st.info("아직 입력된 학생 데이터가 없습니다.")

# -------------------------
# 4. 학생별 그래프
# -------------------------

st.header("4. 학생별 디저트 선호도 그래프")

if data:
    students = list(dict.fromkeys(
        row["학생"] for row in data
    ))

    selected_student = st.selectbox(
        "그래프를 확인할 학생 선택",
        students
    )

    chart_data = {}

    for row in data:
        if row["학생"] == selected_student:
            name = row["디저트"]
            chart_data[name] = max(
                chart_data.get(name, 0),
                row["선호도"]
            )

    st.subheader(selected_student + "의 디저트 선호도")

    st.bar_chart(chart_data)

    st.caption("선호도 점수: 1점(낮음) ~ 5점(높음)")

    # 전체 학생 비교 그래프
    st.subheader("전체 학생의 디저트 선호도")

    all_students = {}

    for row in data:
        key = row["학생"]
        if key not in all_students:
            all_students[key] = []

        all_students[key].append(row["선호도"])

    average_data = {}

    for name, scores in all_students.items():
        average_data[name] = sum(scores) / len(scores)

    st.bar_chart(average_data)

    st.caption("학생별 입력 점수 평균 비교")

    # 디저트별 평균 선호도
    st.subheader("디저트 종류별 평균 선호도")

    dessert_scores = {}

    for row in data:
        name = row["디저트"]

        if name not in dessert_scores:
            dessert_scores[name] = []

        dessert_scores[name].append(row["선호도"])

    average_desserts = {}

    for name, scores in dessert_scores.items():
        average_desserts[name] = (
            sum(scores) / len(scores)
        )

    st.bar_chart(average_desserts)

    # -------------------------
    # 5. 분석 결과
    # -------------------------

    st.header("5. 선호도 분석 결과")

    if average_desserts:
        best = max(
            average_desserts,
            key=average_desserts.get
        )

        st.success(
            "가장 선호도가 높은 디저트: " + best
        )

        st.write(
            "평균 선호도:",
            round(average_desserts[best], 2),
            "점"
        )

    # -------------------------
    # 6. CSV 다운로드
    # -------------------------

    st.header("6. 분석 데이터 다운로드")

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=["학생", "디저트", "선호도"]
    )

    writer.writeheader()
    writer.writerows(data)

    st.download_button(
        label="CSV 파일 다운로드",
        data=output.getvalue().encode("utf-8-sig"),
        file_name="학생별_디저트_선호도.csv",
        mime="text/csv"
    )

else:
    st.info("학생별 데이터를 입력하면 그래프가 생성됩니다.")

st.divider()
st.caption("데이터 출처: 공공데이터포털 - 보성군 차 음식 및 디저트 정보")

