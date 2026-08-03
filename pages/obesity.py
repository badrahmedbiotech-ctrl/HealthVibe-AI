import streamlit as st
import joblib
import pandas as pd


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
    st.warning(translation.t("Please complete your profile first."))
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

patient = st.session_state.patient

# ==========================================
# STEP INDICATOR
# ==========================================

st.title(translation.t("⚖️ Obesity Prediction"))

stepper(st.session_state.step)

# ==========================================
# STEP 1
# ==========================================

if st.session_state.step == 1:

    st.subheader(translation.t("👤 Personal Information"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox(
            translation.t("Gender"),
            ["Male", "Female"],
            index=0 if patient.get("gender", "Male") == "Male" else 1,
            format_func=translation.t
        )

        age = st.number_input(
            translation.t("Age"),
            min_value=1,
            max_value=100,
            value=int(patient.get("age", 25))
        )

    with col2:

        height = st.number_input(
            translation.t("Height (m)"),
            min_value=1.00,
            max_value=2.50,
            value=float(patient.get("height", 1.70)),
            step=0.01
        )

        weight = st.number_input(
            translation.t("Weight (kg)"),
            min_value=20,
            max_value=250,
            value=int(patient.get("weight", 70))
        )

    bmi = weight / (height ** 2)

    st.metric(
        translation.t("BMI"),
        round(bmi, 2)
    )

    patient["gender"] = gender
    patient["age"] = age
    patient["height"] = height
    patient["weight"] = weight
    patient["bmi"] = bmi

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.button(
            translation.t("⬅ Back"),
            disabled=True,
            width="stretch"
        )

    with col2:

        if st.button(
            translation.t("Next ➡"),
            width="stretch"
        ):

            st.session_state.step = 2
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 2
# ==========================================

elif st.session_state.step == 2:

    st.subheader(translation.t("🥗 Lifestyle Information"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        family_history = st.selectbox(
            translation.t("Family History of Overweight"),
            ["no", "yes"],
            index=1 if patient.get("family_history", "no") == "yes" else 0,
            format_func=translation.t
        )

        smoke = st.selectbox(
            translation.t("Smoking"),
            ["no", "yes"],
            index=1 if patient.get("smoke", "no") == "yes" else 0,
            format_func=translation.t
        )

        high_calorie = st.selectbox(
            translation.t("Frequent High Calorie Food"),
            ["no", "yes"],
            index=1 if patient.get("high_calorie", "no") == "yes" else 0,
            format_func=translation.t
        )

        vegetables = st.slider(
            translation.t("Vegetable Consumption"),
            1, 3,
            int(patient.get("vegetables", 2))
        )

        meals = st.slider(
            translation.t("Main Meals Per Day"),
            1, 4,
            int(patient.get("meals", 3))
        )

    with col2:

        water = st.slider(
            translation.t("Daily Water Intake"),
            1.0, 3.0,
            float(patient.get("water", 2.0))
        )

        activity = st.slider(
            translation.t("Physical Activity"),
            0.0, 3.0,
            float(patient.get("activity", 1.0))
        )

        technology = st.slider(
            translation.t("Technology Usage"),
            0.0, 2.0,
            float(patient.get("technology", 1.0))
        )

        alcohol = st.selectbox(
            translation.t("Alcohol Consumption"),
            ["no", "Sometimes", "Frequently"],
            index=["no", "Sometimes", "Frequently"].index(
                patient.get("alcohol", "no")
            ),
            format_func=translation.t
        )

        transport = st.selectbox(
            translation.t("Transportation"),
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
            format_func=translation.t
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
            translation.t("⬅ Back"),
            width="stretch"
        ):
            st.session_state.step = 1
            st.rerun()

    with col2:

        if st.button(
            translation.t("Next ➡"),
            width="stretch"
        ):
            st.session_state.step = 3
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 3
# ==========================================

elif st.session_state.step == 3:

    st.subheader(translation.t("🧠 AI Prediction"))

    st.markdown('<div class="card">', unsafe_allow_html=True)

    patient_summary(patient)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            translation.t("⬅ Back"),
            key="back_step3",
            width="stretch"
        ):

            st.session_state.step = 2
            st.rerun()

    with col2:

        if st.button(
            translation.t("🧠 Predict"),
            key="predict_btn",
            width="stretch"
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

            snacks_map = {
                "no": 0,
                "Sometimes": 1,
                "Frequently": 2,
                "Always": 3
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

            input_data = pd.DataFrame([{

                "Gender": gender_map[patient["gender"]],
                "Age": patient["age"],
                "Height": patient["height"],
                "Weight": patient["weight"],
                "Family history with overweight": yes_no_map[patient["family_history"]],
                "Frequent consumption of high-caloric food": yes_no_map[patient["high_calorie"]],
                "Frequency of vegetable consumption": patient["vegetables"],
                "Number of main meals the person eats per day": patient["meals"],

                # مؤقتًا لحد ما نضيفها في Step 2
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
                    probability = float(
                        model.predict_proba(input_data)[0].max()
                    )
                except:
                    probability = 1.0 if prediction else 0.0

            except Exception as e:

                st.error(f"{translation.t('Prediction Error : ')}{e}")
                st.stop()

            labels = {
                 0: "Insufficient Weight",
                 1: "Normal Weight",
                 2: "Overweight Level I",
                 3: "Overweight Level II",
                 4: "Obesity Type I",
                 5: "Obesity Type II",
                 6: "Obesity Type III"
            }

            patient["prediction"] = int(prediction)
            patient["prediction_text"] = labels[int(prediction)]
            patient["probability"] = probability

            st.session_state.step = 4
            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4
# ==========================================

elif st.session_state.step == 4:

    st.subheader(translation.t("📊 AI Prediction Result"))

    prediction = int(patient.get("prediction", 0))
    result = patient.get("prediction_text", "Unknown")

    probability = patient.get("probability", 0)

    risk = int(probability * 100)

    if prediction <= 1:
        color = "#22C55E"
    elif prediction <= 3:
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

    # ==========================
    # BACK
    # ==========================

    with col1:

        if st.button(
            translation.t("⬅ Back"),
            width="stretch"
        ):

            st.session_state.step = 3
            st.rerun()

    # ==========================
    # SAVE
    # ==========================

    with col2:

        
        if st.button(translation.t("💾 Save Result"), width="stretch"):

            try:

                labels = {
                    0: "Insufficient Weight",
                    1: "Normal Weight",
                    2: "Overweight Level I",
                    3: "Overweight Level II",
                    4: "Obesity Type I",
                    5: "Obesity Type II",
                    6: "Obesity Type III"
                }
                prediction_text = labels.get(prediction, "Unknown")

                assessment_id = save_assessment(

                   user["id"],
                   "Obesity",
                   prediction_text,
                   probability * 100

                )

                save_obesity(

                    assessment_id,
                    patient

                )

                st.success(translation.t("Saved Successfully ✅"))

            except Exception as e:

                st.error(f"{translation.t('Database Error : ')}{e}")

    # ==========================
    # PDF
    # ==========================

    with col3:

     if st.button(translation.t("📄 Download Report"), width="stretch"):
 
        pdf_patient = patient.copy()

        pdf_patient["prediction"] = result
        pdf_patient["probability"] = probability

        pdf = create_pdf(pdf_patient)

        with open(pdf, "rb") as file:

            st.download_button(
                translation.t("⬇ Download PDF"),
                data=file.read(),
                file_name="Obesity_Report.pdf",
                mime="application/pdf",
                width="stretch"
            )