import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="B&W Flashcards", page_icon="🎴", layout="centered")

# --- 커스텀 버튼 스타일 (하얀 배경, 검은 글씨) ---
st.markdown("""
    <style>
    /* 전체 배경 흰색 */
    .stApp { background-color: #FFFFFF; }

    /* 모든 버튼 스타일 강제 지정 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
        transition: 0.2s;
    }

    /* 버튼 호버 효과 (살짝 회색으로 변경) */
    div.stButton > button:hover {
        background-color: #F0F0F0 !important;
        border: 2px solid #000000 !important;
    }

    /* 카드 스타일 */
    .flashcard {
        background-color: #FFFFFF;
        border: 4px solid #000000;
        padding: 50px;
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        box-shadow: 10px 10px 0px #000000;
    }

    .label {
        font-size: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
        color: #666;
    }

    .content {
        font-size: 28px;
        font-weight: bold;
        color: #000;
    }

    /* 입력창 테두리 검정색 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
if 'cards' not in st.session_state:
    st.session_state.cards = [
        {"q": "GitHub란?", "a": "분산 버전 관리 시스템인 Git을 사용하는 프로젝트를 지원하는 웹 호스팅 서비스입니다."},
        {"q": "Streamlit이란?", "a": "데이터 과학 및 머신러닝 팀이 데이터를 공유하기 위한 웹 앱을 만드는 오픈 소스 프레임워크입니다."}
    ]

if 'idx' not in st.session_state:
    st.session_state.idx = 0

if 'flipped' not in st.session_state:
    st.session_state.flipped = False

# --- UI 레이아웃 ---
st.markdown("<h1 style='text-align: center; color: black; letter-spacing: -1px;'>FLASHCARD SYSTEM</h1>", unsafe_allow_html=True)

if len(st.session_state.cards) > 0:
    curr = st.session_state.cards[st.session_state.idx]
    
    # 카드 영역
    mode = "ANSWER" if st.session_state.flipped else "QUESTION"
    text = curr['a'] if st.session_state.flipped else curr['q']
    
    st.markdown(f"""
        <div class="flashcard">
            <div class="label">{mode}</div>
            <div class="content">{text}</div>
        </div>
    """, unsafe_allow_html=True)

    # 버튼 레이아웃 (PREV, FLIP, NEXT)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col1:
        if st.button("PREVIOUS"):
            st.session_state.idx = (st.session_state.idx - 1) % len(st.session_state.cards)
            st.session_state.flipped = False
            st.rerun()
    with col2:
        if st.button("FLIP"):
            st.session_state.flipped = not st.session_state.flipped
            st.rerun()
    with col3:
        if st.button("NEXT"):
            st.session_state.idx = (st.session_state.idx + 1) % len(st.session_state.cards)
            st.session_state.flipped = False
            st.rerun()

    st.markdown(f"<p style='text-align: center; color: black;'>Card {st.session_state.idx + 1} / {len(st.session_state.cards)}</p>", unsafe_allow_html=True)

else:
    st.info("카드가 없습니다.")

# --- 관리 섹션 (MANAGE CARD) ---
st.markdown("---")
with st.expander("➕ MANAGE CARDS (ADD/DELETE)"):
    st.subheader("Add New Card")
    q = st.text_input("Question")
    a = st.text_area("Answer")
    if st.button("ADD CARD"):
        if q and a:
            st.session_state.cards.append({"q": q, "a": a})
            st.rerun()
    
    st.markdown("---")
    if st.button("DELETE CURRENT CARD"):
        if st.session_state.cards:
            st.session_state.cards.pop(st.session_state.idx)
            st.session_state.idx = 0
            st.session_state.flipped = False
            st.rerun()
