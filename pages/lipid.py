import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os

from components.database import save_lipid
from components.auth_guard import require_patient
from components.database import (
    create_tables,
    save_assessment,
    save_lipid,
    get_profile
)

from utils.navigation import sidebar

from components.loading_animation import ai_loading
from components.ai_gauge import ai_gauge
from components.result_card import result_card
from components.recommendation import recommendation
from components.patient_summary import patient_summary
from components.pdf_report import create_pdf

# ==========================================================
# AUTH
# ==========================================================

from components.auth_guard import require_patient
require_patient()

# ==========================================================
# DATABASE
# ==========================================================

from components.database import (
    create_tables,
    get_profile,
    save_assessment,
    save_lipid
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Lipid Profile Assessment - HealthVibe AI",
    page_icon="🩸",
    layout="wide"
)

require_patient()

if "user" not in st.session_state:
    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.user

profile = get_profile(user["id"])

if profile is None:
    st.warning("Please complete your profile first.")
    st.switch_page("pages/Profile.py")
    st.stop()

sidebar()

create_tables()

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "user" not in st.session_state:
    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.user

# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = get_profile(user["id"])

if profile is None:

    st.warning("Please complete your profile first.")

    st.switch_page("pages/Profile.py")

    st.stop()


profile = dict(profile)

create_tables()

# ==========================================
# THEME
# ==========================================

st.markdown("""
<style>

.main {
    background-color:#0e1117;
}

.block-container {
    padding-top:2rem;
}


.hero {

    background:
    linear-gradient(
    135deg,
    rgba(6,182,212,0.25),
    rgba(37,99,235,0.25)
    );

    padding:35px;
    border-radius:20px;
    margin-bottom:25px;
}


.hero h1 {

    color:#f8fafc;
    font-size:38px;
    font-weight:800;

}


.hero p {

    color:#94a3b8;
    font-size:17px;

}



.card {

background:
rgba(30,41,59,0.55);

border:

1px solid rgba(148,163,184,0.15);

border-radius:16px;

padding:25px;

margin-bottom:20px;

}



.card h2 {

color:#e2e8f0;

}



.stButton>button {


background:
linear-gradient(
90deg,
#06b6d4,
#2563eb
);


color:white;

border:none;

border-radius:12px;

padding:12px;

font-size:16px;

font-weight:700;

width:100%;

}



.result-card {


background:
rgba(30,41,59,0.6);

padding:30px;

border-radius:18px;

text-align:center;

border-top:5px solid #06b6d4;


}



.success-card {

border-top-color:#10b981;

}


.danger-card {

border-top-color:#e11d48;

}



.footer {

text-align:center;

padding:25px;

color:#94a3b8;

}



.step-label {

color:#60a5fa;

font-weight:700;

letter-spacing:1px;

}


</style>

""",
unsafe_allow_html=True)



# ==========================================
# SESSION STATE
# ==========================================

if "saved" not in st.session_state:
    st.session_state.saved = False

if "step" not in st.session_state:

    st.session_state.step = 1



if "patient" not in st.session_state:

    st.session_state.patient = {}



if "analyzed" not in st.session_state:

    st.session_state.analyzed = False



if "result" not in st.session_state:

    st.session_state.result = {}



# ==========================================
# STEPS
# ==========================================


STEPS = [

"Personal Information",

"Lifestyle & Medical History",

"Lipid Measurements",

"AI Analysis Result"

]



def next_step():

    st.session_state.step += 1



def back_step():

    st.session_state.step -= 1



patient = st.session_state.patient



# ==========================================
# HEADER
# ==========================================


st.markdown("""

<div class="hero">


<h1>
🩸 Lipid Profile Assessment
</h1>


<p>
AI-powered cholesterol and cardiovascular risk evaluation.
</p>


</div>

""",
unsafe_allow_html=True)



st.progress(
st.session_state.step / len(STEPS)
)



st.markdown(
f"""
<div class="step-label">

STEP {st.session_state.step} / {len(STEPS)}
—
{STEPS[st.session_state.step-1].upper()}

</div>
""",
unsafe_allow_html=True
)


st.write("")
# ==========================================================
# STEP 1
# PERSONAL INFORMATION
# ==========================================================

if st.session_state.step == 1:

    st.subheader("👤 Patient Information")

    name = profile["full_name"] or ""
    age = profile["age"] or 30
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70
    height = profile["height"] or 170

    st.success("✅ Patient information loaded from your profile.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.text_input(
            "Full Name",
            value=name,
            disabled=True
        )

        st.number_input(
            "Age",
            value=int(age),
            disabled=True
        )

    with c2:

        st.text_input(
            "Gender",
            value=gender,
            disabled=True
        )

        st.number_input(
            "Height (cm)",
            value=float(height),
            disabled=True
        )

    with c3:

        st.number_input(
            "Weight (kg)",
            value=float(weight),
            disabled=True
        )

        smoker = st.selectbox(
            "Smoking Status",
            ["Never", "Former", "Current"],
            index=0
        )

    bmi = weight / ((height / 100) ** 2)

    st.info(f"📐 Calculated BMI : {bmi:.2f}")

    if st.button(
        "Next ➜",
        key="lipid_step1",
        use_container_width=True
    ):

        patient["name"] = name
        patient["age"] = age
        patient["gender"] = gender
        patient["weight"] = weight
        patient["height"] = height
        patient["bmi"] = bmi
        patient["smoker"] = smoker

        st.session_state.step = 2
        st.rerun()

# ==========================================================
# STEP 2
# LIFESTYLE & MEDICAL HISTORY
# ==========================================================

elif st.session_state.step == 2:

    st.markdown("""
    <div class="card">
    <h2>🩺 Lifestyle & Medical History</h2>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        diabetes = st.selectbox(
            "Diabetes",
            ["No", "Yes"],
            index=0 if patient.get("diabetes", "No") == "No" else 1
        )

        hypertension = st.selectbox(
            "Hypertension",
            ["No", "Yes"],
            index=0 if patient.get("hypertension", "No") == "No" else 1
        )

        family_history = st.selectbox(
            "Family History of Heart Disease",
            ["No", "Yes"],
            index=0 if patient.get("family_history", "No") == "No" else 1
        )

    with c2:

        exercise = st.slider(
            "Exercise Days / Week",
            0,
            7,
            patient.get("exercise", 3)
        )

        sleep = st.slider(
            "Sleep Hours",
            3,
            12,
            patient.get("sleep", 7)
        )

        diet = st.selectbox(
            "Diet Quality",
            ["Poor", "Average", "Healthy"],
            index=["Poor", "Average", "Healthy"].index(
                patient.get("diet", "Average")
            )
        )

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back",
            key="lipid_back2",
            use_container_width=True
        ):
            st.session_state.step = 1
            st.rerun()

    with col2:

        if st.button(
            "Next ➜",
            key="lipid_next2",
            use_container_width=True
        ):

            patient["diabetes"] = diabetes
            patient["hypertension"] = hypertension
            patient["family_history"] = family_history
            patient["exercise"] = exercise
            patient["sleep"] = sleep
            patient["diet"] = diet

            st.session_state.step = 3
            st.rerun()
            
# ==========================================
# STEP 3
# LIPID MEASUREMENTS
# ==========================================


elif st.session_state.step == 3:


    st.markdown("""
    <div class="card">

    <h2>
    🩸 Lipid Profile Measurements
    </h2>

    """,
    unsafe_allow_html=True)



    c1,c2 = st.columns(2)



    with c1:


        patient["total_chol"] = st.number_input(
            "Total Cholesterol (mg/dL)",
            min_value=50,
            max_value=500,
            value=patient.get("total_chol",180)
        )



        patient["ldl"] = st.number_input(
            "LDL Cholesterol (mg/dL)",
            min_value=10,
            max_value=300,
            value=patient.get("ldl",100)
        )



    with c2:


        patient["hdl"] = st.number_input(
            "HDL Cholesterol (mg/dL)",
            min_value=10,
            max_value=120,
            value=patient.get("hdl",55)
        )



        patient["triglycerides"] = st.number_input(
            "Triglycerides (mg/dL)",
            min_value=20,
            max_value=600,
            value=patient.get("triglycerides",120)
        )



    st.markdown(
    "</div>",
    unsafe_allow_html=True
    )



    col1,col2 = st.columns(2)



    with col1:

        st.button(
            "← Back",
            on_click=back_step,
            use_container_width=True
        )



    with col2:

        if st.button(
            "🤖 Analyze Lipid Profile",
            use_container_width=True
        ):

            risk_score = 0



# ==========================
# Cholesterol
# ==========================


            if patient["total_chol"] >= 240:

                risk_score += 2


            elif patient["total_chol"] >= 200:

                risk_score += 1




# ==========================
# LDL
# ==========================


            if patient["ldl"] >= 160:

                risk_score += 3


            elif patient["ldl"] >= 130:

                risk_score += 2


            elif patient["ldl"] >= 100:

                risk_score += 1




# ==========================
# HDL
# ==========================


            if patient["hdl"] < 40:

                risk_score += 2




# ==========================
# Triglycerides
# ==========================


            if patient["triglycerides"] >= 500:

                risk_score += 3


            elif patient["triglycerides"] >= 200:

                risk_score += 2


            elif patient["triglycerides"] >= 150:

                risk_score += 1




# ==========================
# Lifestyle Factors
# ==========================


            if patient["bmi"] >= 25:

                risk_score += 1


            if patient["smoker"] == "Current":

                risk_score += 2


            if patient["diabetes"] == "Yes":

                risk_score += 2


            if patient["hypertension"] == "Yes":

                risk_score += 2


            if patient["exercise"] < 3:

                risk_score += 1


            if patient["sleep"] < 6:

                risk_score += 1




# ==========================
# Risk Classification
# ==========================


            if risk_score <= 3:

                risk_level = "Low Risk"


            elif risk_score <= 7:
                risk_level = "Moderate Risk"


            else:

                risk_level = "High Risk"




            health_score = max(
                0,
                100 - (risk_score * 8)
            )



# ==========================
# Recommendations
# ==========================


            recommendations = []



            if patient["total_chol"] >= 200:

                recommendations.append(
                    "Reduce saturated fats and processed foods."
                )



            if patient["ldl"] >= 130:

                recommendations.append(
                    "Increase fiber intake and healthy fats."
                )



            if patient["hdl"] < 40:

                recommendations.append(
                    "Exercise regularly to improve HDL levels."
                )



            if patient["triglycerides"] >= 150:

                recommendations.append(
                    "Reduce sugar and refined carbohydrates."
                )



            if patient["bmi"] >= 25:

                recommendations.append(
                    "Weight management can improve cardiovascular health."
                )



            if patient["smoker"] == "Current":

                recommendations.append(
                    "Smoking cessation is strongly recommended."
                )



            if patient["diabetes"] == "Yes":

                recommendations.append(
                    "Maintain good blood glucose control."
                )



            if len(recommendations) == 0:

                recommendations.append(
                    "Maintain your healthy lifestyle and regular checkups."
                )



            st.session_state.result = {

                "risk_score": risk_score,

                "risk_level": risk_level,

                "health_score": health_score,

                "recommendations": recommendations,

                "date":
                datetime.now().strftime("%Y-%m-%d %H:%M")

            }


            st.session_state.analyzed = True


            st.session_state.step = 4


            st.rerun()
# ==========================================================
# STEP 4
# AI RESULT
# ==========================================================

elif st.session_state.step == 4:

    st.subheader("🤖 AI Analysis Result")

    ai_loading()

    # ==========================================
    # AI SCORING
    # ==========================================

    risk_score = 0

    if patient["total_chol"] >= 240:
        risk_score += 2
    elif patient["total_chol"] >= 200:
        risk_score += 1

    if patient["ldl"] >= 160:
        risk_score += 3
    elif patient["ldl"] >= 130:
        risk_score += 2
    elif patient["ldl"] >= 100:
        risk_score += 1

    if patient["hdl"] < 40:
        risk_score += 2

    if patient["triglycerides"] >= 500:
        risk_score += 3
    elif patient["triglycerides"] >= 200:
        risk_score += 2
    elif patient["triglycerides"] >= 150:
        risk_score += 1

    if patient["bmi"] >= 25:
        risk_score += 1

    if patient["smoker"] == "Current":
        risk_score += 2

    if patient["diabetes"] == "Yes":
        risk_score += 2

    if patient["hypertension"] == "Yes":
        risk_score += 2

    if patient["exercise"] < 3:
        risk_score += 1

    if patient["sleep"] < 6:
        risk_score += 1

    # ==========================================
    # RESULT
    # ==========================================

    if risk_score <= 3:
        prediction = 0
        risk_level = "Low Risk"

    elif risk_score <= 7:
        prediction = 1
        risk_level = "Moderate Risk"

    else:
        prediction = 2
        risk_level = "High Risk"

    probability = min(risk_score / 12, 1.0)

    patient["prediction"] = prediction
    patient["probability"] = probability

    # ==========================================
    # SAVE
    # ==========================================

    recommendations = []

    if patient["total_chol"] >= 200:
        recommendations.append("Reduce saturated fats and processed foods.")

    if patient["ldl"] >= 130:
        recommendations.append("Increase fiber intake and healthy fats.")

    if patient["hdl"] < 40:
        recommendations.append("Exercise regularly to improve HDL levels.")

    if patient["triglycerides"] >= 150:
        recommendations.append("Reduce sugar and refined carbohydrates.")

    if patient["bmi"] >= 25:
        recommendations.append("Weight management can improve cardiovascular health.")

    if patient["smoker"] == "Current":
        recommendations.append("Smoking cessation is strongly recommended.")

    if patient["diabetes"] == "Yes":
        recommendations.append("Maintain good blood glucose control.")

    if len(recommendations) == 0:
        recommendations.append("Maintain your healthy lifestyle and regular checkups.")

    health_score = max(0, 100 - risk_score * 8)

    if not st.session_state.saved:

        assessment_id = save_assessment(
            user_id=st.session_state.user["id"],
            disease="Lipid Profile",
            prediction=risk_level,
            probability=float(probability)
        )

        save_lipid(
            assessment_id,
            patient
        )

        st.session_state.saved = True

    st.success("Analysis Completed Successfully ✅")

    st.balloons()

    st.metric("Risk Level", risk_level)
    st.metric("Health Score", f"{health_score}/100")
    st.metric("Probability", f"{probability*100:.1f}%")

    summary = pd.DataFrame({
        "Item": [
            "Total Cholesterol",
            "LDL",
            "HDL",
            "Triglycerides",
            "BMI"
        ],
        "Value": [
            patient["total_chol"],
            patient["ldl"],
            patient["hdl"],
            patient["triglycerides"],
            round(patient["bmi"], 2)
        ]
    })

    st.dataframe(summary, use_container_width=True)

    st.subheader("Recommendations")

    for rec in recommendations:
        st.success(rec)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("🔄 New Assessment", use_container_width=True):
            st.session_state.step = 1
            st.session_state.patient = {}
            st.session_state.saved = False
            st.rerun()
