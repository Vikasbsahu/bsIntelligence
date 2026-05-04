import pandas as pd
import yfinance as yf
import requests
import streamlit as st

# -----------------------------------
# NSE LIVE PRICE (ACCURATE)
# -----------------------------------
def fetch_live_nifty():
    try:
        url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)

        response = session.get(url, headers=headers, timeout=5)
        data = response.json()

        return data["data"][0]["lastPrice"]

    except Exception as e:
        print("NSE Live fetch failed:", e)
        return None


# -----------------------------------
# YAHOO HISTORICAL (BASE DATA)
# -----------------------------------
def fetch_from_yahoo():
    try:
        nifty = yf.download("^NSEI", period="1y", progress=False)
        vix = yf.download("^INDIAVIX", period="1y", progress=False)

        if nifty.empty:
            return None

        df = pd.DataFrame()
        df["Nifty"] = nifty["Close"]

        # VIX fallback handling
        if not vix.empty:
            df["VIX"] = vix["Close"]
        else:
            df["VIX"] = 15

        # -----------------------------------
        # 🔥 OVERRIDE LAST VALUE WITH NSE LIVE
        # -----------------------------------
        live_price = fetch_live_nifty()
        if live_price is not None:
            df.iloc[-1, df.columns.get_loc("Nifty")] = live_price

        # -----------------------------------
        # CALCULATIONS
        # -----------------------------------
        df["52W_High"] = df["Nifty"].rolling(252).max()

        return df.dropna()

    except Exception as e:
        print("Yahoo fetch failed:", e)
        return None


# -----------------------------------
# SAFE FALLBACK (NEVER BREAK APP)
# -----------------------------------
def generate_sample_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=200)

    df = pd.DataFrame(index=dates)
    df["Nifty"] = range(20000, 20200)
    df["VIX"] = [15] * 200
    df["52W_High"] = df["Nifty"].rolling(50).max()

    return df


# -----------------------------------
# MAIN FUNCTION (USED BY APP)
# -----------------------------------
@st.cache_data(ttl=600)
def load_market_data():

    df = fetch_from_yahoo()
    if df is not None and not df.empty:
        return df

    return generate_sample_data()
