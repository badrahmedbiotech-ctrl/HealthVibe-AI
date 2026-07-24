import streamlit as st
import pandas as pd
import plotly.express as px

from utils.navigation import sidebar

from components.database import (
    get_all_history,
    get_user_history,
    total_patients
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Patient History",
    page_icon="📋",
    layout="wide"
)

# ==========================================
# LOGIN CHECK
# ==========================================

if "user" not in st.session_state:

    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.user

# ==========================================
# CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================
# LOAD DATA
# ==========================================

if user["role"] == "Doctor":

    df = get_all_history()

else:

    df = get_user_history(user["id"])

# ==========================================
# EMPTY
# ==========================================

if df.empty:

    st.info("No patient history found.")

    st.stop()

# ==========================================
# HERO
# ==========================================

st.markdown("""

<div class="hero">

<h1>📋 Patient Assessment History</h1>

<p>

View all previous AI assessments.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================
# SEARCH
# ==========================================

search = st.text_input(
    "🔍 Search Patient"
)

if search:

    df = df[
        df["full_name"]
        .str.contains(search, case=False)
    ]
# ==========================================
# METRICS
# ==========================================

high = len(df[df["prediction"] == 1])
low = len(df[df["prediction"] == 0])
total = len(df)

avg_glucose = round(df["glucose"].mean(), 1)
avg_bmi = round(df["bmi"].mean(), 1)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("👥 Total", total)
c2.metric("🔴 High Risk", high)
c3.metric("🟢 Low Risk", low)
c4.metric("🩸 Avg Glucose", avg_glucose)
c5.metric("⚖ Avg BMI", avg_bmi)

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
        color="prediction",
        title="Glucose Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    pie = pd.DataFrame({

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

        pie,

        values="Count",

        names="Risk",

        hole=0.6,

        title="Prediction Distribution"

    )

    fig2.update_layout(

        template="plotly_dark",

        height=420

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

st.write("")

# ==========================================
# TABLE
# ==========================================

st.subheader("📋 Patient Records")

table = df.copy()

table["prediction"] = table["prediction"].replace({

    0: "🟢 Low Risk",

    1: "🔴 High Risk"

})

table = table.sort_values(

    by="created_at",

    ascending=False

)

st.dataframe(

    table,

    hide_index=True,

    use_container_width=True

)

# ==========================================
# CSV
# ==========================================

csv = table.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇ Download CSV",

    csv,

    "patient_history.csv",

    "text/csv",

    use_container_width=True

)

st.write("")
# ==========================================
# PATIENT DETAILS
# ==========================================

st.subheader("👤 Patient Details")

selected = st.selectbox(

    "Choose Assessment",

    df["id"]

)

patient = df[df["id"] == selected].iloc[0]

left, right = st.columns(2)

with left:

    st.markdown("### 👤 Personal Information")

    st.write(f"**Name:** {patient['full_name']}")
    st.write(f"**Age:** {patient['age']}")
    st.write(f"**Gender:** {patient['gender']}")
    st.write(f"**Weight:** {patient['weight']} kg")
    st.write(f"**Height:** {patient['height']} cm")

with right:

    st.markdown("### 🩺 Medical Information")

    st.write(f"**Pregnancies:** {patient['pregnancies']}")
    st.write(f"**Glucose:** {patient['glucose']}")
    st.write(f"**Blood Pressure:** {patient['blood_pressure']}")
    st.write(f"**Skin Thickness:** {patient['skin_thickness']}")
    st.write(f"**Insulin:** {patient['insulin']}")
    st.write(f"**BMI:** {patient['bmi']}")
    st.write(f"**Pedigree:** {patient['pedigree']}")

st.divider()

# ==========================================
# AI RESULT
# ==========================================

probability = float(patient["probability"]) * 100

st.subheader("🤖 AI Prediction")

if patient["prediction"] == 1:

    st.error(f"🔴 High Risk ({probability:.2f}%)")

else:

    st.success(f"🟢 Low Risk ({probability:.2f}%)")

st.progress(min(probability / 100, 1.0))

st.write("")

# ==========================================
# REPORT
# ==========================================

report = f"""
HealthVibe AI
====================================

Patient Name : {patient['full_name']}

Age : {patient['age']}

Gender : {patient['gender']}

Weight : {patient['weight']} kg

Height : {patient['height']} cm

------------------------------------

Pregnancies : {patient['pregnancies']}

Glucose : {patient['glucose']}

Blood Pressure : {patient['blood_pressure']}

Skin Thickness : {patient['skin_thickness']}

Insulin : {patient['insulin']}

BMI : {patient['bmi']}

Pedigree : {patient['pedigree']}

------------------------------------

Prediction :

{"HIGH RISK" if patient["prediction"] == 1 else "LOW RISK"}

Probability :

{probability:.2f} %

====================================

Generated by HealthVibe AI
"""

st.download_button(

    "⬇ Download Report",

    report,

    file_name=f"{patient['full_name']}_Report.txt",

    mime="text/plain",

    use_container_width=True

)

# ==========================================
# DELETE (DOCTOR ONLY)
# ==========================================

if user["role"] == "Doctor":

    st.divider()

    if st.button(

        "🗑 Delete Selected Assessment",

        use_container_width=True

    ):

        from components.database import connect

        conn = connect()

        cur = conn.cursor()

        cur.execute(

            "DELETE FROM patients WHERE id=?",

            (selected,)

        )

        conn.commit()

        conn.close()

        st.success("Assessment deleted successfully.")

        st.rerun()

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
Developed by <b>HealthVibe Team</b>
</p>

</div>

""", unsafe_allow_html=True)