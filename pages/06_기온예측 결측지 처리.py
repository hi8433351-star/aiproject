import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

st.set_page_config(page_title="기온 예측 플랫폼", page_icon="🌡️", layout="wide")
st.title("🌡️ 1907~2025 기온 시계열 분석 및 AI 예측 비교")

@st.cache_data
def load_data():
    try:
        return pd.read_csv('temperature.csv', encoding='cp949')
    except:
        return pd.read_csv('temperature.csv', encoding='utf-8')

df = load_data()

st.sidebar.header("🎛️ 분석 옵션")
month_map = {
    '1월': 1, '2월': 2, '3월': 3, '4월': 4, '5월': 5, '6월': 6,
    '7월': 7, '8월': 8, '9월': 9, '10월': 10, '11월': 11, '12월': 12
}
selected_month_name = st.sidebar.selectbox("월(Month) 선택", list(month_map.keys()))
selected_month_num = month_map[selected_month_name]
target_year = st.sidebar.number_input("미래 예측 연도", min_value=2026, max_value=2100, value=2050)

def parse_date(text):
    try:
        parts = str(text).split('-')
        m_str = parts[0]
        y_val = int(parts[1])
        full_year = 2000 + y_val if y_val <= 26 else 1900 + y_val
        months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
                  'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        return full_year, months.get(m_str, 1)
    except:
        return None, None

res = df['일시'].apply(parse_date)
df['Year'] = [r[0] for r in res]
df['Month'] = [r[1] for r in res]

filtered = df[(df['Month'] == selected_month_num) & (df['Year'] <= 2025)].dropna(subset=['평균기온(℃)'])
filtered = filtered.sort_values('Year')

X = filtered[['Year']].values
y = filtered['평균기온(℃)'].values

st.subheader(f"📈 1907 ~ 2025년 {selected_month_name} 평균기온 변화")
if len(filtered) > 0:
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(filtered['Year'], y, marker='o', color='royalblue', alpha=0.7, label='평균기온')
    z = np.polyfit(filtered['Year'], y, 1)
    ax1.plot(filtered['Year'], np.poly1d(z)(filtered['Year']), color='red', linestyle='--', label='장기 추세선')
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Temperature (℃)")
    ax1.legend()
    st.pyplot(fig1)

st.markdown("---")
st.subheader(f"🤖 3가지 머신러닝 알고리즘을 통한 {target_year}년 기온 예측 비교")

if len(X) > 5:
    lin = LinearRegression().fit(X, y)
    poly = make_pipeline(PolynomialFeatures(degree=2), LinearRegression()).fit(X, y)
    rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)

    future_X = np.arange(filtered['Year'].min(), target_year + 1).reshape(-1, 1)
    
    pred_lin = lin.predict(future_X)
    pred_poly = poly.predict(future_X)
    pred_rf = rf.predict(future_X)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.scatter(X, y, color='gray', alpha=0.4, label='실제 데이터 (1907-2025)')
    ax2.plot(future_X, pred_lin, color='blue', linewidth=2, label='1. 선형 회귀 (Linear Regression)')
    ax2.plot(future_X, pred_poly, color='orange', linewidth=2, linestyle='-.', label='2. 다항 회귀 (Polynomial Regression)')
    ax2.plot(future_X, pred_rf, color='green', linewidth=2, linestyle=':', label='3. 랜덤 포레스트 (Random Forest)')
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Temperature (℃)")
    ax2.legend()
    st.pyplot(fig2)

    c1, c2, c3 = st.columns(3)
    target_arr = np.array([[target_year]])
    c1.metric("선형 회귀 예측", f"{lin.predict(target_arr)[0]:.2f} ℃")
    c2.metric("다항 회귀 예측", f"{poly.predict(target_arr)[0]:.2f} ℃")
    c3.metric("랜덤 포레스트 예측", f"{rf.predict(target_arr)[0]:.2f} ℃")

st.markdown("---")
st.subheader("📖 알고리즘별 작동 원리 및 특징")
st.markdown("""
1. **선형 회귀 (Linear Regression)**: 데이터를 가로지르는 **하나의 직선**을 찾아 장기적인 평균 변화 속도를 일정하게 예측합니다.
2. **다항 회귀 (Polynomial Regression)**: 직선이 아닌 **부드러운 곡선**으로 표현되어 최근 기온 상승 가속도 등의 변화를 유연하게 반영합니다.
3. **랜덤 포레스트 (Random Forest)**: 여러 개의 결정 트리를 조합해 학습하며, 학습 범위를 벗어난 미래 구간에서는 **값이 평평하게 수렴(고정)**하는 특징을 가집니다.
""")
