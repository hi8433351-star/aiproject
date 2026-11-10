import streamlit as st
import pandas as pd
import numpy as np

# ⚠️ 스트림릿 클라우드 서버 환경 충돌(Tcl/Tk GUI 에러) 방지 필수 설정
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# -------------------------------------------------------------------------
# 페이지 설정
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
target_year = st.sidebar.number_input(
    "미래 예측 연도를 입력하세요", 
    min_value=2026, 
    max_value=2100, 
    value=2050, 
    step=1
)

# -------------------------------------------------------------------------
# 데이터 가공 함수 및 정제
# -------------------------------------------------------------------------
def extract_year_month(text):
    try:
