import streamlit as st
import plotly.graph_objs as go


def categorize_value(value):
    if value < 40:
        return 1
    elif 40 <= value < 60:
        return 2
    elif 60 <= value < 80:
        return 3
    elif 80 <= value < 100:
        return 4
    elif 100 <= value < 120:
        return 5
    elif 120 <= value < 140:
        return 6
    else:
        return 7
    
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