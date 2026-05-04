import pandas as pd
import yfinance as yf
import requests
import streamlit as st

def fetch_from_yahoo():
    try:
        nifty = yf.download("^NSEI", period="1y", progress=False)
        vix = yf.download("^INDIAVIX", period="1y", progress=False)

        if nifty.empty or vix.empty:
            return None

        df = pd.DataFrame()
        df["Nifty"] = nifty["Close"]
        df["VIX"] = vix["Close"]

        df["52W_High"] = df["Nifty"].rolling(252).max()

        return df.dropna()

    except:
        return None


def fetch_from_fallback():
    try:
        url = "https://query1.finance.yahoo.com/v7/finance/chart/%5ENSEI"
        r = requests.get(url, timeout=5)

        data = r.json()
        ts = data["chart"]["result"][0]["timestamp"]
        closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]

        df = pd.DataFrame({"Nifty": closes})
        df.index = pd.to_datetime(ts, unit="s")

        df["VIX"] = 15  # fallback
        df["52W_High"] = df["Nifty"].rolling(252).max()

        return df.dropna()

    except:
        return None


def generate_sample_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=200)

    df = pd.DataFrame(index=dates)
    df["Nifty"] = range(20000, 20200)
    df["VIX"] = [15] * 200
    df["52W_High"] = df["Nifty"].rolling(50).max()

    return df


@st.cache_data(ttl=600)
def load_market_data():

    df = fetch_from_yahoo()
    if df is not None and not df.empty:
        return df

    df = fetch_from_fallback()
    if df is not None and not df.empty:
        return df

    return generate_sample_data()
