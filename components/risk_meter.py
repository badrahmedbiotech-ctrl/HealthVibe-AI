import streamlit as st
import translation

def risk_meter(probability):

    if probability is None:
        return

    st.subheader(translation.t("📊 Risk Score"))

    st.progress(float(probability))

    st.metric(
        translation.t("Risk"),
        f"{probability*100:.1f}%"
    )