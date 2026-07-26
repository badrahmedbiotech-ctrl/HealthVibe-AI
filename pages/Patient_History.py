import streamlit as st
import pandas as pd
import plotly.express as px

from utils.navigation import sidebar
from components.language import apply_language
from translations import get_text

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

user = st.session_state.get("user")

# ==========================================
# CSS
# ==========================================
lang = apply_language()

with open("style.css", encoding="utf-8") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================
# LOAD DATA
# ==========================================

if user and user.get("role") == "Doctor":

    df = get_all_history()

else:
    # بدلاً من user["id"] المباشرة:
 user_id = user.get("id") if isinstance(user, dict) else user
df = get_user_history(user_id)

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

st.markdown(f"""
<div class="hero">

<h1>{get_text(lang, "patient_history_hero_title")}</h1>

<p>
{get_text(lang, "patient_history_hero_desc")}
</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================
# SEARCH
# ==========================================

search = st.text_input(
    "🔍 Search Patient",
    get_text(lang, "search_patient_label"),
    placeholder=get_text(lang, "search_patient_placeholder")
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
if len(df) == 0:

    st.warning(get_text(lang, "no_patient_records"))

else:

    high = len(df[df["prediction"] == 1])

    low = len(df[df["prediction"] == 0])

    avg_bmi = round(df["bmi"].mean(), 1)

    total = len(df)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            get_text(lang, "metric_total_patients"),
            total
        )

    with c2:
        st.metric(
            get_text(lang, "metric_high_risk"),
            high
        )

    with c3:
        st.metric(
            get_text(lang, "metric_low_risk"),
            low
        )

    with c4:
        st.metric(
            get_text(lang, "metric_avg_bmi"),
            avg_bmi
        )

    st.write("")

    left, right = st.columns([2, 1])

    with left:

        fig = px.histogram(

            df,

            x="glucose",

            nbins=20,

            title=get_text(lang, "glucose_distribution_title")

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        risk = pd.DataFrame({

            "Risk": [get_text(lang, "risk_label_low"), get_text(lang, "risk_label_high")],

            "Count": [low, high]

        })

        fig2 = px.pie(

            risk,

            values="Count",

            names="Risk",

            hole=.55,

            title=get_text(lang, "risk_distribution_title")

        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )
        st.write("")

st.subheader(get_text(lang, "patient_records_header"))

show_df = df.copy()

if "prediction" in show_df.columns:

    show_df["prediction"] = show_df["prediction"].replace({

        0: get_text(lang, "metric_low_risk"),

        1: get_text(lang, "metric_high_risk")

    })

st.dataframe(

    show_df,

    use_container_width=True,

    hide_index=True

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
    get_text(lang, "download_patient_history_button"),

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

st.subheader(get_text(lang, "view_patient_details_header"))

patient_ids = df["id"].tolist()

selected = st.selectbox(

    get_text(lang, "select_patient_label"),

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

    st.markdown(f"### {get_text(lang, 'personal_info')}")

    st.write(f"**{get_text(lang, 'name_label')}:** {patient['full_name']}")

    st.write(f"**{get_text(lang, 'age')}:** {patient['age']}")

    st.write(f"**{get_text(lang, 'gender')}:** {patient['gender']}")

    st.write(f"**{get_text(lang, 'weight_plain_label')}:** {patient['weight']} kg")

    st.write(f"**{get_text(lang, 'height_plain_label')}:** {patient['height']} cm")

with right:

    st.markdown(f"### {get_text(lang, 'medical_info_header')}")

    st.write(f"**{get_text(lang, 'bmi_label')}:** {patient['bmi']}")

    st.write(f"**{get_text(lang, 'glucose_label')}:** {patient['glucose']}")

    st.write(f"**{get_text(lang, 'blood_pressure_label')}:** {patient['blood_pressure']}")

    st.write(f"**{get_text(lang, 'insulin_label')}:** {patient['insulin']}")

    st.write(f"**{get_text(lang, 'pedigree_label')}:** {patient['pedigree']}")

if patient["prediction"] == 1:

    st.error(get_text(lang, "high_risk_diabetes_msg"))

else:

    st.success(get_text(lang, "low_risk_diabetes_msg"))

    st.write("")

st.divider()

# ==========================================
# AI RESULT
# ==========================================

probability = float(patient["probability"]) * 100

st.subheader("🤖 AI Prediction")

if patient["prediction"] == 1:
    st.subheader(get_text(lang, "delete_patient_header"))

    st.error(f"🔴 High Risk ({probability:.2f}%)")

else:
        get_text(lang, "patient_id_label"),

st.success(f"🟢 Low Risk ({probability:.2f}%)")

st.progress(min(probability / 100, 1.0))

st.write("")

# ==========================================
# REPORT
# ==========================================

if st.button(
        get_text(lang, "delete_record_button"),
        use_container_width=True
    ):
        delete_patient(delete_id)
        st.success(get_text(lang, "patient_deleted_success"))
        st.rerun()

# ==========================
# PDF REPORT
# ==========================

with right:
    st.subheader(get_text(lang, "medical_report_header"))

    report = f"""
HealthVibe AI
_________________________________________________________

{get_text(lang, 'name_label')} : {patient['full_name']}
{get_text(lang, 'age')} : {patient['age']}
{get_text(lang, 'gender')} : {patient['gender']}
{get_text(lang, 'weight_plain_label')} : {patient['weight']} kg
{get_text(lang, 'height_plain_label')} : {patient['height']} cm
"""
___________________________________________ 

f"{get_text(lang, 'pregnancies_label')} : {patient['pregnancies']}"
f"{get_text(lang, 'glucose_label')} : {patient['glucose']}"
f"{get_text(lang, 'blood_pressure_label')} : {patient['blood_pressure']}"
f"{get_text(lang, 'skin_thickness_label')} : {patient['skin_thickness']}"
f"{get_text(lang, 'insulin_label')} : {patient['insulin']}"
f"{get_text(lang, 'bmi_label')} : {patient['bmi']}"
f"{get_text(lang, 'pedigree_label')} : {patient['pedigree']}"

__________________________________________________________________

f"{get_text(lang, 'report_prediction_label')}"

{get_text(lang, 'report_high_risk') if patient["prediction"] == 1 else get_text(lang, 'report_low_risk')}

f"{get_text(lang, 'probability_label')}: {patient.get('probability', 0.0):.2f}%"
___________________________________________________________
{get_text(lang, 'report_generated_by')}
"""
st.download_button(

    "⬇ Download Report",
        get_text(lang, "download_report_button"),

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

st.markdown(f"""
<div class="footer">

<h2 style="color:#00C2FF;">
HealthVibe AI
</h2>

<p>
{get_text(lang, "footer_desc_patient_history")}
</p>

<hr>

<p style="color:#94A3B8;">
Developed by <b>HealthVibe Team</b>
{get_text(lang, "footer_developed_by")}
</p>

</div>

""", unsafe_allow_html=True) 