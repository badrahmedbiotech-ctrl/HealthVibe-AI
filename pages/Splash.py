import streamlit as st
import time
from components.branding import LOGO
from components.branding import *
from components.colors import *

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="assets/logo.jpg",
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
    padding-top:4rem;
    text-align:center;
}

img{
    border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

<<<<<<< HEAD
# ===========================
# Logo
# ===========================

st.image("assets/logo.jpg", width=220)


# ===========================
# Title
# ===========================

st.markdown("""
<h1 style="
text-align:center;
color:#00C2FF;
font-size:48px;
margin-bottom:0;">
HealthVibe AI
</h1>

<h3 style="
text-align:center;
color:#10B981;
margin-top:5px;">
Vibe Better, Live Better
</h3>

<p style="
text-align:center;
color:#A0AEC0;">
AI Clinical Decision Support Platform
</p>
""", unsafe_allow_html=True)

# Loading
with st.spinner("Loading..."):
    time.sleep(2)
=======
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
>>>>>>> 34211f1d364920e717bfcfca7d099bc8c1615862

st.switch_page("pages/Login.py")