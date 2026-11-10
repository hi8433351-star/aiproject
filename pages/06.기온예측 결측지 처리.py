import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# -------------------------------------------------------------------------
# 페이지 설정 및 한글 폰트(시스템 기본) 대응
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="기온 데이터 분석 및 미래 예측 AI",
    page_icon="🌡️",
    layout="wide"
)

# 스타일 설정
sns.set_theme(style="whitegrid")

st.title("🌡️ 기온 데이터 시계열 분석 및 다중 알고리즘 예측 플랫폼")
st.markdown("""
이 앱은 **1907년부터 2025년까지**의 기온 데이터를 바탕으로, 사용자가 선택한 월의 과거 추이를 분석하고 **3가지 대표 예측 알고리즘(선형 회귀, 랜덤 포레스트, 다항 회귀)**을 이용해 미래 기온을 비교·예측합니다.
""")

# -------------------------------------------------------------------------
# 데이터 로드 및 전처리
# -------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # 업로드된 CSV 파일 읽기 (인코딩 에러 방지)
        df = pd.read_csv('temperature.csv', encoding='cp949')
    except:
        df = pd.read_csv('temperature.csv', encoding='utf-8')
    
    # '일시' 컬럼 파싱 (예: 'Oct-07', 'Jan-08' 등 형태)
    # 데이터셋의 날짜 형식을 안전하게 파싱하기 위해 처리
    df['parsed_date'] = pd.to_datetime(df['일시'], format='%b-%y', errors='coerce')
    
    # 만약 2000년대 이후 표기법 문제로 파싱이 안 된다면 다른 포맷 시도
    # (예: 1907년형 데이터가 포함된 전체 기간 파싱 보정)
    return df

df = load_data()

# 사이드바 설정 (사용자 입력)
st.sidebar.header("🎛️ 분석 옵션 설정")

# 월 선택 (1월 ~ 12월)
month_dict = {
    '1월 (Jan)': 1, '2월 (Feb)': 2, '3월 (Mar)': 3, '4월 (Apr)': 4,
    '5월 (May)': 5, '6월 (Jun)': 6, '7월 (Jul)': 7, '8월 (Aug)': 8,
    '9월 (Sep)': 9, '10월 (Oct)': 10, '11월 (Nov)': 11, '12월 (Dec)': 12
}
selected_month_name = st.sidebar.selectbox("분석할 월(Month)을 선택하세요", list(month_dict.keys()))
selected_month_num = month_dict[selected_month_name]

# 예측 연도 입력
max_year_in_data = 2025
target_year = st.sidebar.number_input(
    "미래 예측 연도를 입력하세요", 
    min_value=2026, 
    max_value=2100, 
    value=2050, 
    step=1
)

# -------------------------------------------------------------------------
# 데이터 가공
# -------------------------------------------------------------------------
# 날짜형 변환 검증 및 연도/월 추출
df['Year'] = df['parsed_date'].dt.year
df['Month'] = df['parsed_date'].dt.month

# 2자리 연도를 4자리 연도로 보정 (예: 07 -> 2007, 95 -> 1995 등 데이터 범위에 맞게 조정)
# 파일 내 실제 연도 분포 확인 후 매핑 (1907~2025 범위 가정)
def fix_year(row_year):
    if pd.isna(row_year):
        return None
    if row_year >= 0 and row_year <= 26:
        return 2000 + row_year
    elif row_year > 26 and row_year < 100:
        return 1900 + row_year
    return int(row_year)

# 원본 '일시' 문자열에서 연도와 월을 정확히 추출하는 로직 구현
def extract_year_month(text):
    try:
        parts = text.split('-')
        m_str = parts[0]
        y_str = int(parts[1])
        # 2자리 연도 보정
        full_year = 2000 + y_str if y_str <= 26 else 1900 + y_str
        
        months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
                  'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        return full_year, months.get(m_str, 1)
    except:
        return None, None

res = df['일시'].apply(extract_year_month)
df['Clean_Year'] = [r[0] for r in res]
df['Clean_Month'] = [r[1] for r in res]

# 선택한 월에 해당하는 데이터 필터링 (1907 ~ 2025)
filtered_df = df[(df['Clean_Month'] == selected_month_num) & (df['Clean_Year'] <= 2025)].dropna(subset=['평균기온(℃)'])
filtered_df = filtered_df.sort_values('Clean_Year')

X = filtered_df[['Clean_Year']].values
y = filtered_df['평균기온(℃)'].values

# -------------------------------------------------------------------------
# 섹션 1: 1907년부터 2025년까지 선택한 월의 기온 그래프
# -------------------------------------------------------------------------
st.header(f"📈 1)~2) 1907년 ~ 2025년 [{selected_month_name}] 기온 변화 추이")

if len(filtered_df) > 0:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(filtered_df['Clean_Year'], y, marker='o', linestyle='-', color='dodgerblue', alpha=0.7, label='평균기온')
    
    # 추세선 추가 (Linear)
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
# 섹션 2: 3~5) 3가지 예측 알고리즘 비교 및 미래 기온 예측
# -------------------------------------------------------------------------
st.markdown("---")
st.header(f"🤖 3)~5) 미래 연도({target_year}년) 기온 예측 및 알고리즘 비교")

if len(X) > 5:
    # 1. Linear Regression (선형 회귀)
    lin_model = LinearRegression()
    lin_model.fit(X, y)
    
    # 2. Random Forest Regressor (랜덤 포레스트)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)
    
    # 3. Polynomial Regression (다항 회귀 - 2차)
    poly_model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    poly_model.fit(X, y)
    
    # 미래 예측값 생성용 연도 배열
    future_years = np.arange(filtered_df['Clean_Year'].min(), target_year + 1).reshape(-1, 1)
    
    pred_lin = lin_model.predict(future_years)
    pred_rf = rf_model.predict(future_years)
    pred_poly = poly_model.predict(future_years)
    
    # 그래프 시각화
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    # 실제 데이터
    ax2.scatter(X, y, color='gray', alpha=0.5, label='실제 데이터 (1907-2025)')
    
    # 예측 알고리즘 결과 선
    ax2.plot(future_years, pred_lin, color='blue', linewidth=2, label='1. 선형 회귀 (Linear Regression)')
    ax2.plot(future_years, pred_poly, color='orange', linewidth=2, linestyle='-.', label='2. 다항 회귀 (Polynomial Regression)')
    ax2.plot(future_years, pred_rf, color='green', linewidth=2, linestyle=':', label='3. 랜덤 포레스트 (Random Forest)')
    
    ax2.set_title(f"Comparison of 3 AI Prediction Models up to {target_year} ({selected_month_name})", fontsize=14)
    ax2.set_xlabel("Year", fontsize=12)
    ax2.set_ylabel("Temperature (℃)", fontsize=12)
    ax2.legend()
    st.pyplot(fig2)
    
    # 최종 예측 결과 요약 카드 출력
    st.subheader(f"📌 {target_year}년 {selected_month_name} 예측 기온 결과 요약")
    col1, col2, col3 = st.columns(3)
    
    target_X = np.array([[target_year]])
    res_lin = lin_model.predict(target_X)[0]
    res_poly = poly_model.predict(target_X)[0]
    res_rf = rf_model.predict(target_X)[0]
    
    col1.metric("선형 회귀 예측", f"{res_lin:.2f} ℃")
    col2.metric("다항 회귀 예측", f"{res_poly:.2f} ℃")
    col3.metric("랜덤 포레스트 예측", f"{res_rf:.2f} ℃")

# -------------------------------------------------------------------------
# 섹션 3: 알고리즘 작동 원리 및 특징 설명
# -------------------------------------------------------------------------
st.markdown("---")
st.header("📖 5) 알고리즘별 작동 원리 및 특징 설명")

st.markdown("""
그래프와 위의 결과를 바탕으로, 각 알고리즘이 어떻게 작동하는지 이해할 수 있습니다:

1. **선형 회귀 (Linear Regression, 파란색 실선)**
   * **작동 방식**: 데이터들의 전체적인 흐름을 관통하는 **하나의 직선**을 그립니다. 과거부터 현재까지 기온이 일정한 비율로 꾸준히 상승(또는 하락)했다고 가정합니다.
   * **그래프 상의 특징**: 미래로 갈수록 변화율이 완벽한 직선 형태로 곧게 뻗어 나갑니다. 변동성이 무시되고 장기적인 거시적 트렌드(지구온난화 등)를 단순하게 파악할 때 유용합니다.

2. **다항 회귀 (Polynomial Regression, 주황색 쇄선)**
   * **작동 방식**: 선형 회귀를 확장하여, 직선이 아닌 **곡선(Curve)** 형태로 데이터를 피팅합니다. 최근 들어 기온 상승 속도가 가파라지는 등의 비선형적 가속도를 표현할 수 있습니다.
   * **그래프 상의 특징**: 완만한 직선이 아니라 부드러운 곡선 형태로 휘어지며 미래의 가속화되거나 둔화되는 기온 변화 경향을 유연하게 반영합니다.

3. **랜덤 포레스트 (Random Forest, 초록색 점선)**
   * **작동 방식**: 수많은 **의사결정 나무(Decision Tree)**를 무작위로 만들고, 각 나무가 예측한 값들의 평균을 최종 결과로 도출합니다. 
   * **그래프 상의 특징**: 과거 데이터가 가진 국소적인 패턴과 계단식 구간들을 기억하므로, 입력한 미래 연도가 학습 데이터의 범위를 벗어나면(Extrapolation) **최근 관측된 최고/최저 기온 수준에서 값이 평평하게 수렴(고정)**하려는 성질이 눈에 띱니다.
""")
