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
# HERO
# ==========================================

emoji = "👨‍⚕️" if role == "Doctor" else "👤"

st.markdown(f"""
<div class="hero">

<h1>{emoji} Welcome, {username}</h1>

<p>
HealthVibe AI Clinical Decision Support Platform
</p>

</div>
""", unsafe_allow_html=True)

st.success("🟢 System Online")

st.write("")

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

    st.subheader("🧑‍💻 Patient Dashboard")

    p1, p2, p3 = st.columns(3)

    with p1:

        with st.container(border=True):

            st.markdown("## 🩸 Diabetes Assessment")

            st.write("Predict diabetes risk using AI.")

            if st.button(
                "Open Diabetes",
                key="patient_diabetes",
                use_container_width=True
            ):
                st.switch_page("pages/Diabetes.py")

    with p2:

        with st.container(border=True):

            st.markdown("## ❤️ Hypertension")

            st.write("Predict hypertension risk.")

            if st.button(
                "Open Hypertension",
                key="patient_hyper",
                use_container_width=True
            ):
                st.switch_page("pages/Hypertension.py")

    with p3:

        with st.container(border=True):

            st.markdown("## 🫀 Lipid Profile")

            st.write("Analyze cholesterol levels.")

            if st.button(
                "Open Lipid",
                key="patient_lipid",
                use_container_width=True
            ):
                st.switch_page("pages/lipid.py")

    st.write("")

    p4, p5, p6 = st.columns(3)

    with p4:

        with st.container(border=True):

            st.markdown("## 🩸 Thrombosis")

            st.write("Blood clot prediction.")

            if st.button(
                "Open Thrombosis",
                key="patient_throm",
                use_container_width=True
            ):
                st.switch_page("pages/thrombosis_app.py")

    with p5:

        with st.container(border=True):

            st.markdown("## 📄 My Reports")

            st.write("Download your medical reports.")

            if st.button(
                "Open Reports",
                key="patient_reports",
                use_container_width=True
            ):
                st.info("Coming Soon")

    with p6:

        with st.container(border=True):

            st.markdown("## 📈 My History")

            st.write("View previous predictions.")

            if st.button(
                "Open History",
                key="patient_history",
                use_container_width=True
            ):
                st.info("Coming Soon")

    st.write("")

    st.subheader("✨ Patient Features")

    left, right = st.columns(2)

    with left:

        st.checkbox(
            "AI Diagnosis",
            value=True,
            disabled=True
        )

        st.checkbox(
            "PDF Reports",
            value=True,
            disabled=True
        )

        st.checkbox(
            "Medical History",
            value=True,
            disabled=True
        )

    with right:

        st.checkbox(
            "Doctor Appointment",
            value=False,
            disabled=True
        )

        st.checkbox(
            "Medicine Reminder",
            value=False,
            disabled=True
        )

        st.checkbox(
            "Telemedicine",
            value=False,
            disabled=True
        )

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