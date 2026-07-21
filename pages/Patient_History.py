import streamlit as st
import pandas as pd
import plotly.express as px

from utils.navigation import sidebar
from components.database import (
    get_history,
    search_patient,
    delete_patient
)

# ==========================================
# SESSION PROTECTION
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Patient History",
    page_icon="📋",
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

# ==========================================
# SIDEBAR
# ==========================================

sidebar()

# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">

<h1>📋 Patient History</h1>

<p>
Complete medical history and AI prediction records
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# LOAD DATA
# ==========================================

search = st.text_input(
    "🔍 Search Patient",
    placeholder="Search by patient name..."
)

if search.strip():

    df = search_patient(search.strip())

else:

    df = get_history()

# ==========================================
# EMPTY DATABASE
# ==========================================

if df.empty:

    st.warning("No patient records found.")

    st.stop()

# ==========================================
# DASHBOARD METRICS
# ==========================================

high = len(df[df["prediction"] == 1])
low = len(df[df["prediction"] == 0])
total = len(df)
avg_bmi = round(df["bmi"].mean(), 1)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👥 Total Patients",
        total
    )

with c2:
    st.metric(
        "🔴 High Risk",
        high
    )

with c3:
    st.metric(
        "🟢 Low Risk",
        low
    )

with c4:
    st.metric(
        "⚖ Average BMI",
        avg_bmi
    )

st.write("")

# ==========================================
# CHARTS
# ==========================================

left, right = st.columns([2, 1])

with left:

    fig = px.histogram(
        df,
        x="glucose",
        nbins=20,
        title="Glucose Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    risk = pd.DataFrame({

        "Risk": [
            "Low Risk",
            "High Risk"
        ],

        "Count": [
            low,
            high
        ]

    })

    fig2 = px.pie(
        risk,
        values="Count",
        names="Risk",
        hole=0.55,
        title="Risk Distribution"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.write("")

# ==========================================
# PATIENT TABLE
# ==========================================

st.subheader("📋 Patient Records")

show_df = df.copy()

show_df["prediction"] = show_df["prediction"].replace({
    0: "🟢 Low Risk",
    1: "🔴 High Risk"
})

show_df = show_df.sort_values(
    by="created_at",
    ascending=False
)

st.dataframe(
    show_df,
    use_container_width=True,
    hide_index=True
)

st.write("")

# ==========================================
# DOWNLOADS
# ==========================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    data=csv,
    file_name="Patient_History.csv",
    mime="text/csv",
    use_container_width=True
)

st.write("")

# ==========================================
# PATIENT DETAILS
# ==========================================

st.subheader("👤 Patient Details")

selected = st.selectbox(
    "Choose Patient",
    df["id"]
)

patient = df[df["id"] == selected].iloc[0]

left, right = st.columns(2)

with left:

    st.markdown("### Personal Information")

    st.write(f"**Name:** {patient['full_name']}")
    st.write(f"**Age:** {patient['age']}")
    st.write(f"**Gender:** {patient['gender']}")
    st.write(f"**Weight:** {patient['weight']} kg")
    st.write(f"**Height:** {patient['height']} cm")

with right:

    st.markdown("### Medical Information")

    st.write(f"**Glucose:** {patient['glucose']}")
    st.write(f"**Blood Pressure:** {patient['blood_pressure']}")
    st.write(f"**Insulin:** {patient['insulin']}")
    st.write(f"**BMI:** {patient['bmi']}")
    st.write(f"**Pedigree:** {patient['pedigree']}")

st.write("")

if patient["prediction"] == 1:

    st.error("🔴 High Risk of Diabetes")

else:

    st.success("🟢 Low Risk of Diabetes")

st.write("")

# ==========================================
# PATIENT TABLE
# ==========================================

st.subheader("📋 Patient Records")

show_df = df.copy()

show_df["prediction"] = show_df["prediction"].replace({
    0: "🟢 Low Risk",
    1: "🔴 High Risk"
})

show_df = show_df.sort_values(
    by="created_at",
    ascending=False
)

st.dataframe(
    show_df,
    use_container_width=True,
    hide_index=True
)

st.write("")

# ==========================================
# DOWNLOADS
# ==========================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    data=csv,
    file_name="Patient_History.csv",
    mime="text/csv",
    use_container_width=True
)

st.write("")

# ==========================================
# PATIENT DETAILS
# ==========================================

st.subheader("👤 Patient Details")

selected = st.selectbox(
    "Choose Patient",
    df["id"]
)

patient = df[df["id"] == selected].iloc[0]

left, right = st.columns(2)

with left:

    st.markdown("### Personal Information")

    st.write(f"**Name:** {patient['full_name']}")
    st.write(f"**Age:** {patient['age']}")
    st.write(f"**Gender:** {patient['gender']}")
    st.write(f"**Weight:** {patient['weight']} kg")
    st.write(f"**Height:** {patient['height']} cm")

with right:

    st.markdown("### Medical Information")

    st.write(f"**Glucose:** {patient['glucose']}")
    st.write(f"**Blood Pressure:** {patient['blood_pressure']}")
    st.write(f"**Insulin:** {patient['insulin']}")
    st.write(f"**BMI:** {patient['bmi']}")
    st.write(f"**Pedigree:** {patient['pedigree']}")

st.write("")

if patient["prediction"] == 1:

    st.error("🔴 High Risk of Diabetes")

else:

    st.success("🟢 Low Risk of Diabetes")

st.write("")

# ==========================================
# DELETE PATIENT
# ==========================================

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🗑 Delete Patient")

    delete_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1,
        key="delete_patient"
    )

    confirm = st.checkbox(
        "I confirm deleting this patient"
    )

    if st.button(
        "Delete Record",
        use_container_width=True
    ):

        if confirm:

            delete_patient(delete_id)

            st.success("Patient deleted successfully.")

            st.rerun()

        else:

            st.warning(
                "Please confirm deletion first."
            )

# ==========================================
# SIMPLE REPORT
# ==========================================

with right:

    st.subheader("📄 Medical Report")

    report = f"""
HealthVibe AI
================================

Patient Name : {patient['full_name']}

Age : {patient['age']}

Gender : {patient['gender']}

Weight : {patient['weight']} kg

Height : {patient['height']} cm

--------------------------------

Pregnancies : {patient['pregnancies']}

Glucose : {patient['glucose']}

Blood Pressure : {patient['blood_pressure']}

Skin Thickness : {patient['skin_thickness']}

Insulin : {patient['insulin']}

BMI : {patient['bmi']}

Pedigree : {patient['pedigree']}

--------------------------------

Prediction :

{"HIGH RISK" if patient["prediction"] == 1 else "LOW RISK"}

Probability :

{round(patient["probability"]*100,2)} %

================================

Generated by HealthVibe AI
"""

    st.download_button(
        "⬇ Download Report",
        report,
        file_name=f"{patient['full_name']}_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

st.write("")

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div class="footer">

<h2 style="color:#00C2FF;">
HealthVibe AI
</h2>

<p>
AI-powered Clinical Decision Support Platform
</p>

<hr>

<p style="color:#94A3B8;">
Developed by <b>Badr Ahmed</b>
</p>

</div>
""", unsafe_allow_html=True)