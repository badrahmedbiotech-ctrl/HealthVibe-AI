import streamlit as st
import joblib
import pandas as pd

from components.auth_guard import require_patient
require_patient()

from components.database import (
    get_profile,
    create_tables,
    save_assessment,
    save_diabetes
)

from components.branding import *
from components.colors import *

from utils.navigation import sidebar
from components.stepper import stepper
from components.patient_summary import patient_summary
from components.ai_gauge import ai_gauge
from components.loading_animation import ai_loading
from components.pdf_report import create_pdf

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩸",
    layout="wide"
)

import translation
translation.init()
t = translation.t

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================
# LOGIN CHECK
# ==========================================

if "user" not in st.session_state:
    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.user

profile = get_profile(user["id"])

if profile is None:
    st.warning(t("Please complete your profile first."))
    st.switch_page("pages/Profile.py")
    st.stop()

# ==========================================
# MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("models/diabetes_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"{t('Model Loading Error: ')}{e}")
    st.stop()

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

patient = st.session_state.patient

# ==========================================
# HERO
# ==========================================

progress = (st.session_state.step / 4) * 100

st.markdown(f"""
<div class="hero">

<h1>🩸 {t("Diabetes Prediction")}</h1>

<p>{t("AI Clinical Decision Support System")}</p>

<div style="margin-top:20px;height:10px;background:#1E293B;border-radius:20px;overflow:hidden;">

<div style="
width:{progress}%;
height:100%;
background:linear-gradient(90deg,#00C2FF,#2563EB);
">
</div>

</div>

<p style="margin-top:10px;">
{t("Step")} {st.session_state.step} / 4
</p>

</div>
""", unsafe_allow_html=True)

stepper(st.session_state.step)

st.write("")

# ==========================================
# STEP 1
# ==========================================

if st.session_state.step == 1:

    st.subheader(t("👤 Patient Information"))

    name = profile["full_name"] or ""
    age = profile["age"] or 20
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70.0
    height = profile["height"] or 170.0

    st.success(t("Patient information loaded successfully."))

    c1, c2, c3 = st.columns(3)

    c1.metric(t("Age"), age)
    c2.metric(t("Weight"), f"{weight} kg")
    c3.metric(t("Height"), f"{height} cm")

    st.text_input(t("Full Name"), value=name, disabled=True)
    st.text_input(t("Gender"), value=t(gender), disabled=True)

    if st.button(t("Next ➜"), width="stretch"):

        patient["name"] = name
        patient["age"] = age
        patient["gender"] = gender
        patient["weight"] = weight
        patient["height"] = height

        st.session_state.step = 2
        st.rerun()

# ==========================================
# STEP 2
# ==========================================

elif st.session_state.step == 2:

    st.subheader(t("🩺 Medical Information"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Female Only
    if patient["gender"] == "Female":

        pregnancies = st.number_input(
            t("Pregnancies"),
            min_value=0,
            max_value=20,
            value=patient.get("pregnancies", 0)
        )

    else:

        pregnancies = 0

    glucose = st.number_input(
        t("Glucose"),
        min_value=50,
        max_value=300,
        value=patient.get("glucose", 120)
    )

    blood_pressure = st.number_input(
        t("Blood Pressure"),
        min_value=40,
        max_value=200,
        value=patient.get("blood_pressure", 70)
    )

    insulin = st.number_input(
        t("Insulin"),
        min_value=0,
        max_value=900,
        value=patient.get("insulin", 80)
    )

    patient["pregnancies"] = pregnancies
    patient["glucose"] = glucose
    patient["blood_pressure"] = blood_pressure
    patient["insulin"] = insulin

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            t("⬅ Back"),
            key="back_step2",
            width="stretch"
        ):

            st.session_state.step = 1
            st.rerun()

    with col2:

        if st.button(
            t("Next ➜"),
            key="next_step2",
            width="stretch"
        ):

            st.session_state.step = 3
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)        

# ==========================================
# STEP 3
# ==========================================

elif st.session_state.step == 3:

    st.subheader(t("📋 Clinical Measurements"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    bmi = st.number_input(
        t("BMI"),
        min_value=10.0,
        max_value=80.0,
        value=float(patient.get("bmi", 25.0)),
        step=0.1
    )

    skin = st.number_input(
        t("Skin Thickness"),
        min_value=0,
        max_value=100,
        value=int(patient.get("skin", 20))
    )

    dpf = st.number_input(
        t("Diabetes Pedigree Function"),
        min_value=0.0,
        max_value=3.0,
        value=float(patient.get("dpf", 0.5)),
        step=0.01
    )

    patient["bmi"] = bmi
    patient["skin"] = skin
    patient["dpf"] = dpf

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            t("⬅ Back"),
            key="back_step3",
            width="stretch"
        ):
            st.session_state.step = 2
            st.rerun()

    with col2:

     if st.button(
        t("🧠 Predict"),
        key="predict_btn",
        width="stretch"
    ):

        ai_loading()

        input_data = pd.DataFrame([{
            "Pregnancies": patient["pregnancies"],
            "Glucose": patient["glucose"],
            "BloodPressure": patient["blood_pressure"],
            "SkinThickness": patient["skin"],
            "Insulin": patient["insulin"],
            "BMI": patient["bmi"],
            "DiabetesPedigreeFunction": patient["dpf"],
            "Age": patient["age"]
        }])

        try:
            prediction = model.predict(input_data)[0]

            if hasattr(model, "predict_proba"):
                probability = float(model.predict_proba(input_data)[0][1])
            else:
                probability = 1.0 if prediction == 1 else 0.0

            patient["prediction"] = int(prediction)
            patient["probability"] = probability

        except Exception as e:
            st.error(f"{t('Prediction Error : ')}{e}")
            st.stop()

        st.session_state.step = 4
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4
# ==========================================

elif st.session_state.step == 4:

    st.subheader(t("📊 AI Prediction Result"))

    prediction = patient.get("prediction", 0)

    if prediction == 1:

        risk = 92
        result = t("High Risk")
        color = "#EF4444"

    else:

        risk = 8
        result = t("Low Risk")
        color = "#22C55E"

    ai_gauge(risk)

    st.markdown(f"""
    <div class="card">

    <h2 style="color:{color};">
    {result}
    </h2>

    <p>
    {t("AI Prediction Completed Successfully")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    patient_summary(patient)

    st.write("")

    col1, col2, col3 = st.columns(3)

    # ==========================
    # BACK
    # ==========================

    with col1:

        if st.button(
            t("⬅ Back"),
            width="stretch"
        ):

            st.session_state.step = 3
            st.rerun()

    # ==========================
    # SAVE
    # ==========================

    with col2:

        if st.button(
            t("💾 Save Result"),
            width="stretch"
        ):

            try:

                assessment_id = save_assessment(
                    user["id"],
                   "Diabetes",
                    prediction,
                    patient.get("probability", 0)
                )

                patient["prediction"] = prediction

                save_diabetes(
                    assessment_id,
                    patient
                )

                st.success(t("Saved Successfully ✅"))

            except Exception as e:

                st.error(f"{t('Database Error : ')}{e}")

    # ==========================
    # PDF
    # ==========================

    with col3:

        try:

            pdf = create_pdf(
                "Diabetes Report",
                patient,
                prediction
            )

            st.download_button(
                t("📄 Download PDF"),
                pdf,
                "Diabetes_Report.pdf",
                mime="application/pdf",
                width="stretch"
            )

        except Exception as e:

            st.error(f"{t('PDF Error : ')}{e}")

    st.write("")

    if st.button(
        t("🏠 Back To Dashboard"),
        width="stretch"
    ):

        st.session_state.step = 1
        st.switch_page("pages/Dashboard.py")