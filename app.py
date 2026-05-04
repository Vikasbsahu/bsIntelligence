import streamlit as st
import pandas as pd
import sys
import os
import os
import streamlit as st

st.write("Files in root:", os.listdir())

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data.fetch_data import load_market_data
from data.indicators import calculate_rsi, calculate_dma
from engine.signals import *
from engine.scoring import calculate_score
from engine.deployment import get_deployment
from config.defaults import DEFAULT_WEIGHTS

# -----------------------------------
# LOAD DATA
# -----------------------------------
df = load_market_data()
df = calculate_dma(df)
df["RSI"] = calculate_rsi(df["Nifty"])

latest = df.iloc[-1]

# -----------------------------------
# DERIVED VALUES
# -----------------------------------
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
    "valuation": valuation_signal(valuation_gap),
}

# -----------------------------------
# WEIGHTS (DYNAMIC)
# -----------------------------------
weights = {
    "vix": st.session_state.get("vix_weight", DEFAULT_WEIGHTS["vix"]),
    "drawdown": st.session_state.get("drawdown_weight", DEFAULT_WEIGHTS["drawdown"]),
    "dma": st.session_state.get("dma_weight", DEFAULT_WEIGHTS["dma"]),
    "valuation": st.session_state.get("valuation_weight", DEFAULT_WEIGHTS["valuation"]),
}

# -----------------------------------
# SCORE
# -----------------------------------
buy_score = calculate_score(signals, weights)

# -----------------------------------
# DEPLOYMENT
# -----------------------------------
deploy_pct = get_deployment(buy_score)

# -----------------------------------
# UI
# -----------------------------------
st.title("📊 Personal Investing Dashboard")

st.metric("Buy Score", f"{buy_score}%")
st.metric("Deploy %", f"{deploy_pct}%")
