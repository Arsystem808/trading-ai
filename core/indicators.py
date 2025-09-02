import pandas as pd
import pandas_ta as ta

def calculate_heiken_ashi(df):
    """Рассчитывает свечи Heiken Ashi."""
    heiken_ashi_df = ta.ha(df['Open'], df['High'], df['Low'], df['Close'])
    # Объединяем с оригинальным DataFrame, чтобы сохранить Volume
    df_ha = pd.concat([df[['Date', 'Volume']], heiken_ashi_df], axis=1).set_index('Date')
    df_ha.rename(columns={'HA_open': 'Open', 'HA_high': 'High', 'HA_low': 'Low', 'HA_close': 'Close'}, inplace=True)
    return df_ha

def calculate_macd(df):
    """Рассчитывает MACD."""
    df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)
    return df

def calculate_pivot_points(df, resample_period='W-MON'):
    """Рассчитывает Pivot Points для заданного периода."""
    # Правило для ресемплинга: 'W-MON' для недели, 'M' для месяца, 'Y' для года
    resampled_df = df.resample(resample_period, label='right', closed='right').agg({
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    }).dropna()

    resampled_df['Pivot'] = (resampled_df['High'] + resampled_df['Low'] + resampled_df['Close']) / 3
    resampled_df['R1'] = (2 * resampled_df['Pivot']) - resampled_df['Low']
    resampled_df['S1'] = (2 * resampled_df['Pivot']) - resampled_df['High']
    resampled_df['R2'] = resampled_df['Pivot'] + (resampled_df['High'] - resampled_df['Low'])
    resampled_df['S2'] = resampled_df['Pivot'] - (resampled_df['High'] - resampled_df['Low'])
    resampled_df['R3'] = resampled_df['High'] + 2 * (resampled_df['Pivot'] - resampled_df['Low'])
    resampled_df['S3'] = resampled_df['Low'] - 2 * (resampled_df['High'] - resampled_df['Pivot'])
    
    # Сдвигаем на 1, чтобы использовать данные предыдущего периода для текущего
    return resampled_df[['Pivot', 'R1', 'S1', 'R2', 'S2', 'R3', 'S3']].shift(1)
