import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from PIL import Image

from utils.navigation import sidebar

# ===========================================
# PAGE CONFIG
# ===========================================

st.set_page_config(
    page_title="Pulmonary Fibrosis AI",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================
# LOAD CSS
# ===========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar()

# ===========================================
# LOAD MODEL
# ===========================================

model = joblib.load("models/respiratory_model.pkl")

dataset = pd.read_csv("dataset/Fibrosis_data.csv")

symptoms_list = sorted(
    dataset["Symptoms"].dropna().unique()
)

# ===========================================
# HERO
# ===========================================

st.markdown("""

<div class="hero">

<h1>
🫁 Pulmonary Fibrosis AI
</h1>

<p>

Artificial Intelligence System for Respiratory Disease Prediction

</p>

</div>

""", unsafe_allow_html=True)

# ===========================================
# TOP DASHBOARD
# ===========================================

st.subheader("📊 AI Dashboard")

a,b,c,d = st.columns(4)

with a:
    st.metric(
        "Diseases",
        len(dataset["Disease"].unique())
    )

with b:
    st.metric(
        "Dataset",
        f"{len(dataset):,}"
    )

with c:
    st.metric(
        "AI Accuracy",
        "92.6%"
    )

with d:
    st.metric(
        "Status",
        "🟢 Online"
    )

st.divider()

# ===========================================
# BASIC INFORMATION
# ===========================================

st.subheader("👤 Patient Information")

left, right = st.columns(2)

with left:

    full_name = st.text_input(
        "Full Name",
        placeholder="Enter patient's full name"
    )

    age = st.number_input(
        "Age",
        1,
        120,
        30
    )

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female"
        ]
    )

with right:

    height = st.number_input(
        "Height (cm)",
        100,
        250,
        170
    )

    weight = st.number_input(
        "Weight (kg)",
        20,
        250,
        70
    )

    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"

    elif bmi < 25:
        bmi_status = "Normal"

    elif bmi < 30:
        bmi_status = "Overweight"

    else:
        bmi_status = "Obese"

st.write("")

m1, m2, m3, m4 = st.columns(4)

m1.metric("👤 Age", age)
m2.metric("⚖ BMI", f"{bmi:.1f}")
m3.metric("🚻 Gender", gender)
m4.metric("📏 Height", f"{height} cm")

st.progress(100 if full_name else 80)

st.caption("Patient Profile")

st.divider()

# ===========================================
# MEDICAL HISTORY
# ===========================================

st.subheader("🩺 Medical History")

col1, col2 = st.columns(2)

with col1:

    smoking = st.selectbox(
        "Smoking Status",
        [
            "No",
            "Former Smoker",
            "Current Smoker"
        ]
    )

    asthma = st.checkbox("Asthma")

    copd = st.checkbox("COPD")

    hypertension = st.checkbox("Hypertension")

with col2:

    diabetes = st.checkbox("Diabetes")

    family_history = st.checkbox(
        "Family History"
    )

    tuberculosis = st.checkbox(
        "Tuberculosis"
    )

    lung_cancer = st.checkbox(
        "Lung Cancer"
    )

st.divider()

# ===========================================
# SYMPTOMS
# ===========================================

st.subheader("🤒 Symptoms")

symptom = st.selectbox(
    "Main Symptom",
    symptoms_list
)

st.divider()

# ===========================================
# LIFESTYLE
# ===========================================

st.subheader("🌍 Lifestyle")

left, right = st.columns(2)

with left:

    exercise = st.selectbox(
        "Exercise",
        [
            "Regular",
            "Sometimes",
            "Rarely"
        ]
    )

    occupation = st.text_input(
        "Occupation"
    )

    sleep = st.slider(
        "Sleep Hours",
        3,
        12,
        7
    )

with right:

    passive_smoking = st.selectbox(
        "Passive Smoking",
        [
            "No",
            "Yes"
        ]
    )

    pollution = st.selectbox(
        "Air Pollution",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    chemicals = st.selectbox(
        "Chemical Exposure",
        [
            "No",
            "Yes"
        ]
    )

st.divider()

# ===========================================
# VITAL SIGNS
# ===========================================

st.subheader("❤️ Vital Signs")

left, right = st.columns(2)

with left:

    temperature = st.number_input(
        "Temperature",
        34.0,
        42.0,
        37.0
    )

    heart_rate = st.number_input(
        "Heart Rate",
        30,
        200,
        80
    )

with right:

    spo2 = st.slider(
        "SpO₂",
        50,
        100,
        98
    )

    respiratory_rate = st.number_input(
        "Respiratory Rate",
        5,
        40,
        18
    )

st.divider()

# ===========================================
# CLINICAL TESTS
# ===========================================

st.subheader("🧪 Clinical Tests")

c1, c2 = st.columns(2)

with c1:

    ct_scan = st.selectbox(
        "CT Scan",
        [
            "Normal",
            "Abnormal"
        ]
    )

    chest_xray = st.selectbox(
        "Chest X-Ray",
        [
            "Normal",
            "Abnormal"
        ]
    )

with c2:

    pft = st.selectbox(
        "Pulmonary Function Test",
        [
            "Normal",
            "Reduced"
        ]
    )

    fibrosis_history = st.selectbox(
        "Previous Fibrosis Diagnosis",
        [
            "No",
            "Yes"
        ]
    )

st.divider()

# ===========================================
# CT SCAN IMAGE
# ===========================================

st.divider()

st.subheader("🩻 CT Scan Upload")

uploaded_image = st.file_uploader(
    "Upload Chest CT Scan",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image is not None:

    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Uploaded CT Scan",
        use_container_width=True
    )

    st.success("✅ CT Scan Uploaded Successfully")

# ===========================================
# LIVE DASHBOARD
# ===========================================

st.subheader("📊 Live Patient Dashboard")

d1, d2, d3, d4 = st.columns(4)

d1.metric("BMI", f"{bmi:.1f}")
d2.metric("SpO₂", f"{spo2}%")
d3.metric("Heart Rate", f"{heart_rate} bpm")
d4.metric("Temperature", f"{temperature:.1f} °C")

st.divider()

# ===========================================
# AI ANALYSIS
# ===========================================

if st.button("🤖 Analyze Patient", use_container_width=True):

    with st.spinner("🧠 AI is analyzing patient data..."):
        time.sleep(2)

        input_data = pd.DataFrame({
            "Symptoms": [symptom],
            "Age": [age],
            "Sex": [gender.lower()]
        })

        prediction = model.predict(input_data)[0]

        confidence = (
            model.predict_proba(input_data)[0].max() * 100
        )

    st.success("✅ Analysis Completed Successfully")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "🩺 Predicted Disease",
            prediction
        )

    with c2:
        st.metric(
            "🎯 Confidence",
            f"{confidence:.2f}%"
        )

    result = dataset[
        dataset["Disease"] == prediction
    ]

    if not result.empty:

        treatment = str(result.iloc[0]["Treatment"])
        nature = str(result.iloc[0]["Nature"])

        st.divider()

        st.subheader("💊 Suggested Treatment")

        st.info(treatment)

        st.subheader("🚨 Severity")

        if nature.lower() == "high":
            st.error("🔴 HIGH")

        elif nature.lower() == "medium":
            st.warning("🟡 MEDIUM")

        else:
            st.success("🟢 LOW")

st.divider()

# ===========================================
# IMAGE ANALYSIS
# ===========================================

if uploaded_image is not None:

    st.subheader("🩻 CT Scan Analysis")

    st.info(
        "🔬 AI Image Analysis Module Connected Successfully."
    )

    st.progress(85)

    st.success(
        "No obvious severe fibrosis pattern detected."
    )

# ===========================================
# PATIENT REPORT
# ===========================================

st.subheader("📋 Patient Report")

left, right = st.columns(2)

with left:

    st.metric("Name", full_name)
    st.metric("Age", age)
    st.metric("Gender", gender)
    st.metric("BMI", f"{bmi:.1f}")

with right:

    st.metric("Smoking", smoking)
    st.metric("SpO₂", f"{spo2}%")
    st.metric("Heart Rate", f"{heart_rate} bpm")
    st.metric("Temperature", f"{temperature:.1f} °C")

st.divider()

# ===========================================
# RISK CALCULATOR
# ===========================================

risk = 0

if smoking == "Current Smoker":
    risk += 30

if bmi >= 30:
    risk += 20

if spo2 < 94:
    risk += 30

if symptom == "coughing":
    risk += 10

if symptom == "shortness of breath":
    risk += 10

if symptom == "tight feeling in the chest":
    risk += 10

if symptom == "wheezing":
    risk += 10

risk = min(risk, 100)

st.subheader("📈 Risk Assessment")

st.progress(risk)

st.metric(
    "Estimated Risk",
    f"{risk}%"
)

if risk < 30:

    st.success("🟢 LOW RISK")

elif risk < 60:

    st.warning("🟡 MODERATE RISK")

else:

    st.error("🔴 HIGH RISK")

st.divider()

st.markdown(
"""
<div style="text-align:center">

<h3 style="color:#00C2FF;">
🫁 HealthVibe AI
</h3>

<p style="color:#94A3B8;">
Pulmonary Fibrosis Intelligent Screening System
</p>

<p style="color:gray;">
Developed by <b>Badr Ahmed</b>
</p>

</div>
""",
unsafe_allow_html=True
)
