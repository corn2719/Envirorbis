import streamlit as st
import datetime
import plotly.graph_objs as go
import pandas as pd


# 함수 정의
# 게이지 차트를 그리는 함수 정의
def create_gauge_chart(value, min_value=0, max_value=100, title="Gauge Chart", height=250):
    # Plotly를 사용하여 게이지 차트 생성
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': "pink"},
            'steps': [
                {'range': [min_value, max_value * 0.2], 'color': "red"},
                {'range': [max_value * 0.2, max_value * 0.4], 'color': "orange"},
                {'range': [max_value * 0.4, max_value * 0.6], 'color': "yellow"},
                {'range': [max_value * 0.6, max_value * 0.8], 'color': "lightgreen"},
                {'range': [max_value * 0.8, max_value], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 3},
                'thickness': 1,
                'value': value
            }
        }
    ))
    # 레이아웃 설정을 통해 높이 조정
    fig.update_layout(height=height)

    # Streamlit에 차트 표시
    st.plotly_chart(fig)

# layout을 wide로 지정
st.set_page_config(layout="wide")

# 최상단 제목, 날짜, 산업진흥원 로고
title = 'Envirorbis'
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")
logo_path = "http://dipa.or.kr/wp-content/uploads/2020/07/logo_v_1000.jpg"  # 경로를 상대경로 또는 웹 경로로 수정

# columns를 통해 가로로 배치
col1, col2, col3, col4 = st.columns([3, 1, 1, 1], vertical_alignment="center")

# col1의 글씨 크기 설정 및 좌측 정렬
with col1:
    st.markdown("""
        <style>
        .col1-font {
            font-size:50px !important;
            color: black;
            display: flex;
            font-weight: bold;
            text-align: left;  /* 좌측 정렬 */
            align-items: flex-end; /* 아래 정렬 */
            height: 100%; /* 전체 높이 사용 */
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f'<p class="col1-font">{title}</p>', unsafe_allow_html=True)

# col3의 글씨 크기 설정 및 우측 정렬
with col3:
    st.markdown("""
        <style>
        .col3-font {
            font-size:35px !important;
            color: black;
            display: flex;
            text-align: right;  /* 우측 정렬 */
            align-items: flex-end; /* 아래 정렬 */
            height: 100%; /* 전체 높이 사용 */
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f'<p class="col3-font">{today}</p>', unsafe_allow_html=True)

# col4에서 이미지 중앙 정렬
with col4:
    # 이미지 파일 경로를 사용하여 이미지를 불러옴
    st.image(logo_path, width=150)


### 

# columns를 통해 가로로 배치
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    create_gauge_chart(75, min_value=0, max_value=100, title="목표달성추이", height=300)



###
st.title('입주기업')


# 표 그리기
# 데이터 준비
data = {
    '기업 이름 1': ['기업 A', '기업 B', '기업 C', '기업 D', '기업 E'],
    '전월 1': [100, 200, 300, 400, 500],
    '현월 1': [110, 210, 310, 410, 510],
    '기업 이름 2': ['기업 F', '기업 G', '기업 H', '기업 I', '기업 J'],
    '전월 2': [150, 250, 350, 450, 550],
    '현월 2': [160, 260, 360, 460, 560]
}

# DataFrame 생성
df = pd.DataFrame(data)

# Streamlit 앱에서 DataFrame 출력
st.dataframe(df, use_container_width=True, hide_index=True)