import streamlit as st
import pandas as pd
import plotly.express as px

from utils.navigation import sidebar
from components.language import apply_language
from translations import get_text

from components.database import (
    get_history,
    search_patient,
    delete_patient
)

st.set_page_config(
    page_title="Patient History",
    page_icon="📋",
    layout="wide"
)

lang = apply_language()

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

st.markdown(f"""
<div class="hero">

<h1>{get_text(lang, "patient_history_hero_title")}</h1>

<p>
{get_text(lang, "patient_history_hero_desc")}
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

search = st.text_input(
    get_text(lang, "search_patient_label"),
    placeholder=get_text(lang, "search_patient_placeholder")
)

if search:

    df = search_patient(search)

else:

    df = get_history()

    st.write("")

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

csv = df.to_csv(index=False).encode()

st.download_button(

    get_text(lang, "download_patient_history_button"),

    data=csv,

    file_name="Patient_History.csv",

    mime="text/csv",

    use_container_width=True

)

st.write("")

st.subheader(get_text(lang, "view_patient_details_header"))

patient_ids = df["id"].tolist()

selected = st.selectbox(

    get_text(lang, "select_patient_label"),

    patient_ids

)

patient = df[df["id"] == selected].iloc[0]

left, right = st.columns(2)

with left:

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

left, right = st.columns(2)

# ==========================
# DELETE
# ==========================

with left:

    st.subheader(get_text(lang, "delete_patient_header"))

    delete_id = st.number_input(

        get_text(lang, "patient_id_label"),

        min_value=1,

        step=1,

        key="delete_patient"

    )

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

==============================

{get_text(lang, 'name_label')} : {patient['full_name']}

{get_text(lang, 'age')} : {patient['age']}

{get_text(lang, 'gender')} : {patient['gender']}

{get_text(lang, 'weight_plain_label')} : {patient['weight']} kg

{get_text(lang, 'height_plain_label')} : {patient['height']} cm

------------------------------

{get_text(lang, 'glucose_label')} : {patient['glucose']}

{get_text(lang, 'blood_pressure_label')} : {patient['blood_pressure']}

{get_text(lang, 'insulin_label')} : {patient['insulin']}

{get_text(lang, 'bmi_label')} : {patient['bmi']}

{get_text(lang, 'pedigree_label')} : {patient['pedigree']}

------------------------------

{get_text(lang, 'report_prediction_label')} :

{get_text(lang, 'report_high_risk') if patient["prediction"] == 1 else get_text(lang, 'report_low_risk')}

==============================

{get_text(lang, 'report_generated_by')}

HealthVibe AI

"""

    st.download_button(

        get_text(lang, "download_report_button"),

        report,

        file_name=f"{patient['full_name']}_Report.txt",

        mime="text/plain",

        use_container_width=True

    )

    st.write("")
st.divider()

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
{get_text(lang, "footer_developed_by")}
</p>

</div>
""", unsafe_allow_html=True)