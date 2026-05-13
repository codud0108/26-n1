import streamlit as st
import requests

# --- 설정 ---
API_KEY = "여기에_발급받은_API_KEY를_입력하세요"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- 날씨별 추천 음악 데이터 ---
# 실제로는 Spotify API를 연결하거나 유튜브 링크를 넣으면 더 좋습니다.
MUSIC_RECOMMENDATIONS = {
    "Clear": {"genre": "Pop / Funk", "desc": "햇살 가득한 날! 신나는 팝송 어떠세요?", "icon": "☀️"},
    "Clouds": {"genre": "Lo-fi / Indie", "desc": "구름 낀 하늘, 차분한 인디 음악이 딱이죠.", "icon": "☁️"},
    "Rain": {"genre": "Jazz / Soul", "desc": "빗소리와 어울리는 감성적인 재즈를 추천합니다.", "icon": "🌧️"},
    "Snow": {"genre": "Acoustic / Carol", "desc": "눈 내리는 풍경과 어울리는 따뜻한 어쿠스틱 음악입니다.", "icon": "❄️"},
    "Thunderstorm": {"genre": "Rock / Metal", "desc": "강렬한 비트의 락으로 에너지를 채워보세요!", "icon": "⚡"},
    "Mist": {"genre": "Ambient", "desc": "안개 속을 걷는 듯한 몽환적인 앰비언트 사운드입니다.", "icon": "🌫️"}
}

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="Weather Music App", page_icon="🎵")

st.title("🎵 날씨 맞춤형 노래 추천")
st.write("도시 이름을 입력하면 현재 날씨에 어울리는 음악 장르를 추천해 드립니다.")

city = st.text_input("도시 입력 (예: Seoul, London, Tokyo)", "Seoul")

if st.button("추천 받기"):
    data = get_weather(city)
    
    if data:
        weather_main = data['weather'][0]['main']
        temp = data['main']['temp']
        
        # 날씨 정보 표시
        st.subheader(f"📍 {city}의 현재 날씨")
        col1, col2 = st.columns(2)
        col1.metric("온도", f"{temp}°C")
        col2.metric("날씨", weather_main)

        # 음악 추천 로직
        recommendation = MUSIC_RECOMMENDATIONS.get(weather_main, {"genre": "K-Pop", "desc": "좋은 음악과 함께 즐거운 하루 보내세요!", "icon": "🎶"})
        
        st.divider()
        st.header(f"{recommendation['icon']} 오늘의 추천 장르: **{recommendation['genre']}**")
        st.info(recommendation['desc'])
        
        # (옵션) 유튜브 검색 링크 연결
        search_url = f"https://www.youtube.com/results?search_query={recommendation['genre']}+music+for+a+{weather_main}+day"
        st.link_button("유튜브에서 노래 듣기", search_url)
    else:
        st.error("도시를 찾을 수 없습니다. 영문 철자를 확인해 주세요!")
