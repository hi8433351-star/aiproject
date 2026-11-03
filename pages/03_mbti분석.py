import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.title("🌍 세계 국가별 MBTI 분석")

st.write("원하는 국가를 선택하고 MBTI 비율을 확인해 보세요!")

# -----------------------------
# CSV 파일 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

try:
    df = load_data()

except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.info("countriesMBTI_16types.csv 파일이 프로젝트 최상위 폴더에 있는지 확인해 주세요.")
    st.stop()

except Exception as e:
    st.error(f"파일을 읽을 수 없습니다: {e}")
    st.stop()

# -----------------------------
# 데이터 확인
# -----------------------------
if "Country" not in df.columns:
    st.error("CSV 파일에 Country 열이 없습니다.")
    st.stop()

mbti_columns = [
    col for col in df.columns if col != "Country"
]

countries = sorted(df["Country"].dropna().unique())

# -----------------------------
# 국가 선택
# -----------------------------
st.subheader("🗺️ 국가 선택")

selected_country = st.selectbox(
    "분석할 국가를 선택하세요!",
    countries
)

country_data = df[
    df["Country"] == selected_country
].iloc[0]

# -----------------------------
# MBTI 데이터 정리
# -----------------------------
result = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": pd.to_numeric(
        country_data[mbti_columns],
        errors="coerce"
    ).values
})

result = result.dropna()

# 비율 계산
if not result.empty and result["비율"].max() <= 1:
    result["비율(%)"] = result["비율"] * 100
else:
    result["비율(%)"] = result["비율"]

# 높은 순서대로 정렬
result = result.sort_values(
    "비율(%)",
    ascending=False
).reset_index(drop=True)

if result.empty:
    st.warning("해당 국가의 데이터가 없습니다.")
    st.stop()

# -----------------------------
# 1위 MBTI 표시
# -----------------------------
top_mbti = result.iloc[0]["MBTI"]
top_rate = result.iloc[0]["비율(%)"]

st.success(
    f"🏆 {selected_country}의 1위 MBTI는 "
    f"{top_mbti}입니다! ({top_rate:.2f}%)"
)

# -----------------------------
# 그래프 색상 설정
# 1위 빨간색
# 나머지 파란색 그라데이션
# -----------------------------
blue_gradient = plt.cm.Blues(
    np.linspace(0.45, 0.90, max(len(result) - 1, 1))
)

colors = ["#E53935"] + [
    plt.matplotlib.colors.to_hex(c)
    for c in blue_gradient[:len(result) - 1]
]

# -----------------------------
# 막대그래프
# -----------------------------
st.subheader(f"📊 {selected_country} MBTI 비율 그래프")

fig, ax = plt.subplots(figsize=(11, 7))

bars = ax.barh(
    result["MBTI"],
    result["비율(%)"],
    color=colors,
    edgecolor="white"
)

# 1위가 위쪽에 오도록 설정
ax.invert_yaxis()

# 제목과 축
ax.set_title(
    f"{selected_country} MBTI Distribution",
    fontsize=17,
    fontweight="bold"
)

ax.set_xlabel("비율 (%)")
ax.set_ylabel("MBTI 유형")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.3
)

ax.set_axisbelow(True)

# 그래프 오른쪽에 비율 표시
max_value = result["비율(%)"].max()

ax.set_xlim(
    0,
    max_value * 1.18 if max_value > 0 else 1
)

for bar, value in zip(bars, result["비율(%)"]):

    ax.text(
        bar.get_width() + max_value * 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        fontsize=9
    )

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# -----------------------------
# MBTI 순위표
# -----------------------------
st.subheader("🏅 MBTI 비율 TOP 16")

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
# 마무리 안내
# -----------------------------
st.info(
    "💡 다른 국가를 선택하면 해당 국가의 MBTI 비율 그래프도 자동으로 바뀝니다!"
)

st.caption(
    "※ 본 결과는 제공된 CSV 데이터를 바탕으로 분석한 것입니다."
)
