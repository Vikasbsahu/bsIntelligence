import pandas as pd
import yfinance as yf
import streamlit as st

# -----------------------------------
# FETCH DATA (PRIMARY)
# -----------------------------------
def fetch_market_data():
    try:
        nifty = yf.download("^NSEI", period="6mo", interval="1d", progress=False)
        vix = yf.download("^INDIAVIX", period="6mo", interval="1d", progress=False)

        if nifty.empty:
            return None, "❌ No Data"

        df = pd.DataFrame()
        df["Nifty"] = nifty["Close"]

        if not vix.empty:
            df["VIX"] = vix["Close"]
        else:
            df["VIX"] = 15

        df["52W_High"] = df["Nifty"].rolling(126).max()

        return df.dropna(), "🟢 Yahoo (Stable)"

    except Exception as e:
        print(e)
        return None, "❌ Error"


# -----------------------------------
# SAFE FALLBACK
# -----------------------------------
def fallback_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=200)

    df = pd.DataFrame(index=dates)
    df["Nifty"] = range(20000, 20200)
    df["VIX"] = [15] * 200
    df["52W_High"] = df["Nifty"].rolling(50).max()

    return df, "🔴 Fallback (Not Real)"


# -----------------------------------
# MAIN FUNCTION
# -----------------------------------
@st.cache_data(ttl=600)
def load_market_data():

    df, source = fetch_market_data()

    if df is not None and not df.empty:
        return df, source

    return fallback_data()
