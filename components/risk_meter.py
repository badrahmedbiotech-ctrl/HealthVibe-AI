import streamlit as st

def risk_meter(probability):

    if probability is None:
        return

    st.subheader("📊 Risk Score")

    st.progress(float(probability))

    st.metric(
        "Risk",
        f"{probability*100:.1f}%"
    )