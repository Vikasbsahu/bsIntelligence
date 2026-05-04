import streamlit as st
import plotly.graph_objects as go

from data.fetch_data import load_market_data
from data.indicators import calculate_dma
from engine.signals import *
from engine.scoring import calculate_score
from config.defaults import DEFAULT_WEIGHTS

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="Personal Investing Dashboard", layout="wide")

# -----------------------------------
# LOAD DATA
# -----------------------------------
df, data_source = load_market_data()

if df.empty:
    st.error("❌ No market data available")
    st.stop()

df = calculate_dma(df)

latest = df.iloc[-1]
previous = df.iloc[-6] if len(df) > 5 else df.iloc[0]

# -----------------------------------
# CALCULATIONS
# -----------------------------------
drawdown = ((latest["Nifty"] - latest["52W_High"]) / latest["52W_High"]) * 100
dma_gap = ((latest["Nifty"] - latest["50DMA"]) / latest["50DMA"]) * 100
valuation_gap = ((latest["Nifty"] - latest["200DMA"]) / latest["200DMA"]) * 100

prev_drawdown = ((previous["Nifty"] - previous["52W_High"]) / previous["52W_High"]) * 100
prev_dma_gap = ((previous["Nifty"] - previous["50DMA"]) / previous["50DMA"]) * 100
prev_valuation_gap = ((previous["Nifty"] - previous["200DMA"]) / previous["200DMA"]) * 100

# -----------------------------------
# SIGNALS
# -----------------------------------
signals = {
    "vix": vix_signal(latest["VIX"]),
    "drawdown": drawdown_signal(drawdown),
    "dma": dma_signal(dma_gap),
    "valuation": valuation_signal(valuation_gap)
}

prev_signals = {
    "vix": vix_signal(previous["VIX"]),
    "drawdown": drawdown_signal(prev_drawdown),
    "dma": dma_signal(prev_dma_gap),
    "valuation": valuation_signal(prev_valuation_gap)
}

# -----------------------------------
# SCORE
# -----------------------------------
weights = DEFAULT_WEIGHTS

buy_score = calculate_score(signals, weights)
prev_score = calculate_score(prev_signals, weights)

score_change = round(buy_score - prev_score, 2)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("📊 Personal Investing Dashboard")
st.caption("🟢 Improving | 🔵 Stable | 🔴 Weakening")

# -----------------------------------
# TOP METRICS
# -----------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Nifty", round(latest["Nifty"], 2))
col2.metric("India VIX", round(latest["VIX"], 2))
col3.metric("Drawdown %", f"{drawdown:.2f}%")
col4.metric("50 DMA Gap %", f"{dma_gap:.2f}%")
col5.metric("200 DMA Gap %", f"{valuation_gap:.2f}%")

# -----------------------------------
# INDICATOR SIGNAL DASHBOARD
# -----------------------------------
st.subheader("📡 Indicator Signals")

s1, s2, s3, s4 = st.columns(4)

s1.metric("VIX Signal", f"{signals['vix']}%")
s2.metric("Drawdown Signal", f"{signals['drawdown']}%")
s3.metric("DMA Signal", f"{signals['dma']}%")
s4.metric("Valuation Signal", f"{signals['valuation']}%")

# -----------------------------------
# MASTER SCORE
# -----------------------------------
st.subheader(f"🎯 Buy Opportunity Score: {buy_score}%")
st.progress(int(buy_score))

# -----------------------------------
# WEEKLY TREND
# -----------------------------------
if score_change > 3:
    trend = f"📈 Improving (+{score_change}%)"
    needle_color = "green"
    trend_arrow = "📈"
elif score_change < -3:
    trend = f"📉 Weakening ({score_change}%)"
    needle_color = "red"
    trend_arrow = "📉"
else:
    trend = f"➡️ Stable ({score_change}%)"
    needle_color = "blue"
    trend_arrow = "➡️"

st.info(trend)

# -----------------------------------
# DECISION CONSOLE
# -----------------------------------
st.subheader("🎯 Investor Decision Console")

if buy_score < 30:
    zone = "🟢 Expensive Zone"
    action = "SIP only"
elif buy_score < 50:
    zone = "🟡 Fair Value"
    action = "Normal investing"
elif buy_score < 70:
    zone = "🟠 Correction"
    action = "Gradual buying"
elif buy_score < 85:
    zone = "🔴 Opportunity"
    action = "Aggressive stagger"
else:
    zone = "🚨 Panic Zone"
    action = "Deploy max capital"

colA, colB = st.columns(2)
colA.info(f"Zone: {zone}")
colB.success(f"Action: {action}")

# -----------------------------------
# GAUGE (PROFESSIONAL)
# -----------------------------------
st.subheader("📡 Market Opportunity Meter")

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=buy_score,
    number={'suffix': "%"},
    delta={'reference': prev_score},
    title={
        "text": f"{trend_arrow} Opportunity Score<br><span style='font-size:14px'>{zone}</span>"
    },
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': needle_color},
        'steps': [
            {'range': [0, 30], 'color': "#7CFC00"},
            {'range': [30, 50], 'color': "#FFD700"},
            {'range': [50, 70], 'color': "#FFA500"},
            {'range': [70, 85], 'color': "#FF4500"},
            {'range': [85, 100], 'color': "#8B0000"}
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# CRASH DETECTOR
# -----------------------------------
if latest["VIX"] > 30 and drawdown < -15:
    st.error("🚨 Crash-like setup detected")
elif buy_score >= 75:
    st.warning("⚠️ Strong accumulation zone")
else:
    st.info("ℹ️ No extreme signals")

# -----------------------------------
# CHARTS
# -----------------------------------
st.subheader("📈 Nifty vs DMA")
st.line_chart(df[["Nifty", "50DMA", "200DMA"]])

st.subheader("📉 India VIX")
st.line_chart(df["VIX"])

# -----------------------------------
# DATA TABLE
# -----------------------------------
with st.expander("🔍 View Data"):
    st.dataframe(df.tail(20))
