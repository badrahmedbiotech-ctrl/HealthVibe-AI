import streamlit as st
import joblib
import pandas as pd

from components.branding import *
from components.colors import *

from components.auth_guard import require_patient
require_patient()

from components.database import (
    get_profile,
    save_assessment,
    save_obesity
)

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
    page_title="Obesity Prediction",
    page_icon="⚖️",
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

model = joblib.load("models/obesity_model.pkl")

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

st.markdown(
    f"""
<div class="hero">

<h1>⚖️ {t("Obesity Prediction")}</h1>

<p>
{t("Complete the following assessment to estimate obesity risk using AI.")}
</p>

</div>

""",
    unsafe_allow_html=True
)

stepper(st.session_state.step)

st.write("")

# ==========================================
# STEP 1
# ==========================================

if st.session_state.step == 1:

    st.subheader(t("👤 Patient Information"))

    # Load from profile
    name = profile["full_name"] or ""
    age = profile["age"] or 25
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70
    height = profile["height"] or 170

    st.success(
        t("✅ Patient information loaded from your profile.")
    )

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

        st.text_input(
            t("Gender"),
            value=t(gender),
            disabled=True
        )

    with col2:
        height = st.number_input(
            t("Height (cm)"),
            min_value=100.0,
            max_value=250.0,
            value=float(height),
            step=1.0
        )

        weight = st.number_input(
            t("Weight (kg)"),
            min_value=20,
            max_value=250,
            value=int(weight)
        )

    bmi = weight / ((height / 100) ** 2)

    st.metric(
        t("BMI"),
        round(bmi, 2)
    )

    patient["name"] = name
    patient["gender"] = gender
    patient["age"] = int(age)
    patient["height"] = float(height)
    patient["weight"] = int(weight)
    patient["bmi"] = round(bmi, 2)

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
            width="stretch",
            key="obesity_step1"
        ):
            st.session_state.step = 2
            st.rerun()

# ==========================================
# STEP 2
# ==========================================

elif st.session_state.step == 2:

    st.subheader(t("🥗 Lifestyle Information"))

    col1, col2 = st.columns(2)

    with col1:

        family_history = st.selectbox(
            t("Family History of Overweight"),
            ["no", "yes"],
            index=1 if patient.get("family_history", "no") == "yes" else 0,
            format_func=t
        )

        smoke = st.selectbox(
            t("Smoking"),
            ["no", "yes"],
            index=1 if patient.get("smoke", "no") == "yes" else 0,
            format_func=t
        )

        high_calorie = st.selectbox(
            t("Frequent High Calorie Food"),
            ["no", "yes"],
            index=1 if patient.get("high_calorie", "no") == "yes" else 0,
            format_func=t
        )

        vegetables = st.slider(
            t("Vegetable Consumption (1-3)"),
            1, 3,
            int(patient.get("vegetables", 2))
        )

        meals = st.slider(
            t("Main Meals Per Day (1-4)"),
            1, 4,
            int(patient.get("meals", 3))
        )

    with col2:

        water = st.slider(
            t("Daily Water Intake (1-3)"),
            1.0, 3.0,
            float(patient.get("water", 2.0))
        )

        activity = st.slider(
            t("Physical Activity (0-3)"),
            0.0, 3.0,
            float(patient.get("activity", 1.0))
        )

        technology = st.slider(
            t("Technology Usage (0-2)"),
            0.0, 2.0,
            float(patient.get("technology", 1.0))
        )

        alcohol = st.selectbox(
            t("Alcohol Consumption"),
            ["no", "Sometimes", "Frequently"],
            index=["no", "Sometimes", "Frequently"].index(
                patient.get("alcohol", "no")
            ),
            format_func=t
        )

        transport = st.selectbox(
            t("Transportation"),
            [
                "Walking",
                "Bike",
                "Motorbike",
                "Automobile",
                "Public_Transportation"
            ],
            index=[
                "Walking",
                "Bike",
                "Motorbike",
                "Automobile",
                "Public_Transportation"
            ].index(
                patient.get("transport", "Walking")
            ),
            format_func=t
        )

    patient["family_history"] = family_history
    patient["smoke"] = smoke
    patient["high_calorie"] = high_calorie
    patient["vegetables"] = vegetables
    patient["meals"] = meals
    patient["water"] = water
    patient["activity"] = activity
    patient["technology"] = technology
    patient["alcohol"] = alcohol
    patient["transport"] = transport

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            t("⬅ Back"),
            width="stretch",
            key="obesity_step2_back"
        ):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button(
            t("Next ➜"),
            width="stretch",
            key="obesity_step2_next"
        ):
            st.session_state.step = 3
            st.rerun()

# ==========================================
# STEP 3
# ==========================================

elif st.session_state.step == 3:

    st.subheader(t("🤖 AI Analysis"))

    patient_summary(patient)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            t("⬅ Back"),
            width="stretch",
            key="obesity_step3_back"
        ):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button(
            t("🤖 Predict with AI"),
            width="stretch",
            key="obesity_predict"
        ):

            ai_loading()

            gender_map = {
                "Male": 0,
                "Female": 1
            }

            yes_no_map = {
                "no": 0,
                "yes": 1
            }

            alcohol_map = {
                "no": 0,
                "Sometimes": 1,
                "Frequently": 2
            }

            transport_map = {
                "Walking": 0,
                "Bike": 1,
                "Motorbike": 2,
                "Automobile": 3,
                "Public_Transportation": 4
            }

            # Prepare input data exactly as model expects
            input_data = pd.DataFrame([{
                "Gender": gender_map[patient["gender"]],
                "Age": patient["age"],
                "Height": patient["height"] / 100,  # Convert cm to meters
                "Weight": patient["weight"],
                "Family history with overweight": yes_no_map[patient["family_history"]],
                "Frequent consumption of high-caloric food": yes_no_map[patient["high_calorie"]],
                "Frequency of vegetable consumption": patient["vegetables"],
                "Number of main meals the person eats per day": patient["meals"],
                "Consumption of food between meals": 1,
                "SMOKE": yes_no_map[patient["smoke"]],
                "Daily water consumption": patient["water"],
                "Whether the person takes calorie supplements": 0,
                "Physical activity frequency": patient["activity"],
                "Time spent using technology": patient["technology"],
                "Alcohol consumption": alcohol_map[patient["alcohol"]],
                "Means of transportation used": transport_map[patient["transport"]]
            }])

            try:
                prediction = model.predict(input_data)[0]

                try:
                    # Get probability array and find the max confidence
                    proba_array = model.predict_proba(input_data)[0]
                    # For multi-class, we take the highest probability
                    probability = float(proba_array.max())
                    # Ensure it's between 0-1
                    if probability > 1:
                        probability = probability / 100
                except Exception:
                    probability = 0.5

            except Exception as e:
                st.error(f"{t('Prediction Error')}: {e}")
                st.stop()

            # ✅ Obesity categories (0-6)
            obesity_labels = {
                0: "Insufficient Weight",
                1: "Normal Weight",
                2: "Overweight Level I",
                3: "Overweight Level II",
                4: "Obesity Type I",
                5: "Obesity Type II",
                6: "Obesity Type III"
            }

            patient["prediction"] = int(prediction)
            patient["prediction_text"] = obesity_labels[int(prediction)]
            patient["probability"] = probability

            st.session_state.step = 4
            st.rerun()

# ==========================================
# STEP 4
# ==========================================

elif st.session_state.step == 4:

    st.subheader(t("📊 AI Prediction Result"))

    ai_loading()

    prediction = int(patient.get("prediction", 0))
    result = patient.get("prediction_text", "Unknown")
    probability = patient.get("probability", 0.0)
    
    # Ensure probability is 0-1
    if probability > 1:
        probability = probability / 100
    
    risk = round(probability * 100, 1)

    # ✅ Color based on obesity classification
    obesity_labels = {
        0: "Insufficient Weight",
        1: "Normal Weight",
        2: "Overweight Level I",
        3: "Overweight Level II",
        4: "Obesity Type I",
        5: "Obesity Type II",
        6: "Obesity Type III"
    }

    result = obesity_labels.get(prediction, "Unknown")
    patient["prediction_text"] = result

    # Color logic based on category
    if prediction <= 1:
        color = "#22C55E"  # Green
    elif prediction <= 3:
        color = "#F59E0B"  # Orange
    else:
        color = "#EF4444"  # Red

    st.success(t("Analysis Completed Successfully ✅"))

    st.balloons()

    ai_gauge(risk)

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
        t("Height (cm)"): patient["height"],
        t("BMI"): patient["bmi"],
        t("Prediction"): result,
        t("Confidence"): f"{risk}%"
    })

    st.divider()

    # Save to Database
    if not st.session_state.saved:

        try:
            assessment_id = save_assessment(
                user["id"],
                "Obesity",
                result,
                risk
            )

            obesity_data = {
                "name": patient.get("name"),
                "gender": patient.get("gender"),
                "age": patient.get("age"),
                "height": patient.get("height"),
                "weight": patient.get("weight"),
                "bmi": patient.get("bmi"),
                "family_history": patient.get("family_history"),
                "smoke": patient.get("smoke"),
                "high_calorie": patient.get("high_calorie"),
                "vegetables": patient.get("vegetables"),
                "meals": patient.get("meals"),
                "water": patient.get("water"),
                "activity": patient.get("activity"),
                "technology": patient.get("technology"),
                "alcohol": patient.get("alcohol"),
                "transport": patient.get("transport")
            }

            save_obesity(assessment_id, obesity_data)
            st.session_state.saved = True

        except Exception as e:
            st.error(f"{t('Database Error')}: {e}")

    st.divider()

    # PDF Download
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
            key="obesity_back_result"
        ):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button(
            t("🔄 New Assessment"),
            width="stretch",
            key="obesity_new"
        ):
            st.session_state.step = 1
            st.session_state.patient = {}
            st.session_state.saved = False
            st.rerun()