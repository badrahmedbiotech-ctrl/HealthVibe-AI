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

st.markdown("""
<div class="hero">

<h1>🩸 Diabetes Assessment</h1>

<p>
Complete the following assessment to estimate diabetes risk.
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

    st.subheader("👤 Patient Information")

    name = st.text_input(
        "Full Name",
        value=st.session_state.patient.get("name","")
    )

    age = st.number_input(
        "Age",
        1,
        120,
        st.session_state.patient.get("age",30)
    )

    gender = st.selectbox(
        "Gender",
        ["Male","Female"],
        index=0 if st.session_state.patient.get("gender","Male")=="Male" else 1
    )

    weight = st.number_input(
        "Weight (kg)",
        20,
        250,
        st.session_state.patient.get("weight",70)
    )

    height = st.number_input(
        "Height (cm)",
        80,
        250,
        st.session_state.patient.get("height",170)
    )

    c1,c2 = st.columns([1,1])

    with c2:

        if st.button("Next ➜", use_container_width=True):

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

    st.subheader("🩺 Medical Information")

    pregnancies = st.number_input(
        "Pregnancies",
        min_value=0,
        max_value=20,
        value=st.session_state.patient.get("pregnancies",0)
    )

    glucose = st.number_input(
        "Glucose",
        min_value=50,
        max_value=300,
        value=st.session_state.patient.get("glucose",120)
    )

    blood_pressure = st.number_input(
        "Blood Pressure",
        min_value=40,
        max_value=200,
        value=st.session_state.patient.get("blood_pressure",70)
    )

    insulin = st.number_input(
        "Insulin",
        min_value=0,
        max_value=900,
        value=st.session_state.patient.get("insulin",80)
    )

    c1,c2 = st.columns(2)

    with c1:

        if st.button("⬅ Back", use_container_width=True):

            st.session_state.step = 1
            st.rerun()

    with c2:

        if st.button("Next ➜", use_container_width=True):

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

    st.subheader("📊 Additional Measurements")

    skin_thickness = st.number_input(
        "Skin Thickness",
        min_value=0,
        max_value=100,
        value=st.session_state.patient.get("skin_thickness",20)
    )

    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=70.0,
        value=st.session_state.patient.get("bmi",25.0)
    )

    pedigree = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        max_value=3.0,
        value=st.session_state.patient.get("pedigree",0.50),
        format="%.3f"
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button("⬅ Back", use_container_width=True):

            st.session_state.step = 2
            st.rerun()

    with c2:

        if st.button("🤖 Analyze with AI", use_container_width=True):

            st.session_state.patient["skin_thickness"] = skin_thickness
            st.session_state.patient["bmi"] = bmi
            st.session_state.patient["pedigree"] = pedigree

            st.session_state.step = 4

            st.rerun()

# ==========================================
# STEP 4
# ==========================================

elif st.session_state.step == 4:

    st.subheader("🤖 AI Analysis Result")

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

st.success("Analysis Completed Successfully ✅")

st.write("")

# ==========================
# AI Gauge
# ==========================

ai_gauge(probability)

st.write("")

# ==========================
# Result Card
# ==========================

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

        "Full Name": patient["name"],
        "Age": patient["age"],
        "Gender": patient["gender"],
        "Weight (kg)": patient["weight"],
        "Height (cm)": patient["height"],
        "Pregnancies": patient["pregnancies"],
        "Glucose": patient["glucose"],
        "Blood Pressure": patient["blood_pressure"],
        "Skin Thickness": patient["skin_thickness"],
        "Insulin": patient["insulin"],
        "BMI": patient["bmi"],
        "Pedigree": patient["pedigree"]

    })
# ==========================================
# PDF REPORT
# ==========================================

st.write("")
st.subheader("📄 Medical Report")

pdf_file = create_pdf(patient)

with open(pdf_file, "rb") as pdf:

    st.download_button(

        label="⬇ Download PDF Report",

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

        if st.button("⬅ Back", use_container_width=True):

            st.session_state.step = 3
            st.rerun()

with col2:

        if st.button("🔄 New Assessment", use_container_width=True):

            st.session_state.step = 1
            st.session_state.patient = {}
        if "saved" in st.session_state:
            del st.session_state.saved

            st.rerun()

            close_card()

st.write("")
st.divider()

st.markdown("""
<div class="footer">

<h2 style="color:#00C2FF;">
HealthVibe AI
</h2>

<p>
AI-powered Diabetes Prediction System
</p>

<hr>

<p style="color:#94A3B8;">
Developed by <b>Badr Ahmed</b>
</p>

</div>
""", unsafe_allow_html=True)