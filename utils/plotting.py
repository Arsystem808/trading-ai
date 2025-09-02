 import plotly.graph_objects as go

def create_gauge_chart(confidence_value, confidence_text):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = confidence_value,
        title = {'text': f"Уверенность: {confidence_text}", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "rgba(0,0,0,0.6)"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(230, 0, 0, 0.3)'},
                {'range': [40, 60], 'color': 'rgba(255, 210, 0, 0.4)'},
                {'range': [60, 100], 'color': 'rgba(0, 180, 0, 0.3)'}
            ],
        }))
    
    fig.update_layout(height=300, margin={'t':0, 'b':0, 'l':0, 'r':0})
    return fig
