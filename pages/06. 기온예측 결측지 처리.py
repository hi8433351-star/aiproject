import streamlit as st
import pandas as pd
import numpy as np

# ⚠️ 스트림릿 클라우드 서버 환경(GUI 백엔드 부재) 충돌 방지 필수 설정
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# -------------------------------------------------------------------------
# 1. 페이지 설정
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="기온 데이터 분석 및 미래 예측 AI",
    page_icon="🌡️",
    layout="wide"
)

sns.set_theme(style="whitegrid")

st.title("🌡️ 기온 데이터 시계열 분석 및 다중 알고리즘 예측 플랫폼")
st.markdown("""
이 앱은 **1907년부터 2025년까지**의 기온 데이터를 바탕으로, 사용자가 선택한 월의 과거 추이를 분석하고 **3가지 대표 예측 알고리즘(선형 회귀, 다항 회귀, 랜덤 포레스트)**을 이용해 미래 기온을 비교·예측합니다.
""")

# -------------------------------------------------------------------------
# 2. 데이터 로드 및 전처리
# -------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # 인코딩 에러 방지 (cp949 시도 후 실패시 utf-8)
        df = pd.read_csv('temperature.csv', encoding='cp949')
    except Exception:
        df = pd.read_csv('temperature.csv', encoding='utf-8')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"temperature.csv 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# -------------------------------------------------------------------------
# 3. 사이드바 설정 (사용자 입력)
# -------------------------------------------------------------------------
st.sidebar.header("🎛️ 분석 옵션 설정")

month_dict = {
    '1월 (Jan)': 1, '2월 (Feb)': 2, '3월 (Mar)': 3, '4월 (Apr)': 4,
    '5월 (May)': 5, '6월 (Jun)': 6, '7월 (Jul)': 7, '8월 (Aug)': 8,
    '9월 (Sep)': 9, '10월 (Oct)': 10, '11월 (Nov)': 11, '12월 (Dec)': 12
}
selected_month_name = st.sidebar.selectbox("분석할 월(Month)을 선택하세요", list(month_dict.keys()))
selected_month_num = month_dict[selected_month_name]

target_year = st.sidebar.number_input(
    "미래 예측 연도를 입력하세요", 
    min_value=2026, 
    max_value=2100, 
    value=2050, 
    step=1
)

# -------------------------------------------------------------------------
# 4. 날짜 파싱 및 데이터 가공
# -------------------------------------------------------------------------
def extract_year_month(text):
    try:
        parts = str(text).split('-')
        m_str = parts[0]
        y_str = int(parts[1])
        # 2자리 연도 보정 (07 -> 2007, 99 -> 1999 등)
        full_year = 2000 + y_str if y_str <= 26 else 1900 + y_str
        
        months = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        return full_year, months.get(m_str, 1)
    except Exception:
        return None, None

parsed_results = df['일시'].apply(extract_year_month)
df['Clean_Year'] = [r[0] for r in parsed_results]
df['Clean_Month'] = [r[1] for r in parsed_results]

# 선택한 월에 해당하는 데이터 필터링 (1907 ~ 2025)
filtered_df = df[(df['Clean_Month'] == selected_month_num) & (df['Clean_Year'] <= 2025)].dropna(subset=['평균기온(℃)'])
filtered_df = filtered_df.sort_values('Clean_Year')

X = filtered_df[['Clean_Year']].values
y = filtered_df['평균기온(℃)'].values

# -------------------------------------------------------------------------
# 5. 섹션 1: 1907년부터 2025년까지 선택한 월의 기온 그래프
# -------------------------------------------------------------------------
st.header(f"📈 1)~2) 1907년 ~ 2025년 [{selected_month_name}] 기온 변화 추이")

if len(filtered_df) > 0:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(filtered_df['Clean_Year'], y, marker='o', linestyle='-', color='dodgerblue', alpha=0.7, label='평균기온')
    
    # 장기 추세선 추가
    z = np.polyfit(filtered_df['Clean_Year'], y, 1)
    p = np.poly1d(z)
    ax.plot(filtered_df['Clean_Year'], p(filtered_df['Clean_Year']), color='red', linestyle='--', label='장기 추세선')
    
    ax.set_title(f"1907 - 2025 {selected_month_name} Historical Average Temperature", fontsize=14)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Temperature (℃)", fontsize=12)
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("선택한 월에 해당하는 데이터가 존재하지 않습니다.")

# -------------------------------------------------------------------------
# 6. 섹션 2: 3~5) 3가지 예측 알고리즘 비교 및 미래 기온 예측
# -------------------------------------------------------------------------
st.markdown("---")
st.header(f"🤖 3)~5) 미래 연도({target_year}년) 기온 예측 및 알고리즘 비교")

if len(X) > 5:
    # 1. 선형 회귀 (Linear Regression)
    lin_model = LinearRegression()
    lin_model.fit(X, y)
    
    # 2. 다항 회귀 (Polynomial Regression - 2차)
    poly_model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    poly_model.fit(X, y)
    
    # 3. 랜덤 포레스트 (Random Forest)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)
    
    # 미래 예측 범위 설정
    future_years = np.arange(filtered_df['Clean_Year'].min(), target_year + 1).reshape(-1, 1)
    
    pred_lin = lin_model.predict(future_years)
    pred_poly = poly_model.predict(future_years)
    pred_rf = rf_model.predict(future_years)
    
    # 그래프 시각화
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    ax2.scatter(X, y, color='gray', alpha=0.5, label='실제 데이터 (1907-2025)')
    ax2.plot(future_years, pred_lin, color='blue', linewidth=2, label='1. 선형 회귀 (Linear Regression)')
    ax2.plot(future_years, pred_poly, color='orange', linewidth=2, linestyle='-.', label='2. 다항 회귀 (Polynomial Regression)')
    ax2.plot(future_years, pred_rf, color='green', linewidth=2, linestyle=':', label='3. 랜덤 포레스트 (Random Forest)')
    
    ax2.set_title(f"Comparison of 3 AI Prediction Models up to {target_year} ({selected_month_name})", fontsize=14)
    ax2.set_xlabel("Year", fontsize=12)
    ax2.set_ylabel("Temperature (℃)", fontsize=12)
    ax2.legend()
    st.pyplot(fig2)
    
    # 최종 예측 결과 요약 카드
    st.subheader(f"📌 {target_year}년 {selected_month_name} 예측 기온 결과 요약")
    col1, col2, col3 = st.columns(3)
    
    target_X = np.array([[target_year]])
    res_lin = lin_model.
    
