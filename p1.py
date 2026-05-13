import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="Open View Flashcards", page_icon="📖", layout="centered")

# --- 커스텀 블랙 & 화이트 테마 CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    h1, h2, h3, p, span, label {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }

    /* 플래시카드 스타일: 질문과 답변이 모두 담기도록 높이 조정 */
    .flashcard {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 0px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 8px 8px 0px #000000;
    }

    .q-section {
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 1px solid #EEEEEE;
        padding-bottom: 10px;
        margin-bottom: 15px;
        color: #666666 !important;
    }

    .a-section {
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        margin-top: 20px;
        padding-top: 10px;
        border-top: 1px dashed #000000;
        color: #000000 !important;
    }

    .content-text {
        font-size: 20px;
        font-weight: 500;
        color: #000000;
    }

    .stButton>button {
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 0px;
        border: 1px solid #000000;
        width: 100%;
        height: 50px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #FFFFFF;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
if 'cards' not in st.session_state:
    st.session_state.cards = [
        {"q": "컴퓨터 비전이란?", "a": "컴퓨터가 이미지나 비디오를 이해하도록 하는 인공지능 분야입니다."},
        {"q": "파이썬 f-string?", "a": "f'{변수}' 형태로 문자열 안에 변수를 넣는 간편한 방식입니다."}
    ]

if 'card_index' not in st.session_state:
    st.session_state.card_index = 0

# --- 앱 UI ---
st.title("📖 OPEN-VIEW CARDS")

if len(st.session_state.cards) > 0:
    current_card = st.session_state.cards[st.session_state.card_index]

    # 질문과 답변을 동시에 표시하는 카드
    st.markdown(f"""
        <div class="flashcard">
            <div class="q-section">Question</div>
            <div class="content-text">{current_card['q']}</div>
            <div class="a-section">Answer</div>
            <div class="content-text">{current_card['a']}</div>
        </div>
    """, unsafe_allow_html=True)

    # 제어 버튼 (Flip 삭제, Prev/Next만 유지)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("PREVIOUS"):
            st.session_state.card_index = (st.session_state.card_index - 1) % len(st.session_state.cards)
            st.rerun()
    with col2:
        if st.button("NEXT"):
            st.session_state.card_index = (st.session_state.card_index + 1) % len(st.session_state.cards)
            st.rerun()

    st.write(f"Card {st.session_state.card_index + 1} / {len(st.session_state.cards)}")
else:
    st.info("표시할 카드가 없습니다.")

st.markdown("---")

# 카드 관리 섹션
with st.expander("➕ ADD NEW CARD"):
    with st.form("new_card", clear_on_submit=True):
        q = st.text_input("질문 입력")
        a = st.text_area("정답 입력")
        if st.form_submit_button("저장하기") and q and a:
            st.session_state.cards.append({"q": q, "a": a})
            st.rerun()

if st.button("DELETE CURRENT CARD"):
    if st.session_state.cards:
        st.session_state.cards.pop(st.session_state.card_index)
        st.session_state.card_index = 0
        st.rerun()
