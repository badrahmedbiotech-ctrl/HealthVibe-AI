import streamlit as st
import pandas as pd
from datetime import datetime
from components.branding import *
from components.colors import *

from components.branding import LOGO
col1, col2 = st.columns([1,5])

with col1:
    st.image(str(LOGO), width=90)

with col2:
    st.title("HealthVibe AI")
    st.caption("Vibe Better, Live Better")


from utils.navigation import sidebar

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HealthVibe AI Dashboard",
    page_icon=str(LOGO),
    layout="wide",
    initial_sidebar_state="expanded"
)

import translation
translation.init()

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================
# HERO
# ==========================================

st.markdown(f"""
<div class="hero">

<span class="hero-badge">
{translation.t("🟢 AI Clinical Decision Support Platform")}
</span>

<div style="
display:flex;
justify-content:space-between;
align-items:center;
flex-wrap:wrap;
gap:40px;
">

<div>

<h1>
🩺 {translation.t("Welcome to HealthVibe AI")}
</h1>

<p style="font-size:20px;">

{translation.t("Predict diseases early.")}
{translation.t("Generate smart medical reports.")}
{translation.t("Empower doctors and patients using Artificial Intelligence.")}

</p>

</div>

<div style="font-size:120px;">
🧬
</div>

</div>

</div>
""", unsafe_allow_html=True)

# ==========================================
# QUICK ACTIONS
# ==========================================

st.write("")

a1, a2, a3, a4 = st.columns(4)

with a1:

    if st.button(
        translation.t("🚀 Start Diagnosis"),
        width="stretch"
    ):
        st.switch_page("pages/Diabetes.py")

with a2:

    if st.button(
        translation.t("🤖 AI Assistant"),
        width="stretch"
    ):
        st.switch_page("pages/chatbot.py")

with a3:

    if st.button(
        translation.t("📋 Medical History"),
        width="stretch"
    ):
        st.switch_page("pages/Patient_History.py")

with a4:

    if st.button(
        translation.t("👤 My Profile"),
        width="stretch"
    ):
        st.switch_page("pages/Profile.py")

st.write("")
st.divider()

# ==========================================
# PLATFORM FEATURES
# ==========================================

st.subheader(translation.t("✨ Platform Features"))

f1, f2, f3, f4 = st.columns(4)

features = [

    (
        "🤖",
        "AI Diagnosis",
        "Predict diseases using Artificial Intelligence."
    ),

    (
        "📄",
        "Medical Reports",
        "Generate downloadable clinical reports."
    ),

    (
        "📊",
        "Risk Assessment",
        "Evaluate patient risk level instantly."
    ),

    (
        "🔒",
        "Secure Data",
        "Protected patient records and authentication."
    )

]

cards = [f1, f2, f3, f4]

for col, feature in zip(cards, features):

    icon, title, desc = feature

    with col:

        st.markdown(f"""
        <div class="card">

        <div style="font-size:55px;">
        {icon}
        </div>

        <h3>{translation.t(title)}</h3>

        <p>{translation.t(desc)}</p>

        </div>
        """, unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================
# PLATFORM STATISTICS
# ==========================================

st.subheader(translation.t("📊 HealthVibe AI Statistics"))

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric(translation.t("Patients"), translation.t("1,250+"))

with s2:
    st.metric(translation.t("Predictions"), translation.t("8,600+"))

with s3:
    st.metric(translation.t("Doctors"), translation.t("120+"))

with s4:
    st.metric(translation.t("Accuracy"), translation.t("98.7%"))

# ==========================================
# AI MODULES
# ==========================================

st.subheader(translation.t("🩺 AI Prediction Modules"))

m1, m2, m3 = st.columns(3)

with m1:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🩸</div>

    <h3>{translation.t("Diabetes Prediction")}</h3>

    <p>
    {translation.t("AI-based Blood Glucose Risk Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        translation.t("Open Diabetes"),
        key="home_diabetes",
        width="stretch"
    ):
        st.switch_page("pages/Diabetes.py")

with m2:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">❤️</div>

    <h3>{translation.t("Hypertension")}</h3>

    <p>
    {translation.t("Blood Pressure Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        translation.t("Open Hypertension"),
        key="home_hyper",
        width="stretch"
    ):
        st.switch_page("pages/Hypertension.py")

with m3:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🫀</div>

    <h3>{translation.t("Lipid Profile")}</h3>

    <p>
    {translation.t("Cholesterol Risk Analysis")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        translation.t("Open Lipid"),
        key="home_lipid",
        width="stretch"
    ):
        st.switch_page("pages/lipid.py")

st.write("")

m4, m5, m6 = st.columns(3)

with m4:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">⚖️</div>

    <h3>{translation.t("Obesity")}</h3>

    <p>
    {translation.t("BMI & Obesity Risk Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        translation.t("Open Obesity"),
        key="home_obesity",
        width="stretch"
    ):
        st.switch_page("pages/obesity.py")

with m5:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🫁</div>

    <h3>{translation.t("Pulmonary Fibrosis")}</h3>

    <p>
    {translation.t("Lung Disease Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        translation.t("Open Pulmonary"),
        key="home_pulmonary",
        width="stretch"
    ):
        st.switch_page("pages/Pulmonary_Fibrosis.py")

with m6:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🩻</div>

    <h3>{translation.t("CT Scan AI")}</h3>

    <p>
    {translation.t("Medical Image Detection")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        translation.t("Open CT Scan"),
        key="home_ct",
        width="stretch"
    ):
        st.switch_page("pages/CT_Scan_AI.py")

st.write("")
st.divider()    

# ==========================================
# WHY HEALTHVIBE AI
# ==========================================

st.subheader(translation.t("🌍 Why Choose HealthVibe AI ?"))

left, right = st.columns([2,1])

with left:

    st.markdown(f"""
    <div class="card">

    <h3>{translation.t("🏥 Intelligent Healthcare Platform")}</h3>

    <p>

    {translation.t("✔ Early Disease Detection")}

    <br><br>

    {translation.t("✔ AI Clinical Decision Support")}

    <br><br>

    {translation.t("✔ Instant Medical Reports")}

    <br><br>

    {translation.t("✔ Patient History Tracking")}

    <br><br>

    {translation.t("✔ Doctor Dashboard")}

    <br><br>

    {translation.t("✔ Secure Database")}

    <br><br>

    {translation.t("✔ Fast Predictions")}

    </p>

    </div>
    """, unsafe_allow_html=True)

with right:

    st.markdown(f"""
    <div class="card">

    <h3>{translation.t("❤️ HealthVibe Score")}</h3>

    </div>
    """, unsafe_allow_html=True)

    st.progress(0.98)

    st.metric(
        translation.t("AI Accuracy"),
        translation.t("98.7%")
    )

    st.metric(
        translation.t("Prediction Speed"),
        translation.t("< 3 sec")
    )

    st.metric(
        translation.t("Availability"),
        translation.t("24/7")
    )

st.write("")
st.divider()

# ==========================================
# FUTURE MODULES
# ==========================================

st.subheader(translation.t("🚀 Upcoming Features"))

u1, u2, u3 = st.columns(3)

with u1:

    st.info(translation.t("📅 Smart Appointment System"))

with u2:

    st.info(translation.t("💊 Medication Reminder"))

with u3:

    st.info(translation.t("📱 Mobile Application"))

st.write("")
st.divider()

# ==========================================
# GET STARTED
# ==========================================

st.subheader(translation.t("🎯 Ready to Start?"))

g1, g2 = st.columns(2)

with g1:

    if st.button(
        translation.t("🩺 Start Your First Diagnosis"),
        width="stretch",
        key="home_start"
    ):
        st.switch_page("pages/Diabetes.py")

with g2:

    if st.button(
        translation.t("🤖 Talk with AI Assistant"),
        width="stretch",
        key="home_ai"
    ):
        st.switch_page("pages/chatbot.py")

st.write("")
st.divider()

# ==========================================
# FOOTER
# ==========================================

st.markdown(f"""
<div style="
text-align:center;
padding:40px 20px;
">

<h2 style="
color:#00C2FF;
margin-bottom:10px;
">
{translation.t("🩺 HealthVibe AI")}
</h2>

<p style="font-size:18px;">
{translation.t("AI Clinical Decision Support Platform")}
</p>

<p style="color:#94A3B8;">
{translation.t("Empowering Healthcare with Artificial Intelligence")}
</p>

<hr style="
margin:20px 0;
border:1px solid #2A2A2A;
">

<p style="color:#94A3B8;">
{translation.t("Developed by ")}<b>Badr Ahmed</b>
</p>

<p style="color:#94A3B8;">
{translation.t("Version 2.0")}
</p>

<p style="color:#94A3B8;">
{translation.t("© 2026 HealthVibe AI • All Rights Reserved")}
</p>

</div>
""", unsafe_allow_html=True)