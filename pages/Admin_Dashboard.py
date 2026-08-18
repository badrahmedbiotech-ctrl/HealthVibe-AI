import streamlit as st
import pandas as pd

from components.auth_guard import require_admin
from utils.navigation import sidebar

from components.database import (
    total_patients,
    total_assessments,
    average_risk,
    disease_statistics,
    risk_statistics,
    get_all_history,
    get_all_profiles
)

from components.doctor_db import (
    doctors_count,
    available_doctors,
    get_doctors
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="HealthVibe AI | Admin Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# ADMIN SECURITY
# ==========================================================

admin = require_admin()


# ==========================================================
# CSS
# ==========================================================

with open("style.css", encoding="utf-8") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# ==========================================================
# SIDEBAR
# ==========================================================

sidebar()


# ==========================================================
# LOAD DATA
# ==========================================================

patients = total_patients()

assessments = total_assessments()

doctors = doctors_count()

available = available_doctors()

avg_risk = average_risk()

history = get_all_history()

profiles = get_all_profiles()

doctors_df = get_doctors()


# ==========================================================
# HERO
# ==========================================================

st.markdown(
    f"""
### 👑 ADMIN CONTROL CENTER

# Welcome, {admin["full_name"]}

HealthVibe AI Platform Administration
""",
    unsafe_allow_html=False
)

st.write("")


# ==========================================================
# PLATFORM OVERVIEW
# ==========================================================

st.subheader("📊 Platform Overview")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "👤 Patients",
        patients
    )


with c2:

    st.metric(
        "👨‍⚕️ Doctors",
        doctors
    )


with c3:

    st.metric(
        "📋 Assessments",
        assessments
    )


with c4:

    st.metric(
        "🟢 Available Doctors",
        available
    )


st.write("")


# ==========================================================
# AI OVERVIEW
# ==========================================================

st.subheader("🤖 AI & Risk Overview")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "📈 Average Risk",
        f"{avg_risk:.1f}%"
    )


with c2:

    if not history.empty:

        high_risk = len(
            history[
                history["prediction"] == "High Risk"
            ]
        )

    else:

        high_risk = 0


    st.metric(
        "🔴 High Risk",
        high_risk
    )


with c3:

    if not history.empty:

        moderate_risk = len(
            history[
                history["prediction"] == "Moderate Risk"
            ]
        )

    else:

        moderate_risk = 0


    st.metric(
        "🟡 Moderate Risk",
        moderate_risk
    )


with c4:

    if not history.empty:

        low_risk = len(
            history[
                history["prediction"] == "Low Risk"
            ]
        )

    else:

        low_risk = 0


    st.metric(
        "🟢 Low Risk",
        low_risk
    )


st.divider()


# ==========================================================
# DISEASE ANALYTICS
# ==========================================================

st.subheader("🦠 Disease Analytics")


try:

    disease_df = disease_statistics()

    if not disease_df.empty:

        st.bar_chart(
            disease_df,
            x="Disease",
            y="Count",
            use_container_width=True
        )

    else:

        st.info(
            "No disease statistics available."
        )

except Exception:

    st.info(
        "No disease statistics available."
    )


st.write("")


# ==========================================================
# RISK ANALYTICS
# ==========================================================

st.subheader("📈 Risk Analytics")


try:

    risk_df = risk_statistics()

    if not risk_df.empty:

        st.bar_chart(
            risk_df,
            x="Disease",
            y="Average Risk",
            use_container_width=True
        )

    else:

        st.info(
            "No risk statistics available."
        )

except Exception:

    st.info(
        "No risk statistics available."
    )


st.divider()


# ==========================================================
# LATEST ASSESSMENTS
# ==========================================================

st.subheader("📋 Latest Assessments")


if history.empty:

    st.info(
        "No assessments available."
    )

else:

    latest = (
        history
        .sort_values(
            "created_at",
            ascending=False
        )
        .head(10)
    )


    columns = [
        "patient_name",
        "disease",
        "prediction",
        "probability",
        "created_at"
    ]


    available_columns = [
        col
        for col in columns
        if col in latest.columns
    ]


    st.dataframe(
        latest[available_columns],
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ==========================================================
# PATIENTS
# ==========================================================

st.subheader("👥 Patients")


if profiles.empty:

    st.info(
        "No patients registered."
    )

else:

    st.dataframe(
        profiles,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ==========================================================
# DOCTORS
# ==========================================================

st.subheader("👨‍⚕️ Doctors")


if doctors_df.empty:

    st.info(
        "No doctors registered."
    )

else:

    doctor_table = doctors_df.copy()


    if "available" in doctor_table.columns:

        doctor_table["available"] = (
            doctor_table["available"]
            .replace({
                1: "🟢 Available",
                0: "🔴 Unavailable",
                True: "🟢 Available",
                False: "🔴 Unavailable"
            })
        )


    st.dataframe(
        doctor_table,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ==========================================================
# SYSTEM SUMMARY
# ==========================================================

st.subheader("⚙️ System Summary")


c1, c2 = st.columns(2)


with c1:

    st.markdown(
        f"""
        ### 👑 Administrator

        **Name:** {admin["full_name"]}

        **Email:** {admin["email"]}

        **Role:** {admin["role"]}
        """
    )


with c2:

    st.markdown(
        f"""
        ### 🏥 HealthVibe AI

        **Patients:** {patients}

        **Doctors:** {doctors}

        **Assessments:** {assessments}

        **Available Doctors:** {available}

        **Average Risk:** {avg_risk:.1f}%
        """
    )


st.divider()


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    """
## 💙 HealthVibe AI

**Admin Control Center**

---

Developed by **Visionaries**
"""
)