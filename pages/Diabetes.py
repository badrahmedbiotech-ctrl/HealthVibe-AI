import streamlit as st
import joblib
import pandas as pd

from components.pdf_report import create_pdf
from utils.navigation import sidebar
from components.result_card import result_card
from components.recommendation import recommendation
from components.patient_summary import patient_summary
from components.ai_gauge import ai_gauge
from components.loading_animation import ai_loading
from components.stepper import stepper
from components.glass_card import open_card, close_card
from components.language import apply_language
from translations import get_text
from components.database import (
    create_tables,
    save_patient
)
from database.db import create_table
from database.db import insert_patient

create_table()

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩸",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

lang = apply_language()

sidebar()

# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("models/diabetes_model.pkl")

model = load_model()

# إنشاء قاعدة البيانات إذا لم تكن موجودة
create_tables()

# ==========================================
# SESSION STATE
# ==========================================

if "step" not in st.session_state:
    st.session_state.step = 1

if "patient" not in st.session_state:
    st.session_state.patient = {}

# ==========================================
# HERO
# ==========================================

st.markdown(f"""
<div class="hero">

<h1>{get_text(lang, "diabetes_hero_title")}</h1>

<p>
{get_text(lang, "diabetes_hero_desc")}
</p>

</div>
""", unsafe_allow_html=True)

stepper(st.session_state.step)

st.write()

open_card()

# ==========================================
# STEP 1
# ==========================================

if st.session_state.step == 1:

    st.subheader(get_text(lang, "step1_header"))

    name = st.text_input(
        get_text(lang, "full_name"),
        value=st.session_state.patient.get("name", "")
    )

    age = st.number_input(
        get_text(lang, "age"),
        1,
        120,
        st.session_state.patient.get("age", 30)
    )

    gender = st.selectbox(
        get_text(lang, "gender"),
        [get_text(lang, "male"), get_text(lang, "female")],
        index=0 if st.session_state.patient.get("gender", get_text(lang, "male")) == get_text(lang, "male") else 1
    )

    weight = st.number_input(
        get_text(lang, "weight"),
        20,
        250,
        st.session_state.patient.get("weight", 70)
    )

    height = st.number_input(
        get_text(lang, "height"),
        80,
        250,
        st.session_state.patient.get("height", 170)
    )

    c1, c2 = st.columns([1, 1])

    with c2:

        if st.button(get_text(lang, "next"), use_container_width=True):

            st.session_state.patient["name"] = name
            st.session_state.patient["age"] = age
            st.session_state.patient["gender"] = gender
            st.session_state.patient["weight"] = weight
            st.session_state.patient["height"] = height

            st.session_state.step = 2

            st.rerun()

# ==========================================
# STEP 2
# ==========================================

elif st.session_state.step == 2:

    st.subheader(get_text(lang, "step2_header"))

    pregnancies = st.number_input(
        get_text(lang, "pregnancies_label"),
        min_value=0,
        max_value=20,
        value=st.session_state.patient.get("pregnancies", 0)
    )

    glucose = st.number_input(
        get_text(lang, "glucose_label"),
        min_value=50,
        max_value=300,
        value=st.session_state.patient.get("glucose", 120)
    )

    blood_pressure = st.number_input(
        get_text(lang, "blood_pressure_label"),
        min_value=40,
        max_value=200,
        value=st.session_state.patient.get("blood_pressure", 70)
    )

    insulin = st.number_input(
        get_text(lang, "insulin_label"),
        min_value=0,
        max_value=900,
        value=st.session_state.patient.get("insulin", 80)
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(get_text(lang, "back"), use_container_width=True):

            st.session_state.step = 1
            st.rerun()

    with c2:

        if st.button(get_text(lang, "next"), use_container_width=True):

            st.session_state.patient["pregnancies"] = pregnancies
            st.session_state.patient["glucose"] = glucose
            st.session_state.patient["blood_pressure"] = blood_pressure
            st.session_state.patient["insulin"] = insulin

            st.session_state.step = 3

            st.rerun()

# ==========================================
# STEP 3
# ==========================================

elif st.session_state.step == 3:

    st.subheader(get_text(lang, "step3_header"))

    skin_thickness = st.number_input(
        get_text(lang, "skin_thickness_label"),
        min_value=0,
        max_value=100,
        value=st.session_state.patient.get("skin_thickness", 20)
    )

    bmi = st.number_input(
        get_text(lang, "bmi_label"),
        min_value=10.0,
        max_value=70.0,
        value=st.session_state.patient.get("bmi", 25.0)
    )

    pedigree = st.number_input(
        get_text(lang, "pedigree_label"),
        min_value=0.0,
        max_value=3.0,
        value=st.session_state.patient.get("pedigree", 0.50),
        format="%.3f"
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(get_text(lang, "back"), use_container_width=True):

            st.session_state.step = 2
            st.rerun()

    with c2:

        if st.button(get_text(lang, "analyze_ai_button"), use_container_width=True):

            st.session_state.patient["skin_thickness"] = skin_thickness
            st.session_state.patient["bmi"] = bmi
            st.session_state.patient["pedigree"] = pedigree

            st.session_state.step = 4

            st.rerun()

# ==========================================
# STEP 4
# ==========================================

elif st.session_state.step == 4:

    st.subheader(get_text(lang, "step4_header"))

    patient = st.session_state.patient

    input_data = pd.DataFrame([[
        patient["pregnancies"],
        patient["glucose"],
        patient["blood_pressure"],
        patient["skin_thickness"],
        patient["insulin"],
        patient["bmi"],
        patient["pedigree"],
        patient["age"]
    ]], columns=[
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age"
    ])

    # ==========================
    # AI Loading
    # ==========================

    ai_loading()

    # ==========================
    # Prediction
    # ==========================

    prediction = model.predict(input_data)[0]

    try:
        probability = model.predict_proba(input_data)[0][1]
    except:
        probability = None

    # ==========================
    # SAVE RESULT TO DATABASE
    # ==========================

    patient["prediction"] = int(prediction)
    patient["probability"] = float(probability) if probability is not None else 0.0

    if "saved" not in st.session_state:
        save_patient(patient)
        st.session_state.saved = True

    # ==========================
    # SUCCESS
    # ==========================

    st.success(get_text(lang, "analysis_success_diabetes"))

    st.write("")

    # ==========================
    # AI Gauge
    # ==========================

    ai_gauge(probability)

    st.write("")

    # ==========================================
    # SAVE TO DATABASE
    # ==========================================

    insert_patient(

        (

            patient["name"],

            patient["age"],

            patient["gender"],

            patient["weight"],

            patient["height"],

            patient["pregnancies"],

            patient["glucose"],

            patient["blood_pressure"],

            patient["skin_thickness"],

            patient["insulin"],

            patient["bmi"],

            patient["pedigree"],

            int(prediction),

            float(probability if probability is not None else 0)

        )

    )

    result_card(prediction, probability)

    st.write("")

    # ==========================
    # Recommendation
    # ==========================

    recommendation(prediction)

    st.write("")

    # ==========================
    # Patient Summary
    # ==========================

    patient_summary({

        get_text(lang, "full_name"): patient["name"],
        get_text(lang, "age"): patient["age"],
        get_text(lang, "gender"): patient["gender"],
        get_text(lang, "weight"): patient["weight"],
        get_text(lang, "height"): patient["height"],
        get_text(lang, "pregnancies_label"): patient["pregnancies"],
        get_text(lang, "glucose_label"): patient["glucose"],
        get_text(lang, "blood_pressure_label"): patient["blood_pressure"],
        get_text(lang, "skin_thickness_label"): patient["skin_thickness"],
        get_text(lang, "insulin_label"): patient["insulin"],
        get_text(lang, "bmi_label"): patient["bmi"],
        get_text(lang, "pedigree_label"): patient["pedigree"]

    })

    # ==========================================
    # PDF REPORT
    # ==========================================

    st.write("")
    st.subheader(get_text(lang, "medical_report_header"))

    pdf_file = create_pdf(patient)

    with open(pdf_file, "rb") as pdf:

        st.download_button(

            label=get_text(lang, "download_pdf_report_button"),

            data=pdf,

            file_name=pdf_file,

            mime="application/pdf",

            use_container_width=True

        )

    st.write("")

    # ==========================
    # Buttons
    # ==========================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(get_text(lang, "back"), use_container_width=True):

            st.session_state.step = 3
            st.rerun()

    with col2:

        if st.button(get_text(lang, "new_assessment_button"), use_container_width=True):

            st.session_state.step = 1
            st.session_state.patient = {}
            if "saved" in st.session_state:
                del st.session_state.saved

            st.rerun()

    close_card()

st.write("")
st.divider()

st.markdown(f"""
<div class="footer">

<h2 style="color:#00C2FF;">
{get_text(lang, "app_title")}
</h2>

<p>
{get_text(lang, "footer_desc_diabetes")}
</p>

<hr>

<p style="color:#94A3B8;">
{get_text(lang, "footer_developed_by")}
</p>

</div>
""", unsafe_allow_html=True)