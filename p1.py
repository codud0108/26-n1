import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="수학 함수 시각화 마스터", layout="centered")

st.title("수학 그래프 시각화하기")
st.write("1차, 2차, 3차 함수부터 초월함수까지, 수식을 입력하면 실시간으로 그래프를 그려줍니다.")

# 사이드바 설정
st.sidebar.header("⚙️ 그래프 설정")
x_min = st.sidebar.number_input("X 최소값", value=-5.0)
x_max = st.sidebar.number_input("X 최대값", value=5.0)
points = st.sidebar.slider("그래프 부드러움 (데이터 수)", min_value=100, max_value=1000, value=500)

# 상세 가이드 표 제공
st.markdown("### 💡 함수식 입력 문법 & 예시 가이드")
st.markdown("""
| 함수 종류 | 수학적 표현 | **앱에 입력할 형태 (복사해서 테스트해보세요!)** |
| :--- | :--- | :--- |
| **1차 함수** | $y = 2x + 3$ | `2*x + 3` |
| **2차 함수** | $y = x^2 - 4x + 4$ | `x**2 - 4*x + 4` |
| **3차 함수** | $y = x^3 - 3x$ | `x**3 - 3*x` |
| **4차 함수** | $y = x^4 - 2x^2$ | `x**4 - 2*x**2` |
| **분수/무리함수** | $y = \\frac{1}{x}$, $y = \\sqrt{x}$ | `1/x` 또는 `sqrt(x)` *(X 범위를 양수로 조절하세요)* |
| **삼각함수** | $y = 2\\sin(x)$ | `2 * sin(x)` |
| **종합 예시** | $y = x^3 - 3x^2 + 2$ | `x**3 - 3*x**2 + 2` |

⚠️ **주의사항**: `2x`처럼 기호를 생략하면 에러가 납니다. 반드시 **`2*x`**로 곱하기 기호를 넣어주세요! 거듭제곱은 **`**`**입니다.
""")

st.write("---")

# 함수식 입력받기 (기본값으로 3차 함수 지정)
user_input = st.text_input(
    "수학 함수식을 입력하세요 (x에 대한 식):", 
    value="x**3 - 3*x"
)

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
        
        # 입력된 식 계산
        y = eval(user_input, {"__builtins__": None}, allowed_words)
        
        # 분수함수 등에서 발생할 수 있는 inf(무한대) 값 처리
        y = np.where(np.isinf(y), np.nan, y)
        
        # Plotly 그래프 그리기
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y, 
            mode='lines', 
            name=f"y = {user_input}", 
            line=dict(color='#FF4B4B', width=3)
        ))
        
        # 축 및 그리드 설정 변경
        fig.update_layout(
            title=f"<b>주어진 함수의 그래프: $y = {user_input}$</b>",
            xaxis_title="X 축",
            yaxis_title="Y 축",
            template="plotly_white",
            hovermode="x unified"
        )
        
        # X축, Y축 기준선(0선) 추가해서 수학 그래프 느낌 강조
        fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")
        fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="gray")
        
        # 스트림릿에 그래프 출력
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(
            f"❌ 수식을 계산하는 중 오류가 발생했습니다. 입력 문법을 확인해주세요.\n"
            f"정확한 예시: x**3 - 3*x (곱하기는 *, 거듭제곱은 **)"
        )
