import streamlit as st
import time

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

import translation
translation.init()

st.markdown("""
<style>
#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

.block-container{
padding-top:6rem;
text-align:center;
}

img{
border-radius:25px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<h1 style="text-align:center;
color:#00C2FF;
font-size:60px;">
🩺
</h1>

<h1 style="text-align:center;">
{translation.t("HealthVibe AI")}
</h1>

<p style="text-align:center;color:gray;">
{translation.t("AI Clinical Decision Support System")}
</p>
""", unsafe_allow_html=True)
st.markdown(
f"""
<h1 style='color:white;'>{translation.t("HealthVibe AI")}</h1>
<h4 style='color:#10B981;'>{translation.t("Vibe Better, Live Better")}</h4>
""",
unsafe_allow_html=True
)

st.spinner(translation.t("Loading..."))

time.sleep(2)

st.switch_page("pages/Login.py")