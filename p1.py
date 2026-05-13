import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="Minimal Flashcards", page_icon="🎴", layout="centered")

# --- 커스텀 블랙 & 화이트 테마 CSS ---
st.markdown("""
    <style>
    /* 전체 배경색 흰색 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 텍스트 색상 검정색 */
    h1, h2, h3, p, span, label {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }

    /* 플래시카드 스타일 */
    .flashcard {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        min-height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        box-shadow: 5px 5px 0px #000000;
    }

    .card-text {
        font-size: 24px;
        font-weight: bold;
        color: #000000;
    }

    /* 버튼 스타일 (검정 배경, 흰 글씨) */
    .stButton>button {
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 0px;
        border: 1px solid #000000;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #000000;
    }

    /* 입력창 스타일 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 1px solid #000000 !important;
        border-radius: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 (세션 상태) ---
if 'cards' not in st.session_state:
    st.session_state.cards = [
        {"q": "Streamlit이란?", "a": "파이썬으로 웹 앱을 빠르게 만드는 라이브러리입니다."},
        {"q": "GitHub의 역할은?", "a": "코드의 버전 관리와 협업을 위한 플랫폼입니다."}
    ]

if 'card_index' not in st.session_state:
    st.session_state.card_index = 0

if 'flipped' not in st.session_state:
    st.session_state.flipped = False

# --- 앱 UI ---
st.title("🎴 MINIMAL FLASHCARDS")

# 현재 카드 정보
if len(st.session_state.cards) > 0:
    current_card = st.session_state.cards[st.session_state.card_index]

    # 카드 표시 구역
    display_text = current_card['a'] if st.session_state.flipped else current_card['q']
    label_text = "ANSWER" if st.session_state.flipped else "QUESTION"
    
    st.markdown(f"<p style='text-align:center; font-size:12px; font-weight:bold;'>{label_text}</p>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="flashcard">
            <div class="card-text">{display_text}</div>
        </div>
    """, unsafe_allow_html=True)

    # 제어 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("PREV"):
            st.session_state.card_index = (st.session_state.card_index - 1) % len(st.session_state.cards)
            st.session_state.flipped = False
            st.rerun()

    with col2:
        if st.button("FLIP"):
            st.session_state.flipped = not st.session_state.flipped
            st.rerun()

    with col3:
        if st.button("NEXT"):
            st.session_state.card_index = (st.session_state.card_index + 1) % len(st.session_state.cards)
            st.session_state.flipped = False
            st.rerun()

    st.write(f"Card {st.session_state.card_index + 1} of {len(st.session_state.cards)}")

else:
    st.info("카드가 없습니다. 아래에서 카드를 추가해 보세요.")

st.markdown("---")

# --- 카드 추가 및 삭제 관리 ---
with st.expander("➕ MANAGE CARDS"):
    with st.form("add_card_form", clear_on_submit=True):
        new_q = st.text_input("Question")
        new_a = st.text_area("Answer")
        submit = st.form_submit_button("ADD CARD")
        
        if submit and new_q and new_a:
            st.session_state.cards.append({"q": new_q, "a": new_a})
            st.success("카드가 추가되었습니다!")
            st.rerun()

    if st.button("DELETE CURRENT CARD"):
        if len(st.session_state.cards) > 0:
            st.session_state.cards.pop(st.session_state.card_index)
            st.session_state.card_index = 0
            st.session_state.flipped = False
            st.rerun()
