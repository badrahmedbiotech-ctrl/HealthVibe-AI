import streamlit as st
import pandas as pd

from utils.navigation import sidebar

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon=str(LOGO),
    layout="wide",
    initial_sidebar_state="expanded"
)

import translation
translation.init()
t = translation.t

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
🟢 {t("AI Clinical Decision Support Platform")}
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
{t("🩺 Welcome to HealthVibe AI")}
</h1>

<p style="font-size:20px;">

{t("Predict diseases early.")}
{t("Generate smart medical reports.")}
{t("Empower doctors and patients using Artificial Intelligence.")}

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
        t("🚀 Start Diagnosis"),
        width="stretch"
    ):
        st.switch_page("pages/Diabetes.py")

with a2:

    if st.button(
        t("🤖 AI Assistant"),
        width="stretch"
    ):
        st.switch_page("pages/chatbot.py")

with a3:

    if st.button(
        t("📋 Medical History"),
        width="stretch"
    ):
        st.switch_page("pages/Patient_History.py")

with a4:

    if st.button(
        t("👤 My Profile"),
        width="stretch"
    ):
        st.switch_page("pages/Profile.py")

st.write("")
st.divider()

# ==========================================
# PLATFORM FEATURES
# ==========================================

st.subheader(t("✨ Platform Features"))

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

        <h3>{t(title)}</h3>

        <p>{t(desc)}</p>

        </div>
        """, unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================
# PLATFORM STATISTICS
# ==========================================

st.subheader(t("📊 HealthVibe AI Statistics"))

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric(t("Patients"), "1,250+")

with s2:
    st.metric(t("Predictions"), "8,600+")

with s3:
    st.metric(t("Doctors"), "120+")

with s4:
    st.metric(t("Accuracy"), "98.7%")

# ==========================================
# AI MODULES
# ==========================================

st.subheader(t("🩺 AI Prediction Modules"))

m1, m2, m3 = st.columns(3)

with m1:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🩸</div>

    <h3>{t("Diabetes Prediction")}</h3>

    <p>
    {t("AI-based Blood Glucose Risk Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        t("Open Diabetes"),
        key="home_diabetes",
        width="stretch"
    ):
        st.switch_page("pages/Diabetes.py")

with m2:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">❤️</div>

    <h3>{t("Hypertension")}</h3>

    <p>
    {t("Blood Pressure Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        t("Open Hypertension"),
        key="home_hyper",
        width="stretch"
    ):
        st.switch_page("pages/Hypertension.py")

with m3:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🫀</div>

    <h3>{t("Lipid Profile")}</h3>

    <p>
    {t("Cholesterol Risk Analysis")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        t("Open Lipid"),
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

    <h3>{t("Obesity")}</h3>

    <p>
    {t("BMI & Obesity Risk Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        t("Open Obesity"),
        key="home_obesity",
        width="stretch"
    ):
        st.switch_page("pages/obesity.py")

with m5:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🫁</div>

    <h3>{t("Pulmonary Fibrosis")}</h3>

    <p>
    {t("Lung Disease Prediction")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        t("Open Pulmonary"),
        key="home_pulmonary",
        width="stretch"
    ):
        st.switch_page("pages/Pulmonary_Fibrosis.py")

with m6:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:60px;">🩻</div>

    <h3>{t("CT Scan AI")}</h3>

    <p>
    {t("Medical Image Detection")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        t("Open CT Scan"),
        key="home_ct",
        width="stretch"
    ):
        st.switch_page("pages/CT_Scan_AI.py")

st.write("")
st.divider()    

# ==========================================
# WHY HEALTHVIBE AI
# ==========================================

st.subheader(t("🌍 Why Choose HealthVibe AI ?"))

left, right = st.columns([2,1])

with left:

    st.markdown(f"""
    <div class="card">

    <h3>{t("🏥 Intelligent Healthcare Platform")}</h3>

    <p>

    {t("✔ Early Disease Detection")}

    <br><br>

    {t("✔ AI Clinical Decision Support")}

    <br><br>

    {t("✔ Instant Medical Reports")}

    <br><br>

    {t("✔ Patient History Tracking")}

    <br><br>

    {t("✔ Doctor Dashboard")}

    <br><br>

    {t("✔ Secure Database")}

    <br><br>

    {t("✔ Fast Predictions")}

    </p>

    </div>
    """, unsafe_allow_html=True)

with right:

    st.markdown(f"""
    <div class="card">

    <h3>{t("❤️ HealthVibe Score")}</h3>

    </div>
    """, unsafe_allow_html=True)

    st.progress(0.98)

    st.metric(
        t("AI Accuracy"),
        "98.7%"
    )

    st.metric(
        t("Prediction Speed"),
        "< 3 sec"
    )

    st.metric(
        t("Availability"),
        "24/7"
    )

st.write("")
st.divider()

# ==========================================
# FUTURE MODULES
# ==========================================

st.subheader(t("🚀 Upcoming Features"))

u1, u2, u3 = st.columns(3)

with u1:

    st.info(t("📅 Smart Appointment System"))

with u2:

    st.info(t("💊 Medication Reminder"))

with u3:

    st.info(t("📱 Mobile Application"))

st.write("")
st.divider()

# ==========================================
# GET STARTED
# ==========================================

st.subheader(t("🎯 Ready to Start?"))

g1, g2 = st.columns(2)

with g1:

    if st.button(
        t("🩺 Start Your First Diagnosis"),
        width="stretch",
        key="home_start"
    ):
        st.switch_page("pages/Diabetes.py")

with g2:

    if st.button(
        t("🤖 Talk with AI Assistant"),
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
🩺 {t("HealthVibe AI")}
</h2>

<p style="font-size:18px;">
{t("AI Clinical Decision Support Platform")}
</p>

<p style="color:#94A3B8;">
{t("Empowering Healthcare with Artificial Intelligence")}
</p>

<hr style="
margin:20px 0;
border:1px solid #2A2A2A;
">

<p style="color:#94A3B8;">
{t("Developed by ")}<b>Badr Ahmed</b>
</p>

<p style="color:#94A3B8;">
{t("Version 2.0")}
</p>

<p style="color:#94A3B8;">
{t("© 2026 HealthVibe AI • All Rights Reserved")}
</p>

</div>
""", unsafe_allow_html=True)