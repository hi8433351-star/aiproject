
import re
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# =====================================
# 1. 페이지 설정
# =====================================

st.set_page_config(
    page_title="연령별 인구 분석",
    page_icon="💗",
    layout="wide"
)

st.title("💗 연령별 인구 분석")
st.write("행정구역, 성별, 연도를 선택하여 인구 변화를 확인해 보세요!")


# =====================================
# 2. CSV 파일 경로
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "population.csv"


# =====================================
# 3. CSV 파일 불러오기
# =====================================

@st.cache_data
def load_data():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"population.csv 파일을 찾을 수 없습니다: {CSV_PATH}"
        )

    encodings = [
        "cp949",
        "euc-kr",
        "utf-8-sig",
        "utf-8"
    ]

    for encoding in encodings:

        try:
            data = pd.read_csv(
                CSV_PATH,
                encoding=encoding
            )

            return data

        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 한글 인코딩을 확인해 주세요.")


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()


# =====================================
# 4. 데이터 정리
# =====================================

if "행정구역" not in df.columns:
    st.error("행정구역 열을 찾을 수 없습니다.")
    st.stop()

df["행정구역"] = df["행정구역"].astype(str).str.strip()

for col in df.columns:

    if col != "행정구역":

        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )


# =====================================
# 5. 연도 확인
# =====================================

years = sorted({
    int(match.group(1))
    for col in df.columns
    if (match := re.match(r"^(\d{4})년_", col))
})

if not years:
    st.error("연도 정보를 찾을 수 없습니다.")
    st.stop()


# =====================================
# 6. 행정구역 선택
# =====================================

st.subheader("🔎 분석 조건 선택")

col1, col2, col3 = st.columns(3)

districts = df["행정구역"].dropna().tolist()

with col1:

    selected_district = st.selectbox(
        "🏘️ 행정구역 선택",
        districts
    )

with col2:

    selected_gender = st.selectbox(
        "👥 성별 선택",
        ["전체", "남성", "여성"]
    )

with col3:

    selected_year = st.selectbox(
        "📅 연도 선택",
        years,
        index=len(years) - 1,
        format_func=lambda x: f"{x}년"
    )


# =====================================
# 7. 성별에 따른 데이터 선택
# =====================================

gender_code = {
    "전체": "",
    "남성": "남_",
    "여성": "여_"
}

prefix = (
    f"{selected_year}년_"
    f"{gender_code[selected_gender]}"
    "거주자_"
)


# =====================================
# 8. 연령대 데이터 찾기
# =====================================

age_columns = []

for col in df.columns:

    if col.startswith(prefix):

        age_name = col[len(prefix):]

        if re.match(
            r"^\d+~\d+세$|^100세 이상$",
            age_name
        ):

            age_columns.append((age_name, col))


def age_sort_key(item):

    age = item[0]

    if age == "100세 이상":
        return 100

    return int(age.split("~")[0])


age_columns.sort(key=age_sort_key)

if not age_columns:

    st.error("선택한 조건의 연령별 데이터가 없습니다.")
    st.stop()


# =====================================
# 9. 선택한 행정구역 데이터
# =====================================

selected_data = df[
    df["행정구역"] == selected_district
]

if selected_data.empty:

    st.error("선택한 행정구역 데이터가 없습니다.")
    st.stop()

row = selected_data.iloc[0]

age_labels = []
population_values = []

for age_name, col_name in age_columns:

    value = row[col_name]

    if pd.isna(value):
        value = 0

    age_labels.append(age_name)
    population_values.append(int(value))


chart_df = pd.DataFrame({
    "나이": age_labels,
    "인구수": population_values
})


# =====================================
# 10. 인구 정보
# =====================================

total_population = sum(population_values)

st.subheader("📌 분석 결과")

m1, m2, m3 = st.columns(3)

m1.metric(
    "선택 행정구역",
    selected_district
)

m2.metric(
    "선택 성별",
    selected_gender
)

m3.metric(
    "연령별 인구 합계",
    f"{total_population:,}명"
)


# =====================================
# 11. 핫핑크 꺾은선 그래프
# =====================================

st.subheader("📈 연령대별 인구수 그래프")

fig = go.Figure()

fig.add_trace(
    go.Scatter(

        x=chart_df["나이"],

        y=chart_df["인구수"],

        mode="lines+markers",

        name="인구수",

        line=dict(
            color="#FF1493",
            width=4
        ),

        marker=dict(
            color="#FF1493",
            size=9
        ),

        hovertemplate=
        "나이: %{x}<br>" +
        "인구수: %{y:,}명<extra></extra>"
    )
)


# =====================================
# 12. 그래프 디자인
# =====================================

fig.update_layout(

    title=f"{selected_year}년 {selected_district} {selected_gender} 인구",

    xaxis_title="나이",

    yaxis_title="인구수(명)",

    height=550,

    plot_bgcolor="white",

    paper_bgcolor="white",

    font=dict(
        family="sans-serif",
        size=13,
        color="#333333"
    ),

    hovermode="x unified",

    showlegend=False,

    margin=dict(
        l=30,
        r=30,
        t=70,
        b=50
    )
)


# =====================================
# 13. 가로축 설정
# =====================================

fig.update_xaxes(

    type="category",

    categoryorder="array",

    categoryarray=age_labels,

    showgrid=True,

    gridcolor="#F8C9E1",

    gridwidth=1,

    showline=True,

    linecolor="#999999",

    tickangle=0
)


# =====================================
# 14. 세로축 설정
# =====================================

fig.update_yaxes(

    rangemode="tozero",

    showgrid=True,

    gridcolor="#F3B6D5",

    # 주요 눈금 5,000명
    dtick=5000,

    # 보조 구분선 1,000명
    minor=dict(
        dtick=1000,
        showgrid=True,
        gridcolor="#FCE4F0"
    ),

    tickformat=",d",

    ticksuffix="명",

    showline=True,

    linecolor="#999999",

    zeroline=True
)


# =====================================
# 15. 그래프 출력
# =====================================

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "가로축: 10살 단위 연령대 / "
    "세로축: 1,000명 간격 보조선, "
    "5,000명 간격 주요 눈금"
)


# =====================================
# 16. 데이터 표
# =====================================

with st.expander("📋 연령대별 인구 데이터 확인"):

    st.dataframe(
        chart_df,
        use_container_width=True,
        hide_index=True
    )


# =====================================
# 17. CSV 다운로드
# =====================================

csv_data = chart_df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 인구 분석 데이터 다운로드",

    data=csv_data,

    file_name="연령별_인구분석.csv",

    mime="text/csv"
)


# =====================================
# 18. 데이터 출처
# =====================================

st.divider()

st.caption("📌 데이터 출처: population.csv")
