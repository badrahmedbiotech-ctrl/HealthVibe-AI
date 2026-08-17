import streamlit as st
import pandas as pd
import joblib

from components.auth_guard import require_patient
require_patient()

from components.database import (
    get_profile,
    create_tables,
    save_assessment,
    save_fibrosis
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
    page_title="Respiratory Disease Prediction",
    page_icon="🫁",
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
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("models/respiratory_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"{t('Model Loading Error: ')}{e}")
    st.stop()

dataset = pd.read_csv("dataset/Fibrosis_data.csv")

create_tables()

# ==========================================
# SESSION STATE
# ==========================================

if "step" not in st.session_state:
    st.session_state.step = 1

if "patient" not in st.session_state:
    st.session_state.patient = {}

patient = st.session_state.patient

# ==========================================
# HERO
# ==========================================

progress = (st.session_state.step / 4) * 100

st.markdown(f"""
<div class="hero">

<h1>🫁 {t("Respiratory Disease Prediction")}</h1>

<p>
{t("AI Clinical Decision Support System")}
</p>

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
    age = profile["age"] or 30
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70.0
    height = profile["height"] or 170.0

    bmi = round(weight / ((height / 100) ** 2), 1)

    st.success(t("Patient information loaded successfully."))

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(t("Age"), age)
    c2.metric(t("Weight"), f"{weight} kg")
    c3.metric(t("Height"), f"{height} cm")
    c4.metric(t("BMI"), bmi)

    st.text_input(
        t("Full Name"),
        value=name,
        disabled=True
    )

    st.text_input(
        t("Gender"),
        value=gender,
        disabled=True
    )

    if st.button(
        t("Next ➜"),
        key="next_step1",
        width="stretch"
    ):

        patient["name"] = name
        patient["age"] = age
        patient["gender"] = gender
        patient["weight"] = weight
        patient["height"] = height
        patient["bmi"] = bmi

        st.session_state.step = 2
        st.rerun()

# ==========================================
# STEP 2
# ==========================================

elif st.session_state.step == 2:

    st.subheader(t("🩺 Medical Information"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    symptoms = sorted(
        dataset["Symptoms"]
        .dropna()
        .unique()
        .tolist()
    )

    symptom = st.selectbox(
        t("Main Symptom"),
        symptoms,
        index=0
    )

    smoking = st.selectbox(
        t("Smoking Status"),
        [
            t("Never"),
            t("Former"),
            t("Current")
        ]
    )

    exercise = st.selectbox(
        t("Physical Activity"),
        [
            t("Regular"),
            t("Sometimes"),
            t("Rarely")
        ]
    )

    pollution = st.selectbox(
        t("Air Pollution Exposure"),
        [
            t("Low"),
            t("Medium"),
            t("High")
        ]
    )

    chemicals = st.selectbox(
        t("Chemical Exposure"),
        [
            t("No"),
            t("Yes")
        ]
    )

    sleep = st.slider(
        t("Sleep Hours"),
        3,
        12,
        7
    )

    patient["symptom"] = symptom
    patient["smoking"] = smoking
    patient["exercise"] = exercise
    patient["pollution"] = pollution
    patient["chemicals"] = chemicals
    patient["sleep"] = sleep

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

    st.subheader(t("🧠 AI Prediction"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    patient_summary(patient)

    st.divider()

    st.subheader(t("❤️ Vital Signs"))

    col1, col2 = st.columns(2)

    with col1:

        spo2 = st.slider(
            t("SpO₂ (%)"),
            50,
            100,
            patient.get("spo2", 98)
        )

        temperature = st.number_input(
            t("Temperature (°C)"),
            min_value=34.0,
            max_value=42.0,
            value=float(patient.get("temperature", 37.0)),
            step=0.1
        )

    with col2:

        heart_rate = st.number_input(
            t("Heart Rate (bpm)"),
            min_value=30,
            max_value=200,
            value=int(patient.get("heart_rate", 80))
        )

        respiratory_rate = st.number_input(
            t("Respiratory Rate"),
            min_value=5,
            max_value=40,
            value=int(patient.get("respiratory_rate", 18))
        )

    patient["spo2"] = spo2
    patient["temperature"] = temperature
    patient["heart_rate"] = heart_rate
    patient["respiratory_rate"] = respiratory_rate

    # NOTE: the trained model only accepts Symptoms / Age / Sex (the
    # columns it was trained on in Fibrosis_data.csv). Vital signs are
    # still collected and shown/saved/printed in the report, but they are
    # not fed into the model since it was never trained on them.

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

                "Symptoms": patient["symptom"],
                "Age": patient["age"],
                "Sex": patient["gender"].lower()

            }])

            try:

                prediction = model.predict(input_data)[0]

                try:

                    # Confidence of the predicted class, kept on a 0-1
                    # scale (same convention as Hypertension.py) so it
                    # can be reused directly by ai_gauge / save_assessment
                    # / create_pdf without any extra scaling.
                    probability = float(
                        model.predict_proba(input_data)[0].max()
                    )

                except Exception:

                    probability = 1.0

            except Exception as e:

                st.error(f"{t('Prediction Error : ')}{e}")
                st.stop()

            patient["prediction"] = prediction
            patient["prediction_text"] = prediction
            patient["probability"] = probability

            st.session_state.step = 4
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4
# ==========================================

elif st.session_state.step == 4:

    st.subheader(t("📊 AI Prediction Result"))

    prediction = patient.get("prediction_text", "Unknown")

    # probability is always kept on a 0-1 scale here, exactly like
    # Hypertension.py. Never multiply it by 100 before passing it to
    # ai_gauge / save_assessment / create_pdf — only when formatting
    # text for display (probability * 100 for the "%" label).
    probability = float(patient.get("probability", 0))

    ai_gauge(probability)

    st.metric(
        t("AI Confidence"),
        f"{probability * 100:.1f}%"
    )

    result = dataset[
        dataset["Disease"] == prediction
    ]

    treatment = t("Consult your physician.")

    nature = "Unknown"

    if not result.empty:

        if "Treatment" in result.columns:
            treatment = str(result.iloc[0]["Treatment"])

        if "Nature" in result.columns:
            nature = str(result.iloc[0]["Nature"])

    # ==========================
    # COLORS
    # ==========================

    if nature.lower() == "high":

        color = "#EF4444"

    elif nature.lower() == "medium":

        color = "#F59E0B"

    else:

        color = "#22C55E"

    st.markdown(f"""
    <div class="card">

    <h2 style="color:{color};">

    {prediction}

    </h2>

    <p>

    {t("AI Prediction Completed Successfully")}

    </p>

    </div>

    """, unsafe_allow_html=True)

    patient_summary(patient)

    st.divider()

    st.subheader(t("💊 Suggested Treatment"))

    st.info(treatment)

    st.subheader(t("🚨 Disease Severity"))

    if nature.lower() == "high":

        st.error(t("🔴 High"))

    elif nature.lower() == "medium":

        st.warning(t("🟡 Medium"))

    else:

        st.success(t("🟢 Low"))

    st.divider()

    st.subheader(t("⚠ Medical Disclaimer"))

    st.warning(t("""

This AI prediction is intended for screening purposes only.

It is NOT a confirmed medical diagnosis.

Please consult a qualified healthcare professional
for examination, confirmation and treatment.

"""))

    st.write("")

    col1, col2, col3 = st.columns(3)

    # ==========================
    # BACK
    # ==========================

    with col1:

        if st.button(
            t("⬅ Back"),
            key="back_step4",
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
            key="save_fibrosis",
            width="stretch"
        ):

            try:

                # Same call convention as Hypertension.py: probability
                # saved on a 0-1 scale (NOT multiplied by 100), keyword
                # arguments named the same way.
                assessment_id = save_assessment(
                    user_id=user["id"],
                    disease="Respiratory Disease",
                    prediction=str(prediction),
                    probability=float(probability)
                )

                save_fibrosis(
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

        if st.button(
            t("📄 Download Report"),
            key="pdf_respiratory",
            width="stretch"
        ):

            pdf_patient = patient.copy()

            pdf_patient["prediction"] = prediction
            pdf_patient["probability"] = probability

            pdf = create_pdf(pdf_patient)

            with open(pdf, "rb") as file:

                st.download_button(

                    t("⬇ Download PDF"),

                    data=file.read(),

                    file_name="Respiratory_Report.pdf",

                    mime="application/pdf",

                    key="download_pdf"

                )

    st.divider()

    if st.button(

        t("🏠 Back To Dashboard"),

        key="dashboard_btn",

        width="stretch"

    ):

        st.session_state.step = 1
        st.session_state.patient = {}

        st.switch_page("pages/Dashboard.py")

st.divider()

st.warning(t("""
⚠️ **Medical Disclaimer**

This AI prediction is intended only for preliminary screening and educational purposes.

It **does not replace a physician's diagnosis**.

If you have persistent symptoms such as:

• Shortness of breath
• Chest pain
• Persistent cough
• Fever
• Coughing blood

Please consult a pulmonologist or healthcare provider immediately.

Further investigations such as Chest X-ray, CT Scan, Pulmonary Function Test (PFT), blood tests, and clinical examination may be required to confirm the diagnosis.
"""))
st.markdown(
f"""
---
<center>

### 🫁 HealthVibe AI

{t("Respiratory Disease Screening System")}

{t("Developed by ")}**Visionaries**

</center>
""",
unsafe_allow_html=True
)