import streamlit as st
from utils.navigation import sidebar

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

sidebar()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">

<h1>🩺 HealthVibe AI</h1>

<p>
Artificial Intelligence Platform for Early Disease Detection
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# STATISTICS
# ==========================================

st.subheader("📊 System Overview")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("🧠 AI Models", "4")

with m2:
    st.metric("🏥 Diseases", "18")

with m3:
    st.metric("📈 Accuracy", "92.6%")

with m4:
    st.metric("🟢 Status", "ONLINE")

st.write("")

# ==========================================
# MODULES
# ==========================================

st.subheader("🚀 AI Modules")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
<div class="dashboard-card">

<h2>🩺 Diabetes Prediction</h2>

<p>

Predict diabetes using patient clinical data,
BMI, glucose level and vital signs.

</p>

<br>

<span style="color:
#22C55E;font-size:18px;">
● Ready
</span>

</div>
""", unsafe_allow_html=True)

    if st.button("Open Diabetes", use_container_width=True):
        st.switch_page("pages/Diabetes.py")

with col2:

    st.markdown("""
<div class="dashboard-card">

<h2>🫁 Pulmonary Fibrosis</h2>

<p>

AI-powered respiratory assessment
with pulmonary fibrosis prediction.

</p>

<br>

<span style="color:
#22C55E;font-size:18px;">
● Ready
</span>

</div>
""", unsafe_allow_html=True)

    if st.button("Open Pulmonary Fibrosis", use_container_width=True):
        st.switch_page("pages/Pulmonary_Fibrosis.py")

st.write("")

col3, col4 = st.columns(2)

with col3:

    st.markdown("""
<div class="dashboard-card">

<h2>❤️ Heart Disease</h2>

<p>

Machine Learning model for
heart disease prediction.

</p>

<br>

<span style="color:
#F59E0B;font-size:18px;">
Coming Soon
</span>

</div>
""", unsafe_allow_html=True)

with col4:

    st.markdown("""
<div class="dashboard-card">

<h2>🩻 Breast Cancer</h2>

<p>

Breast cancer diagnosis
using Artificial Intelligence.

</p>

<br>

<span style="color:
#F59E0B;font-size:18px;">
Coming Soon
</span>

</div>
""", unsafe_allow_html=True)

# ==========================================
# QUICK INFO
# ==========================================

st.write("")
st.subheader("📌 Platform Features")

a, b, c = st.columns(3)

with a:
    st.info("🤖 AI-powered disease prediction")

with b:
    st.info("⚡ Fast patient assessment")

with c:
    st.info("📊 Professional medical dashboard")

# ==========================================
# FOOTER
# ==========================================

st.write("")
st.divider()

st.markdown("""
<div class="footer">

<h2 style="color:
#00C2FF;">
HealthVibe AI
</h2>

<p>
Artificial Intelligence Platform for Early Disease Detection
</p>

<hr>

<p style="color:
#94A3B8;">
Developed by <b>Badr Ahmed</b>
</p>

</div>
""", unsafe_allow_html=True)