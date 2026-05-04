st.subheader("📊 Backtest Insight")

df["Signal"] = df["Nifty"].pct_change().rolling(5).mean()

best_entries = df[df["Signal"] < -0.02]

st.write("Best historical entry points:")
st.dataframe(best_entries.tail(10))
