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

st.switch_page("pages/Login.py")