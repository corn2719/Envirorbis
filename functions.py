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
            'bar': {'color': "black"},
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

# 행의 수에 따라 열을 나누는 함수
def split_data(df):
    half = len(df) // 2
    if len(df) % 2 != 0:
        half += 1  # 홀수 개일 때는 첫 열에 하나 더 추가
    left_df = df.iloc[:half]
    right_df = df.iloc[half:].reset_index(drop=True)
    return left_df, right_df

# HTML과 CSS를 활용한 표 생성
def generate_html_table(df):
    left_df, right_df = split_data(df)
    
    html_table = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 10px;
        text-align: center;
        border: 1px solid #dddddd;
    }
    th {
        background-color: #f2f2f2;
    }
    </style>
    <table>
        <tr>
            <th>기업이름</th>
            <th>전월</th>
            <th>현월</th>
            <th>기업이름</th>
            <th>전월</th>
            <th>현월</th>
        </tr>
    """

    for i in range(len(left_df)):
        html_table += "<tr>"
        for col in left_df.columns:
            value = left_df[col][i]
            if col == '현월':
                prev_value = left_df['전월'][i]
                color = "black" if value == prev_value else "green" if value < prev_value else "red"
                html_table += f'<td style="color: {color};">{value}</td>'
            else:
                html_table += f"<td>{value}</td>"

        if i < len(right_df):
            for col in right_df.columns:
                value = right_df[col][i]
                if col == '현월':
                    prev_value = right_df['전월'][i]
                    color = "black" if value == prev_value else "green" if value < prev_value else "red"
                    html_table += f'<td style="color: {color};">{value}</td>'
                else:
                    html_table += f"<td>{value}</td>"
        else:
            html_table += "<td></td><td></td><td></td>"

        html_table += "</tr>"

    html_table += "</table>"
    return html_table