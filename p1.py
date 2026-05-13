import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="Flashcard Manager", page_icon="🗂️", layout="centered")

# --- 커스텀 스타일 (하얀 배경, 검은 글씨 버튼 고정) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* 모든 버튼 스타일: 하얀 배경 + 검은 글씨 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: bold !important;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #F0F0F0 !important;
    }

    /* 플래시카드 디자인 */
    .flashcard {
        background-color: #FFFFFF;
        border: 4px solid #000000;
        padding: 40px;
        text-align: center;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 10px 10px 0px #000000;
        margin-bottom: 30px;
    }

    .card-label { font-size: 12px; font-weight: bold; color: #888; text-transform: uppercase; margin-bottom: 10px; }
    .card-content { font-size: 24px; font-weight: bold; color: #000; }

    /* 리스트 아이템 스타일 */
    .card-item {
        border-bottom: 1px solid #000;
        padding: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 초기화 ---
if 'cards' not in st.session_state:
    st.session_state.cards = [
        {"q": "GitHub란?", "a": "코드 저장소 및 협업 플랫폼"},
        {"q": "Streamlit이란?", "a": "파이썬 웹 앱 프레임워크"}
    ]

if 'idx' not in st.session_state:
    st.session_state.idx = 0

if 'flipped' not in st.session_state:
    st.session_state.flipped = False

# --- 메인 학습 화면 ---
st.title("🎴 FLASHCARD STUDY")

if st.session_state.cards:
    # 인덱스 범위 초과 방지
    st.session_state.idx = min(st.session_state.idx, len(st.session_state.cards) - 1)
    curr = st.session_state.cards[st.session_state.idx]
    
    mode = "ANSWER" if st.session_state.flipped else "QUESTION"
    text = curr['a'] if st.session_state.flipped else curr['q']

    st.markdown(f"""
        <div class="flashcard">
            <div class="card-label">{mode}</div>
            <div class="card-content">{text}</div>
        </div>
    """, unsafe_allow_html=True)

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
else:
    st.info("카드가 비어있습니다. 아래에서 추가해주세요.")

st.markdown("---")

# --- 카드 관리 섹션 (MANAGE CARDS) ---
st.header("🛠️ MANAGE CARDS")

# 1. 카드 추가
with st.expander("➕ ADD NEW CARD"):
    new_q = st.text_input("질문")
    new_a = st.text_area("정답")
    if st.button("ADD CARD"):
        if new_q and new_a:
            st.session_state.cards.append({"q": new_q, "a": new_a})
            st.success("추가되었습니다!")
            st.rerun()

# 2. 개별 카드 삭제 리스트
with st.expander("🗑️ DELETE SPECIFIC CARDS", expanded=True):
    if not st.session_state.cards:
        st.write("삭제할 카드가 없습니다.")
    else:
        for i, card in enumerate(st.session_state.cards):
            col_txt, col_btn = st.columns([4, 1])
            with col_txt:
                st.markdown(f"**{i+1}. {card['q']}**")
            with col_btn:
                # 각 카드마다 고유한 키(key)를 부여하여 삭제 버튼 생성
                if st.button(f"DELETE", key=f"del_{i}"):
                    st.session_state.cards.pop(i)
                    # 현재 인덱스 조정
                    st.session_state.idx = max(0, st.session_state.idx - 1)
                    st.rerun()
