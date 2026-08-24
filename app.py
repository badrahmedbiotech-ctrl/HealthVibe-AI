import streamlit as st
from PIL import Image
from components.branding import *
from components.colors import *
import translation

icon = Image.open("assets/logo_icon.png")

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon=icon,
    layout="wide"
)

translation.init()

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown(f"""
<div style="text-align:center;padding-top:50px;">

<h1 style="font-size:55px;color:#00C2FF;">
🏥 {translation.t("HealthVibe AI")}
</h1>

<h3 style="color:white;">
{translation.t("AI Clinical Decision Support Platform")}
</h3>

<p style="color:#94A3B8;font-size:20px;">
{translation.t("Choose how you want to continue")}
</p>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2, col3 = st.columns(3)

# ==========================================================
# PATIENT
# ==========================================================

with col1:

    st.markdown(
        f"## 👤 {translation.t('Patient')}"
    )

    st.write(
        translation.t("Access your medical dashboard")
    )

    if st.button(
        translation.t("Continue as Patient"),
        width="stretch"
    ):

        st.session_state.role = "Patient"

        st.switch_page("pages/Login.py")


# ==========================================================
# DOCTOR
# ==========================================================

with col2:

    st.markdown(
        f"## 👨‍⚕️ {translation.t('Doctor')}"
    )

    st.write(
        translation.t("Access your doctor dashboard")
    )

    if st.button(
        translation.t("Continue as Doctor"),
        width="stretch"
    ):

        st.session_state.role = "Doctor"

        st.switch_page("pages/Login.py")


# ==========================================================
# ADMIN
# ==========================================================

with col3:

    st.markdown("## 🛡️ Admin")

    st.write(
        "Full access to HealthVibe AI platform"
    )

    if st.button(
        "Continue as Admin",
        width="stretch"
    ):

        st.session_state.role = "Admin"

        st.switch_page("pages/Login.py")