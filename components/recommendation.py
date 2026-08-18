import streamlit as st
import translation

def recommendation(prediction):

    st.subheader(translation.t("💡 Medical Recommendation"))

    if prediction == 1:

        st.warning(translation.t("reco_high_risk"))

    else:

        st.success(translation.t("reco_healthy_lifestyle"))