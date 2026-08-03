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

    df = pd.DataFrame({

        translation.t("Feature"): features,

        translation.t("Value"): data.values()

    })

    st.dataframe(
        df,
        width="stretch"
    )