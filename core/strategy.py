import pandas as pd
import yfinance as yf
from core.indicators import calculate_heiken_ashi, calculate_macd, calculate_pivot_points

def get_ai_analysis(ticker, timeframe_map):
    """
    Основная функция для анализа тикера на основе интуитивной стратегии.
    """
    timeframe = timeframe_map['timeframe']
    resample_period = timeframe_map['resample']
    
    try:
        # 1. Загрузка данных
        # Для 4h нужно загружать дневные данные и потом ресемплить, т.к. yfinance имеет ограничения
        if timeframe == '4h':
            data = yf.download(ticker, period="60d", interval='1h', progress=False)
            data = data.resample('4H').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}).dropna()
        else:
            data = yf.download(ticker, period="5y", interval=timeframe, progress=False)
        
        if data.empty:
            return {"signal": "WAIT", "confidence": "Низкая", "reason": "Не удалось загрузить данные для тикера."}

        data.reset_index(inplace=True)
        # Переименовываем колонку для консистентности
        if 'Datetime' in data.columns:
            data.rename(columns={'Datetime': 'Date'}, inplace=True)
        else:
             data.rename(columns={'index': 'Date'}, inplace=True)


        # 2. Расчет индикаторов
        df_ha = calculate_heiken_ashi(data.copy())
        df_ha = calculate_macd(df_ha)
        
        pivots = calculate_pivot_points(data.set_index('Date').copy(), resample_period=resample_period)
        
        # Объединяем все данные
        df_final = df_ha.join(pivots).dropna()
        
        if df_final.empty:
            return {"signal": "WAIT", "confidence": "Низкая", "reason": "Недостаточно данных для анализа."}

        # 3. Логика принятия решений (анализ последней свечи)
        last_candle = df_final.iloc[-1]
        prev_candle = df_final.iloc[-2]

        # --- Логика для ШОРТ сигнала ---
        is_near_r2 = abs(last_candle['High'] - last_candle['R2']) / last_candle['R2'] < 0.02 # Близость 2%
        is_near_r3 = abs(last_candle['High'] - last_candle['R3']) / last_candle['R3'] < 0.02

        macd_hist = df_final['MACDh_12_26_9']
        is_long_green_series = (macd_hist.iloc[-6:-1] > 0).all() and len(macd_hist) > 5
        is_macd_exhausted = is_long_green_series and (macd_hist.iloc[-1] < macd_hist.iloc[-2])
        
        if (is_near_r2 or is_near_r3) and is_macd_exhausted:
            confidence = "Высокая" if is_near_r3 else "Средняя"
            return {"signal": "SHORT", "confidence": confidence, "reason": "Обнаружено истощение роста у сильного уровня сопротивления."}

        # --- Логика для ЛОНГ сигнала ---
        is_near_s2 = abs(last_candle['Low'] - last_candle['S2']) / last_candle['S2'] < 0.02
        is_near_s3 = abs(last_candle['Low'] - last_candle['S3']) / last_candle['S3'] < 0.02
        
        is_long_red_series = (macd_hist.iloc[-6:-1] < 0).all() and len(macd_hist) > 5
        is_macd_selling_exhausted = is_long_red_series and (abs(macd_hist.iloc[-1]) < abs(macd_hist.iloc[-2]))

        if (is_near_s2 or is_near_s3) and is_macd_selling_exhausted:
            confidence = "Высокая" if is_near_s3 else "Средняя"
            return {"signal": "LONG", "confidence": confidence, "reason": "Обнаружено затухание продаж у сильного уровня поддержки."}

        # --- Если нет сигнала ---
        return {"signal": "WAIT", "confidence": "Низкая", "reason": "На рынке нет очевидной точки для входа по вашей стратегии."}

    except Exception as e:
        return {"signal": "WAIT", "confidence": "Низкая", "reason": f"Произошла ошибка: {str(e)}"}
