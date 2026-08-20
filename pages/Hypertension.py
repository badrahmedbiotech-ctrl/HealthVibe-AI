# ==========================================================
# HEALTHVIBE AI - HYPERTENSION ASSESSMENT
# PART 1 : SETUP + LOGIN + MODEL + SESSION
# ==========================================================


import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

from components.branding import *
from components.colors import *
# ==========================================================
# AUTHENTICATION
# ==========================================================

from components.auth_guard import require_patient

require_patient()


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Hypertension Assessment",
    page_icon="🩸",
    layout="wide"
)

import translation
translation.init()
t = translation.t


# ==========================================================
# LOGIN CHECK
# ==========================================================

if "user" not in st.session_state:
    st.switch_page("pages/Login.py")
    st.stop()


user = st.session_state["user"]


# ==========================================================
# LOAD PROFILE
# ==========================================================

from components.database import get_profile

profile = get_profile(user["id"])


if profile is None:

    st.warning(
        t("Please complete your profile first.")
    )

    st.switch_page(
        "pages/Profile.py"
    )

    st.stop()



# ==========================================================
# COMPONENTS
# ==========================================================

from utils.navigation import sidebar

from components.database import (
    create_tables,
    save_assessment,
    save_hypertension
)

from components.stepper import stepper

from components.result_card import result_card

from components.recommendation import recommendation

from components.patient_summary import patient_summary

from components.ai_gauge import ai_gauge

from components.loading_animation import ai_loading

from components.pdf_report import create_pdf



# ==========================================================
# STYLE
# ==========================================================

with open(
    "style.css",
    encoding="utf-8"
) as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


sidebar()



# ==========================================================
# MODEL
# ==========================================================


MODEL_PATH = "models/hypertension_model.pkl"


@st.cache_resource
def load_model():

    return joblib.load(
        MODEL_PATH
    )



model = load_model()



create_tables()



# ==========================================================
# SESSION STATE
# ==========================================================


if "step" not in st.session_state:

    st.session_state.step = 1



if "patient" not in st.session_state:

    st.session_state.patient = {}



if "result" not in st.session_state:

    st.session_state.result = None



if "saved" not in st.session_state:

    st.session_state.saved = False



patient = st.session_state.patient



# ==========================================================
# STEPS
# ==========================================================


STEPS = [

    t("Personal Information"),

    t("Blood Pressure"),

    t("Symptoms"),

    t("Medical History"),

    t("Medications"),

    t("Lifestyle"),

    t("Lab Upload"),

    t("AI Result")

]



# ==========================================================
# HERO
# ==========================================================


st.markdown(
f"""
<div class="hero">

<h1>🩸 {t("Hypertension Assessment")}</h1>

<p>
{t("Complete the following assessment to estimate blood pressure risk using AI.")}
</p>

</div>

""",
unsafe_allow_html=True
)



stepper(
    st.session_state.step
)


st.write("")



# ==========================================================
# DATA OPTIONS
# ==========================================================


OCCUPATIONS = [

t("Office / Desk Job"),

t("IT / Software"),

t("Teacher"),

t("Healthcare Worker"),

t("Driver / Transport"),

t("Military / Police / Security"),

t("Construction / Manual Labor"),

t("Business Owner"),

t("Student"),

t("Homemaker"),

t("Retired"),

t("Other")

]



SYMPTOMS = [

t("Headache"),

t("Dizziness"),

t("Blurred Vision"),

t("Chest Pain"),

t("Shortness of Breath"),

t("Fatigue"),

t("Palpitations"),

t("Nosebleeds")

]



STRESS_LEVELS = [

t("Low"),

t("Moderate"),

t("High"),

t("Very High")

]


SLEEP_OPTIONS = [

t("Less than 5 hours"),

t("5-6 hours"),

t("7-8 hours"),

t("More than 8 hours")

]


ACTIVITY_LEVELS = [

t("Sedentary"),

t("Light"),

t("Moderate"),

t("Active")

]



MEDICATIONS = [

"Lisinopril",

"Losartan",

"Amlodipine",

"Metoprolol",

t("Other")

]



FAMILY_HISTORY = [

t("Hypertension"),

t("Diabetes"),

t("Heart Disease"),

t("Stroke"),

t("Kidney Disease")

]



# ==========================================================
# NAVIGATION FUNCTIONS
# ==========================================================


def next_step():

    st.session_state.step += 1



def back_step():

    st.session_state.step -= 1
    # ==========================================================
# STEP 1
# PERSONAL INFORMATION
# ==========================================================


if st.session_state.step == 1:


    st.subheader(
        t("👤 Patient Information")
    )


    name = profile["full_name"] or ""

    age = profile["age"] or 30

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
            value=gender,
            disabled=True
        )



    with col2:


        st.number_input(
            t("Weight (kg)"),
            value=float(weight),
            disabled=True
        )


        st.number_input(
            t("Height (cm)"),
            value=float(height),
            disabled=True
        )



        occupation = st.selectbox(

            t("Occupation"),

            OCCUPATIONS,

            index=0

        )



    st.write("")



    if st.button(

        t("Next ➜"),

        key="hypertension_step1",

        width="stretch"

    ):


        patient["name"] = name

        patient["age"] = age

        patient["gender"] = gender

        patient["weight"] = weight

        patient["height"] = height

        patient["occupation"] = occupation


        st.session_state.step = 2

        st.rerun()





# ==========================================================
# STEP 2
# BLOOD PRESSURE
# ==========================================================


elif st.session_state.step == 2:


    st.subheader(
        t("🩺 Blood Pressure Information")
    )



    systolic = st.number_input(

        t("Systolic Blood Pressure"),

        min_value=70,

        max_value=250,

        value=patient.get(
            "systolic",
            120
        )

    )



    diastolic = st.number_input(

        t("Diastolic Blood Pressure"),

        min_value=40,

        max_value=150,

        value=patient.get(
            "diastolic",
            80
        )

    )



    cholesterol = st.number_input(

        t("Total Cholesterol"),

        min_value=100,

        max_value=400,

        value=patient.get(
            "cholesterol",
            200
        )

    )



    col1,col2 = st.columns(2)



    with col1:

        if st.button(

            t("⬅ Back"),

            key="bp_back",

            width="stretch"

        ):

            st.session_state.step = 1

            st.rerun()



    with col2:


        if st.button(

            t("Next ➜"),

            key="bp_next",

            width="stretch"

        ):


            patient["systolic"] = systolic
            patient["diastolic"] = diastolic
            patient["cholesterol"] = cholesterol

            patient["heart_rate"] = patient.get("heart_rate", 75)

            patient["age"] = profile["age"] or 30
            patient["weight"] = profile["weight"] or 70
            patient["height"] = profile["height"] or 170
            patient["gender"] = profile["gender"] or "Male"
            patient["name"] = profile["full_name"] or ""

            st.session_state.step = 3

            st.rerun()






# ==========================================================
# STEP 3
# SYMPTOMS
# ==========================================================


elif st.session_state.step == 3:



    st.subheader(
        t("🤕 Symptoms")
    )



    symptoms = st.multiselect(

        t("Select symptoms you experience"),

        SYMPTOMS,

        default=patient.get(
            "symptoms",
            []
        )

    )



    stress = st.selectbox(

        t("Stress Level"),

        STRESS_LEVELS

    )



    sleep = st.selectbox(

        t("Average Sleep"),

        SLEEP_OPTIONS

    )



    col1,col2 = st.columns(2)



    with col1:

        if st.button(

            t("⬅ Back"),

            key="sym_back",

            width="stretch"

        ):

            st.session_state.step = 2

            st.rerun()



    with col2:

        if st.button(

            t("Next ➜"),

            key="sym_next",

            width="stretch"

        ):


            patient["symptoms"] = symptoms

            patient["stress"] = stress

            patient["sleep"] = sleep


            st.session_state.step = 4

            st.rerun()







# ==========================================================
# STEP 4
# MEDICAL HISTORY
# ==========================================================


elif st.session_state.step == 4:



    st.subheader(
        t("📋 Medical History")
    )



    diabetes = st.selectbox(

        t("Do you have diabetes?"),

        [
            t("No"),
            t("Yes")
        ]

    )



    heart_rate = st.number_input(

        t("Resting Heart Rate"),

        min_value=40,

        max_value=200,

        value=patient.get(
            "heart_rate",
            75
        )

    )



    family = st.multiselect(

        t("Family Medical History"),

        FAMILY_HISTORY,

        default=patient.get(
            "family_history",
            []
        )

    )



    col1,col2 = st.columns(2)



    with col1:


        if st.button(

            t("⬅ Back"),

            key="med_back",

            width="stretch"

        ):


            st.session_state.step = 3

            st.rerun()



    with col2:


        if st.button(

            t("Next ➜"),

            key="med_next",

            width="stretch"

        ):


            patient["diabetes"] = diabetes

            patient["heart_rate"] = heart_rate

            patient["family_history"] = family


            st.session_state.step = 5

            st.rerun()
            # ==========================================================
# STEP 5
# MEDICATIONS
# ==========================================================


elif st.session_state.step == 5:


    st.subheader(
        t("💊 Medications")
    )


    taking_medicine = st.selectbox(

        t("Are you taking blood pressure medication?"),

        [
            t("No"),
            t("Yes")
        ]

    )


    medicine = ""


    if taking_medicine == t("Yes"):

        medicine = st.selectbox(

            t("Medication name"),

            MEDICATIONS

        )



    col1,col2 = st.columns(2)



    with col1:

        if st.button(

            t("⬅ Back"),

            key="medication_back",

            width="stretch"

        ):

            st.session_state.step = 4

            st.rerun()



    with col2:

        if st.button(

            t("Next ➜"),

            key="medication_next",

            width="stretch"

        ):


            patient["taking_medicine"] = taking_medicine

            patient["medicine"] = medicine


            st.session_state.step = 6

            st.rerun()







# ==========================================================
# STEP 6
# LIFESTYLE
# ==========================================================

elif st.session_state.step == 6:

    st.subheader(t("🏃 Lifestyle Information"))

    smoking = st.selectbox(
        t("Do you smoke?"),
        [t("No"), t("Yes")],
        index=0 if patient.get("smoking", "No") == "No" else 1
    )

    cigs_per_day = patient.get("cigs_per_day", 0)

    if smoking == t("Yes"):
        cigs_per_day = st.number_input(
            t("Cigarettes Per Day"),
            min_value=1,
            max_value=60,
            value=max(1, cigs_per_day)
        )

    activity = st.selectbox(
        t("Physical Activity Level"),
        ACTIVITY_LEVELS,
        index=0
    )

    salt = st.selectbox(
        t("Salt Intake"),
        [t("Low"), t("Moderate"), t("High")],
        index=1
    )

    alcohol = st.selectbox(
        t("Alcohol Consumption"),
        [t("Never"), t("Sometimes"), t("Regularly")],
        index=0
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            t("⬅ Back"),
            key="life_back",
            width="stretch"
        ):
            st.session_state.step = 5
            st.rerun()

    with col2:

        if st.button(
            t("Next ➜"),
            key="life_next",
            width="stretch"
        ):

            patient["smoking"] = smoking
            patient["cigs_per_day"] = cigs_per_day
            patient["activity"] = activity
            patient["salt"] = salt
            patient["alcohol"] = alcohol

            st.session_state.step = 7
            st.rerun()



# ==========================================================
# STEP 7
# ADDITIONAL LABS
# ==========================================================


elif st.session_state.step == 7:



    st.subheader(
        t("🧪 Additional Lab Information")
    )



    notes = st.text_area(

        t("Additional medical notes (optional)")

    )



    upload = st.file_uploader(

        t("Upload lab report (optional)"),

        type=[
            "png",
            "jpg",
            "jpeg",
            "pdf"
        ]

    )



    col1,col2 = st.columns(2)



    with col1:


        if st.button(

            t("⬅ Back"),

            key="lab_back",

            width="stretch"

        ):


            st.session_state.step = 6

            st.rerun()



    with col2:


        if st.button(

            t("🤖 Predict "),

            key="analyze_hypertension",

            width="stretch"

        ):


            patient["notes"] = notes

            patient["lab_upload"] = upload


            st.session_state.step = 8

            st.rerun()






# ==========================================================
# STEP 8
# AI ANALYSIS
# ==========================================================

elif st.session_state.step == 8:

    st.subheader(t("🤖 AI Analysis Result"))

    ai_loading()

    # -----------------------------
    # Feature Engineering
    # -----------------------------

    male = 1 if patient.get("gender") == "Male" else 0

    currentSmoker = 1 if patient.get("smoking") == t("Yes") else 0

    cigsPerDay = patient.get("cigs_per_day", 0)

    BPMeds = 1 if patient.get("taking_medicine") == t("Yes") else 0

    diabetes = 1 if patient.get("diabetes") == t("Yes") else 0

    age = patient.get("age", 30)

    sysBP = patient.get("systolic", 120)

    diaBP = patient.get("diastolic", 80)

    totChol = patient.get("cholesterol", 200)

    BMI = round(
        patient.get("weight",70)
        /
        ((patient.get("height",170)/100)**2),
        2
    )

    heartRate = patient.get("heart_rate",75)

    glucose = patient.get("glucose",100)

    pulse_pressure = sysBP - diaBP

    mean_arterial_pressure = (sysBP + 2*diaBP)/3

    age_bmi = age * BMI

    smoking_load = currentSmoker * cigsPerDay

    # -----------------------------
    # MODEL INPUT
    # -----------------------------

    input_data = pd.DataFrame([[

        male,
        age,
        currentSmoker,
        cigsPerDay,
        BPMeds,
        diabetes,
        totChol,
        sysBP,
        diaBP,
        BMI,
        heartRate,
        glucose,
        pulse_pressure,
        mean_arterial_pressure,
        age_bmi,
        smoking_load

    ]],

    columns=[

        "male",
        "age",
        "currentSmoker",
        "cigsPerDay",
        "BPMeds",
        "diabetes",
        "totChol",
        "sysBP",
        "diaBP",
        "BMI",
        "heartRate",
        "glucose",
        "pulse_pressure",
        "mean_arterial_pressure",
        "age_bmi",
        "smoking_load"

    ])

     # -----------------------------
    # Prediction
    # -----------------------------

    prediction = model.predict(input_data)[0]

    try:
        probability = model.predict_proba(input_data)[0][1]
    except:
        probability = float(prediction)

    patient["prediction"] = int(prediction)
    patient["probability"] = float(probability)

    # -----------------------------
    # SAVE
    # -----------------------------

    if not st.session_state.saved:

        assessment_id = save_assessment(
            user_id=st.session_state.user["id"],
            disease="Hypertension",
            prediction=str(prediction),
            probability=float(probability)
        )


        save_hypertension(
            assessment_id,
            patient
        )

        st.session_state.saved = True

    # -----------------------------
    # RESULT UI
    # -----------------------------

    st.success(t("Analysis Completed Successfully ✅"))

    st.balloons()

    ai_gauge(probability)

    result_card(
        prediction,
        probability
    )

    recommendation(prediction)

    patient_summary({

        t("Full Name"): patient["name"],
        t("Age"): patient["age"],
        t("Gender"): patient["gender"],
        t("Weight"): patient["weight"],
        t("Height"): patient["height"],
        t("Systolic BP"): sysBP,
        t("Diastolic BP"): diaBP,
        t("Heart Rate"): heartRate,
        t("BMI"): BMI

    })

    st.divider()

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
            key="bp_back_result"
        ):
            st.session_state.step = 7
            st.rerun()

    with col2:

        if st.button(
            t("🔄 New Assessment"),
            width="stretch",
            key="bp_new"
        ):
            st.session_state.step = 1
            st.session_state.patient = {}
            st.session_state.saved = False
            st.rerun()