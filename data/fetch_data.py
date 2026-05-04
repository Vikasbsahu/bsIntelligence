import yfinance as yf
import pandas as pd

def load_market_data():
    nifty = yf.download("^NSEI", period="10y", auto_adjust=True)
    vix = yf.download("^INDIAVIX", period="10y", auto_adjust=True)

    nifty_close = nifty["Close"].squeeze()
    vix_close = vix["Close"].squeeze()

    combined = pd.DataFrame({
        "Nifty": nifty_close,
        "VIX": vix_close
    }).dropna()

    combined["52W_High"] = combined["Nifty"].rolling(252).max()
    combined["50DMA"] = combined["Nifty"].rolling(50).mean()
    combined["200DMA"] = combined["Nifty"].rolling(200).mean()

    return combined
