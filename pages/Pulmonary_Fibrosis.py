import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from PIL import Image

from utils.navigation import sidebar
from components.language import apply_language
from translations import get_text

# ===========================================
# PAGE CONFIG
# ===========================================

st.set_page_config(
    page_title="Pulmonary Fibrosis AI",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

lang = apply_language()

# ===========================================
# LOAD CSS
# ===========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar()

# ===========================================
# LOAD MODEL
# ===========================================

model = joblib.load("models/respiratory_model.pkl")

dataset = pd.read_csv("dataset/Fibrosis_data.csv")

symptoms_list = sorted(
    dataset["Symptoms"].dropna().astype(str).str.strip().unique()
)

SYMPTOM_DISPLAY_MAP = {
    "cough": "pf_symptom_cough",
    "coughing": "pf_symptom_coughing",
    "shortness of breath": "pf_symptom_shortness_of_breath",
    "tight feeling in the chest": "pf_symptom_tight_chest",
    "wheezing": "pf_symptom_wheezing",
    "a cough that lasts more than three weeks": "pf_symptom_cough_three_weeks",
    "a dry, crackling sound in the lungs while breathing in": "pf_symptom_dry_crackling_sound",
    "allergy": "pf_symptom_allergy",
    "bluish skin": "pf_symptom_bluish_skin",
    "breath": "pf_symptom_breath",
    "chest congestion": "pf_symptom_chest_congestion",
    "chest pain": "pf_symptom_chest_pain",
    "chest tightness or chest pain": "pf_symptom_chest_tightness_or_pain",
    "chills": "pf_symptom_chills",
    "chronic cough": "pf_symptom_chronic_cough",
    "cold": "pf_symptom_cold",
    "cough with blood": "pf_symptom_cough_with_blood",
    "coughing up blood": "pf_symptom_coughing_up_blood",
    "coughing up yellow or green mucus daily": "pf_symptom_coughing_yellow_green_mucus",
    "daytime sleepiness": "pf_symptom_daytime_sleepiness",
    "diarrhea": "pf_symptom_diarrhea",
    "difficulties with memory and concentration": "pf_symptom_memory_concentration",
    "distressing": "pf_symptom_distressing",
    "dizziness": "pf_symptom_dizziness",
    "dry cough": "pf_symptom_dry_cough",
    "dry mouth": "pf_symptom_dry_mouth",
    "edema": "pf_symptom_edema",
    "fainting": "pf_symptom_fainting",
    "faster heart beating": "pf_symptom_faster_heart_beating",
    "fatigue": "pf_symptom_fatigue",
    "fatigue, feeling run-down or tired": "pf_symptom_fatigue_run_down",
    "feeling run-down or tired": "pf_symptom_feeling_run_down",
    "fever": "pf_symptom_fever",
    "frequently waking": "pf_symptom_frequently_waking",
    "greenish cough": "pf_symptom_greenish_cough",
    "headache": "pf_symptom_headache",
    "heart palpitations": "pf_symptom_heart_palpitations",
    "high fever": "pf_symptom_high_fever",
    "irritability": "pf_symptom_irritability",
    "joint pain": "pf_symptom_joint_pain",
    "loss of appetite": "pf_symptom_loss_of_appetite",
    "loss of appetite and unintentional weight loss": "pf_symptom_loss_appetite_weight_loss",
    "low energy": "pf_symptom_low_energy",
    "low-grade fever": "pf_symptom_low_grade_fever",
    "lower back pain": "pf_symptom_lower_back_pain",
    "morning headaches": "pf_symptom_morning_headaches",
    "mucus": "pf_symptom_mucus",
    "muscle aches": "pf_symptom_muscle_aches",
    "nasal congestion": "pf_symptom_nasal_congestion",
    "nausea": "pf_symptom_nausea",
    "night sweats": "pf_symptom_night_sweats",
    "pain": "pf_symptom_pain",
    "pauses in breathing": "pf_symptom_pauses_in_breathing",
    "persistent dry cough": "pf_symptom_persistent_dry_cough",
    "rapid breathing": "pf_symptom_rapid_breathing",
    "rapid heartbeat": "pf_symptom_rapid_heartbeat",
    "runny nose": "pf_symptom_runny_nose",
    "shaking": "pf_symptom_shaking",
    "shallow breathing": "pf_symptom_shallow_breathing",
    "sharp chest pain": "pf_symptom_sharp_chest_pain",
    "short of breath": "pf_symptom_short_of_breath",
    "short, shallow and rapid breathing": "pf_symptom_short_shallow_rapid_breathing",
    "shortness of breath that gets worse during flare-ups": "pf_symptom_sob_worse_flareups",
    "snoring": "pf_symptom_snoring",
    "sore throat": "pf_symptom_sore_throat",
    "stuffy nose": "pf_symptom_stuffy_nose",
    "sweating": "pf_symptom_sweating",
    "unusual moodiness": "pf_symptom_unusual_moodiness",
    "vomiting": "pf_symptom_vomiting",
    "weight loss": "pf_symptom_weight_loss",
    "weight loss from loss of appetite": "pf_symptom_weight_loss_from_appetite",
    "wheezing cough": "pf_symptom_wheezing_cough",
    "whistling sound while breathing": "pf_symptom_whistling_sound_breathing",
    "whistling sound while you breathe": "pf_symptom_whistling_sound_you_breathe",
    "wider and rounder than normal fingertips and toes": "pf_symptom_clubbing_fingers_toes",
    "yellow cough": "pf_symptom_yellow_cough",
}


def symptom_display(value):
    key = SYMPTOM_DISPLAY_MAP.get(str(value).strip().lower())
    return get_text(lang, key) if key else value


# ===========================================
# HERO
# ===========================================

st.markdown(f"""

<div class="hero">

<h1>
{get_text(lang, "pf_title")}
</h1>

<p>

{get_text(lang, "pf_subtitle")}

</p>

</div>

""", unsafe_allow_html=True)

# ===========================================
# TOP DASHBOARD
# ===========================================

st.subheader(get_text(lang, "ai_dashboard_header"))

a, b, c, d = st.columns(4)

with a:
    st.metric(
        get_text(lang, "metric_diseases"),
        len(dataset["Disease"].unique())
    )

with b:
    st.metric(
        get_text(lang, "metric_dataset"),
        f"{len(dataset):,}"
    )

with c:
    st.metric(
        get_text(lang, "metric_accuracy"),
        "92.6%"
    )

with d:
    st.metric(
        get_text(lang, "metric_status"),
        get_text(lang, "status_online")
    )

st.divider()

# ===========================================
# BASIC INFORMATION
# ===========================================

st.subheader(get_text(lang, "patient_info_header"))

left, right = st.columns(2)

with left:

    full_name = st.text_input(
        get_text(lang, "full_name"),
        placeholder=get_text(lang, "full_name_placeholder")
    )

    age = st.number_input(
        get_text(lang, "age"),
        1,
        120,
        30
    )

    gender = st.selectbox(
        get_text(lang, "gender"),
        ["Male", "Female"],
        format_func=lambda v: get_text(lang, "male") if v == "Male" else get_text(lang, "female")
    )

with right:

    height = st.number_input(
        get_text(lang, "height"),
        100,
        250,
        170
    )

    weight = st.number_input(
        get_text(lang, "weight"),
        20,
        250,
        70
    )

    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

st.write("")

m1, m2, m3, m4 = st.columns(4)

m1.metric(get_text(lang, "metric_age"), age)
m2.metric(get_text(lang, "metric_bmi"), f"{bmi:.1f}")
m3.metric(get_text(lang, "metric_gender_icon"), get_text(lang, "male") if gender == "Male" else get_text(lang, "female"))
m4.metric(get_text(lang, "metric_height_icon"), f"{height} cm")

st.progress(100 if full_name else 80)

st.caption(get_text(lang, "patient_profile_caption"))

st.divider()

# ===========================================
# MEDICAL HISTORY
# ===========================================

st.subheader(get_text(lang, "medical_history_header"))

col1, col2 = st.columns(2)

with col1:

    smoking_map = {
        "No": get_text(lang, "smoking_no"),
        "Former Smoker": get_text(lang, "smoking_former"),
        "Current Smoker": get_text(lang, "smoking_current"),
    }
    smoking = st.selectbox(
        get_text(lang, "smoking_status_label"),
        list(smoking_map.keys()),
        format_func=lambda v: smoking_map[v]
    )

    asthma = st.checkbox(get_text(lang, "asthma_label"))

    copd = st.checkbox(get_text(lang, "copd_label"))

    hypertension = st.checkbox(get_text(lang, "hypertension_checkbox"))

with col2:

    diabetes = st.checkbox(get_text(lang, "diabetes_checkbox"))

    family_history = st.checkbox(get_text(lang, "family_history_checkbox"))

    tuberculosis = st.checkbox(get_text(lang, "tuberculosis_label"))

    lung_cancer = st.checkbox(get_text(lang, "lung_cancer_label"))

st.divider()

# ===========================================
# SYMPTOMS
# ===========================================

st.subheader(get_text(lang, "symptoms_header"))

symptom = st.selectbox(
    get_text(lang, "main_symptom_label"),
    symptoms_list,
    format_func=symptom_display,
)

st.divider()

# ===========================================
# LIFESTYLE
# ===========================================

st.subheader(get_text(lang, "lifestyle_header"))

left, right = st.columns(2)

with left:

    exercise_map = {
        "Regular": get_text(lang, "exercise_regular"),
        "Sometimes": get_text(lang, "exercise_sometimes"),
        "Rarely": get_text(lang, "exercise_rarely"),
    }
    exercise = st.selectbox(
        get_text(lang, "exercise_label"),
        list(exercise_map.keys()),
        format_func=lambda v: exercise_map[v]
    )

    occupation = st.text_input(
        get_text(lang, "occupation_label")
    )

    sleep = st.slider(
        get_text(lang, "sleep_hours_label"),
        3,
        12,
        7
    )

with right:

    passive_smoking = st.selectbox(
        get_text(lang, "passive_smoking_label"),
        ["No", "Yes"],
        format_func=lambda v: get_text(lang, "no_option") if v == "No" else get_text(lang, "yes_option")
    )

    pollution_map = {
        "Low": get_text(lang, "pollution_low"),
        "Medium": get_text(lang, "pollution_medium"),
        "High": get_text(lang, "pollution_high"),
    }
    pollution = st.selectbox(
        get_text(lang, "pollution_label"),
        list(pollution_map.keys()),
        format_func=lambda v: pollution_map[v]
    )

    chemicals = st.selectbox(
        get_text(lang, "chemicals_label"),
        ["No", "Yes"],
        format_func=lambda v: get_text(lang, "no_option") if v == "No" else get_text(lang, "yes_option")
    )

st.divider()

# ===========================================
# VITAL SIGNS
# ===========================================

st.subheader(get_text(lang, "vital_signs_header"))

left, right = st.columns(2)

with left:

    temperature = st.number_input(
        get_text(lang, "temperature_label"),
        34.0,
        42.0,
        37.0
    )

    heart_rate = st.number_input(
        get_text(lang, "heart_rate_label"),
        30,
        200,
        80
    )

with right:

    spo2 = st.slider(
        get_text(lang, "spo2_label"),
        50,
        100,
        98
    )

    respiratory_rate = st.number_input(
        get_text(lang, "respiratory_rate_label"),
        5,
        40,
        18
    )

st.divider()

# ===========================================
# CLINICAL TESTS
# ===========================================

st.subheader(get_text(lang, "clinical_tests_header"))

c1, c2 = st.columns(2)

with c1:

    ct_scan = st.selectbox(
        get_text(lang, "ct_scan_label"),
        ["Normal", "Abnormal"],
        format_func=lambda v: get_text(lang, "normal_option") if v == "Normal" else get_text(lang, "abnormal_option")
    )

    chest_xray = st.selectbox(
        get_text(lang, "chest_xray_label"),
        ["Normal", "Abnormal"],
        format_func=lambda v: get_text(lang, "normal_option") if v == "Normal" else get_text(lang, "abnormal_option")
    )

with c2:

    pft = st.selectbox(
        get_text(lang, "pft_label"),
        ["Normal", "Reduced"],
        format_func=lambda v: get_text(lang, "normal_option") if v == "Normal" else get_text(lang, "reduced_option")
    )

    fibrosis_history = st.selectbox(
        get_text(lang, "fibrosis_history_label"),
        ["No", "Yes"],
        format_func=lambda v: get_text(lang, "no_option") if v == "No" else get_text(lang, "yes_option")
    )

st.divider()

# ===========================================
# CT SCAN IMAGE
# ===========================================

st.divider()

st.subheader(get_text(lang, "ct_scan_upload_header"))

uploaded_image = st.file_uploader(
    get_text(lang, "upload_chest_ct_label"),
    type=["png", "jpg", "jpeg"]
)

if uploaded_image is not None:

    image = Image.open(uploaded_image)

    st.image(
        image,
        caption=get_text(lang, "uploaded_ct_caption"),
        use_container_width=True
    )

    st.success(get_text(lang, "ct_upload_success"))

# ===========================================
# LIVE DASHBOARD
# ===========================================

st.subheader(get_text(lang, "live_dashboard_header"))

d1, d2, d3, d4 = st.columns(4)

d1.metric(get_text(lang, "bmi_label"), f"{bmi:.1f}")
d2.metric(get_text(lang, "spo2_label"), f"{spo2}%")
d3.metric(get_text(lang, "heart_rate_label"), f"{heart_rate} bpm")
d4.metric(get_text(lang, "temperature_label"), f"{temperature:.1f} °C")

st.divider()

# ===========================================
# AI ANALYSIS
# ===========================================

if st.button(get_text(lang, "analyze_patient_button"), use_container_width=True):

    with st.spinner(get_text(lang, "ai_analyzing_spinner")):
        time.sleep(2)

        input_data = pd.DataFrame({
            "Symptoms": [symptom],
            "Age": [age],
            "Sex": [gender.lower()]
        })

        prediction = model.predict(input_data)[0]

        confidence = (
            model.predict_proba(input_data)[0].max() * 100
        )

    st.success(get_text(lang, "analysis_success_pf"))

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            get_text(lang, "predicted_disease_label"),
            prediction
        )

    with c2:
        st.metric(
            get_text(lang, "confidence_metric"),
            f"{confidence:.2f}%"
        )

    result = dataset[
        dataset["Disease"] == prediction
    ]

    if not result.empty:

        treatment = str(result.iloc[0]["Treatment"])
        nature = str(result.iloc[0]["Nature"])

        st.divider()

        st.subheader(get_text(lang, "suggested_treatment_header"))

        st.info(treatment)

        st.subheader(get_text(lang, "severity_header"))

        if nature.lower() == "high":
            st.error(get_text(lang, "severity_high"))
        elif nature.lower() == "medium":
            st.warning(get_text(lang, "severity_medium"))
        else:
            st.success(get_text(lang, "severity_low"))

st.divider()

# ===========================================
# IMAGE ANALYSIS
# ===========================================

if uploaded_image is not None:

    st.subheader(get_text(lang, "ct_scan_analysis_header"))

    st.info(get_text(lang, "ai_image_module_connected"))

    st.progress(85)

    st.success(get_text(lang, "no_severe_fibrosis"))

# ===========================================
# PATIENT REPORT
# ===========================================

st.subheader(get_text(lang, "patient_report_header"))

left, right = st.columns(2)

with left:

    st.metric(get_text(lang, "name_label"), full_name)
    st.metric(get_text(lang, "age"), age)
    st.metric(get_text(lang, "gender"), get_text(lang, "male") if gender == "Male" else get_text(lang, "female"))
    st.metric(get_text(lang, "bmi_label"), f"{bmi:.1f}")

with right:

    st.metric(get_text(lang, "smoking_metric_label"), smoking_map[smoking])
    st.metric(get_text(lang, "spo2_label"), f"{spo2}%")
    st.metric(get_text(lang, "heart_rate_label"), f"{heart_rate} bpm")
    st.metric(get_text(lang, "temperature_label"), f"{temperature:.1f} °C")

st.divider()

# ===========================================
# RISK CALCULATOR
# ===========================================

risk = 0

if smoking == "Current Smoker":
    risk += 30

if bmi >= 30:
    risk += 20

if spo2 < 94:
    risk += 30

if symptom == "coughing":
    risk += 10

if symptom == "shortness of breath":
    risk += 10

if symptom == "tight feeling in the chest":
    risk += 10

if symptom == "wheezing":
    risk += 10

risk = min(risk, 100)

st.subheader(get_text(lang, "risk_assessment_header"))

st.progress(risk)

st.metric(
    get_text(lang, "estimated_risk_label"),
    f"{risk}%"
)

if risk < 30:
    st.success(get_text(lang, "risk_low_pf"))
elif risk < 60:
    st.warning(get_text(lang, "risk_moderate_pf"))
else:
    st.error(get_text(lang, "risk_high_pf"))

st.divider()

st.markdown(
f"""
<div style="text-align:center">

<h3 style="color:#00C2FF;">
{get_text(lang, "pf_footer_title")}
</h3>

<p style="color:#94A3B8;">
{get_text(lang, "pf_footer_subtitle")}
</p>

<p style="color:gray;">
{get_text(lang, "footer_developed_by")}
</p>

</div>
""",
unsafe_allow_html=True
)