import streamlit as st
import pandas as pd

from data.fetch_data import load_market_data
from data.indicators import calculate_dma, calculate_rsi
from engine.signals import *
from engine.scoring import calculate_score
from config.defaults import DEFAULT_WEIGHTS
from utils.helpers import format_change

st.set_page_config(page_title="Investing Dashboard", layout="wide")

# -----------------------------------
# LOAD DATA
# -----------------------------------
df = load_market_data()

if df.empty:
    st.error("❌ No data available")
    st.stop()

df = calculate_dma(df)
df["RSI"] = calculate_rsi(df["Nifty"])

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest

# -----------------------------------
# METRICS
# -----------------------------------
nifty_change = ((latest["Nifty"] - prev["Nifty"]) / prev["Nifty"]) * 100
vix_change = ((latest["VIX"] - prev["VIX"]) / prev["VIX"]) * 100

drawdown = ((latest["Nifty"] - latest["52W_High"]) / latest["52W_High"]) * 100
dma_gap = ((latest["Nifty"] - latest["50DMA"]) / latest["50DMA"]) * 100
valuation_gap = ((latest["Nifty"] - latest["200DMA"]) / latest["200DMA"]) * 100

# -----------------------------------
# SIGNALS
# -----------------------------------
signals = {
    "vix": vix_signal(latest["VIX"]),
    "drawdown": drawdown_signal(drawdown),
    "dma": dma_signal(dma_gap),
    "valuation": valuation_signal(valuation_gap)
}

weights = DEFAULT_WEIGHTS

buy_score = calculate_score(signals, weights)

# -----------------------------------
# UI
# -----------------------------------
st.title("📊 Personal Investing Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Nifty", round(latest["Nifty"], 2), format_change(nifty_change))

with col2:
    st.metric("India VIX", round(latest["VIX"], 2), format_change(vix_change))

with col3:
    st.metric("Buy Score", f"{buy_score}%")

# -----------------------------------
# CHARTS
# -----------------------------------
st.subheader("📈 Nifty Trend")
st.line_chart(df["Nifty"])

st.subheader("📉 VIX Trend")
st.line_chart(df["VIX"])
