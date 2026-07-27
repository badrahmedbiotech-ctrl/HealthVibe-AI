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
# HERO SECTION
# ==========================================

col1, col2 = st.columns([1, 4])

with col1:

  st.markdown("""
<div style="text-align:center;">
    <h1 style="font-size:70px;">🩺</h1>
    <h2 style="color:#00C2FF;">HealthVibe AI</h2>
</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <h1 style="
    color:white;
    margin-bottom:-10px;
    ">
    Welcome Back, {username} 👋
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h4 style="color:#9CA3AF;">
    AI Clinical Decision Support System
    </h4>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# HEALTH SCORE
# ==========================================

left, right = st.columns([2, 1])

with left:

    st.markdown("""
    <div style="
    background:#111827;
    padding:25px;
    border-radius:20px;
    border:1px solid #1F2937;
    ">

    <h3 style="color:white;">
    ❤️ Health Score
    </h3>

    <h1 style="
    color:#22C55E;
    font-size:55px;
    ">
    96%
    </h1>

    <p style="color:#9CA3AF;">
    Your overall health status is excellent.
    </p>

    </div>
    """, unsafe_allow_html=True)

with right:

    st.metric(
        "Patients",
        patients
    )

    st.metric(
        "Predictions",
        history
    )

    st.metric(
        "Doctors",
        doctors
    )

# ==========================================
# METRICS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Patients",
        patients
    )

with c2:

    st.metric(
        "Predictions",
        history
    )

with c3:

    st.metric(
        "Doctors",
        doctors
    )

with c4:

    st.metric(
        "Available",
        available
    )

st.write("")

# ==========================================
# PATIENT DASHBOARD
# ==========================================

if role == "Patient":

    st.subheader("🚀 AI Prediction Modules")

    row1 = st.columns(4)

    cards = [

        ("🩸", "Diabetes", "pages/Diabetes.py"),

        ("❤️", "Hypertension", "pages/Hypertension.py"),

        ("⚖️", "Obesity", "pages/obesity.py"),

        ("🫀", "Lipid", "pages/lipid.py"),

    ]

    for col, card in zip(row1, cards):

        with col:

            st.markdown(f"""
            <div style="
            background:#111827;
            border-radius:20px;
            padding:20px;
            text-align:center;
            border:1px solid #1F2937;
            min-height:180px;
            ">

            <h1>{card[0]}</h1>

            <h4 style="color:white;">
            {card[1]}
            </h4>

            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"Open {card[1]}",
                key=card[1],
                use_container_width=True
            ):
                st.switch_page(card[2])

    st.write("")

    row2 = st.columns(4)

    cards2 = [

        ("🧬", "Thrombosis", "pages/thrombosis_app.py"),

        ("🫁", "Pulmonary", "pages/Pulmonary_Fibrosis.py"),

        ("🩻", "CT Scan", "pages/CT_Scan_AI.py"),

        ("🤖", "AI Assistant", "pages/chatbot.py"),

    ]

    for col, card in zip(row2, cards2):

        with col:

            st.markdown(f"""
            <div style="
            background:#111827;
            border-radius:20px;
            padding:20px;
            text-align:center;
            border:1px solid #1F2937;
            min-height:180px;
            ">

            <h1>{card[0]}</h1>

            <h4 style="color:white;">
            {card[1]}
            </h4>

            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"Open {card[1]}",
                key="btn"+card[1],
                use_container_width=True
            ):
                st.switch_page(card[2])

    st.write("")

    c1, c2 = st.columns(2)

    with c1:

        st.info("📄 Last Prediction\n\nNo prediction yet.")

    with c2:

        st.info("📋 Medical History\n\nNo records available.")

# ==========================================
# DOCTOR DASHBOARD
# ==========================================

elif role == "Doctor":

    st.subheader("👨‍⚕️ Doctor Dashboard")

    d1, d2, d3 = st.columns(3)

    with d1:

        with st.container(border=True):

            st.markdown("## 👥 Patients")

            st.write("Manage patient records.")

            if st.button(
                "Open Patients",
                key="doctor_patients",
                use_container_width=True
            ):
                st.switch_page("pages/doctor_db.py")

    with d2:

        with st.container(border=True):

            st.markdown("## 📊 Dashboard")

            st.write("View all AI predictions.")

            if st.button(
                "Open Dashboard",
                key="doctor_dashboard",
                use_container_width=True
            ):
                st.switch_page("pages/doctor_db.py")

    with d3:

        with st.container(border=True):

            st.markdown("## 📄 Reports")

            st.write("View patient reports.")

            if st.button(
                "Open Reports",
                key="doctor_reports",
                use_container_width=True
            ):
                st.info("Coming Soon")

    st.write("")

    st.subheader("⚙️ Doctor Features")

    left, right = st.columns(2)

    with left:

        st.checkbox(
            "Patient Management",
            value=True,
            disabled=True
        )

        st.checkbox(
            "Doctor Management",
            value=True,
            disabled=True
        )

        st.checkbox(
            "AI Predictions",
            value=True,
            disabled=True
        )

    with right:

        st.checkbox(
            "Appointments",
            value=False,
            disabled=True
        )

        st.checkbox(
            "Medical Imaging",
            value=False,
            disabled=True
        )

        st.checkbox(
            "Hospital Integration",
            value=False,
            disabled=True
        )

# ==========================================
# SYSTEM STATUS
# ==========================================

st.divider()

st.subheader("📊 System Status")

st.progress(96)

st.success("HealthVibe AI is running normally.")

st.caption("Version 2.0")

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
HealthVibe AI
</h2>

<p>
AI Clinical Decision Support System
</p>

<hr>

<p style="color:#94A3B8;">
Developed by <b>Badr Ahmed</b>
</p>

</div>
""", unsafe_allow_html=True)