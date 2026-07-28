import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile

from utils.navigation import sidebar


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
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = 1
if "d_dimer" not in st.session_state:
    st.session_state.d_dimer = 250.0


if "age" not in st.session_state:
    st.session_state.age = 45


if "swelling" not in st.session_state:
    st.session_state.swelling = "No"


if "pain" not in st.session_state:
    st.session_state.pain = "No"


if "history" not in st.session_state:
    st.session_state.history = "No"


if "mobility" not in st.session_state:
    st.session_state.mobility = "No"


if "name" not in st.session_state:
    st.session_state.name = ""

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


if "risk_result" not in st.session_state:
    st.session_state.risk_result = ""


if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0



# ==========================================================
# PDF GENERATOR
# ==========================================================
def generate_pdf(data):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.set_title(
        "HealthVibe AI - Thrombosis Report"
    )

    # ==========================
    # TITLE
    # ==========================

    pdf.set_font(
        "Arial",
        "B",
        22
    )

    pdf.cell(
        0,
        12,
        "HealthVibe AI",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        14
    )

    pdf.cell(
        0,
        10,
        "Thrombosis Risk Assessment Report",
        ln=True
    )

    pdf.ln(10)

    # ==========================
    # PATIENT INFORMATION
    # ==========================

    pdf.set_font(
        "Arial",
        "B",
        14
    )

    pdf.cell(
        0,
        10,
        "Patient Information",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        12
    )

    for key, value in data.items():

        clean_value = str(value)

        clean_value = (
            clean_value
            .replace("🟢", "")
            .replace("🟡", "")
            .replace("🔴", "")
            .replace("⚠️", "")
        )

        pdf.cell(
            0,
            8,
            f"{key}: {clean_value}",
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
"""

<div class="hero">

<h1>
🩸 Thrombosis AI
</h1>


<p>
Artificial Intelligence System for Blood Clot Risk Assessment
</p>


</div>

""",
unsafe_allow_html=True
)



# ==========================================================
# DASHBOARD
# ==========================================================


st.subheader(
    "📊 AI Dashboard"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Disease",
        "Thrombosis"
    )


with c2:

    st.metric(
        "Risk Factors",
        "6"
    )


with c3:

    st.metric(
        "AI System",
        "Active"
    )


with c4:

    st.metric(
        "Status",
        "🟢 Online"
    )



st.divider()



# ==========================================================
# PAGE 1 - PATIENT INFORMATION
# ==========================================================


if st.session_state.page == 1:


    st.header(
        "👤 Patient Information"
    )


    left, right = st.columns(2)



    with left:


        name = st.text_input(
            "Patient Name",
            key="name"
        )


        age = st.number_input(
            "Age",
            1,
            120,
            45,
            key="age"
        )



    with right:


        d_dimer = st.number_input(

            "D-Dimer Level (ng/mL)",

            min_value=0.0,

            value=250.0,

            key="d_dimer"
        )



        blood_type = st.selectbox(

            "Blood Type",

            [
                "A",
                "B",
                "AB",
                "O"
            ],

            key="blood_type"

        )



    st.divider()


    st.progress(
        33
    )


    st.caption(
        "Step 1 of 3"
    )


    st.divider()



    if st.button(
        "Next ➜",
        use_container_width=True
    ):

        st.session_state.page = 2

        st.rerun()
        # ==========================================================
# PAGE 2 - CLINICAL INFORMATION
# ==========================================================


if st.session_state.page == 2:


    st.header(
        "🩺 Clinical Symptoms & History"
    )


    col1, col2 = st.columns(2)



    with col1:


        swelling = st.selectbox(

            "Leg Swelling / Edema",

            [
                "No",
                "Yes"
            ],

            key="swelling"

        )


        pain = st.selectbox(

            "Leg Pain / Tenderness",

            [
                "No",
                "Yes"
            ],

            key="pain"

        )


        history = st.selectbox(

            "Previous History of Blood Clots",

            [
                "No",
                "Yes"
            ],

            key="history"

        )



    with col2:


        mobility = st.selectbox(

            "Recent Prolonged Immobility",

            [
                "No",
                "Yes"
            ],

            key="mobility"

        )


        surgery = st.selectbox(

            "Recent Surgery",

            [
                "No",
                "Yes"
            ],

            key="surgery"

        )


        family_history = st.selectbox(

            "Family History of Thrombosis",

            [
                "No",
                "Yes"
            ],

            key="family_history"

        )



    st.divider()



    st.subheader(
        "❤️ Additional Health Factors"
    )


    c1, c2 = st.columns(2)



    with c1:


        smoking = st.selectbox(

            "Smoking Status",

            [
                "No",
                "Yes"
            ],

            key="smoking"

        )


        hypertension = st.selectbox(

            "Hypertension",

            [
                "No",
                "Yes"
            ],

            key="hypertension"

        )



    with c2:


        diabetes = st.selectbox(

            "Diabetes",

            [
                "No",
                "Yes"
            ],

            key="diabetes"

        )


        cholesterol = st.selectbox(

            "High Cholesterol",

            [
                "No",
                "Yes"
            ],

            key="cholesterol"

        )



    st.divider()


    st.progress(
        66
    )


    st.caption(
        "Step 2 of 3"
    )



    st.divider()



    back, next_btn = st.columns(2)



    with back:

        if st.button(
            "⬅ Back",
            use_container_width=True
        ):

            st.session_state.page = 1

            st.rerun()



    with next_btn:

        if st.button(
            "Next ➜",
            use_container_width=True
        ):

            st.session_state.page = 3

            st.rerun()
            # ==========================================================
# PAGE 3 - AI ANALYSIS & REPORT
# ==========================================================


if st.session_state.page == 3:


    st.header(
        "🤖 AI Thrombosis Analysis"
    )


    st.write(
        "The AI system analyzes clinical factors to estimate thrombosis risk."
    )


    st.divider()



    # ======================================================
    # CALCULATE RISK
    # ======================================================


    risk_score = 0

    factors = []

    contributions = []



    if st.session_state.d_dimer > 500:

        risk_score += 2

        factors.append(
            "Elevated D-Dimer"
        )

        contributions.append(2)



    if st.session_state.swelling == "Yes":

        risk_score += 1

        factors.append(
            "Leg Swelling"
        )

        contributions.append(1)



    if st.session_state.pain == "Yes":

        risk_score += 1

        factors.append(
            "Leg Pain"
        )

        contributions.append(1)



    if st.session_state.history == "Yes":

        risk_score += 2

        factors.append(
            "Previous Blood Clot"
        )

        contributions.append(2)



    if st.session_state.mobility == "Yes":

        risk_score += 1

        factors.append(
            "Prolonged Immobility"
        )

        contributions.append(1)



    if st.session_state.age > 60:

        risk_score += 1

        factors.append(
            "Age Factor"
        )

        contributions.append(1)



    if len(factors) == 0:

        factors.append(
            "No Risk Factors"
        )

        contributions.append(0)



    probability = min(
        (risk_score / 8) * 100,
        100
    )



    if probability >= 70:

        result = "🔴 High Risk"

    elif probability >= 35:

        result = "🟡 Moderate Risk"

    else:

        result = "🟢 Low Risk"



    st.session_state.risk_score = probability

    st.session_state.risk_result = result



    # ======================================================
    # RESULT CARDS
    # ======================================================


    c1, c2 = st.columns(2)



    with c1:

        st.metric(
            "Risk Probability",
            f"{probability:.1f}%"
        )



    with c2:

        st.metric(
            "Assessment",
            result
        )



    st.divider()



    # ======================================================
    # GAUGE CHART
    # ======================================================


    st.subheader(
        "📊 Risk Probability Gauge"
    )


    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=probability,

            title={
                "text":
                "Thrombosis Risk (%)"
            },

            gauge={

                "axis":{
                    "range":[0,100]
                }

            }

        )

    )


    fig.update_layout(
        height=300
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    st.divider()



    # ======================================================
    # EXPLAINABLE AI
    # ======================================================


    st.subheader(
        "🧠 Explainable AI"
    )


    chart = go.Figure(

        go.Bar(

            x=contributions,

            y=factors,

            orientation="h"

        )

    )


    chart.update_layout(
        height=300,
        xaxis_title="Risk Contribution",
        yaxis_title="Factors"
    )


    st.plotly_chart(
        chart,
        use_container_width=True
    )



    st.divider()



    # ======================================================
    # RECOMMENDATIONS
    # ======================================================


    st.subheader(
        "💡 Recommendations"
    )


    recommendations = []


    if probability >= 70:

        recommendations.extend([

            "Consult cardiovascular specialist immediately.",

            "Doppler ultrasound may be required.",

            "Avoid prolonged immobility."

        ])


    elif probability >= 35:

        recommendations.extend([

            "Monitor symptoms carefully.",

            "Maintain regular movement.",

            "Discuss risk factors with your doctor."

        ])


    else:

        recommendations.extend([

            "Maintain healthy lifestyle.",

            "Stay hydrated.",

            "Exercise regularly."

        ])



    for item in recommendations:

        st.write(
            "✔️",
            item
        )



    st.divider()



    # ======================================================
    # MEDICAL APPROACH
    # ======================================================


    st.subheader(
        "💊 Medical Options (Doctor Consultation)"
    )


    medications = [

        "Anticoagulants may be prescribed depending on diagnosis.",

        "Compression stockings may be recommended.",

        "Treatment plan must be decided by a physician."

    ]


    for med in medications:

        st.write(
            "•",
            med
        )



    st.divider()



    # ======================================================
    # PDF REPORT
    # ======================================================


    report_data = {

        "Patient Name":
        st.session_state.name,

        "Age":
        st.session_state.age,

        "D-Dimer":
        st.session_state.d_dimer,

        "Risk":
        result,

        "Probability":
        f"{probability:.1f}%"

    }



    pdf_path = generate_pdf(
        report_data
    )



    with open(
        pdf_path,
        "rb"
    ) as file:


        st.download_button(

            "📄 Download PDF Report",

            file,

            file_name="Thrombosis_Report.pdf",

            mime="application/pdf",

            use_container_width=True

        )



    st.divider()



    # ======================================================
    # NAVIGATION
    # ======================================================


    if st.button(
        "⬅ Back",
        use_container_width=True
    ):

        st.session_state.page = 2

        st.rerun()



# ==========================================================
# FOOTER
# ==========================================================


st.markdown(

"""

<div style="text-align:center">

<h3 style="color:#00C2FF;">
🩸 HealthVibe AI
</h3>


<p style="color:#94A3B8;">
Thrombosis Intelligent Risk Screening System
</p>


<p style="color:gray;">
Developed by <b>Badr Ahmed</b>
</p>


</div>

""",

unsafe_allow_html=True

)
