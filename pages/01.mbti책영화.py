```python
import streamlit as st
import random

# 페이지 설정은 다른 Streamlit 명령보다 먼저 실행
st.set_page_config(
    page_title="MBTI 책 & 영화 추천",
    page_icon="📚",
    layout="centered"
)

# -------------------------------
# 1. 기본 화면
# -------------------------------

st.title("📚 MBTI 책 & 영화 추천 🎬")
st.write("내 MBTI에 어울리는 책과 영화를 찾아보자!")
st.write("원하는 단서를 선택하면 취향에 맞는 작품을 추천해 줄게. 😊")

# -------------------------------
# 2. MBTI 데이터
# -------------------------------

mbti_data = {
    "ISTJ": ("꼼꼼하고 현실적인 스타일 📝", "자기계발"),
    "ISFJ": ("따뜻하고 배려심 있는 스타일 💗", "감동"),
    "INFJ": ("깊이 생각하는 스타일 🌙", "성장"),
    "INTJ": ("분석적이고 논리적인 스타일 🧠", "과학"),
    "ISTP": ("호기심 많고 실용적인 스타일 🔧", "추리"),
    "ISFP": ("감성적이고 자유로운 스타일 🎨", "힐링"),
    "INFP": ("상상력이 풍부한 스타일 🦋", "판타지"),
    "INTP": ("탐구하고 분석하는 스타일 🔍", "과학"),
    "ESTP": ("활동적이고 도전적인 스타일 🏃", "모험"),
    "ESFP": ("밝고 활발한 스타일 🎉", "코미디"),
    "ENFP": ("창의적이고 열정적인 스타일 ✨", "판타지"),
    "ENTP": ("아이디어가 풍부한 스타일 💡", "추리"),
    "ESTJ": ("체계적이고 책임감 있는 스타일 📌", "자기계발"),
    "ESFJ": ("친절하고 사교적인 스타일 🤝", "감동"),
    "ENFJ": ("공감 능력이 뛰어난 스타일 🌷", "성장"),
    "ENTJ": ("목표 지향적인 스타일 🚀", "도전")
}

# -------------------------------
# 3. 책 데이터
# -------------------------------

books = [
    {
        "title": "아몬드",
        "author": "손원평",
        "genre": "성장",
        "mood": "감동",
        "desc": "감정과 공감의 의미를 생각하게 하는 소설"
    },
    {
        "title": "완득이",
        "author": "김려령",
        "genre": "성장",
        "mood": "유쾌함",
        "desc": "한 청소년의 성장과 주변 사람들의 이야기를 담은 소설"
    },
    {
        "title": "불편한 편의점",
        "author": "김호연",
        "genre": "감동",
        "mood": "힐링",
        "desc": "편의점을 중심으로 다양한 사람들의 이야기가 펼쳐지는 소설"
    },
    {
        "title": "달러구트 꿈 백화점",
        "author": "이미예",
        "genre": "판타지",
        "mood": "힐링",
        "desc": "꿈을 사고파는 신비로운 세계를 그린 소설"
    },
    {
        "title": "해리 포터와 마법사의 돌",
        "author": "J.K. 롤링",
        "genre": "판타지",
        "mood": "모험",
        "desc": "마법 학교에서 펼쳐지는 신비한 모험 이야기"
    },
    {
        "title": "어린 왕자",
        "author": "앙투안 드 생텍쥐페리",
        "genre": "성장",
        "mood": "감성",
        "desc": "사랑과 관계, 삶의 의미를 돌아보게 하는 이야기"
    },
    {
        "title": "데미안",
        "author": "헤르만 헤세",
        "genre": "성장",
        "mood": "생각할 거리",
        "desc": "자신만의 길을 찾아가는 과정을 다룬 소설"
    },
    {
        "title": "셜록 홈즈의 모험",
        "author": "아서 코난 도일",
        "genre": "추리",
        "mood": "긴장감",
        "desc": "명탐정 셜록 홈즈의 흥미로운 추리 이야기"
    },
    {
        "title": "미움받을 용기",
        "author": "기시미 이치로, 고가 후미타케",
        "genre": "자기계발",
        "mood": "생각할 거리",
        "desc": "인간관계와 자기 자신을 바라보는 관점을 다룬 책"
    },
    {
        "title": "코스모스",
        "author": "칼 세이건",
        "genre": "과학",
        "mood": "생각할 거리",
        "desc": "우주와 과학에 관한 흥미로운 이야기를 담은 책"
    },
    {
        "title": "죽이고 싶은 아이",
        "author": "이꽃님",
        "genre": "추리",
        "mood": "긴장감",
        "desc": "사건을 둘러싼 진실을 추적하는 청소년 소설"
    },
    {
        "title": "시간을 파는 상점",
        "author": "김선영",
        "genre": "판타지",
        "mood": "감성",
        "desc": "시간과 선택의 의미를 생각하게 하는 청소년 소설"
    }
]

# -------------------------------
# 4. 영화 데이터
# 모든 영화는 2010년 이후 개봉작
# -------------------------------

movies = [
    {
        "title": "인사이드 아웃",
        "year": 2015,
        "genre": "애니메이션",
        "mood": "감동",
        "desc": "마음속 감정들을 통해 감정의 소중함을 알려 주는 영화"
    },
    {
        "title": "코코",
        "year": 2017,
        "genre": "애니메이션",
        "mood": "감동",
        "desc": "가족과 꿈, 음악의 의미를 전하는 따뜻한 영화"
    },
    {
        "title": "스파이더맨: 뉴 유니버스",
        "year": 2018,
        "genre": "액션",
        "mood": "모험",
        "desc": "새로운 영웅이 자신의 가능성을 발견하는 이야기"
    },
    {
        "title": "인터스텔라",
        "year": 2014,
        "genre": "SF",
        "mood": "생각할 거리",
        "desc": "우주 탐험을 통해 사랑과 시간, 인류의 미래를 생각하게 하는 영화"
    },
    {
        "title": "마션",
        "year": 2015,
        "genre": "SF",
        "mood": "모험",
        "desc": "화성에 홀로 남겨진 주인공이 지혜와 끈기로 생존하는 이야기"
    },
    {
        "title": "주토피아",
        "year": 2016,
        "genre": "애니메이션",
        "mood": "유쾌함",
        "desc": "편견을 넘어 꿈을 향해 나아가는 주인공의 이야기"
    },
    {
        "title": "월터의 상상은 현실이 된다",
        "year": 2013,
        "genre": "드라마",
        "mood": "힐링",
        "desc": "평범한 일상에서 벗어나 새로운 도전을 시작하는 이야기"
    },
    {
        "title": "히든 피겨스",
        "year": 2016,
        "genre": "드라마",
        "mood": "감동",
        "desc": "편견을 극복하고 자신의 능력을 증명한 여성 수학자들의 이야기"
    },
    {
        "title": "레디 플레이어 원",
        "year": 2018,
        "genre": "SF",
        "mood": "모험",
        "desc": "가상 세계에서 펼쳐지는 흥미진진한 모험"
    },
    {
        "title": "극한직업",
        "year": 2019,
        "genre": "코미디",
        "mood": "유쾌함",
        "desc": "잠복 수사를 위해 치킨집을 운영하게 된 형사들의 코미디"
    },
    {
        "title": "소울",
        "year": 2020,
        "genre": "애니메이션",
        "mood": "생각할 거리",
        "desc": "삶의 목적과 일상의 행복에 대해 생각하게 하는 영화"
    },
    {
        "title": "엘리멘탈",
        "year": 2023,
        "genre": "애니메이션",
        "mood": "감동",
        "desc": "서로 다른 환경에서 살아온 두 인물의 만남과 관계를 다룬 영화"
    }
]

# -------------------------------
# 5. MBTI 선택
# -------------------------------

st.subheader("1️⃣ 나의 MBTI 선택하기")

selected_mbti = st.selectbox(
    "너의 MBTI를 선택해 줘!",
    list(mbti_data.keys())
)

st.info(
    f"{selected_mbti}: {mbti_data[selected_mbti][0]}"
)

# -------------------------------
# 6. 추천 단서 선택
# -------------------------------

st.subheader("2️⃣ 원하는 단서 선택하기")

clue_options = [
    "MBTI 맞춤 추천",
    "감동",
    "판타지",
    "추리",
    "성장",
    "자기계발",
    "과학",
    "애니메이션",
    "SF",
    "액션",
    "코미디",
    "힐링",
    "모험",
    "유쾌함",
    "생각할 거리"
]

selected_clue = st.selectbox(
    "어떤 작품을 보고 싶어?",
    clue_options
)

# -------------------------------
# 7. 추천 함수
# -------------------------------

def recommend_books(mbti, clue):
    if clue == "MBTI 맞춤 추천":
        target = mbti_data[mbti][1]

        # MBTI에 해당하는 장르를 우선 추천
        result = [
            book for book in books
            if book["genre"] == target
            or book["mood"] == target
        ]
    else:
        result = [
            book for book in books
            if book["genre"] == clue
            or book["mood"] == clue
        ]

    # 조건에 맞는 작품이 부족하면 전체 목록에서 보충
    if len(result) < 2:
        result = result + [
            book for book in books
            if book not in result
        ]

    return random.sample(result, 2)


def recommend_movies(mbti, clue):
    if clue == "MBTI 맞춤 추천":
        target = mbti_data[mbti][1]

        if target in ["과학"]:
            result = [
                movie for movie in movies
                if movie["genre"] == "SF"
            ]
        elif target in ["추리", "도전"]:
            result = [
                movie for movie in movies
                if movie["mood"] == "모험"
            ]
        elif target == "코미디":
            result = [
                movie for movie in movies
                if movie["genre"] == "코미디"
                or movie["mood"] == "유쾌함"
            ]
        elif target == "판타지":
            result = [
                movie for movie in movies
                if movie["mood"] == "모험"
                or movie["genre"] == "애니메이션"
            ]
        else:
            result = [
                movie for movie in movies
                if movie["mood"] == "감동"
                or movie["mood"] == "생각할 거리"
            ]

    else:
        # 장르 단서
        genre_matches = [
            movie for movie in movies
            if movie["genre"] == clue
        ]

        # 분위기 단서
        mood_matches = [
            movie for movie in movies
            if movie["mood"] == clue
        ]

        result = genre_matches + mood_matches

    # 영화가 2개 미만이면 전체 영화에서 보충
    if len(result) < 2:
        result = result + [
            movie for movie in movies
            if movie not in result
        ]

    # 2010년 이후 개봉한 영화만 추천
    result = [
        movie for movie in result
        if movie["year"] > 2010
    ]

    return random.sample(result, 2)


# -------------------------------
# 8. 추천 결과 표시
# -------------------------------

if st.button("🎁 책과 영화 추천받기", use_container_width=True):

    recommended_books = recommend_books(
        selected_mbti,
        selected_clue
    )

    recommended_movies = recommend_movies(
        selected_mbti,
        selected_clue
    )

    st.divider()

    st.header("📚 너를 위한 책 2권")

    for number, book in enumerate(recommended_books, start=1):
        with st.container(border=True):
            st.subheader(f"📖 {number}. {book['title']}")
            st.write(f"✍️ 작가: {book['author']}")
            st.write(f"🏷️ 장르: {book['genre']}")
            st.write(f"💬 추천 이유: {book['desc']}")

    st.divider()

    st.header("🎬 너를 위한 영화 2개")

    for number, movie in enumerate(recommended_movies, start=1):
        with st.container(border=True):
            st.subheader(f"🍿 {number}. {movie['title']}")
            st.write(f"📅 개봉 연도: {movie['year']}년")
            st.write(f"🏷️ 장르: {movie['genre']}")
            st.write(f"💬 추천 이유: {movie['desc']}")

    st.success("🎉 추천 완료! 마음에 드는 작품을 즐겨 봐!")

    st.caption(
        "※ MBTI에 따른 추천은 재미를 위한 참고 자료야. "
        "실제 취향과 다를 수 있어!"
    )

# -------------------------------
# 9. 하단 안내
# -------------------------------

st.divider()
st.caption("📚 책 2권 + 🎬 영화 2개를 추천하는 MBTI 맞춤 서비스")
st.caption("영화는 2010년 이후 개봉작으로 구성했어.")
```
