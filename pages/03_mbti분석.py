import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="세계 국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# 제목 및 소개
# -----------------------------
st.title("🌍 세계 국가별 MBTI 비율 분석")
st.write(
    "국가를 선택하면 해당 국가의 MBTI 16가지 유형별 비율을 "
    "막대그래프로 확인할 수 있어요!"
)

# -----------------------------
# CSV 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("countriesMBTI_16types.csv")
    return data

try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "countriesMBTI_16types.csv 파일을 찾을 수 없어요. "
        "app.py와 같은 폴더에 CSV 파일을 업로드했는지 확인해 주세요."
    )
    st.stop()

except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류가 발생했어요: {e}")
    st.stop()

# -----------------------------
# 데이터 확인
# -----------------------------
if "Country" not in df.columns:
    st.error("CSV 파일에 'Country' 열이 없습니다.")
    st.stop()

mbti_columns = [
    col for col in df.columns if col != "Country"
]

if len(mbti_columns) != 16:
    st.warning(
        f"현재 데이터에서 MBTI 열을 {len(mbti_columns)}개 찾았어요."
    )

# 국가 이름 목록
countries = sorted(
    df["Country"].dropna().unique().tolist()
)

# -----------------------------
# 국가 선택
# -----------------------------
st.subheader("🗺️ 국가 선택하기")

selected_country = st.selectbox(
    "분석하고 싶은 국가를 선택하세요.",
    countries
)

# 선택한 국가 데이터
country_data = df[
    df["Country"] == selected_country
].iloc[0]

# -----------------------------
# MBTI 비율 데이터 정리
# -----------------------------
result = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": pd.to_numeric(
        country_data[mbti_columns],
        errors="coerce"
    ).values
})

result = result.dropna(subset=["비율"])

# 비율을 퍼센트로 변환
if not result.empty and result["비율"].max() <= 1:
    result["비율(%)"] = result["비율"] * 100
else:
    result["비율(%)"] = result["비율"]

# 높은 비율부터 정렬
result = result.sort_values(
    "비율(%)",
    ascending=False
).reset_index(drop=True)

# -----------------------------
# 가장 높은 MBTI 안내
# -----------------------------
if result.empty:
    st.warning("선택한 국가의 MBTI 데이터가 없습니다.")
    st.stop()

top_mbti = result.iloc[0]["MBTI"]
top_rate = result.iloc[0]["비율(%)"]

st.success(
    f"🏆 {selected_country}에서 가장 비율이 높은 MBTI는 "
    f"**{top_mbti}**이며, 비율은 **{top_rate:.2f}%**입니다."
)

# -----------------------------
# 그래프 색상 설정
# 1위는 빨간색
# 나머지는 파란색 그라데이션
# -----------------------------
blue_gradient = plt.cm.Blues(
    np.linspace(0.45, 0.90, max(len(result) - 1, 1))
)

bar_colors = ["#E53935"] + [
    plt.matplotlib.colors.to_hex(color)
    for color in blue_gradient[:len(result) - 1]
]

# -----------------------------
# 막대그래프
# -----------------------------
st.subheader(
    f"📊 {selected_country}의 MBTI 비율"
)

fig, ax = plt.subplots(figsize=(11, 7))

bars = ax.barh(
    result["MBTI"],
    result["비율(%)"],
    color=bar_colors,
    edgecolor="white",
    height=0.72
)

# 1위가 맨 위에 표시되도록 설정
ax.invert_yaxis()

# 그래프 제목
ax.set_title(
    f"{selected_country} MBTI Distribution",
    fontsize=17,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("비율 (%)", fontsize=12)
ax.set_ylabel("MBTI 유형", fontsize=12)

# 격자 표시
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.3
)

ax.set_axisbelow(True)

# 막대 끝에 비율 표시
max_value = result["비율(%)"].max()

ax.set_xlim(
    0,
    max_value * 1.18 if max_value > 0 else 1
)

for bar, value in zip(
    bars,
    result["비율(%)"]
):
    ax.text(
        bar.get_width() + max_value * 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        fontsize=9
    )

plt.tight_layout()

# Streamlit 화면에 그래프 표시
st.pyplot(fig)

plt.close(fig)

# -----------------------------
# MBTI 순위표
# -----------------------------
st.subheader("🏅 MBTI 비율 순위")

ranking = result.copy()

ranking.index = ranking.index + 1
ranking.index.name = "순위"

st.dataframe(
    ranking[["MBTI", "비율(%)"]].style.format({
        "비율(%)": "{:.2f}%"
    }),
    use_container_width=True
)

# -----------------------------
# 데이터 안내
# -----------------------------
st.caption(
    "※ 그래프는 업로드된 CSV 파일의 국가별 MBTI 비율 데이터를 "
    "바탕으로 표시합니다. 자료의 조사 대상과 수집 방식에 따라 "
    "실제 인구의 MBTI 분포와 차이가 있을 수 있습니다."
)
