import streamlit as st
import csv
import os

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="세계 국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("🌍 세계 국가별 MBTI 분석")

st.write(
    "158개 국가의 MBTI 데이터를 바탕으로 "
    "국가별 MBTI 비율을 확인해 보세요!"
)

st.markdown("---")


# -----------------------------
# CSV 파일 불러오기
# -----------------------------
@st.cache_data
def load_data():

    # 현재 파이썬 파일 위치
    current_path = os.path.abspath(__file__)

    # pages 폴더의 상위 폴더
    base_path = os.path.dirname(
        os.path.dirname(current_path)
    )

    # CSV 파일 경로
    file_path = os.path.join(
        base_path,
        "countriesMBTI_16types.csv"
    )

    # CSV 읽기
    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)
        data = list(reader)

    return data


# -----------------------------
# 데이터 불러오기
# -----------------------------
try:
    data = load_data()

except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.info(
        "countriesMBTI_16types.csv 파일이 "
        "aiproject 폴더에 있는지 확인해 주세요."
    )
    st.stop()

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.stop()


# -----------------------------
# 데이터 확인
# -----------------------------
if not data:
    st.error("CSV 파일에 데이터가 없습니다.")
    st.stop()

if "Country" not in data[0]:
    st.error("CSV 파일에 Country 열이 없습니다.")
    st.stop()


# MBTI 유형 가져오기
mbti_types = [
    key for key in data[0].keys()
    if key != "Country"
]

if not mbti_types:
    st.error("MBTI 데이터가 없습니다.")
    st.stop()


# -----------------------------
# 국가 선택
# -----------------------------
st.subheader("🗺️ 국가 선택하기")

countries = sorted([
    row["Country"]
    for row in data
    if row.get("Country")
])

if not countries:
    st.error("국가 목록이 없습니다.")
    st.stop()

selected_country = st.selectbox(
    "분석하고 싶은 국가를 선택하세요!",
    countries
)


# -----------------------------
# 선택한 국가 데이터
# -----------------------------
country_data = next(
    row for row in data
    if row["Country"] == selected_country
)


# -----------------------------
# MBTI 비율 계산
# -----------------------------
result = []

for mbti in mbti_types:

    try:
        value = float(country_data[mbti])

        result.append({
            "MBTI": mbti,
            "비율": value
        })

    except (ValueError, TypeError):
        continue


if not result:
    st.warning("해당 국가의 MBTI 데이터가 없습니다.")
    st.stop()


# -----------------------------
# 퍼센트 변환
# -----------------------------
if max(item["비율"] for item in result) <= 1:

    for item in result:
        item["비율"] *= 100


# -----------------------------
# 비율 순서대로 정렬
# -----------------------------
result.sort(
    key=lambda x: x["비율"],
    reverse=True
)


# -----------------------------
# 1위 MBTI 표시
# -----------------------------
top_mbti = result[0]["MBTI"]
top_rate = result[0]["비율"]

st.success(
    f"🏆 {selected_country}의 1위 MBTI는 "
    f"{top_mbti}입니다! ({top_rate:.2f}%)"
)

st.markdown("---")


# -----------------------------
# 그래프 제목
# -----------------------------
st.subheader(
    f"📊 {selected_country}의 MBTI 비율"
)

st.caption(
    "MBTI 유형별 비율을 높은 순서대로 확인해 보세요."
)


# -----------------------------
# 그래프 데이터 만들기
# -----------------------------
chart_data = {}

for item in result:

    chart_data[item["MBTI"]] = item["비율"]


# -----------------------------
# 막대그래프 출력
# -----------------------------
st.bar_chart(
    chart_data,
    horizontal=True,
    x_label="비율 (%)",
    y_label="MBTI 유형"
)


# -----------------------------
# MBTI 순위표
# -----------------------------
st.markdown("---")

st.subheader("🏅 MBTI 비율 순위 TOP 16")

ranking_data = []

for index, item in enumerate(result):

    ranking_data.append({
        "순위": index + 1,
        "MBTI": item["MBTI"],
        "비율": f"{item['비율']:.2f}%"
    })

st.table(ranking_data)


# -----------------------------
# 마무리 안내
# -----------------------------
st.markdown("---")

st.info(
    "💡 다른 국가를 선택하면 해당 국가의 "
    "MBTI 비율 그래프도 자동으로 바뀝니다!"
)

st.caption(
    "※ 제공된 CSV 데이터를 바탕으로 분석한 결과입니다."
)
