import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# 1. 페이지 설정
st.set_page_config(page_title="아이리스 품종 예측 앱", page_icon="🌸", layout="centered")

st.title("🌸 아이리스(Iris) 품종 예측 및 시각화 앱")
st.write("꽃잎(Petal)의 길이와 너비를 입력하면, **랜덤 포레스트(Random Forest)** 모델이 품종을 예측하고 그 이유를 시각화해 줍니다.")

# 2. 데이터 및 모델 학습 (캐싱 활용)
@st.cache_resource
def load_data_and_model():
    iris = load_iris()
    X = iris.data[:, 2:]  # 시각화를 위해 꽃잎 길이(2), 꽃잎 너비(3)만 사용
    y = iris.target
    
    # 가장 많이 쓰이는 분류 모델인 Random Forest 학습
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return iris, X, y, model

iris, X, y, model = load_data_and_model()

# 품종 레이블 매핑
target_names = iris.target_names # ['setosa', 'versicolor', 'virginica']
korean_names = {
    'setosa': '아이리스 세토사 (Setosa)',
    'versicolor': '아이리스 버시컬러 (Versicolor)',
    'virginica': '아이리스 버지니카 (Virginica)'
}

# 3. 사이드바 사용자 입력
st.sidebar.header("🔍 입력 변수 설정")
st.sidebar.write("꽃잎의 규격을 슬라이더로 조절하세요.")

user_petal_length = st.sidebar.slider(
    "꽃잎 길이 (Petal Length, cm)", 
    float(X[:, 0].min()), float(X[:, 0].max()), float(X[:, 0].mean())
)
user_petal_width = st.sidebar.slider(
    "꽃잎 너비 (Petal Width, cm)", 
    float(X[:, 1].min()), float(X[:, 1].max()), float(X[:, 1].mean())
)

# 4. 예측 수행
user_input = np.array([[user_petal_length, user_petal_width]])
prediction = model.predict(user_input)[0]
prediction_proba = model.predict_proba(user_input)[0]

pred_species_en = target_names[prediction]
pred_species_kr = korean_names[pred_species_en]

# 5. 결과 출력
st.subheader("📌 예측 결과")
st.success(고객님이 입력하신 조건의 예측 품종은 **`{pred_species_kr}`** 입니다!)

# 확률 바차트 표시
st.write("##### 품종별 예측 확률")
prob_df = pd.DataFrame({
    '품종': [korean_names[name] for name in target_names],
    '확률 (%)': prediction_proba * 100
})
st.bar_chart(prob_df.set_index('품종'))

# 6. 시각화 (결정 경계 및 사용자 입력 위치)
st.subheader("📊 분류 이유 시각화 (Decision Boundary)")
st.write("배경 색상은 모델이 각 영역을 어떤 품종으로 판단하는지 나타내며, **초록색 별표(★)**는 사용자가 입력한 위치입니다.")

fig, ax = plt.subplots(figsize=(8, 6))

# 결정 경계를 위한 그리드 생성
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                     np.arange(y_min, y_max, 0.02))

Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# 영역 색상 채우기
cmap_light = plt.matplotlib.colors.ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
ax.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.3)

# 실제 데이터 훈련 포인트 scatter plot
scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.matplotlib.colors.ListedColormap(['#FF0000', '#008000', '#0000FF']),
                     edgecolor='k', s=40, alpha=0.8)

# 사용자가 입력한 포인트 표시 (초록색 큰 별)
ax.scatter(user_petal_length, user_petal_width, color='green', marker='*', s=300, edgecolor='yellow', linewidth=1.5, label='사용자 입력값')

ax.set_xlabel('Petal Length (꽃잎 길이)')
ax.set_ylabel('Petal Width (꽃잎 너비)')
ax.set_title('Iris Petal Length vs Width & Classification Regions')
ax.legend(loc='lower right')

st.pyplot(fig)
