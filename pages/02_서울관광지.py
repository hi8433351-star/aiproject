import streamlit as st
import pandas as pd
import pydeck as pdk
import urllib.parse

# -----------------------------
# 1. 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Discover Seoul",
    page_icon="🇰🇷",
    layout="wide"
)

# -----------------------------
# 2. 서울 관광지 데이터
# -----------------------------
places = [
    {
        "순위": 1,
        "관광지": "경복궁",
        "영문명": "Gyeongbokgung Palace",
        "위도": 37.5796,
        "경도": 126.9770,
        "설명": "조선 시대 궁궐과 한국 전통 건축의 아름다움을 만날 수 있어요."
    },
    {
        "순위": 2,
        "관광지": "명동",
        "영문명": "Myeong-dong",
        "위도": 37.5636,
        "경도": 126.9850,
        "설명": "다양한 쇼핑 매장과 길거리 음식을 즐길 수 있어요."
    },
    {
        "순위": 3,
        "관광지": "남산서울타워",
        "영문명": "N Seoul Tower",
        "위도": 37.5512,
        "경도": 126.9882,
        "설명": "서울의 전경과 아름다운 야경을 감상할 수 있는 명소예요."
    },
    {
        "순위": 4,
        "관광지": "북촌한옥마을",
        "영문명": "Bukchon Hanok Village",
        "위도": 37.5826,
        "경도": 126.9830,
        "설명": "전통 한옥을 통해 한국의 옛 주거 문화를 경험할 수 있어요."
    },
    {
        "순위": 5,
        "관광지": "홍대거리",
        "영문명": "Hongdae",
        "위도": 37.5563,
        "경도": 126.9236,
        "설명": "거리 공연과 개성 있는 상점, 카페를 즐길 수 있어요."
    },
    {
        "순위": 6,
        "관광지": "광장시장",
        "영문명": "Gwangjang Market",
        "위도": 37.5700,
        "경도": 126.9997,
        "설명": "빈대떡과 다양한 분식 등 한국 시장 음식을 맛볼 수 있어요."
    },
    {
        "순위": 7,
        "관광지": "동대문디자인플라자",
        "영문명": "Dongdaemun Design Plaza",
        "위도": 37.5671,
        "경도": 127.0095,
        "설명": "독특한 건축물과 전시를 통해 디자인 문화를 만날 수 있어요."
    },
    {
        "순위": 8,
        "관광지": "코엑스·별마당도서관",
        "영문명": "COEX & Starfield Library",
        "위도": 37.5125,
        "경도": 127.0588,
        "설명": "쇼핑 공간과 천장까지 이어지는 책장이 인상적인 도서관이 있어요."
    },
    {
        "순위": 9,
        "관광지": "남대문시장",
        "영문명": "Namdaemun Market",
        "위도": 37.5591,
        "경도": 126.9777,
        "설명": "다양한 상품과 먹거리를 구경할 수 있는 전통시장이에요."
    },
    {
        "순위": 10,
        "관광지": "청계천",
        "영문명": "Cheonggyecheon Stream",
        "위도": 37.5692,
        "경도": 126.9788,
        "설명": "도심 속 산책로에서 물길과 주변 풍경을 즐길 수 있어요."
    }
]

df = pd.DataFrame(places)

# -----------------------------
# 3. 앱 제목
# -----------------------------
st.title("🇰🇷 Discover Seoul")
st.subheader("외국인 관광객을 위한 서울 관광지 TOP 10")

st.write(
    "서울의 대표 관광지를 지도에서 찾아보고 "
    "각 장소의 매력을 알아보세요! 🗺️"
)

st.info(
    "📌 이 목록은 서울의 대표 관광지를 소개하기 위한 "
    "추천 목록이며, 공식적인 외국인 선호도 순위는 아닙니다."
)

# -----------------------------
# 4. 서울 지도
# -----------------------------
st.divider()
st.header("📍 서울 관광지도")

# 지도의 중심 위치와 확대 수준
view_state = pdk.ViewState(
    latitude=37.5665,
    longitude=126.9850,
    zoom=11,
    pitch=0
)

# 관광지 위치를 표시하는 빨간색 점
marker_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[경도, 위도]",
    get_radius=180,
    get_fill_color=[220, 55, 55, 220],
    get_line_color=[255, 255, 255],
    line_width_min_pixels=2,
    pickable=True,
    auto_highlight=True
)

# 각 관광지의 순위 숫자 표시
text_layer = pdk.Layer(
    "TextLayer",
    data=df,
    get_position="[경도, 위도]",
    get_text="순위",
    get_size=16,
    get_color=[25, 25, 25, 255],
    get_alignment_baseline="bottom",
    get_pixel_offset=[0, -12],
    get_text_anchor="middle",
    pickable=True
)

# 마커에 마우스를 올렸을 때 나타나는 설명
tooltip = {
    "html": """
        <b>{순위}위. {관광지}</b><br/>
        {영문명}<br/>
        {설명}
    """,
    "style": {
        "backgroundColor": "#222222",
        "color": "white"
    }
}

# 지도 출력
deck = pdk.Deck(
    layers=[marker_layer, text_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="light"
)

st.pydeck_chart(
    deck,
    use_container_width=True
)

st.caption(
    "🔴 빨간색 마커는 관광지 위치예요. "
    "마커에 마우스를 올리면 관광지 정보를 확인할 수 있어요."
)

# -----------------------------
# 5. 지도 아래 관광지 설명
# -----------------------------
st.divider()
st.header("🎒 서울 관광지 TOP 10 소개")

st.write(
    "각 관광지의 특징을 간단하게 확인하고 "
    "Google 지도에서 위치도 찾아보세요."
)

# 두 개의 열로 관광지 카드 표시
for start in range(0, len(places), 2):

    col1, col2 = st.columns(2)

    for offset, col in enumerate([col1, col2]):

        index = start + offset

        if index >= len(places):
            continue

        place = places[index]

        with col:

            with st.container(border=True):

                st.subheader(
                    f"{place['순위']}. {place['관광지']}"
                )

                st.caption(place["영문명"])

                st.write(place["설명"])

                # Google 지도 검색 링크 생성
                query = urllib.parse.quote(
                    place["관광지"] + " Seoul"
                )

                google_maps_url = (
                    "https://www.google.com/maps/search/"
                    "?api=1&query=" + query
                )

                st.link_button(
                    "🌍 Google 지도에서 위치 보기",
                    google_maps_url,
                    use_container_width=True
                )

# -----------------------------
# 6. 마무리 안내
# -----------------------------
st.divider()

st.success(
    "💡 여행 팁: 경복궁과 북촌한옥마을에서는 "
    "한국의 전통문화를, 명동과 홍대에서는 "
    "서울의 활기찬 도시문화를 경험해 보세요!"
)

st.caption(
    "Discover Seoul | 서울 관광지 소개 프로젝트 🇰🇷"
)
