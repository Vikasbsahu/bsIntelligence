import pandas as pd

def calculate_dma(df):
    df["50DMA"] = df["Nifty"].rolling(50).mean()
    df["200DMA"] = df["Nifty"].rolling(200).mean()
    return df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
