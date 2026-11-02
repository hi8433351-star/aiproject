import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="MBTI 책 & 영화 추천",
    page_icon="📚",
    layout="centered"
)

# 제목
st.title("📚 MBTI 맞춤 책 & 영화 추천 🎬")
st.write("내 MBTI에 어울리는 책과 영화를 찾아보자!")
st.write("취향에 맞는 단서를 선택하면 추천 결과가 바뀌어 😊")

# MBTI 목록
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# MBTI별 추천 성향
mbti_info = {
    "ISTJ": ("현실적이고 꼼꼼한 스타일 📝", "성장과 지식을 얻을 수 있는 작품"),
    "ISFJ": ("따뜻하고 배려심 있는 스타일 💗", "마음이 따뜻해지는 작품"),
    "INFJ": ("깊이 생각하는 스타일 🌙", "의미와 메시지가 있는 작품"),
    "INTJ": ("분석적이고 계획적인 스타일 🧠", "생각할 거리를 주는 작품"),
    "ISTP": ("호기심 많고 실용적인 스타일 🔧", "모험과 추리가 있는 작품"),
    "ISFP": ("감성적이고 자유로운 스타일 🎨", "감성과 예술을 느낄 수 있는 작품"),
    "INFP": ("상상력이 풍부한 스타일 🦋", "상상력과 감동이 있는 작품"),
    "INTP": ("논리적이고 탐구하는 스타일 🔍", "새로운 지식을 얻는 작품"),
    "ESTP": ("활동적이고 도전적인 스타일 🏃", "속도감과 재미가 있는 작품"),
    "ESFP": ("밝고 사교적인 스타일 🎉", "유쾌하고 즐거운 작품"),
    "ENFP": ("창의적이고 열정적인 스타일 ✨", "새로운 세계를 보여 주는 작품"),
    "ENTP": ("아이디어가 많고 재치 있는 스타일 💡", "독특하고 흥미로운 작품"),
    "ESTJ": ("체계적이고 책임감 있는 스타일 📌", "목표와 성취를 다룬 작품"),
    "ESFJ": ("친절하고 사람을 좋아하는 스타일 🤝", "우정과 관계를 다룬 작품"),
    "ENFJ": ("공감 능력이 뛰어난 스타일 🌷", "희망과 성장을 다룬 작품"),
    "ENTJ": ("목표 지향적이고 자신감 있는 스타일 🚀", "도전과 성공을 다룬 작품")
}

# 책 데이터
books = [
    {
        "title": "아몬드",
        "author": "손원평",
        "genre": "감동",
        "mood": "따뜻한",
        "desc": "감정과 공감의 의미를 생각하게 하는 소설"
    },
    {
        "title": "완득이",
        "author": "김려령",
        "genre": "성장",
        "mood": "유쾌한",
        "desc": "한 청소년의 성장과 주변 사람들의 이야기를 담은 소설"
    },
    {
        "title": "불편한 편의점",
        "author": "김호연",
        "genre": "감동",
        "mood": "따뜻한",
        "desc": "편의점을 중심으로 다양한 사람들의 이야기가 펼쳐지는 소설"
    },
    {
        "title": "달러구트 꿈 백화점",
        "author": "이미예",
        "genre": "판타지",
        "mood": "따뜻한",
        "desc": "꿈을 사고파는 신비로운 세계를 그린 소설"
    },
    {
        "title": "해리 포터와 마법사의 돌",
        "author": "J.K. 롤링",
        "genre": "판타지",
        "mood": "모험적인",
        "desc": "마법 학교에서 펼쳐지는 신비한 모험 이야기"
    },
    {
        "title": "어린 왕자",
        "author": "앙투안 드 생텍쥐페리",
        "genre": "성장",
        "mood": "감성적인",
        "desc": "사랑과 관계, 삶의 의미를 돌아보게 하는 이야기"
    },
    {
        "title": "데미안",
        "author": "헤르만 헤세",
        "genre": "성장",
        "mood": "감성적인",
        "desc": "자신만의 길을 찾아가는 과정을 다룬 소설"
    },
    {
        "title": "셜록 홈즈의 모험",
        "author": "아서 코난 도일",
        "genre": "추리",
        "mood": "긴장감 있는",
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
        "mood": "긴장감 있는",
        "desc": "사건을 둘러싼 진실을 추적하는 청소년 소설"
    },
    {
        "title": "시간을 파는 상점",
        "author": "김선영",
        "genre": "판타지",
        "mood": "감성적인",
        "desc": "시간과 선택의 의미를 생각하게 하는 청소년 소설"
    }
]

# 영화 데이터: 모두 2010년 이후 개봉작
movies = [
    {
        "title": "인사이드 아웃",
        "year": 2015,
        "genre": "애니메이션",
        "mood": "감동",
        "desc": "마음속 감정들이 펼치는 이야기를 통해 감정의 소중함을 알려 주는 영화"
    },
    {
        "title": "코코",
        "year": 2017,
        "genre": "애니메이션",
        "mood": "감동",
        "desc": "가족과 꿈, 음악의 의미를 전하는 따뜻한 애니메이션"
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

# MBTI별 추천 단서
mbti_genre = {
    "ISTJ": "자기계발",
    "ISFJ": "감동",
    "INFJ": "성장",
    "INTJ": "과학",
    "ISTP": "추리",
    "ISFP": "감성",
    "INFP": "판타지",
    "INTP": "과학",
    "ESTP": "액션",
    "ESFP": "코미디",
    "ENFP": "판타지",
    "ENTP": "추리",
    "ESTJ": "자기계발",
    "ESFJ": "감동",
    "ENFJ": "성장",
    "ENTJ": "자기계발"
}

# 입력 영역
st.subheader("1️⃣ 나의 MBTI 선택하기")

selected_mbti = st.selectbox(
    "너의 MBTI는 뭐야?",
    mbti_list
)

st.info(
    f"✨ {selected_mbti} 유형은 "
    f"{mbti_info[selected_mbti][0]}!"
)

st.write(mbti_info[selected_mbti][1] + "을 추천해 줄게.")

st.divider()

# 단서 선택
st.subheader("2️⃣ 원하는 단서 선택하기")

clue = st.selectbox(
    "어떤 작품을 보고 싶어?",
    [
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
)

# 추천 버튼
if st.button("🎁 책과 영화 추천받기", use_container_width=True):

    # 선택한 단서에 맞는 책 필터링
    if clue == "MBTI 맞춤 추천":
        book_clue = mbti_genre[selected_mbti]

        matched_books = [
            b for b in books if b["genre"] == book_clue
        ]

        if len(matched_books) < 2:
            matched_books = books

    elif clue == "감동":
        matched_books = [
            b for b in books
            if b["mood"] == "따뜻한"
        ]

    elif clue == "판타지":
        matched_books = [
            b for b in books
            if b["genre"] == "판타지"
        ]

    elif clue in ["추리", "성장", "자기계발", "과학"]:
        matched_books = [
            b for b in books
            if b["genre"] == clue
        ]

    elif clue == "생각할 거리":
        matched_books = [
            b for b in books
            if b["mood"] == clue
        ]

    elif clue == "힐링":
        matched_books = [
            b for b in books
            if b["mood"] == "따뜻한"
        ]

    elif clue == "유쾌함":
        matched_books = [
            b for b in books
            if b["mood"] == "유쾌한"
        ]

    elif clue == "모험":
        matched_books = [
            b for b in books
            if b["genre"] == "판타지"
        ]

    elif clue == "액션":
        matched_books = [
            b for b in books
            if b["genre"] == "추리"
        ]

    elif clue == "코미디":
        matched_books = [
            b for b in books
            if b["mood"] == "유쾌한"
        ]

    elif clue == "애니메이션":
        matched_books = [
            b for b in books
            if b["genre"] == "판타지"
        ]

    elif clue == "SF":
        matched_books = [
            b for b in books
            if b["genre"] == "과학"
        ]

    else:
        matched_books = books

    # 선택한 단서에 맞는 영화 필터링
    movie_genres = [
        "애니메이션", "SF", "액션", "코미디"
    ]

    movie_moods = [
        "감동", "모험", "유쾌함", "힐링", "생각할 거리"
    ]

    if clue == "MBTI 맞춤 추천":
        if selected_mbti in ["ISTP", "ENTP"]:
            matched_movies = [
                m for m in movies
                if m["genre"] in ["SF", "액션"]
            ]
        elif selected_mbti in ["ESFP", "ESTP"]:
            matched_movies = [
                m for m in movies
                if m["mood"] in ["유쾌함", "모험"]
            ]
        else:
            matched_movies = [
                m for m in movies
                if m["mood"] in ["감동", "생각할 거리"]
            ]

    elif clue in movie_genres:
        matched_movies = [
            m for m in movies
            if m["genre"] == clue
        ]

    elif clue in movie_moods:
        matched_movies = [
            m for m in movies
            if m["mood"] == clue
        ]

    elif clue == "판타지":
        matched_movies = [
            m for m in movies
            if m["genre"] in ["애니메이션", "SF"]
        ]

    elif clue == "추리":
        matched_movies = [
            m for m in movies
            if m["genre"] in ["SF", "액션"]
        ]

    elif clue == "성장":
        matched_movies = [
            m for m in movies
            if m["mood"] in ["감동", "모험"]
        ]

    elif clue == "자기계발":
        matched_movies = [
            m for m in movies
            if m["mood"] in ["감동", "생각할 거리"]
        ]

    elif clue == "과학":
        matched_movies = [
            m for m in movies
            if m["genre"] == "SF"
        ]

    else:
        matched_movies = movies

    # 결과가 적을 때 전체 목록에서 보충
    random.seed(selected_mbti + clue)

    if len(matched_books) < 2:
        matched_books = books.copy()

    if len(matched_movies) < 2:
        matched_movies = movies.copy()

    recommended_books = random.sample(
        matched_books, 2
    )

    recommended_movies = random.sample(
        matched_movies, 2
    )

    st.divider()
    st.header("📚 너를 위한 책 추천!")

    for i, book in enumerate(recommended_books, 1):
        st.subheader(f"📖 책 {i}: {book['title']}")
        st.write(f"✍️ 작가: {book['author']}")
        st.write(f"🏷️ 장르: {book['genre']}")
        st.write(f"💬 추천 이유: {book['desc']}")

    st.divider()
    st.header("🎬 너를 위한 영화 추천!")

    for i, movie in enumerate(recommended_movies, 1):
        st.subheader(
            f"🍿 영화 {i}: {movie['title']}"
        )
        st.write(f"📅 개봉 연도: {movie['year']}년")
        st.write(f"🏷️ 장르: {movie['genre']}")
        st.write(f"💬 추천 이유: {movie['desc']}")

    st.success(
        "🎉 추천 완료! 마음에 드는 작품을 골라서 즐겨 봐!"
    )

    st.caption(
        "※ MBTI는 재미를 위한 참고 자료야. "
        "실제 취향과 추천 결과는 다를 수 있어!"
    )
