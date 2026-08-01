import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile

import numpy as np
import joblib

from utils.navigation import sidebar

from components.database import (
    save_assessment,
    save_thrombosis
)

# ==========================================================
# LOAD AI MODEL
# ==========================================================

model = joblib.load("models/thrombosis_model.pkl")
scaler = joblib.load("models/thrombosis_scaler.pkl")

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="HealthVibe - Thrombosis AI",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD CSS
# ==========================================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================================
# SESSION DEFAULTS
# ==========================================================

defaults = {

    "page":1,

    "name":"",

    "age":45,

    "gender":"Male",

    "height":170,

    "weight":70,

    "blood_type":"O",

    "d_dimer":250.0,

    "swelling":"No",

    "pain":"No",

    "history":"No",

    "mobility":"No",

    "surgery":"No",

    "family_history":"No",

    "smoking":"No",

    "hypertension":"No",

    "diabetes":"No",

    "cholesterol":"No",

    "risk_result":"",

    "risk_score":0,

    "saved_result":False

}

for key,value in defaults.items():

    if key not in st.session_state:

        st.session_state[key]=value

# ==========================================================
# PDF REPORT
# ==========================================================

def generate_pdf(data):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial","B",20)

    pdf.cell(
        0,
        12,
        "HealthVibe AI",
        ln=True
    )

    pdf.set_font("Arial","",14)

    pdf.cell(
        0,
        10,
        "Thrombosis Assessment Report",
        ln=True
    )

    pdf.ln(8)

    pdf.set_font("Arial","",12)

    for k,v in data.items():

        value = str(v)

        value = (
            value
            .replace("🟢","")
            .replace("🟡","")
            .replace("🔴","")
        )

        pdf.cell(
            0,
            8,
            f"{k}: {value}",
            ln=True
        )

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    pdf.output(temp.name)

    return temp.name
# ==========================================================
# HERO
# ==========================================================

st.markdown(
f"""
<div class="hero">

<span class="hero-badge">
🩸 AI Disease Screening
</span>

<h1>
Thrombosis Risk Prediction
</h1>

<p>
Artificial Intelligence Based Blood Clot Screening System
</p>

</div>
""",
unsafe_allow_html=True
)

st.write("")

# ==========================================================
# DASHBOARD
# ==========================================================

st.subheader("📊 AI Dashboard")

m1,m2,m3,m4 = st.columns(4)

with m1:
    st.metric(
        "Disease",
        "Thrombosis"
    )

with m2:
    st.metric(
        "AI Model",
        "Random Forest"
    )

with m3:
    st.metric(
        "Risk Factors",
        "10"
    )

with m4:
    st.metric(
        "Status",
        "🟢 Ready"
    )

st.divider()

# ==========================================================
# PAGE 1
# ==========================================================

if st.session_state.page == 1:

    st.header("👤 Patient Information")

    col1,col2 = st.columns(2)

    with col1:

        st.session_state.name = st.text_input(
            "Patient Name",
            value=st.session_state.name
        )

        st.session_state.age = st.number_input(
            "Age",
            1,
            120,
            value=st.session_state.age
        )

        st.session_state.gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ],
            index=0 if st.session_state.gender=="Male" else 1
        )

    with col2:

        st.session_state.height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=230,
            value=st.session_state.height
        )

        st.session_state.weight = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=250,
            value=st.session_state.weight
        )

        st.session_state.d_dimer = st.number_input(
            "D-Dimer (ng/mL)",
            min_value=0.0,
            value=float(st.session_state.d_dimer)
        )

        st.session_state.blood_type = st.selectbox(
            "Blood Type",
            [
                "A",
                "B",
                "AB",
                "O"
            ],
            index=["A","B","AB","O"].index(st.session_state.blood_type)
        )

    st.divider()

    st.progress(33)

    st.caption("Step 1 / 3")

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

    st.header("🩺 Clinical Information")

    c1,c2 = st.columns(2)

    with c1:

        st.session_state.swelling = st.selectbox(
            "Leg Swelling",
            ["No","Yes"],
            index=0 if st.session_state.swelling=="No" else 1
        )

        st.session_state.pain = st.selectbox(
            "Leg Pain",
            ["No","Yes"],
            index=0 if st.session_state.pain=="No" else 1
        )

        st.session_state.history = st.selectbox(
            "Previous Blood Clot",
            ["No","Yes"],
            index=0 if st.session_state.history=="No" else 1
        )

        st.session_state.mobility = st.selectbox(
            "Recent Immobility",
            ["No","Yes"],
            index=0 if st.session_state.mobility=="No" else 1
        )

        st.session_state.surgery = st.selectbox(
            "Recent Surgery",
            ["No","Yes"],
            index=0 if st.session_state.surgery=="No" else 1
        )

    with c2:

        st.session_state.family_history = st.selectbox(
            "Family History",
            ["No","Yes"],
            index=0 if st.session_state.family_history=="No" else 1
        )

        st.session_state.smoking = st.selectbox(
            "Smoking",
            ["No","Yes"],
            index=0 if st.session_state.smoking=="No" else 1
        )

        st.session_state.hypertension = st.selectbox(
            "Hypertension",
            ["No","Yes"],
            index=0 if st.session_state.hypertension=="No" else 1
        )

        st.session_state.diabetes = st.selectbox(
            "Diabetes",
            ["No","Yes"],
            index=0 if st.session_state.diabetes=="No" else 1
        )

        st.session_state.cholesterol = st.selectbox(
            "High Cholesterol",
            ["No","Yes"],
            index=0 if st.session_state.cholesterol=="No" else 1
        )

    st.divider()

    st.progress(66)

    st.caption("Step 2 / 3")

    left,right = st.columns(2)

    with left:

        if st.button(
            "⬅ Back",
            use_container_width=True
        ):

            st.session_state.page = 1
            st.rerun()

    with right:

        if st.button(
            "Analyze ➜",
            use_container_width=True
        ):

            st.session_state.page = 3
            st.rerun()

# ==========================================================
# PAGE 3
# ==========================================================

if st.session_state.page == 3:

    st.header("🤖 AI Prediction")

    st.write(
        "HealthVibe AI is analyzing your clinical data..."
    )

    st.divider()

    # ==========================================
    # PREPARE DATA
    # ==========================================

    gender = 1 if st.session_state.gender == "Male" else 0

    X = np.array([[
        st.session_state.age,
        gender,
        st.session_state.height,
        st.session_state.weight,
        st.session_state.d_dimer
    ]])

    X = scaler.transform(X)

    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0][1] * 100

    if prediction == 1:

        result = "🔴 High Risk"

    else:

        result = "🟢 Low Risk"

    st.session_state.risk_score = probability
    st.session_state.risk_result = result

    # ==========================================
    # SAVE RESULT
    # ==========================================

    if not st.session_state.saved_result:

        assessment_id = save_assessment(

            st.session_state.user["id"],

            "Thrombosis",

            result,

            probability

        )

        save_thrombosis(

            assessment_id,

            {

                "d_dimer": st.session_state.d_dimer,

                "platelets":0,

                "inr":0,

                "prediction":result

            }

        )

        st.session_state.saved_result = True

    # ==========================================
    # RESULT
    # ==========================================

    m1,m2 = st.columns(2)

    with m1:

        st.metric(

            "Risk Probability",

            f"{probability:.1f}%"

        )

    with m2:

        st.metric(

            "Prediction",

            result

        )

    st.divider()

    # ==========================================
    # GAUGE
    # ==========================================

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=probability,

            title={"text":"Risk %"},

            gauge={

                "axis":{"range":[0,100]},

                "bar":{"color":"red"},

                "steps":[

                    {"range":[0,35],"color":"lightgreen"},

                    {"range":[35,70],"color":"khaki"},

                    {"range":[70,100],"color":"salmon"}

                ]

            }

        )

    )

    fig.update_layout(height=320)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ==========================================
    # RISK FACTORS
    # ==========================================

    factors=[]

    if st.session_state.d_dimer>500:
        factors.append("High D-Dimer")

    if st.session_state.swelling=="Yes":
        factors.append("Leg Swelling")

    if st.session_state.pain=="Yes":
        factors.append("Leg Pain")

    if st.session_state.history=="Yes":
        factors.append("Previous Thrombosis")

    if st.session_state.mobility=="Yes":
        factors.append("Immobility")

    if st.session_state.surgery=="Yes":
        factors.append("Recent Surgery")

    if st.session_state.smoking=="Yes":
        factors.append("Smoking")

    if st.session_state.hypertension=="Yes":
        factors.append("Hypertension")

    if st.session_state.diabetes=="Yes":
        factors.append("Diabetes")

    if st.session_state.cholesterol=="Yes":
        factors.append("High Cholesterol")

    st.subheader("⚠ Risk Factors")

    if len(factors)==0:

        st.success("No major risk factors detected.")

    else:

        for item in factors:

            st.warning(item)
            st.divider()

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================

    st.subheader("💡 AI Recommendations")

    if prediction == 1:

        st.error("""
### High Risk

- Consult a vascular specialist immediately.
- Doppler Ultrasound is recommended.
- Avoid prolonged sitting.
- Maintain hydration.
- Follow physician instructions.
""")

    else:

        st.success("""
### Low Risk

- Continue regular physical activity.
- Maintain healthy body weight.
- Drink enough water.
- Avoid smoking.
- Keep regular follow-up if symptoms appear.
""")

    st.divider()

    # ==========================================
    # PDF REPORT
    # ==========================================

    report = {

        "Patient Name":st.session_state.name,

        "Age":st.session_state.age,

        "Gender":st.session_state.gender,

        "Height":st.session_state.height,

        "Weight":st.session_state.weight,

        "Blood Type":st.session_state.blood_type,

        "D-Dimer":st.session_state.d_dimer,

        "Prediction":result,

        "Probability":f"{probability:.1f}%"

    }

    pdf_path = generate_pdf(report)

    with open(pdf_path,"rb") as file:

        st.download_button(

            "📄 Download Report",

            file,

            file_name="HealthVibe_Thrombosis_Report.pdf",

            mime="application/pdf",

            use_container_width=True

        )

    st.divider()

    # ==========================================
    # QUICK ACTIONS
    # ==========================================

    c1,c2 = st.columns(2)

    with c1:

        if st.button(

            "⬅ Back",

            use_container_width=True

        ):

            st.session_state.page = 2

            st.rerun()

    with c2:

        if st.button(

            "🏠 Dashboard",

            use_container_width=True

        ):

            st.switch_page("pages/Dashboard.py")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown("""

<div style="text-align:center;padding:20px;">

<h3 style="color:#00C2FF;">
HealthVibe AI
</h3>

<p style="color:gray;">
Artificial Intelligence Disease Prediction Platform
</p>

<p style="color:gray;">
Developed by <b>Badr Ahmed</b>
</p>

</div>

""",unsafe_allow_html=True)
    