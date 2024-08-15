import streamlit as st
import datetime
# import plotly.graph_objs as go
import pandas as pd
from pytz import timezone
from functions import *

# data
file_path = "/Users/keunwoook/Library/Mobile Documents/com~apple~CloudDocs/Document/Envirorbis/test_data.xlsx"
df = pd.read_excel(file_path, header=0)

# 데이터 범주화    
df['전월'] = df['전월'].apply(categorize_value)
df['현월'] = df['현월'].apply(categorize_value)

# layout을 wide로 지정
st.set_page_config(layout="wide")

# 최상단 제목, 날짜, 산업진흥원 로고
title = '에너지 모니터링 시스템'
kst = timezone('Asia/Seoul')
now = datetime.datetime.now()
now = now.astimezone(kst)
today = now.strftime("%Y-%m-%d")
logo_path = "http://dipa.or.kr/wp-content/uploads/2020/07/logo_h_1000.jpg"  # 경로를 상대경로 또는 웹 경로로 수정

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
            text-align: right;  /* 우측 정렬 */
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


### 

# columns를 통해 가로로 배치
col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="center")
with col1:
    create_gauge_chart(75, min_value=0, max_value=100, title="목표달성추이", height=300)

with col2:
    st.markdown(draw_box('목표치', '3000 KWh', width='100%', height=310, text_color='black', margin_bottom='0px'), unsafe_allow_html=True)

# 박스를 col3에 표시
with col3:
    st.markdown(draw_box('현월', '3100 KWh', width='100%', height=150, text_color='black', margin_bottom='10px'), unsafe_allow_html=True)
    st.markdown(draw_box('전월대비', '+30%', width='100%', height=150, text_color='red', margin_bottom='0px'), unsafe_allow_html=True)


with col4:
    st.markdown(draw_box('전체 기업 수', '10 개', width='100%', height=150, text_color='black', margin_bottom='10px'), unsafe_allow_html=True)
    st.markdown(draw_box('전체 기업 평균', '310 KWh', width='100%', height=150, text_color='black', margin_bottom='0px'), unsafe_allow_html=True)



###
st.title('입주기업')


# 표 그리기
# 데이터프레임을 5행씩 두 개로 나누기
df_upper = df.iloc[:5, :]
df_lower = df.iloc[5:, :]

col1, col2 = st.columns(2)

# 조건에 따라 색상을 지정하는 함수 정의
# 현월 값의 색상 지정 함수 정의
def color_current_month(row):
    if row['현월'] < row['전월']:
        return ['color: black', 'color: black', 'color: green']
    elif row['현월'] > row['전월']:
        return ['color: black', 'color: black', 'color: red']
    else:
        return ['color: black', 'color: black', 'color: black']

# 데이터프레임에 스타일 적용
styled_df_lower = df_lower.style.apply(lambda row: color_current_month(row), axis=1, subset=['기업 이름', '전월', '현월'])
styled_df_upper = df_upper.style.apply(lambda row: color_current_month(row), axis=1, subset=['기업 이름', '전월', '현월'])


with col1:
    st.dataframe(styled_df_lower, hide_index=True, use_container_width=True)

with col2:
    st.dataframe(styled_df_upper, hide_index=True, use_container_width=True)