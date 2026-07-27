import streamlit as st
import time

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

st.markdown("""
<h1 style="text-align:center;
color:#00C2FF;
font-size:60px;">
🩺
</h1>

<h1 style="text-align:center;">
HealthVibe AI
</h1>

<p style="text-align:center;color:gray;">
AI Clinical Decision Support System
</p>
""", unsafe_allow_html=True)
st.markdown(
"""
<h1 style='color:white;'>HealthVibe AI</h1>
<h4 style='color:#10B981;'>Vibe Better, Live Better</h4>
""",
unsafe_allow_html=True
)

st.spinner("Loading...")

time.sleep(2)

st.switch_page("pages/Login.py")