import streamlit as st
from core.strategy import get_ai_analysis
from core.text_generator import generate_ai_summary
from utils.plotting import create_gauge_chart

# --- Настройки страницы ---
st.set_page_config(page_title="Интуитивный Торговый ИИ", layout="wide")

# --- Заголовок ---
st.title("Интуитивный Торговый ИИ 🧠")
st.markdown("Этот ассистент анализирует рынок на основе вашей уникальной стратегии, основанной на опыте и интуиции.")

# --- Боковая панель для ввода данных ---
with st.sidebar:
    st.header("Панель управления")
    ticker = st.text_input("Введите тикер актива:", "QQQ").upper()
    
    horizon = st.radio(
        "Выберите горизонт инвестирования:",
        ["Долгосрок (Недельный)", "Среднесрок (Дневной)", "Краткосрок (4-часовой)"],
        index=1 # По умолчанию выбран среднесрок
    )

    analyze_button = st.button("🚀 Проанализировать")

# --- Словарь для маппинга горизонта ---
horizon_map = {
    "Долгосрок (Недельный)": {"timeframe": "1wk", "resample": "M"},
    "Среднесрок (Дневной)": {"timeframe": "1d", "resample": "W-MON"},
    "Краткосрок (4-часовой)": {"timeframe": "4h", "resample": "D"},
}
selected_timeframe_map = horizon_map[horizon]


# --- Основная логика при нажатии кнопки ---
if analyze_button:
    with st.spinner(f"Анализирую {ticker} на {horizon.lower()} горизонте... Это может занять до 30 секунд."):
        analysis_result = get_ai_analysis(ticker, selected_timeframe_map)

    st.subheader(f"Анализ для {ticker} | Горизонт: {horizon}")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Отображение Gauge Chart
        confidence_text = analysis_result.get("confidence", "Низкая")
        confidence_map = {"Низкая": 25, "Средняя": 50, "Высокая": 85}
        confidence_value = confidence_map.get(confidence_text, 0)
        
        st.plotly_chart(create_gauge_chart(confidence_value, confidence_text), use_container_width=True)

    with col2:
        # Отображение человекоподобного вывода
        summary_text = generate_ai_summary(analysis_result)
        st.info(summary_text)

# --- Инструкция по использованию ---
st.markdown("---")
st.write("Как это работает: Введите тикер любого актива (например, AAPL, BTC-USD, EURUSD=X), выберите горизонт и нажмите 'Проанализировать'. ИИ применит вашу стратегию и даст рекомендацию.")
