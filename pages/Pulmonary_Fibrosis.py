import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import os

from PIL import Image

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from utils.navigation import sidebar


# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "prediction" not in st.session_state:
    st.session_state.prediction = ""

if "confidence" not in st.session_state:
    st.session_state.confidence = 0

if "risk_level" not in st.session_state:
    st.session_state.risk_level = ""

if "health_score" not in st.session_state:
    st.session_state.health_score = 0

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
# ==========================================================
# GLOBAL VARIABLES
# ==========================================================

full_name = ""

age = 30

gender = "Male"

height = 170

weight = 70

bmi = weight / ((height / 100) ** 2)

smoking = "No"

symptom = ""

exercise = "Regular"

sleep = 7

pollution = "Low"

chemicals = "No"

spo2 = 98

heart_rate = 80

temperature = 37

# ==========================================================
# PDF REPORT
# ==========================================================

def generate_pdf(

    full_name,
    age,
    gender,
    bmi,
    prediction,
    confidence,
    risk_level,
    health_score,
    recommendations

):

    file_name = "Pulmonary_Report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>HealthVibe AI</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Pulmonary Fibrosis Report",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            f"Patient : {full_name}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Age : {age}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Gender : {gender}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"BMI : {bmi:.2f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    elements.append(
        Paragraph(
            f"Prediction : {prediction}",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Confidence : {confidence:.1f} %",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Risk Level : {risk_level}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Health Score : {health_score}/100",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    elements.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    for item in recommendations:

        elements.append(

            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )

        )

    doc.build(elements)

    return file_name


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Pulmonary Fibrosis AI",

    page_icon="🫁",

    layout="wide",

    initial_sidebar_state="expanded"

)


# ==========================================================
# CSS
# ==========================================================

with open(
    "style.css",
    encoding="utf-8"
) as f:

    st.markdown(

        f"<style>{f.read()}</style>",

        unsafe_allow_html=True

    )


# ==========================================================
# SIDEBAR
# ==========================================================

sidebar()


# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load(
    "models/respiratory_model.pkl"
)

dataset = pd.read_csv(
    "dataset/Fibrosis_data.csv"
)

symptoms_list = sorted(

    dataset["Symptoms"]

    .dropna()

    .unique()

)
# ==========================================================
# HERO
# ==========================================================

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

# ==========================================================
# AI DASHBOARD
# ==========================================================

st.subheader("📊 AI Dashboard")

d1, d2, d3, d4 = st.columns(4)

with d1:

    st.metric(
        "Diseases",
        len(dataset["Disease"].unique())
    )

with d2:

    st.metric(
        "Dataset Size",
        f"{len(dataset):,}"
    )

with d3:

    st.metric(
        "AI Accuracy",
        "92.6%"
    )

with d4:

    st.metric(
        "Status",
        "🟢 Online"
    )

st.divider()

# ==========================================================
# PAGE 1
# ==========================================================

if st.session_state.page == 1:

    st.header("👤 Patient Information")

    left, right = st.columns(2)

    with left:

        full_name = st.text_input(
            "Full Name",
            placeholder="Enter patient's full name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=30
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
            min_value=100,
            max_value=250,
            value=170
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=250,
            value=70
        )

        bmi = weight / ((height / 100) ** 2)

        if bmi < 18.5:
            bmi_status = "Underweight"

        elif bmi < 25:
            bmi_status = "Healthy Weight"

        elif bmi < 30:
            bmi_status = "Overweight"

        else:
            bmi_status = "Obese"

    st.info(
        f"Calculated BMI : {bmi:.2f}"
    )

    st.success(
        f"BMI Status : {bmi_status}"
    )

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Age",
            age
        )

    with c2:
        st.metric(
            "BMI",
            f"{bmi:.1f}"
        )

    with c3:
        st.metric(
            "Gender",
            gender
        )

    with c4:
        st.metric(
            "Height",
            f"{height} cm"
        )

    st.progress(20)

    st.caption("Step 1 of 3")

    st.divider()

    next_col = st.columns([5, 1])

    with next_col[1]:

        if st.button(
            "Next ➜",
            use_container_width=True
        ):

            st.session_state.page = 2
            st.rerun()
            # ==========================================================
# PAGE 2
# ==========================================================

if st.session_state.page == 2:

    st.header("🩺 Medical History")

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

    st.header("🌍 Lifestyle")

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

    st.progress(60)

    st.caption("Step 2 of 3")

    st.divider()

    left_btn, _, right_btn = st.columns([1,3,1])

    with left_btn:

        if st.button(
            "⬅ Back",
            use_container_width=True
        ):

            st.session_state.page = 1
            st.rerun()

    with right_btn:

        if st.button(
            "Next ➜",
            use_container_width=True
        ):

            st.session_state.page = 3
            st.rerun()
            # ==========================================================
# PAGE 3
# ==========================================================

if st.session_state.page == 3:

    st.header("🤒 Symptoms")

    symptom = st.selectbox(
        "Main Symptom",
        symptoms_list
    )

    st.divider()

    # ======================================================
    # VITAL SIGNS
    # ======================================================

    st.header("❤️ Vital Signs")

    left, right = st.columns(2)

    with left:

        temperature = st.number_input(
            "Temperature (°C)",
            34.0,
            42.0,
            37.0
        )

        heart_rate = st.number_input(
            "Heart Rate (bpm)",
            30,
            200,
            80
        )

    with right:

        spo2 = st.slider(
            "SpO₂ (%)",
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

    # ======================================================
    # CLINICAL TESTS
    # ======================================================

    st.header("🧪 Clinical Tests")

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

    # ======================================================
    # CT SCAN
    # ======================================================

    st.header("🩻 Chest CT Scan")

    uploaded_image = st.file_uploader(
        "Upload Chest CT Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image is not None:

        image = Image.open(uploaded_image)

        st.image(
            image,
            caption="Uploaded CT Scan",
            use_container_width=True
        )

        st.success(
            "✅ CT Scan uploaded successfully."
        )

    st.progress(100)

    st.caption("Step 3 of 3")

    st.divider()

    left_btn, _, right_btn = st.columns([1,3,1])

    with left_btn:

        if st.button(
            "⬅ Back",
            use_container_width=True
        ):

            st.session_state.page = 2
            st.rerun()

    with right_btn:

        analyze = st.button(
            "🤖 Analyze Patient",
            use_container_width=True
        )

    if analyze:

        st.session_state.analyzed = True

        with st.spinner(
            "🧠 AI is analyzing patient data..."
        ):

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

        st.session_state.prediction = prediction
        st.session_state.confidence = confidence

        st.rerun()
        # ==========================================================
# RESULTS PAGE
# ==========================================================

if st.session_state.analyzed:

    st.divider()

    st.header("📊 AI Analysis Results")


    prediction = st.session_state.prediction
    confidence = st.session_state.confidence


    # ======================================================
    # RESULT CARDS
    # ======================================================

    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "🫁 Predicted Disease",
            prediction
        )


    with c2:

        st.metric(
            "🎯 Confidence",
            f"{confidence:.1f}%"
        )


    st.divider()


    # ======================================================
    # RISK ASSESSMENT
    # ======================================================

    st.header("❤️ Risk Assessment")


    risk = 0


    if smoking == "Current Smoker":
        risk += 30


    if bmi >= 30:
        risk += 20


    if spo2 < 94:
        risk += 30


    if symptom in [
        "coughing",
        "shortness of breath",
        "wheezing",
        "tight feeling in the chest"
    ]:

        risk += 10


    risk = min(risk,100)


    st.progress(risk)


    st.metric(
        "Estimated Risk",
        f"{risk}%"
    )


    if risk < 30:

        risk_level = "Low Risk"

        st.success(
            "🟢 LOW RISK"
        )


    elif risk < 60:

        risk_level = "Moderate Risk"

        st.warning(
            "🟡 MODERATE RISK"
        )


    else:

        risk_level = "High Risk"

        st.error(
            "🔴 HIGH RISK"
        )


    st.session_state.risk_level = risk_level



    st.divider()


    # ======================================================
    # HEALTH SCORE
    # ======================================================

    st.header("❤️ Health Score")


    health_score = 100


    health_score -= risk // 2


    if bmi >= 30:

        health_score -= 10


    if smoking == "Current Smoker":

        health_score -= 10


    if exercise == "Rarely":

        health_score -= 10


    if sleep < 6:

        health_score -= 5


    health_score = max(
        0,
        health_score
    )


    st.session_state.health_score = health_score


    st.metric(
        "Overall Health Score",
        f"{health_score}/100"
    )


    if health_score >= 85:

        st.success(
            "🟢 Excellent Health Status"
        )


    elif health_score >= 70:

        st.info(
            "🟡 Good Health Status"
        )


    elif health_score >= 50:

        st.warning(
            "🟠 Moderate Health Status"
        )


    else:

        st.error(
            "🔴 High Health Risk"
        )


    st.divider()


    # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    st.header("💡 Personalized Recommendations")


    recommendations = []


    if smoking == "Current Smoker":

        recommendations.append(
            "🚭 Stop smoking to reduce respiratory risk."
        )


    if bmi >= 25:

        recommendations.append(
            "⚖️ Maintain a healthy body weight."
        )


    if exercise == "Rarely":

        recommendations.append(
            "🏃 Increase physical activity gradually."
        )


    if sleep < 6:

        recommendations.append(
            "😴 Improve sleep quality."
        )


    if pollution == "High":

        recommendations.append(
            "😷 Avoid polluted environments."
        )


    if chemicals == "Yes":

        recommendations.append(
            "🧪 Reduce chemical exposure."
        )


    if len(recommendations) == 0:

        recommendations.append(
            "🎉 Continue your healthy lifestyle."
        )


    st.session_state.recommendations = recommendations


    for item in recommendations:

        st.write(
            "✔️",
            item
        )


    st.divider()


    # ======================================================
    # TREATMENT INFORMATION
    # ======================================================

    st.header("💊 Suggested Treatment")


    result = dataset[
        dataset["Disease"] == prediction
    ]


    if not result.empty:

        treatment = str(
            result.iloc[0]["Treatment"]
        )

        nature = str(
            result.iloc[0]["Nature"]
        )


        st.info(
            treatment
        )


        st.subheader(
            "🚨 Severity"
        )


        if nature.lower() == "high":

            st.error(
                "🔴 HIGH"
            )


        elif nature.lower() == "medium":

            st.warning(
                "🟡 MEDIUM"
            )


        else:

            st.success(
                "🟢 LOW"
            )

    else:

        st.info(
            "No additional treatment information available."
        )
        # ==========================================================
# PATIENT REPORT
# ==========================================================

if st.session_state.analyzed:

    st.divider()

    st.header("📋 Patient Report")


    r1, r2 = st.columns(2)


    with r1:

        st.metric(
            "👤 Patient Name",
            full_name
        )

        st.metric(
            "Age",
            age
        )

        st.metric(
            "Gender",
            gender
        )

        st.metric(
            "BMI",
            f"{bmi:.1f}"
        )


    with r2:

        st.metric(
            "🫁 Prediction",
            st.session_state.prediction
        )

        st.metric(
            "🎯 Confidence",
            f"{st.session_state.confidence:.1f}%"
        )

        st.metric(
            "❤️ Risk",
            st.session_state.risk_level
        )

        st.metric(
            "Health Score",
            f"{st.session_state.health_score}/100"
        )


    st.divider()


    # ======================================================
    # PDF DOWNLOAD
    # ======================================================


    pdf_file = generate_pdf(

        full_name,

        age,

        gender,

        bmi,

        st.session_state.prediction,

        st.session_state.confidence,

        st.session_state.risk_level,

        st.session_state.health_score,

        st.session_state.recommendations

    )


    with open(pdf_file, "rb") as file:

        st.download_button(

            label="📄 Download PDF Report",

            data=file,

            file_name="Pulmonary_Fibrosis_Report.pdf",

            mime="application/pdf",

            use_container_width=True

        )


# ==========================================================
# FOOTER
# ==========================================================

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
        