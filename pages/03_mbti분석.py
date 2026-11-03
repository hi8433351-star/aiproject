import streamlit as st
import csv
import os
import html

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="세계 국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# 제목 및 소개
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

    # 현재 파일의 상위 폴더 경로
    base_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # CSV 파일 경로
    file_path = os.path.join(
        base_path,
        "countriesMBTI_16types.csv"
    )

    # CSV 데이터 읽기
    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)
        data = list(reader)

    return data


try:
    data = load_data()

except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")

    st.info(
        "countriesMBTI_16types.csv 파일을 "
        "aiproject 폴더에 넣어 주세요."
    )

    st.stop()

except Exception as e:
    st.error(f"데이터를 불러올 수 없습니다: {e}")
    st.stop()


# -----------------------------
# 데이터 확인
# -----------------------------
if not data or "Country" not in data[0]:
    st.error("CSV 파일의 데이터 형식을 확인해 주세요.")
    st.stop()


# MBTI 유형 목록
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
# 데이터가 소수 형태라면 퍼센트로 변환
if max(item["비율"] for item in result) <= 1:

    for item in result:
        item["비율"] *= 100


# -----------------------------
# 비율 높은 순서대로 정렬
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
# MBTI 막대그래프
# -----------------------------
st.subheader(
    f"📊 {selected_country}의 MBTI 비율"
)

st.write(
    "🥇 1위는 빨간색, 나머지는 파란색 그라데이션입니다."
)


# 가장 높은 비율
max_value = max(
    item["비율"] for item in result
)


# -----------------------------
# 색상 그라데이션
# -----------------------------
for index, item in enumerate(result):

    mbti = html.escape(item["MBTI"])
    value = item["비율"]

    # 막대 길이 계산
    if max_value > 0:
        width = value / max_value * 100
    else:
        width = 0


    # 1위 빨간색
    if index == 0:

        color = "#E53935"

    # 나머지 파란색 그라데이션
    else:

        blue_level = 45 + int(
            (index - 1) /
            max(len(result) - 2, 1) * 45
        )

        color = (
            f"rgb({blue_level},"
            f"{blue_level + 40},230)"
        )


    # 막대그래프 출력
    st.markdown(
        f"""
        <div style="margin-bottom: 16px;">

            <div style="
                display: flex;
                justify-content: space-between;
                margin-bottom: 6px;
                font-weight: bold;
                font-size: 15px;
            ">

                <span>
                    {index + 1}위&nbsp;&nbsp;{mbti}
                </span>

                <span>
                    {value:.2f}%
                </span>

            </div>

            <div style="
                width: 100%;
                height: 25px;
                background-color: #eeeeee;
                border-radius: 6px;
                overflow: hidden;
            ">

                <div style="
                    width: {width:.2f}%;
                    height: 25px;
                    background-color: {color};
                    border-radius: 6px;
                ">
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("---")


# -----------------------------
# MBTI 순위표
# -----------------------------
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
