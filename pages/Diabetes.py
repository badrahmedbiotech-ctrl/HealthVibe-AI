import streamlit as st

from components.auth_guard import require_patient

require_patient()

import joblib
import pandas as pd
from utils.db import insert_patient  # أو حسب المسار الخاص بالـ database عندك

# ==========================
# LOGIN CHECK
# ==========================

if "user" not in st.session_state:
    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state["user"]

from components.database import get_profile

profile = get_profile(user["id"])

if profile is None:
    st.warning("Please complete your profile first.")
    st.switch_page("pages/Profile.py")
    st.stop()

from utils.navigation import sidebar
from components.database import get_profile
from components.stepper import stepper
from components.result_card import result_card
from components.recommendation import recommendation
from components.patient_summary import patient_summary
from components.ai_gauge import ai_gauge
from components.loading_animation import ai_loading
from components.pdf_report import create_pdf

from components.stepper import stepper
from components.glass_card import open_card, close_card
from components.language import apply_language
from translations import get_text
from components.database import (
    create_tables,
    save_patient
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩸",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

lang = apply_language()

sidebar()

# ==========================================
# MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("models/diabetes_model.pkl")

model = load_model()

create_tables()

# ==========================================
# SESSION
# ==========================================

if "step" not in st.session_state:
    st.session_state.step = 1

if "patient" not in st.session_state:
    st.session_state.patient = {}

if "saved" not in st.session_state:
    st.session_state.saved = False

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

st.write("")

# ==========================================
# STEP 1
# ==========================================

if st.session_state.step == 1:

    st.subheader(get_text(lang, "step1_header"))

    name = profile["full_name"] or ""
    age = profile["age"] or 20
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70.0
    height = profile["height"] or 170.0

    st.success("✅ Patient information loaded from your profile.")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Full Name", value=name, disabled=True)
        st.number_input("Age", value=int(age), disabled=True)
        st.text_input("Gender", value=gender, disabled=True)

    with col2:
        st.number_input("Weight (kg)", value=float(weight), disabled=True)
        st.number_input("Height (cm)", value=float(height), disabled=True)

    st.write("")
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

    if st.button(
        "Next ➜",
        key="next_step1",
        use_container_width=True
    ):

        st.session_state.patient["name"] = name
        st.session_state.patient["age"] = age
        st.session_state.patient["gender"] = gender
        st.session_state.patient["weight"] = weight
        st.session_state.patient["height"] = height
        if st.button(get_text(lang, "next"), use_container_width=True):

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

    st.write("")
    c1, c2 = st.columns(2)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(get_text(lang, "back"), use_container_width=True):

         if st.button(
            "⬅ Back",
            key="back_step2",
            use_container_width=True
        ):
            st.session_state.step = 1
            st.rerun()

    with col2:

        if st.button(
            "Next ➜",
            key="next_step2",
            use_container_width=True
        ):
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

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(get_text(lang, "back"), use_container_width=True):

         if st.button(
            "⬅ Back",
            key="back_step3",
            use_container_width=True
        ):
            st.session_state.step = 2
            st.rerun()

    with col2:

        if st.button(
            "🤖 Analyze with AI",
            key="analyze_ai",
            use_container_width=True
        ):
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

    input_data = pd.DataFrame(
        [[
            patient["pregnancies"],
            patient["glucose"],
            patient["blood_pressure"],
            patient["skin_thickness"],
            patient["insulin"],
            patient["bmi"],
            patient["pedigree"],
            patient["age"]
        ]],
        columns=[
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ]
    )

    ai_loading()

    prediction = model.predict(input_data)[0]

    try:
        probability = model.predict_proba(input_data)[0][1]
    except Exception:
        probability = 0

    patient["prediction"] = int(prediction)
    patient["probability"] = float(probability)

    if not st.session_state.saved:

        patient["user_id"] = st.session_state.user["id"]

        save_patient(patient)

        st.session_state.saved = True

    st.success("Analysis Completed Successfully ✅")

    ai_gauge(probability)

    st.write("")
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

    result_card(
        prediction,
        probability
    )

    st.write("")

    recommendation(prediction)

    st.write("")

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

    st.divider()

    st.subheader("📄 Medical Report")
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

            "⬇ Download PDF Report",
            label=get_text(lang, "download_pdf_report_button"),

            data=pdf,

            file_name=pdf_file,

            mime="application/pdf",

            use_container_width=True

        )

    st.write("")


    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(

            "⬅ Back",

            key="back_step4",

            use_container_width=True

        ):
            col1, col2 = st.columns(2)

    with col1:

        if st.button(get_text(lang, "back"), use_container_width=True):

            st.session_state.step = 3

            st.rerun()

    with col2:

        if st.button(

            "🔄 New Assessment",

            key="new_assessment",

            use_container_width=True

        ):

            st.session_state.step = 1
            st.session_state.patient = {}
            st.session_state.saved = False

            st.rerun()

# ==========================================
# FOOTER
# ==========================================
        if st.button(get_text(lang, "new_assessment_button"), use_container_width=True):

            st.session_state.step = 1
            st.session_state.patient = {}
            if "saved" in st.session_state:
                del st.session_state.saved

            st.rerun()

    close_card()

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