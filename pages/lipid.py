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

from utils.navigation import sidebar
from components.stepper import stepper
from components.patient_summary import patient_summary
from components.ai_gauge import ai_gauge
from components.loading_animation import ai_loading
from components.pdf_report import create_pdf

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="HealthVibe AI - Lipid",
    page_icon="🫀",
    layout="wide"
)

import translation
translation.init()

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
    st.warning(translation.t("Please complete your profile first."))
    st.switch_page("pages/Profile.py")
    st.stop()

# ==================================================
# LOAD MODEL
# ==================================================

@st.cache_resource
def load_model():
    return joblib.load("models/lipid_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"{translation.t('Model Loading Error: ')}{e}")
    st.stop()

create_tables()

# ==================================================
# SESSION
# ==================================================

if "step" not in st.session_state:
    st.session_state.step = 1

if "patient" not in st.session_state:
    st.session_state.patient = {}

if "saved" not in st.session_state:
    st.session_state.saved = False

patient = st.session_state.patient

# ==================================================
# HERO
# ==================================================

progress = (st.session_state.step / 4) * 100

st.markdown(f"""
<div class="hero">

<h1>🫀 {translation.t("Lipid Risk Prediction")}</h1>

<p>{translation.t("AI Clinical Decision Support System")}</p>

<div style="
margin-top:20px;
height:10px;
background:#1E293B;
border-radius:20px;
overflow:hidden;
">

<div style="
width:{progress}%;
height:100%;
background:linear-gradient(90deg,#00C2FF,#2563EB);
"></div>

</div>

<p style="margin-top:10px;">
{translation.t("Step")} {st.session_state.step} / 4
</p>

</div>
""", unsafe_allow_html=True)

stepper(st.session_state.step)

st.write("")

# ==================================================
# STEP 1
# ==================================================

if st.session_state.step == 1:

    st.subheader(translation.t("👤 Patient Information"))

    name = profile["full_name"] or ""
    age = profile["age"] or 20
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70
    height = profile["height"] or 170

    st.success(translation.t("Patient information loaded successfully."))

    c1, c2, c3 = st.columns(3)

    c1.metric(translation.t("Age"), age)
    c2.metric(translation.t("Weight"), f"{weight} kg")
    c3.metric(translation.t("Height"), f"{height} cm")

    st.text_input(
        translation.t("Full Name"),
        value=name,
        disabled=True
    )

    st.text_input(
        translation.t("Gender"),
        value=gender,
        disabled=True
    )

    if st.button(
        translation.t("Next ➜"),
        key="lipid_next1",
        width="stretch"
    ):

        patient["name"] = name
        patient["age"] = age
        patient["gender"] = gender
        patient["weight"] = weight
        patient["height"] = height

        st.session_state.step = 2
        st.rerun()
# ==================================================
# STEP 2
# ==================================================

elif st.session_state.step == 2:

    st.subheader(translation.t("🩺 Clinical Information"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        total_cholesterol = st.number_input(
            translation.t("Total Cholesterol (mg/dL)"),
            min_value=50,
            max_value=500,
            value=int(patient.get("cholesterol_total", 180))
        )

        ldl = st.number_input(
            translation.t("LDL Cholesterol (mg/dL)"),
            min_value=20,
            max_value=300,
            value=int(patient.get("ldl", 100))
        )

        hdl = st.number_input(
            translation.t("HDL Cholesterol (mg/dL)"),
            min_value=10,
            max_value=120,
            value=int(patient.get("hdl", 50))
        )

        triglycerides = st.number_input(
            translation.t("Triglycerides (mg/dL)"),
            min_value=20,
            max_value=600,
            value=int(patient.get("triglycerides", 150))
        )

    with col2:

        fasting_bs = st.number_input(
            translation.t("Fasting Blood Sugar"),
            min_value=50,
            max_value=300,
            value=int(patient.get("fasting_blood_sugar", 90))
        )

        hba1c = st.number_input(
            translation.t("HbA1c (%)"),
            min_value=3.0,
            max_value=15.0,
            value=float(patient.get("hba1c", 5.5)),
            step=0.1
        )

        systolic = st.number_input(
            translation.t("Systolic Blood Pressure"),
            min_value=70,
            max_value=250,
            value=int(patient.get("resting_bp_systolic", 120))
        )

        smoker = st.selectbox(
            translation.t("Smoking Status"),
            ["No", "Yes"],
            index=0 if patient.get("smoker_status", "No") == "No" else 1
        )

    bmi = round(
        patient["weight"] / ((patient["height"] / 100) ** 2),
        2
    )

    st.metric(translation.t("BMI"), bmi)

    patient["cholesterol_total"] = total_cholesterol
    patient["ldl"] = ldl
    patient["hdl"] = hdl
    patient["triglycerides"] = triglycerides
    patient["fasting_blood_sugar"] = fasting_bs
    patient["hba1c"] = hba1c
    patient["resting_bp_systolic"] = systolic
    patient["smoker_status"] = smoker
    patient["bmi"] = bmi

    st.write("")

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            translation.t("⬅ Back"),
            key="lipid_back2",
            width="stretch"
        ):

            st.session_state.step = 1
            st.rerun()

    with c2:

        if st.button(
            translation.t("Next ➜"),
            key="lipid_next2",
            width="stretch"
        ):

            st.session_state.step = 3
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
# ==================================================
# STEP 3
# ==================================================

elif st.session_state.step == 3:

    st.subheader(translation.t("🧠 AI Prediction"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    patient_summary(patient)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            translation.t("⬅ Back"),
            key="lipid_back3",
            width="stretch"
        ):

            st.session_state.step = 2
            st.rerun()

    with col2:

        if st.button(
            translation.t("🧠 Predict"),
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
                    probability = float(
                        model.predict_proba(input_data)[0].max()
                    )
                except:
                    probability = 1.0

            except Exception as e:

                st.error(f"{translation.t('Prediction Error : ')}{e}")
                st.stop()

            patient["prediction"] = int(prediction)
            patient["probability"] = probability

            labels = {

                0: "Low Risk",
                1: "Borderline Risk",
                2: "High Risk"

            }

            patient["prediction_text"] = labels.get(
                int(prediction),
                "Unknown"
            )

            st.session_state.step = 4
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
# ==================================================
# STEP 4
# ==================================================

elif st.session_state.step == 4:

    st.subheader(translation.t("📊 AI Prediction Result"))

    prediction = int(patient.get("prediction", 0))
    probability = float(patient.get("probability", 0))

    result = patient.get("prediction_text", "Unknown")

    risk = int(probability * 100)

    if prediction == 0:
        color = "#22C55E"

    elif prediction == 1:
        color = "#F59E0B"

    else:
        color = "#EF4444"

    ai_gauge(risk)

    st.markdown(f"""
    <div class="card">

    <h2 style="color:{color};">
    {translation.t(result)}
    </h2>

    <p>
    {translation.t("AI Prediction Completed Successfully")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    patient_summary(patient)

    st.write("")

    col1, col2, col3 = st.columns(3)

    # =====================================
    # BACK
    # =====================================

    with col1:

        if st.button(
            translation.t("⬅ Back"),
            key="lipid_back4",
            width="stretch"
        ):

            st.session_state.step = 3
            st.rerun()

    # =====================================
    # SAVE
    # =====================================

    with col2:

        if st.button(
            translation.t("💾 Save Result"),
            key="lipid_save",
            width="stretch"
        ):

            try:

                assessment_id = save_assessment(

                    user["id"],
                    "Lipid",
                    result,
                    probability * 100

                )

                save_lipid(

                    assessment_id,
                    patient

                )

                st.success(translation.t("Saved Successfully ✅"))

            except Exception as e:

                st.error(f"{translation.t('Database Error : ')}{e}")

    # =====================================
    # PDF
    # =====================================

    with col3:

        if st.button(
            translation.t("📄 Download Report"),
            key="lipid_pdf",
            width="stretch"
        ):

            pdf_patient = patient.copy()

            pdf_patient["prediction"] = result
            pdf_patient["probability"] = probability

            pdf = create_pdf(pdf_patient)

            with open(pdf, "rb") as file:

                st.download_button(

                    translation.t("⬇ Download PDF"),

                    data=file.read(),

                    file_name="Lipid_Report.pdf",

                    mime="application/pdf",

                    key="lipid_download"

                )

    st.divider()

    if st.button(

        translation.t("🏠 Back To Dashboard"),

        key="lipid_dashboard",

        width="stretch"

    ):

        st.session_state.step = 1
        st.session_state.patient = {}
        st.switch_page("pages/Dashboard.py")