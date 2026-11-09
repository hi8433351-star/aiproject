
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ==================================
# 1. 페이지 설정
# ==================================

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")
st.write("서울의 월별 평균기온과 연도별 최고기온을 분석해 보세요!")


# ==================================
# 2. CSV 파일 경로 및 데이터 불러오기
# ==================================

CSV_PATH = Path(__file__).parent.parent / "temperature_utf8.csv"


@st.cache_data
def load_data():

    df = pd.read_csv(
        CSV_PATH,
        encoding="utf-8-sig"
    )

    df["날짜"] = pd.to_datetime(
        df["날짜"],
        format="%Y-%m",
        errors="coerce"
    )

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month

    columns = [
        "평균기온(℃)",
        "최고기온(℃)",
        "최저기온(℃)"
    ]

    for col in columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df


# 데이터 확인
if not CSV_PATH.exists():
    st.error("temperature_utf8.csv 파일을 찾을 수 없습니다.")
    st.stop()

try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 오류: {e}")
    st.stop()


# ==================================
# 3. 월 이름 설정
# ==================================

month_labels = [
    "1월", "2월", "3월", "4월",
    "5월", "6월", "7월", "8월",
    "9월", "10월", "11월", "12월"
]


# ==================================
# 4. 월별 평균기온 그래프
# ==================================

st.subheader("📊 1. 서울 월별 평균기온")

st.write(
    "전체 관측 기간을 기준으로 계산한 "
    "서울의 월별 평균기온입니다."
)

monthly_avg = (
    df.groupby("월")["평균기온(℃)"]
    .mean()
    .reindex(range(1, 13))
)

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=month_labels,
        y=monthly_avg.values,
        mode="lines+markers",
        name="월별 평균기온",
        line=dict(
            color="orange",
            width=3
        ),
        marker=dict(size=9)
    )
)

fig1.update_layout(
    title="서울 월별 평균기온",
    xaxis_title="월",
    yaxis_title="평균기온(℃)",
    legend_title="기온 구분",
    template="plotly_white",
    height=450,
    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ==================================
# 5. 연도 선택
# ==================================

st.divider()

st.subheader("📈 2. 연도별 최고기온 분석")

st.write(
    "연도 1개를 선택하면 해당 연도의 월별 최고기온을 확인하고, "
    "연도 2개를 선택하면 두 연도를 비교할 수 있습니다."
)

years = sorted(
    df["연도"].dropna().astype(int).unique().tolist()
)

if len(years) == 0:
    st.warning("분석할 연도 데이터가 없습니다.")
    st.stop()

selected_years = st.multiselect(
    "분석할 연도를 선택하세요 (최대 2개)",
    options=years,
    default=[years[-1]],
    max_selections=2
)


# ==================================
# 6. 최고기온 그래프
# ==================================

if len(selected_years) == 0:

    st.info("연도를 선택해 주세요.")

else:

    fig2 = go.Figure()

    colors = [
        "hotpink",
        "skyblue"
    ]

    for i, year in enumerate(selected_years):

        year_df = df[
            df["연도"] == year
        ].copy()

        year_monthly = (
            year_df.groupby("월")["최고기온(℃)"]
            .mean()
            .reindex(range(1, 13))
        )

        fig2.add_trace(
            go.Scatter(
                x=month_labels,
                y=year_monthly.values,
                mode="lines+markers",
                name=f"{year}년 최고기온",
                line=dict(
                    color=colors[i],
                    width=3
                ),
                marker=dict(size=8)
            )
        )

    if len(selected_years) == 1:

        graph_title = (
            f"{selected_years[0]}년 월별 최고기온"
        )

    else:

        graph_title = (
            f"{selected_years[0]}년과 "
            f"{selected_years[1]}년 최고기온 비교"
        )

    fig2.update_layout(
        title=graph_title,
        xaxis_title="월",
        yaxis_title="최고기온(℃)",
        legend_title="연도",
        template="plotly_white",
        height=500,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # ==================================
    # 7. 선택 연도 데이터 표
    # ==================================

    st.subheader("📋 연도별 최고기온 데이터")

    table_data = df[
        df["연도"].isin(selected_years)
    ].pivot_table(
        index="월",
        columns="연도",
        values="최고기온(℃)",
        aggfunc="mean"
    )

    table_data = table_data.reindex(
        range(1, 13)
    )

    table_data.index = month_labels
    table_data.index.name = "월"

    st.dataframe(
        table_data,
        use_container_width=True
    )


# ==================================
# 8. 마무리
# ==================================

st.divider()

st.caption(
    "자료: 서울 기온 데이터 | 온도 단위: ℃"
)
\
