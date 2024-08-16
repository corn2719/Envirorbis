import streamlit as st
import datetime
import pandas as pd
from pytz import timezone
from functions import *

# layout을 wide로 지정
st.set_page_config(layout="wide", page_title="용인시산업진흥원 에너지 모니터링시스템 모니용", initial_sidebar_state="collapsed")

# 사이드바에서 파일 업로드
uploaded_file = st.sidebar.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"], )
goal_value = st.sidebar.slider("목표값을 입력하세요", min_value=0, max_value=1000, step=10, value=600)

# 파일이 업로드되었는지 확인
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=0)  # 업로드된 파일로부터 데이터프레임 생성
else:
    # 데이터 예시 (3열 형태)
    data = {
        '기업 이름': ['기업A', '기업B', '기업C', '기업D', '기업E', '기업F', '기업G', '기업H', '기업I', '기업J'],
        '전월': [30, 60, 90, 100, 20, 30, 20, 80, 60, 100],
        '현월': [40, 50, 70, 130, 40, 60, 30, 70, 30, 100]
    }

    # 데이터프레임 생성
    df = pd.DataFrame(data)

# 최상단 제목, 날짜, 산업진흥원 로고
title = '모니용'
kst = timezone('Asia/Seoul')
now = datetime.datetime.now()
now = now.astimezone(kst)
today = now.strftime("%Y-%m-%d")
logo_path = "http://dipa.or.kr/wp-content/uploads/2020/07/logo_h_1000.jpg"

# Caculate values
this_month = df['현월'].sum()
prev_month = df['전월'].sum()
n_of_corp = len(df['기업 이름'])

# goal_value = 800

achivement_rate = round(100 * goal_value / this_month, 1)
if achivement_rate > 100:
    achivement_rate = 100

increase_rate = round(100 * (this_month - prev_month) / prev_month, 2)

mean_usage = round(this_month / n_of_corp, 2)

# columns를 통해 가로로 배치
col1, col2, col3, col5, col4 = st.columns([1, 1, 1, 1, 1], vertical_alignment="center")

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
            height:00%; /* 전체 높이 사용 */
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
            text-align: center;  /* 우측 정렬 */
            align-items: flex-end; /* 아래 정렬 */
            height:00%; /* 전체 높이 사용 */
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f'<p class="col3-font">{today}</p>', unsafe_allow_html=True)

# col4에서 이미지 중앙 정렬
with col4:
    # 이미지 파일 경로를 사용하여 이미지를 불러옴
    st.image(logo_path, width=150)

# columns를 통해 가로로 배치
col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="center")
with col1:
    create_gauge_chart(achivement_rate, min_value=0, max_value=100, title="목표달성추이", height=300)

with col2:
    st.markdown(draw_box('목표치', f'{goal_value} kWh', width='100%', height=310, text_color='black', margin_bottom='0px'), unsafe_allow_html=True)

# 박스를 col3에 표시
with col3:
    st.markdown(draw_box('현월', f'{this_month} kWh', width='100%', height=150, text_color='black', margin_bottom='10px'), unsafe_allow_html=True)
    # increase_rate에 따라 텍스트와 색상 설정
    if increase_rate > 0:
        display_text = f'+{increase_rate}%'  # 양수일 때 + 표시
        text_color = 'red'
    elif increase_rate < 0:
        display_text = f'-{abs(increase_rate)}%'  # 음수일 때 - 표시
        text_color = 'green'
    else:
        display_text = '0%'  # 0일 때
        text_color = 'black'  # 0인 경우 텍스트 색상은 기본 검정색으로 설정

    # draw_box 함수 호출
    st.markdown(
        draw_box('전월대비', display_text, width='100%', height=150, text_color=text_color, margin_bottom='0px'), 
        unsafe_allow_html=True
    )

with col4:
    st.markdown(draw_box('전체 기업 수', f'{n_of_corp} 개', width='100%', height=150, text_color='black', margin_bottom='10px'), unsafe_allow_html=True)
    st.markdown(draw_box('전체 기업 평균', f'{mean_usage} kWh', width='100%', height=150, text_color='black', margin_bottom='0px'), unsafe_allow_html=True)

with col5:
    image_path = "https://www.keepcalmcollection.com/cdn/shop/products/eighty-percent-of-success__66641.jpg?v=1632960458&width=990"
    st.image(image_path, use_column_width=True)

###
st.subheader('입주기업')

# 표 그리기
# 데이터 범주화    
df['전월'] = df['전월'].apply(categorize_value)
df['현월'] = df['현월'].apply(categorize_value)

# Streamlit에 HTML 표 출력
html_table = generate_html_table(df)
st.markdown(html_table, unsafe_allow_html=True)
