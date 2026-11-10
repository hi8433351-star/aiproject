
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울 월별 기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 월별 평균기온 분석 및 예측")
st.write(
    "1907년부터 2025년까지의 기온 데이터를 분석하고 "
    "세 가지 알고리즘으로 미래 기온을 예측해 보세요!"
)

st.info(
    "※ 미래 기온은 과거 데이터의 수학적 추세를 이용한 참고용 예측이며, "
    "실제 미래 기온과 다를 수 있습니다."
)

# ==========================================
# 2. 데이터 불러오기
# ==========================================

CSV_PATH = Path(__file__).parent.parent / "temperature_utf8.csv"


@st.cache_data
def load_data():

    df = pd.read_csv(
        CSV_PATH,
        encoding="utf-8-sig"
    )

    df.columns = df.columns.str.strip()

    # 날짜 열 확인
    if "날짜" in df.columns:
        date_col = "날짜"
    elif "일시" in df.columns:
        date_col = "일시"
    else:
        raise ValueError("CSV 파일에서 날짜 열을 찾을 수 없습니다.")

    # 날짜 변환
    df["날짜변환"] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    # 연도와 월 추출
    df["연도"] = df["날짜변환"].dt.year
    df["월"] = df["날짜변환"].dt.month

    # 평균기온 숫자 변환
    df["평균기온(℃)"] = pd.to_numeric(
        df["평균기온(℃)"],
        errors="coerce"
    )

    # 결측치 제거
    df = df.dropna(
        subset=["연도", "월", "평균기온(℃)"]
    )

    df["연도"] = df["연도"].astype(int)
    df["월"] = df["월"].astype(int)

    # 1907~2025년 데이터만 사용
    df = df[
        (df["연도"] >= 1907) &
        (df["연도"] <= 2025)
    ]

    return df


if not CSV_PATH.exists():
    st.error(
        "temperature_utf8.csv 파일을 찾을 수 없습니다. "
        "최상위 폴더에 CSV 파일을 넣어 주세요."
    )
    st.stop()

try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# ==========================================
# 3. 월 선택 및 예측 연도 입력
# ==========================================

st.subheader("📅 분석 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "분석할 월을 선택하세요.",
        options=list(range(1, 13)),
        format_func=lambda x: f"{x}월",
        index=0
    )

with col2:
    forecast_year = st.number_input(
        "예측할 미래 연도를 입력하세요.",
        min_value=2026,
        max_value=2050,
        value=2035,
        step=1
    )

forecast_year = int(forecast_year)

st.write(
    f"현재 선택: **{selected_month}월 / {forecast_year}년까지 예측**"
)


# ==========================================
# 4. 선택한 월의 연도별 평균기온
# ==========================================

month_data = df[
    df["월"] == selected_month
].copy()

year_data = (
    month_data.groupby("연도")["평균기온(℃)"]
    .mean()
    .sort_index()
)

if len(year_data) < 10:
    st.warning("예측에 사용할 데이터가 부족합니다.")
    st.stop()

st.divider()

st.subheader(
    f"📊 {selected_month}월 연도별 평균기온 (1907~2025년)"
)

st.write(
    "선택한 월의 실제 평균기온이 연도별로 어떻게 변화했는지 보여줍니다."
)

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=year_data.index,
        y=year_data.values,
        mode="lines+markers",
        name="실제 평균기온",
        line=dict(color="royalblue", width=2),
        marker=dict(size=5)
    )
)

fig1.update_layout(
    title=f"{selected_month}월 실제 평균기온 변화",
    xaxis_title="연도",
    yaxis_title="평균기온(℃)",
    template="plotly_white",
    height=450,
    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ==========================================
# 5. 세 가지 예측 알고리즘 계산
# ==========================================

# 실제 데이터의 연도와 기온
x = year_data.index.to_numpy(dtype=float)
y = year_data.values.astype(float)

# 예측에 사용할 전체 연도
all_years = np.arange(
    int(x.min()),
    forecast_year + 1
)

# ------------------------------------------
# 알고리즘 1: 선형 회귀
# ------------------------------------------

linear_model = np.polyfit(
    x,
    y,
    1
)

linear_prediction = np.polyval(
    linear_model,
    all_years
)


# ------------------------------------------
# 알고리즘 2: 2차 다항 회귀
# ------------------------------------------

polynomial_model = np.polyfit(
    x,
    y,
    2
)

polynomial_prediction = np.polyval(
    polynomial_model,
    all_years
)


# ------------------------------------------
# 알고리즘 3: 10년 이동평균
# ------------------------------------------

# 연도별 데이터가 빠진 경우를 고려해
# 1907~2025년의 연도 축을 먼저 만든다.

complete_years = np.arange(
    1907,
    2026
)

complete_data = year_data.reindex(
    complete_years
)

# 최근 10년의 이동평균 계산
moving_average = complete_data.rolling(
    window=10,
    min_periods=5
).mean()

# 마지막으로 계산 가능한 이동평균
last_average = moving_average.dropna().iloc[-1]

# 과거 구간의 이동평균
moving_history = moving_average.reindex(
    all_years[all_years <= 2025]
)

# 미래 구간은 최근 10년 평균으로 유지
future_years = all_years[all_years > 2025]

future_average = np.full(
    len(future_years),
    last_average
)

moving_years = np.concatenate([
    moving_history.index.to_numpy(),
    future_years
])

moving_prediction = np.concatenate([
    moving_history.to_numpy(dtype=float),
    future_average
])


# ==========================================
# 6. 세 알고리즘 한 그래프에서 비교
# ==========================================

st.divider()

st.subheader(
    f"🔮 {selected_month}월 미래 평균기온 예측 비교"
)

st.write(
    "실제 기온과 세 가지 알고리즘의 예측 추세를 "
    "하나의 그래프에서 비교할 수 있습니다."
)

fig2 = go.Figure()

# 실제 기온
fig2.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        name="실제 평균기온",
        line=dict(color="black", width=2),
        marker=dict(size=4)
    )
)

# 선형 회귀
fig2.add_trace(
    go.Scatter(
        x=all_years,
        y=linear_prediction,
        mode="lines",
        name="① 선형 회귀",
        line=dict(
            color="red",
            width=3,
            dash="dash"
        )
    )
)

# 2차 다항 회귀
fig2.add_trace(
    go.Scatter(
        x=all_years,
        y=polynomial_prediction,
        mode="lines",
        name="② 2차 다항 회귀",
        line=dict(
            color="green",
            width=3,
            dash="dot"
        )
    )
)

# 10년 이동평균
fig2.add_trace(
    go.Scatter(
        x=moving_years,
        y=moving_prediction,
        mode="lines",
        name="③ 10년 이동평균",
        line=dict(
            color="orange",
            width=3,
            dash="dashdot"
        )
    )
)

# 2025년 기준선
fig2.add_vline(
    x=2025,
    line_dash="solid",
    line_color="gray",
    annotation_text="예측 시작",
    annotation_position="top"
)

fig2.update_layout(
    title=f"{selected_month}월 평균기온 알고리즘별 비교",
    xaxis_title="연도",
    yaxis_title="평균기온(℃)",
    legend_title="구분",
    template="plotly_white",
    height=550,
    hovermode="x unified"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==========================================
# 7. 예측 결과 비교
# ==========================================

st.subheader(
    f"📋 {forecast_year}년 예측 결과"
)

linear_result = np.polyval(
    linear_model,
    forecast_year
)

polynomial_result = np.polyval(
    polynomial_model,
    forecast_year
)

moving_result = last_average

result_df = pd.DataFrame({
    "알고리즘": [
        "선형 회귀",
        "2차 다항 회귀",
        "10년 이동평균"
    ],
    "예측 평균기온(℃)": [
        round(linear_result, 2),
        round(polynomial_result, 2),
        round(moving_result, 2)
    ]
})

st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 8. 알고리즘별 작동 원리 설명
# ==========================================

st.divider()

st.subheader("💡 예측 알고리즘은 어떻게 작동할까?")

# 알고리즘 1
with st.expander("① 선형 회귀 (Linear Regression)"):

    st.write(
        "**작동 원리**"
    )

    st.write(
        "과거의 연도별 평균기온을 이용해 가장 잘 맞는 "
        "직선 형태의 추세선을 찾습니다."
    )

    st.write(
        "그 직선을 미래 연도까지 연장하여 "
        "기온이 얼마나 변할지 예측합니다."
    )

    st.write(
        "**그래프에서 확인하기**"
    )

    st.write(
        "빨간색 점선으로 표시됩니다. "
        "직선 형태로 일정한 상승 또는 하락 추세를 보여줍니다."
    )

    st.write(
        "**특징**"
    )

    st.write(
        "계산이 간단하고 전체적인 장기 추세를 파악하기 좋지만, "
        "기온 변화가 곡선 형태일 때는 충분히 반영하지 못할 수 있습니다."
    )


# 알고리즘 2
with st.expander("② 2차 다항 회귀 (Polynomial Regression)"):

    st.write(
        "**작동 원리**"
    )

    st.write(
        "직선뿐만 아니라 곡선 형태의 변화도 표현할 수 있도록 "
        "2차 함수 형태의 추세선을 만듭니다."
    )

    st.write(
        "과거 기온 데이터에 맞는 곡선을 계산한 뒤 "
        "미래 연도까지 연장합니다."
    )

    st.write(
        "**그래프에서 확인하기**"
    )

    st.write(
        "초록색 점선으로 표시됩니다. "
        "직선과 달리 위아래로 휘어지는 형태가 나타날 수 있습니다."
    )

    st.write(
        "**특징**"
    )

    st.write(
        "기온 변화의 곡선 추세를 표현할 수 있지만, "
        "미래로 멀리 예측할수록 실제와 차이가 커질 수 있습니다."
    )


# 알고리즘 3
with st.expander("③ 10년 이동평균 (Moving Average)"):

    st.write(
        "**작동 원리**"
    )

    st.write(
        "최근 10년의 평균기온을 계산해 "
        "짧은 기간의 큰 변동을 줄이고 전체적인 흐름을 확인합니다."
    )

    st.write(
        "미래 기온은 가장 최근에 계산된 10년 이동평균값이 "
        "계속 유지된다고 가정합니다."
    )

    st.write(
        "**그래프에서 확인하기**"
    )

    st.write(
        "주황색 일점쇄선으로 표시됩니다. "
        "미래 구간에서는 최근 10년 평균값을 유지하는 수평선으로 나타납니다."
    )

    st.write(
        "**특징**"
    )

    st.write(
        "최근 기온 수준을 쉽게 파악할 수 있지만, "
        "미래의 상승이나 하락 추세를 직접 예측하지는 못합니다."
    )


# ==========================================
# 9. 마무리 안내
# ==========================================

st.divider()

st.subheader("📌 분석할 때 알아둘 점")

st.write(
    "세 알고리즘은 같은 과거 기온 데이터를 사용하지만 "
    "계산하는 방식이 다르기 때문에 미래 예측 결과도 다르게 나타납니다."
)

st.write(
    "특히 기온은 온실가스, 해양과 대기 상태, 도시 환경 등 "
    "여러 요인의 영향을 받으므로 이 그래프는 실제 기후예측 모델이 아닌 "
    "과거 데이터의 통계적 추세를 비교하는 학습용 분석입니다."
)

st.caption(
    "분석 기간: 1907년~2025년 | 온도 단위: ℃"
)
