import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="수학 함수 그래프 시각화 Tool", layout="centered")

st.title("함수 그래프 시각화하기")
st.write("원하는 수학 함수식을 입력하면 실시간으로 그래프를 그려줍니다.")

# 사이드바에서 범위 및 설정 입력
st.sidebar.header("⚙️ 그래프 설정")
x_min = st.sidebar.number_input("X 최소값", value=-10.0)
x_max = st.sidebar.number_input("X 최대값", value=10.0)
points = st.sidebar.slider("조밀도 (데이터 포인트 수)", min_value=50, max_value=1000, value=500)

# 안내 문구
st.markdown("""
> 💡 **입력 가이드:**
> * 곱하기는 `*`, 거듭제곱은 `**` 로 입력하세요. (예: $x^2$은 `x**2`)
> * 파이($\pi$)는 `pi`, 자연상수($e$)는 `e`로 입력할 수 있습니다.
> * 지원 함수: `sin`, `cos`, `tan`, `log`, `exp`, `sqrt`, `abs` 등
""")

# 함수식 입력받기
user_input = st.text_input("수학 함수식을 입력하세요 (x에 대한 식):", value="sin(x) * exp(-0.1*x)")

if user_input:
    try:
        # X 축 데이터 생성
        x = np.linspace(x_min, x_max, points)
        
        # 안전한 계산을 위한 환경 사전 정의 (numpy 함수 매핑)
        allowed_words = {
            'x': x,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'log': np.log,
            'exp': np.exp,
            'sqrt': np.sqrt,
            'abs': np.abs,
            'pi': np.pi,
            'e': np.e
        }
        
        # 입력된 식 계산 (__builtins__를 차단하여 최소한의 보안 확보)
        y = eval(user_input, {"__builtins__": None}, allowed_words)
        
        # Plotly를 이용한 인터랙티브 그래프 그리기
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f"y = {user_input}", line=dict(color='#00CC96', width=3)))
        
        fig.update_layout(
            title=f"<b>주어진 함수의 그래프: $y = {user_input}$</b>",
            xaxis_title="X 축",
            yaxis_title="Y 축",
            template="plotly_white",
            hovermode="x unified"
        )
        
        # 스트림릿에 그래프 출력
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(
            f"❌ 수식을 계산하는 중 오류가 발생했습니다. 입력을 다시 확인해주세요.\n"
            f"오류 메시지: {e}"
        )
