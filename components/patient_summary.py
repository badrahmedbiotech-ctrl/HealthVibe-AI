import streamlit as st
import pandas as pd
import translation

FIELD_LABELS = {

    "name": "Full Name",
    "age": "Age",
    "gender": "Gender",
    "weight": "Weight",
    "height": "Height",
    "bmi": "BMI",

    "cholesterol_total": "Total Cholesterol",
    "ldl": "LDL Cholesterol",
    "hdl": "HDL Cholesterol",
    "triglycerides": "Triglycerides",
    "fasting_blood_sugar": "Fasting Blood Sugar",
    "hba1c": "HbA1c",
    "resting_bp_systolic": "Systolic Blood Pressure",
    "smoker_status": "Smoking Status",

    "pregnancies": "Pregnancies",
    "glucose": "Glucose",
    "blood_pressure": "Blood Pressure",
    "insulin": "Insulin",
    "skin": "Skin Thickness",
    "dpf": "Diabetes Pedigree Function",


    "prediction": "Prediction",
    "probability": "Probability",
    "prediction_text": "Prediction Result"

}


def patient_summary(data):

    st.subheader(translation.t("📋 Patient Summary"))

    features = [
        translation.t(FIELD_LABELS.get(key, key))
        for key in data.keys()
    ]

    values = [
        translation.t(str(v))
        for v in data.values()
    ]

    df = pd.DataFrame({

        translation.t("Feature"): features,

        translation.t("Value"): values

    })

    st.dataframe(
        df,
        width="stretch"
    )