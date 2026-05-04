import pandas as pd
import yfinance as yf
import streamlit as st

# -----------------------------------
# FETCH DATA (STABLE VERSION)
# -----------------------------------
def fetch_market_data():
    try:
        # Use ETF proxy instead of ^NSEI
        nifty = yf.download("NIFTYBEES.NS", period="1y", progress=False)
        vix = yf.download("^INDIAVIX", period="1y", progress=False)

        if nifty.empty:
            return None

        df = pd.DataFrame()

        # Convert ETF to index-like scale
        df["Nifty"] = nifty["Close"] * 100   # approx conversion

        # VIX fallback
        if not vix.empty:
            df["VIX"] = vix["Close"]
        else:
            df["VIX"] = 15

        df["52W_High"] = df["Nifty"].rolling(252).max()

        return df.dropna()

    except Exception as e:
        print("Data fetch failed:", e)
        return None


# -----------------------------------
# FALLBACK (NEVER BREAK APP)
# -----------------------------------
def generate_sample_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=200)

    df = pd.DataFrame(index=dates)
    df["Nifty"] = range(20000, 20200)
    df["VIX"] = [15] * 200
    df["52W_High"] = df["Nifty"].rolling(50).max()

    return df


# -----------------------------------
# MAIN FUNCTION
# -----------------------------------
@st.cache_data(ttl=600)
def load_market_data():

    df = fetch_market_data()

    if df is not None and not df.empty:
        return df

    return generate_sample_data()
