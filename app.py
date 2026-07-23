import streamlit as st

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🏥",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("""

<div style="text-align:center;padding-top:50px;">

<h1 style="font-size:55px;color:#00C2FF;">
🏥 HealthVibe AI
</h1>

<h3 style="color:white;">
AI Clinical Decision Support Platform
</h3>

<p style="color:#94A3B8;font-size:20px;">
Choose how you want to continue
</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2 = st.columns(2)

with col1:

    st.markdown("## 👤 Patient")

    st.write("Access your medical dashboard")

    if st.button(
        "Continue as Patient",
        use_container_width=True
    ):

        st.session_state.role = "Patient"

        st.switch_page("pages/Login.py")

with col2:

    st.markdown("## 👨‍⚕️ Doctor")

    st.write("Access your doctor dashboard")

    if st.button(
        "Continue as Doctor",
        use_container_width=True
    ):

        st.session_state.role = "Doctor"

        st.switch_page("pages/Login.py")