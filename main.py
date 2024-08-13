import streamlit as st
import datetime
import plotly.graph_objs as go
import pandas as pd

# data
# 데이터 준비
data = {
    '기업 이름': ['기업 A', '기업 B', '기업 C', '기업 D', '기업 E', '기업 F', '기업 G', '기업 H', '기업 I', '기업 J'],
    '전월': [7, 3, 6, 1, 2, 6, 4, 7, 2, 5],
    '현월': [3, 4, 4, 6 ,2, 1, 6 ,7 ,3, 5]
}
# DataFrame 생성
df = pd.DataFrame(data)


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
                'thickness': 0.4,
                'value': value
            }
        }
    ))
    # 레이아웃 설정을 통해 높이 조정
    fig.update_layout(height=height)

    # Streamlit에 차트 표시
    st.plotly_chart(fig)

# 박스를 그리는 함수 정의
def draw_box(title, content, width='100%', height=150, border_color='#CACCCB', background_color='#E2E3E5', text_color='black', margin_bottom='10px'):
    return f"""
    <div style="width: {width}px; height: {height}px; border: 2px solid {border_color}; border-radius: 10px; padding: 20px; background-color: {background_color}; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: {margin_bottom};">
        <p style="font-size: 24px; margin: 0;">{title}</p>
        <p style="font-size: 45px; font-weight: bold; color: {text_color}; margin: 0;">{content}</p>
    </div>
    """

# layout을 wide로 지정
st.set_page_config(layout="wide")

# 최상단 제목, 날짜, 산업진흥원 로고
title = '에너지 모니터링 시스템'
now = datetime.datetime.now()
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