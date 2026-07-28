import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Lipid Profile Assessment - HealthVibe AI",
    page_icon="🩸",
    layout="wide"
)


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
# ==========================================
# STEP 1
# PERSONAL INFORMATION
# ==========================================


if st.session_state.step == 1:


    st.markdown("""
    <div class="card">

    <h2>
    👤 Personal Information
    </h2>

    """,
    unsafe_allow_html=True)



    c1, c2, c3 = st.columns(3)



    with c1:


        patient["name"] = st.text_input(
            "Full Name",
            value=patient.get("name","")
        )


        patient["age"] = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=patient.get("age",30)
        )



    with c2:


        patient["gender"] = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ],
            index=
            0 if patient.get("gender","Male")=="Male"
            else 1
        )



        patient["height"] = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=patient.get("height",170)
        )



    with c3:


        patient["weight"] = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=250,
            value=patient.get("weight",70)
        )


        patient["smoker"] = st.selectbox(
            "Smoking Status",
            [
                "Never",
                "Former",
                "Current"
            ]
        )



    bmi = patient["weight"] / (
        (patient["height"]/100)**2
    )


    patient["bmi"] = bmi



    st.info(
        f"📐 Calculated BMI : {bmi:.2f}"
    )



    st.markdown(
    "</div>",
    unsafe_allow_html=True
    )



    st.button(
        "Next →",
        on_click=next_step,
        use_container_width=True
    )




# ==========================================
# STEP 2
# LIFESTYLE & MEDICAL HISTORY
# ==========================================


elif st.session_state.step == 2:



    st.markdown("""
    <div class="card">

    <h2>
    🩺 Lifestyle & Medical History
    </h2>

    """,
    unsafe_allow_html=True)



    c1,c2 = st.columns(2)



    with c1:


        patient["diabetes"] = st.selectbox(
            "Diabetes",
            [
                "No",
                "Yes"
            ]
        )



        patient["hypertension"] = st.selectbox(
            "Hypertension",
            [
                "No",
                "Yes"
            ]
        )



        patient["family_history"] = st.selectbox(
            "Family History of Heart Disease",
            [
                "No",
                "Yes"
            ]
        )



    with c2:


        patient["exercise"] = st.slider(
            "Exercise Days / Week",
            0,
            7,
            3
        )



        patient["sleep"] = st.slider(
            "Sleep Hours",
            3,
            12,
            7
        )



        patient["diet"] = st.selectbox(
            "Diet Quality",
            [
                "Poor",
                "Average",
                "Healthy"
            ]
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

        st.button(
            "Next →",
            on_click=next_step,
            use_container_width=True
        )
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
            # ==========================================
# STEP 4
# AI ANALYSIS RESULT
# ==========================================


elif st.session_state.step == 4:


    result = st.session_state.result



    st.markdown("""
    <div class="hero">

    <h1>
    🤖 AI Lipid Analysis Result
    </h1>

    <p>
    Your lipid profile has been analyzed successfully.
    </p>

    </div>

    """,
    unsafe_allow_html=True)



    risk_level = result["risk_level"]

    health_score = result["health_score"]



    # ==========================
    # RESULT CARD
    # ==========================


    if risk_level == "High Risk":

        card = "danger-card"

        icon = "🔴"


    elif risk_level == "Moderate Risk":

        card = ""

        icon = "🟡"


    else:

        card = "success-card"

        icon = "🟢"




    st.markdown(
    f"""
    <div class="result-card {card}">

    <h2>
    {icon} {risk_level}
    </h2>

    <h3>
    Overall Health Score
    </h3>

    <h1 style="color:#06b6d4;">
    {health_score}/100
    </h1>


    </div>

    """,
    unsafe_allow_html=True
    )



    st.write("")



    # ==========================
    # PATIENT SUMMARY
    # ==========================


    st.markdown("""
    <div class="card">

    <h2>
    👤 Patient Summary
    </h2>

    """,
    unsafe_allow_html=True)



    c1,c2 = st.columns(2)



    with c1:

        st.write(
        f"""
        **Name:** {patient.get('name','-')}

        **Age:** {patient.get('age','-')}

        **Gender:** {patient.get('gender','-')}

        **BMI:** {patient.get('bmi',0):.2f}

        """
        )



    with c2:

        st.write(
        f"""
        **Total Cholesterol:** {patient.get('total_chol')} mg/dL

        **LDL:** {patient.get('ldl')} mg/dL

        **HDL:** {patient.get('hdl')} mg/dL

        **Triglycerides:** {patient.get('triglycerides')} mg/dL

        """
        )



    st.markdown(
    "</div>",
    unsafe_allow_html=True
    )



    # ==========================
    # RECOMMENDATIONS
    # ==========================


    st.markdown("""
    <div class="card">

    <h2>
    💡 Personalized Recommendations
    </h2>

    """,
    unsafe_allow_html=True)



    for rec in result["recommendations"]:

        st.write(
            "✔️",
            rec
        )



    st.markdown(
    "</div>",
    unsafe_allow_html=True
    )



    # ==========================
    # CHART
    # ==========================


    st.markdown("""
    <div class="card">

    <h2>
    📊 Lipid Profile Chart
    </h2>

    """,
    unsafe_allow_html=True)



    chart = pd.DataFrame({

        "Test":

        [

            "Total Cholesterol",

            "LDL",

            "HDL",

            "Triglycerides"

        ],


        "Value":

        [

            patient["total_chol"],

            patient["ldl"],

            patient["hdl"],

            patient["triglycerides"]

        ]

    })



    st.bar_chart(

        chart,

        x="Test",

        y="Value"

    )



    st.markdown(
    "</div>",
    unsafe_allow_html=True
    )



    # ==========================
    # HEALTH GUIDANCE
    # ==========================


    st.markdown("""
    <div class="card">

    <h2>
    ⚕️ Medical Guidance
    </h2>

    """,
    unsafe_allow_html=True)



    if risk_level == "Low Risk":


        st.success(
        """
        Your lipid profile looks healthy.
        Continue your current lifestyle and perform regular checkups.
        """
        )


    elif risk_level == "Moderate Risk":


        st.warning(
        """
        Some lipid values need improvement.
        Lifestyle modifications and follow-up testing are recommended.
        """
        )


    else:


        st.error(
        """
        Your lipid profile indicates increased cardiovascular risk.
        Please consult a healthcare professional.
        """
        )



    st.markdown(
    "</div>",
    unsafe_allow_html=True
    )



    st.caption(
    "⚕️ This AI assessment provides an estimated risk evaluation and does not replace professional medical diagnosis."
    )



    st.divider()



    col1,col2 = st.columns(2)



    with col1:


        if st.button(
            "⬅ Back",
            use_container_width=True
        ):

            st.session_state.step = 3

            st.rerun()



    with col2:


        if st.button(
            "🔄 New Assessment",
            use_container_width=True
        ):


            st.session_state.step = 1

            st.session_state.patient = {}

            st.session_state.result = {}

            st.session_state.analyzed = False

            st.rerun()
            # ==========================================
# PDF REPORT
# ==========================================


def generate_pdf(patient, result):


    file_name = "HealthVibe_Lipid_Report.pdf"


    doc = SimpleDocTemplate(
        file_name,
        pagesize=A4
    )


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
            "Lipid Profile Assessment Report",
            styles["Heading2"]
        )
    )


    elements.append(Spacer(1,20))



    elements.append(
        Paragraph(
            f"""
            Name: {patient.get('name','-')}<br/>
            Age: {patient.get('age','-')}<br/>
            Gender: {patient.get('gender','-')}<br/>
            BMI: {patient.get('bmi',0):.2f}
            """,
            styles["BodyText"]
        )
    )



    elements.append(Spacer(1,15))



    elements.append(
        Paragraph(
            f"""
            Total Cholesterol:
            {patient.get('total_chol')} mg/dL<br/>

            LDL:
            {patient.get('ldl')} mg/dL<br/>

            HDL:
            {patient.get('hdl')} mg/dL<br/>

            Triglycerides:
            {patient.get('triglycerides')} mg/dL
            """,
            styles["BodyText"]
        )
    )



    elements.append(Spacer(1,20))



    elements.append(
        Paragraph(
            f"""
            Risk Level:
            {result.get('risk_level')}<br/>

            Health Score:
            {result.get('health_score')}/100
            """,
            styles["Heading2"]
        )
    )



    elements.append(
        Paragraph(
            "Recommendations:",
            styles["Heading2"]
        )
    )



    for item in result.get("recommendations",[]):

        elements.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )



    elements.append(Spacer(1,20))


    elements.append(
        Paragraph(
            """
            This report is generated by HealthVibe AI.
            It is an AI-based assessment and does not replace professional medical advice.
            """,
            styles["BodyText"]
        )
    )



    doc.build(elements)



    return file_name





# ==========================================
# DOWNLOAD REPORT
# ==========================================


if st.session_state.analyzed:



    st.divider()



    st.markdown("""
    <div class="card">

    <h2>
    📄 Medical Report
    </h2>

    <p>
    Generate and download your complete AI lipid assessment report.
    </p>

    </div>

    """,
    unsafe_allow_html=True)



    if st.button(
        "📄 Generate PDF Report",
        use_container_width=True
    ):



        pdf_file = generate_pdf(
            patient,
            st.session_state.result
        )



        with open(pdf_file,"rb") as file:


            st.download_button(

                "⬇ Download PDF Report",

                data=file,

                file_name=
                "HealthVibe_Lipid_Report.pdf",

                mime=
                "application/pdf",

                use_container_width=True

            )





# ==========================================
# FOOTER
# ==========================================


st.divider()



st.markdown("""

<div class="footer">


<h2 style="color:#00C2FF;">

🩺 HealthVibe AI

</h2>



<p>

AI-powered Lipid Profile Assessment Platform

</p>



<hr>



<p>

Made with ❤️ using Streamlit & AI

</p>



<p style="color:#94A3B8;">

© 2026 HealthVibe AI • All Rights Reserved

</p>



</div>


""",
unsafe_allow_html=True)
