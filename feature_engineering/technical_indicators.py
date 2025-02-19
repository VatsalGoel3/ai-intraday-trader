import pandas as pd
import ta
import ta.momentum
import ta.trend
import ta.volatility

def compute_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Computes several technical indicators on the DataFrame.

    Parameters:
        data (DataFrame): Must contain a 'close' column for closing prices.

    Returns:
        DataFrame: Original data with added technical indicator columns.
    """
    # Calculate 20-day Simple Moving Average (SMA)
    data['sma_20'] = data['close'].rolling(window=20).mean() # Averages closing prices over 20 days

    # Calculate 20-day Exponential Moving Average (EMA)
    data['ema_20'] = data['close'].ewm(span=20, adjust=False).mean() #Gives more weight to recent prices

    # Calculate 14-day Relative Strength Index (RSI)
    data['rsi'] = ta.momentum.rsi(data['close'], window=14) # Measures speed and change of price movements

    # Calculate Moving Average Convergence Divergence (MACD)
    data['macd'] = ta.trend.macd(data['close']) # Shows the relationship between two moving averages

    # Calculate Bollinger Bands (20-day window, 2 standard deviations)
    bb_indicator = ta.volatility.BollingerBands(data['close'], window=20, window_dev=2)
    data['bb_high'] = bb_indicator.bollinger_hband() # Upper band representing overbought conditions
    data['bb_low'] = bb_indicator.bollinger_lband() # Lower band representing oversold conditions

    return data