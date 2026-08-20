import streamlit as st
import pandas as pd
import joblib

from components.auth_guard import require_patient
require_patient()

from components.database import (
    get_profile,
    create_tables,
    save_assessment,
    save_lipid
)
from components.branding import *
from components.colors import *
from utils.navigation import sidebar
from components.stepper import stepper
from components.patient_summary import patient_summary
from components.ai_gauge import ai_gauge
from components.loading_animation import ai_loading
from components.pdf_report import create_pdf

import translation
translation.init()
t = translation.t

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Lipid Risk Prediction",
    page_icon="🫀",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==================================================
# LOGIN
# ==================================================

if "user" not in st.session_state:
    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.user

profile = get_profile(user["id"])

if profile is None:
    st.warning(t("Please complete your profile first."))
    st.switch_page("pages/Profile.py")
    st.stop()

# ==================================================
# LOAD MODEL
# ==================================================

st.cache_resource
def load_model():
    return joblib.load("models/lipid_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"{t('Model Loading Error')}: {e}")
    st.stop()

create_tables()

# ==================================================
# SESSION (namespaced to this page so it never
# collides with Diabetes / Obesity session state)
# ==================================================

if "lipid_step" not in st.session_state:
    st.session_state.lipid_step = 1

if "lipid_patient" not in st.session_state:
    st.session_state.lipid_patient = {}

if "lipid_saved" not in st.session_state:
    st.session_state.lipid_saved = False

patient = st.session_state.lipid_patient

# ==================================================
# HERO
# ==================================================

st.markdown(f"""
<div class="hero">

<h1>🫀 {t("Lipid Risk Prediction")}</h1>

<p>{t("AI Clinical Decision Support System")}</p>

</div>
""", unsafe_allow_html=True)

stepper(st.session_state.lipid_step)

st.write("")

# ==================================================
# STEP 1
# ==================================================

if st.session_state.lipid_step == 1:

    st.subheader(t("👤 Patient Information"))

    # Load from profile
    name = profile["full_name"] or ""
    age = profile["age"] or 20
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70
    height = profile["height"] or 170

    st.success(t("✅ Patient information loaded from your profile."))

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            t("Full Name"),
            value=name,
            disabled=True
        )

        st.number_input(
            t("Age"),
            value=int(age),
            disabled=True
        )

    with col2:
        st.text_input(
            t("Gender"),
            value=t(gender),
            disabled=True
        )

        st.metric(t("Weight"), f"{weight} kg")
        st.metric(t("Height"), f"{height} cm")

    bmi = round(weight / ((height / 100) ** 2), 2)
    st.metric(t("BMI"), bmi)

    patient["name"] = name
    patient["age"] = int(age)
    patient["gender"] = gender
    patient["weight"] = int(weight)
    patient["height"] = float(height)
    patient["bmi"] = bmi

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            t("⬅ Back"),
            disabled=True,
            width="stretch"
        )

    with col2:
        if st.button(
            t("Next ➜"),
            key="lipid_step1_next",
            width="stretch"
        ):
            st.session_state.lipid_step = 2
            st.rerun()

# ==================================================
# STEP 2
# ==================================================

elif st.session_state.lipid_step == 2:

    st.subheader(t("🩺 Clinical Information"))

    col1, col2 = st.columns(2)

    with col1:

        total_cholesterol = st.number_input(
            t("Total Cholesterol (mg/dL)"),
            min_value=50,
            max_value=500,
            value=int(patient.get("cholesterol_total", 180))
        )

        ldl = st.number_input(
            t("LDL Cholesterol (mg/dL)"),
            min_value=20,
            max_value=300,
            value=int(patient.get("ldl", 100))
        )

        hdl = st.number_input(
            t("HDL Cholesterol (mg/dL)"),
            min_value=10,
            max_value=120,
            value=int(patient.get("hdl", 50))
        )

        triglycerides = st.number_input(
            t("Triglycerides (mg/dL)"),
            min_value=20,
            max_value=600,
            value=int(patient.get("triglycerides", 150))
        )

    with col2:

        fasting_bs = st.number_input(
            t("Fasting Blood Sugar (mg/dL)"),
            min_value=50,
            max_value=300,
            value=int(patient.get("fasting_blood_sugar", 90))
        )

        hba1c = st.number_input(
            t("HbA1c (%)"),
            min_value=3.0,
            max_value=15.0,
            value=float(patient.get("hba1c", 5.5)),
            step=0.1
        )

        systolic = st.number_input(
            t("Systolic Blood Pressure (mmHg)"),
            min_value=70,
            max_value=250,
            value=int(patient.get("resting_bp_systolic", 120))
        )

        smoker = st.selectbox(
            t("Smoking Status"),
            ["No", "Yes"],
            index=0 if patient.get("smoker_status", "No") == "No" else 1,
            format_func=t
        )

    patient["cholesterol_total"] = total_cholesterol
    patient["ldl"] = ldl
    patient["hdl"] = hdl
    patient["triglycerides"] = triglycerides
    patient["fasting_blood_sugar"] = fasting_bs
    patient["hba1c"] = hba1c
    patient["resting_bp_systolic"] = systolic
    patient["smoker_status"] = smoker

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            t("⬅ Back"),
            key="lipid_step2_back",
            width="stretch"
        ):
            st.session_state.lipid_step = 1
            st.rerun()

    with col2:
        if st.button(
            t("Next ➜"),
            key="lipid_step2_next",
            width="stretch"
        ):
            st.session_state.lipid_step = 3
            st.rerun()

# ==================================================
# STEP 3
# ==================================================

elif st.session_state.lipid_step == 3:

    st.subheader(t("🧠 AI Analysis"))

    patient_summary(patient)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            t("⬅ Back"),
            key="lipid_step3_back",
            width="stretch"
        ):
            st.session_state.lipid_step = 2
            st.rerun()

    with col2:
        if st.button(
            t("🤖 Predict "),
            key="lipid_predict",
            width="stretch"
        ):

            ai_loading()

            sex = 1 if patient["gender"] == "Male" else 0
            smoker = 1 if patient["smoker_status"] == "Yes" else 0

            input_data = pd.DataFrame([{
                "age": patient["age"],
                "sex": sex,
                "cholesterol_total": patient["cholesterol_total"],
                "ldl": patient["ldl"],
                "hdl": patient["hdl"],
                "triglycerides": patient["triglycerides"],
                "fasting_blood_sugar": patient["fasting_blood_sugar"],
                "hba1c": patient["hba1c"],
                "bmi": patient["bmi"],
                "resting_bp_systolic": patient["resting_bp_systolic"],
                "smoker_status": smoker
            }])

            try:
                prediction = model.predict(input_data)[0]

                try:
                    # Get probability array
                    proba_array = model.predict_proba(input_data)[0]
                    # Take the probability for the predicted class
                    probability = float(proba_array[int(prediction)])
                    
                    # ✅ Keep normalizing until it's in 0-1 range
                    while probability > 1:
                        probability = probability / 100
                    
                    # Ensure it's between 0-1 (safety check)
                    probability = max(0.0, min(probability, 1.0))
                    
                except Exception:
                    probability = 0.5

            except Exception as e:
                st.error(f"{t('Prediction Error')}: {e}")
                st.stop()

            labels = {
                0: "Low Risk",
                1: "Borderline Risk",
                2: "High Risk"
            }

            patient["prediction"] = int(prediction)
            patient["prediction_text"] = labels.get(int(prediction), "Unknown")
            patient["probability"] = probability

            st.session_state.lipid_step = 4
            st.rerun()

# ==================================================
# STEP 4
# ==================================================

elif st.session_state.lipid_step == 4:

    st.subheader(t("📊 AI Prediction Result"))

    ai_loading()

    prediction = int(patient.get("prediction", 0))
    probability = patient.get("probability", 0.0)

    # ✅ Keep normalizing until it's in 0-1 range
    while probability > 1:
        probability = probability / 100
    
    # Ensure it's between 0-1 (safety check)
    probability = max(0.0, min(probability, 1.0))
    risk = round(probability * 100, 1)

    labels = {
        0: "Low Risk",
        1: "Borderline Risk",
        2: "High Risk"
    }

    result = labels.get(prediction, "Unknown")
    patient["prediction_text"] = result

    # Color mapping based on risk level
    if prediction == 0:
        color = "#22C55E"  # Green - Low Risk
    elif prediction == 1:
        color = "#F59E0B"  # Orange - Borderline
    else:
        color = "#EF4444"  # Red - High Risk

    st.success(t("Analysis Completed Successfully ✅"))

    st.balloons()

    # Pass probability (0-1) to ai_gauge, not risk (0-100)
    ai_gauge(probability)

    st.markdown(f"""
    <div class="card">
    <h2 style="color:{color};">
    {t(result)}
    </h2>
    <p>
    {t("AI Prediction Completed Successfully")}
    </p>
    </div>
    """, unsafe_allow_html=True)

    patient_summary({
        t("Full Name"): patient["name"],
        t("Age"): patient["age"],
        t("Gender"): patient["gender"],
        t("Weight (kg)"): patient["weight"],
        t("BMI"): patient["bmi"],
        t("Total Cholesterol"): patient["cholesterol_total"],
        t("LDL"): patient["ldl"],
        t("HDL"): patient["hdl"],
        t("Prediction"): result,
        t("Confidence"): f"{risk}%"
    })

    st.write("")

    # ==================================================
    # SAVE TO DATABASE (Automatic)
    # ==================================================

    if not st.session_state.lipid_saved:

        try:
            assessment_id = save_assessment(
                user["id"],
                "Lipid",
                result,
                risk
            )

            # Prepare only required fields for lipid table
            lipid_data = {
                "name": patient.get("name"),
                "gender": patient.get("gender"),
                "age": patient.get("age"),
                "weight": patient.get("weight"),
                "height": patient.get("height"),
                "bmi": patient.get("bmi"),
                "cholesterol_total": patient.get("cholesterol_total"),
                "ldl": patient.get("ldl"),
                "hdl": patient.get("hdl"),
                "triglycerides": patient.get("triglycerides"),
                "fasting_blood_sugar": patient.get("fasting_blood_sugar"),
                "hba1c": patient.get("hba1c"),
                "resting_bp_systolic": patient.get("resting_bp_systolic"),
                "smoker_status": patient.get("smoker_status")
            }

            save_lipid(assessment_id, lipid_data)
            st.session_state.lipid_saved = True

        except Exception as e:
            st.error(f"{t('Database Error')}: {e}")

    st.divider()

    # ==================================================
    # PDF DOWNLOAD (Automatic)
    # ==================================================

    pdf_file = create_pdf(patient)

    with open(pdf_file, "rb") as pdf:
        st.download_button(
            t("⬇ Download PDF Report"),
            pdf,
            file_name=pdf_file,
            mime="application/pdf",
            width="stretch"
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            t("⬅ Back"),
            width="stretch",
            key="lipid_back_result"
        ):
            st.session_state.lipid_step = 3
            st.rerun()

    with col2:
        if st.button(
            t("🔄 New Assessment"),
            width="stretch",
            key="lipid_new"
        ):
            st.session_state.lipid_step = 1
            st.session_state.lipid_patient = {}
            st.session_state.lipid_saved = False
            st.rerun()