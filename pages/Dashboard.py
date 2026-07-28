import streamlit as st
from utils.navigation import sidebar

from components.database import (
    total_patients,
    get_all_history
)

from components.doctor_db import (
    doctors_count,
    available_doctors
)

# ==========================================
# SESSION PROTECTION
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.switch_page("app.py")
    st.stop()

username = st.session_state.get("username", "User")
role = st.session_state.get("role", "Patient")

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HealthVibe AI Dashboard",
    page_icon="🩺",
    layout="wide"
)

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
# HELPERS
# ==========================================

def disease_card(icon, title, desc, page, key):

    st.markdown(f"""
    <div class="dashboard-card">
        <h1>{icon}</h1>
        <h4>{title}</h4>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Analyze →",
        key=key,
        use_container_width=True
    ):
        st.switch_page(page)

# ==========================================
# DATABASE METRICS
# ==========================================

try:
    patients = total_patients()
except:
    patients = 0

try:
    history = len(get_all_history())
except:
    history = 0

try:
    doctors = doctors_count()
except:
    doctors = 0

try:
    available = available_doctors()
except:
    available = 0

# ==========================================
# HERO
# ==========================================

st.markdown(f"""
<div class="hero">

<span class="hero-badge">
🟢 AI System Online
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
👋 Welcome Back, {username}
</h1>

<p>
Your AI Healthcare Assistant
</p>

</div>

<div style="
font-size:110px;
">
🩺
</div>

</div>

</div>
""", unsafe_allow_html=True)

b1, b2 = st.columns(2)

with b1:

    if st.button(
        "🚀 Start Diagnosis",
        use_container_width=True
    ):
        st.switch_page("pages/Diabetes.py")

with b2:

    if st.button(
        "🤖 AI Chatbot",
        use_container_width=True
    ):
        st.switch_page("pages/chatbot.py")

st.write("")

# ==========================================
# QUICK STATS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Patients",
        patients,
        "+12"
    )

with c2:
    st.metric(
        "Predictions",
        history,
        "+18"
    )

with c3:
    st.metric(
        "Doctors",
        doctors,
        f"{available} Online"
    )

with c4:
    st.metric(
        "Accuracy",
        "98.7%",
        "+0.4%"
    )

st.write("")
# ==========================================
# AI PREDICTION MODULES
# ==========================================

st.markdown("""
<h2 style='margin-top:10px;margin-bottom:20px;'>
🩺 AI Prediction Modules
</h2>
""", unsafe_allow_html=True)

row1 = st.columns(3)

with row1[0]:
    disease_card(
        "🩸",
        "Diabetes",
        "Blood Sugar Prediction",
        "pages/Diabetes.py",
        "diabetes_card"
    )

with row1[1]:
    disease_card(
        "❤️",
        "Hypertension",
        "Blood Pressure Analysis",
        "pages/Hypertension.py",
        "hypertension_card"
    )

with row1[2]:
    disease_card(
        "🫀",
        "Lipid",
        "Lipid Profile Analysis",
        "pages/lipid.py",
        "lipid_card"
    )

st.write("")

row2 = st.columns(3)

with row2[0]:
    disease_card(
        "⚖️",
        "Obesity",
        "BMI & Risk Prediction",
        "pages/obesity.py",
        "obesity_card"
    )

with row2[1]:
    disease_card(
        "🫁",
        "Pulmonary",
        "Pulmonary Fibrosis",
        "pages/Pulmonary_Fibrosis.py",
        "pulmonary_card"
    )

with row2[2]:
    disease_card(
        "🩻",
        "CT Scan AI",
        "Medical Image Detection",
        "pages/CT_Scan_AI.py",
        "ct_card"
    )

st.write("")
st.divider()

# ==========================================
# HEALTH SCORE + AI ASSISTANT
# ==========================================

left, right = st.columns([2,1])

with left:

    st.markdown("""
    <div class="card">

    <h3>❤️ Health Score</h3>

    <h1 style="
    color:#22C55E;
    font-size:55px;
    ">
    96%
    </h1>

    <p>
    Your overall health status is excellent.
    Keep following your healthy lifestyle.
    </p>

    </div>
    """, unsafe_allow_html=True)

with right:

    st.markdown("""
    <div class="card">

    <h3>🤖 AI Assistant</h3>

    <p>
    Need medical help?

    Our AI assistant is ready
    to answer your questions.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Open AI Chat",
        use_container_width=True,
        key="hero_chat"
    ):
        st.switch_page("pages/chatbot.py")

st.write("")
st.divider()

# ==========================================
# RECENT ACTIVITY
# ==========================================

st.subheader("📈 Recent Activity")

a1, a2 = st.columns(2)

with a1:

    st.success("🩸 Diabetes prediction completed")

    st.info("🩻 CT Scan uploaded")

    st.info("🤖 AI Consultation")

with a2:

    st.info("🫀 Lipid Analysis")

    st.info("🫁 Pulmonary Screening")

    st.success("📄 Report Generated")

st.write("")
st.divider()
# ==========================================
# LATEST REPORTS
# ==========================================

st.subheader("📄 Latest Reports")

reports = [
    ("Ahmed Mohamed", "Diabetes", "Completed", "Today"),
    ("Sara Ali", "Hypertension", "Pending", "Yesterday"),
    ("Omar Hassan", "CT Scan", "Completed", "2 days ago"),
    ("Mona Adel", "Pulmonary", "Review", "3 days ago"),
]

for patient, disease, status, date in reports:

    if status == "Completed":
        badge = "🟢"
    elif status == "Pending":
        badge = "🟡"
    else:
        badge = "🔵"

    with st.container(border=True):

        c1, c2, c3, c4 = st.columns([3,2,2,2])

        with c1:
            st.write(f"**{patient}**")

        with c2:
            st.write(disease)

        with c3:
            st.write(f"{badge} {status}")

        with c4:
            st.caption(date)

st.write("")
st.divider()

# ==========================================
# PATIENT DASHBOARD
# ==========================================

if role == "Patient":

    st.subheader("📊 Dashboard Summary")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div class="card">

        <h3>📈 Prediction Summary</h3>

        <p>
        • Total Predictions : <b>58</b><br>
        • Successful Reports : <b>54</b><br>
        • Pending Reviews : <b>4</b>

        </p>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="card">

        <h3>💡 Health Tips</h3>

        <p>

        💧 Drink enough water<br><br>

        🥗 Eat healthy food<br><br>

        🚶 Walk 30 minutes daily<br><br>

        😴 Sleep 7-8 hours

        </p>

        </div>
        """, unsafe_allow_html=True)

    st.write("")
# ==========================================
# DOCTOR DASHBOARD
# ==========================================

elif role == "Doctor":

    st.subheader("👨‍⚕️ Doctor Dashboard")

    d1, d2, d3 = st.columns(3)

    with d1:

        st.markdown("""
        <div class="card">

        <h3>👥 Patient Management</h3>

        <p>
        Manage all registered patients,
        review their medical history,
        and monitor AI predictions.
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Patient Manager",
            key="doctor_patient_manager",
            use_container_width=True
        ):
            st.switch_page("pages/doctor_db.py")

    with d2:

        st.markdown("""
        <div class="card">

        <h3>📊 AI Analytics</h3>

        <p>
        View prediction statistics,
        system analytics,
        and AI performance.
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "View Analytics",
            key="doctor_analytics",
            use_container_width=True
        ):
            st.switch_page("pages/doctor_db.py")

    with d3:

        st.markdown("""
        <div class="card">

        <h3>📄 Medical Reports</h3>

        <p>
        Browse reports,
        download results,
        and review patient history.
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Reports",
            key="doctor_reports_new",
            use_container_width=True
        ):
            st.info("Coming Soon")

    st.write("")

    st.subheader("⚙️ Doctor Features")

    c1, c2 = st.columns(2)

    with c1:
        st.checkbox("Patient Management", value=True, disabled=True)
        st.checkbox("Doctor Management", value=True, disabled=True)
        st.checkbox("AI Prediction System", value=True, disabled=True)

    with c2:
        st.checkbox("Appointments", value=False, disabled=True)
        st.checkbox("Hospital Integration", value=False, disabled=True)
        st.checkbox("Medical Imaging", value=False, disabled=True)

st.write("")
st.divider()

# ==========================================
# SYSTEM STATUS
# ==========================================

st.subheader("⚡ System Status")

st.progress(96)

m1, m2, m3 = st.columns(3)

with m1:
    st.success("🟢 AI Server Online")

with m2:
    st.info("🩺 Models Loaded")

with m3:
    st.success("🔒 Secure Connection")

st.caption("HealthVibe AI Version 2.0")
# ==========================================
# QUICK ACCESS
# ==========================================

st.write("")
st.subheader("⚡ Quick Access")

q1, q2, q3 = st.columns(3)

with q1:

    st.markdown("""
    <div class="card">

    <h3>🤖 AI Assistant</h3>

    <p>
    Ask any medical question and
    receive AI-powered assistance.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Open Chatbot",
        key="quick_chat",
        use_container_width=True
    ):
        st.switch_page("pages/chatbot.py")

with q2:

    st.markdown("""
    <div class="card">

    <h3>📋 Medical History</h3>

    <p>
    Review your previous
    AI predictions and reports.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Open History",
        key="history_btn",
        use_container_width=True
    ):
        st.switch_page("pages/Patient_History.py")

with q3:

    st.markdown("""
    <div class="card">

    <h3>👤 My Profile</h3>

    <p>
    Manage your account,
    settings and personal data.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Open Profile",
        key="profile_btn",
        use_container_width=True
    ):
        st.switch_page("pages/Profile.py")

st.write("")

# ==========================================
# LOGOUT
# ==========================================

st.divider()

if st.button(
    "🚪 Logout",
    key="logout_btn",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.email = ""
    st.session_state.user_id = None

    st.switch_page("app.py")

# ==========================================
# FOOTER
# ==========================================

st.write("")

st.markdown("""
<div class="footer">

<h2 style="color:#00C2FF;">
🩺 HealthVibe AI
</h2>

<p>
AI Clinical Decision Support Platform
</p>

<hr>

<p>
Made with ❤️ using Streamlit & AI
</p>

<p style="color:#94A3B8;">
© 2026 HealthVibe AI • All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)