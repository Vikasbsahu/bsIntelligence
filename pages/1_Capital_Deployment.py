import streamlit as st

st.title("🏦 Capital Deployment")

score = st.slider("Buy Score (%)", 0, 100, 50)

if score < 30:
    deploy = 10
elif score < 50:
    deploy = 30
elif score < 70:
    deploy = 60
else:
    deploy = 90

st.metric("Recommended Deployment %", f"{deploy}%")
