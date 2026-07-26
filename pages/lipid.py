import streamlit as st
import pandas as pd

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os


# ==========================
# PDF Generator Function
# ==========================
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "health_score" not in st.session_state:
    st.session_state.health_score = 0

if "risk_level" not in st.session_state:
    st.session_state.risk_level = ""

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []    
def generate_pdf(age, gender, bmi, total_chol, ldl, hdl, triglycerides,
                 health_score, risk_level, recommendations):

    file_name = "Lipid_Report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>HealthVibe AI</b>", styles["Title"]))
    elements.append(Paragraph("Lipid Profile Report", styles["Heading1"]))

    elements.append(Paragraph(f"Age : {age}", styles["BodyText"]))
    elements.append(Paragraph(f"Gender : {gender}", styles["BodyText"]))
    elements.append(Paragraph(f"BMI : {bmi:.2f}", styles["BodyText"]))

    elements.append(Paragraph("<br/>", styles["BodyText"]))

    elements.append(Paragraph(f"Total Cholesterol : {total_chol}", styles["BodyText"]))
    elements.append(Paragraph(f"LDL : {ldl}", styles["BodyText"]))
    elements.append(Paragraph(f"HDL : {hdl}", styles["BodyText"]))
    elements.append(Paragraph(f"Triglycerides : {triglycerides}", styles["BodyText"]))

    elements.append(Paragraph("<br/>", styles["BodyText"]))

    elements.append(Paragraph(
        f"Overall Risk : {risk_level}",
        styles["Heading2"]
    ))

    elements.append(Paragraph(
        f"Health Score : {health_score}/100",
        styles["Heading2"]
    ))

    elements.append(Paragraph(
        "Recommendations:",
        styles["Heading2"]
    ))

    for rec in recommendations:
        elements.append(
            Paragraph(f"• {rec}", styles["BodyText"])
        )

    doc.build(elements)

    return file_name



# ==========================
# Streamlit Page
# ==========================

st.set_page_config(
    page_title="Lipid Profile Analyzer",
    page_icon="🩸",
    layout="wide"
)


st.title("🩸 Lipid Profile Analyzer")

st.markdown(
    "Analyze your lipid profile and receive a personalized health report."
)

st.divider()


# ==========================
# Personal Information
# ==========================

st.subheader("👤 Personal Information")


col1, col2 = st.columns(2)


with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=30
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    height = st.number_input(
        "Height (cm)",
        min_value=100,
        max_value=250,
        value=170
    )


with col2:

    weight = st.number_input(
        "Weight (kg)",
        min_value=20,
        max_value=250,
        value=70
    )

    smoker = st.selectbox(
        "Smoking",
        ["Never", "Former", "Current"]
    )

    family_history = st.selectbox(
        "Family History of Heart Disease",
        ["No", "Yes"]
    )


# ==========================
# BMI
# ==========================

bmi = weight / ((height / 100) ** 2)

st.info(f"Calculated BMI : {bmi:.2f}")

st.divider()
# ==========================
# Medical Conditions
# ==========================

st.subheader("🩺 Medical Conditions")

col1, col2 = st.columns(2)

with col1:

    diabetes = st.selectbox(
        "Diabetes",
        ["No", "Yes"]
    )

    hypertension = st.selectbox(
        "Hypertension",
        ["No", "Yes"]
    )

with col2:

    exercise = st.slider(
        "Exercise (days/week)",
        0,
        7,
        3
    )

    sleep = st.slider(
        "Sleep Hours",
        3,
        12,
        7
    )

st.divider()

# ==========================
# Lipid Profile
# ==========================

st.subheader("🩸 Lipid Profile")

col1, col2 = st.columns(2)

with col1:

    total_chol = st.number_input(
        "Total Cholesterol (mg/dL)",
        50,
        500,
        180
    )

    ldl = st.number_input(
        "LDL (mg/dL)",
        10,
        300,
        100
    )

with col2:

    hdl = st.number_input(
        "HDL (mg/dL)",
        10,
        120,
        55
    )

    triglycerides = st.number_input(
        "Triglycerides (mg/dL)",
        20,
        600,
        120
    )

    st.divider()
    analyze = st.button(
    "🔍 Analyze Lipid Profile",
    use_container_width=True
     )

if analyze:

    st.session_state.analyzed = True

    st.divider()
    st.header("📊 Lipid Analysis Results")

    risk_score = 0

    # ==========================
    # Total Cholesterol
    # ==========================

    st.subheader("🩸 Total Cholesterol")

    if total_chol < 200:
        st.success("🟢 Normal")
    elif total_chol < 240:
        st.warning("🟡 Borderline High")
        risk_score += 1
    else:
        st.error("🔴 High")
        risk_score += 2

    # ==========================
    # LDL
    # ==========================

    st.subheader("🧬 LDL")

    if ldl < 100:
        st.success("🟢 Optimal")
    elif ldl < 130:
        st.info("🟡 Near Optimal")
        risk_score += 1
    elif ldl < 160:
        st.warning("🟠 Borderline High")
        risk_score += 2
    else:
        st.error("🔴 High")
        risk_score += 3

    # ==========================
    # HDL
    # ==========================
    risk_score = 0
    st.subheader("💙 HDL")

    if hdl >= 60:
        st.success("🟢 Excellent")
    elif hdl >= 40:
        st.info("🟡 Acceptable")
    else:
        st.error("🔴 Low HDL")
        risk_score += 2

    # ==========================
    # Triglycerides
    # ==========================

    st.subheader("🧪 Triglycerides")

    if triglycerides < 150:
        st.success("🟢 Normal")
    elif triglycerides < 200:
        st.warning("🟡 Borderline High")
        risk_score += 1
    elif triglycerides < 500:
        st.error("🔴 High")
        risk_score += 2
    else:
        st.error("🚨 Very High")
        risk_score += 3

    st.divider()
    st.header("🎯 Overall Lipid Risk")

    if risk_score <= 2:
        risk_level = "Low Risk"
        st.success("🟢 Low Risk")

    elif risk_score <= 5:
        risk_level = "Moderate Risk"
        st.warning("🟡 Moderate Risk")

    else:
        risk_level = "High Risk"
        st.error("🔴 High Risk")

    st.divider()

   # ==========================
   # Personalized Recommendations
   # ==========================

    st.header("💡 Personalized Recommendations")
    recommendations = []
    # Cholesterol
    if total_chol >= 200:
      recommendations.append(
        "🥗 Reduce foods rich in saturated fats and fried meals."
    )

    # LDL
    if ldl >= 130:
      recommendations.append(
        "🐟 Increase fish, olive oil and healthy fats."
    )

    # HDL
    if hdl < 40:
      recommendations.append(
        "🏃 Exercise regularly to increase HDL."
    )

    # Triglycerides
    if triglycerides >= 150:
      recommendations.append(
        "🍭 Reduce sugar, sweets and soft drinks."
    )

    # BMI
    if bmi >= 25:
      recommendations.append(
        "⚖️ Losing 5-10% of your body weight can improve your lipid profile."
    )
      
    #Smoking
    if smoker == "Current":
      recommendations.append(
        "🚭 Stop smoking to reduce cardiovascular risk."
    )

    # Exercise
    if exercise < 3:
      recommendations.append(
        "🏋️ Aim for at least 150 minutes of exercise per week."
    )

    # Sleep
    if sleep < 6:
      recommendations.append(
        "😴 Improve your sleep quality (7-9 hours/day)."
    )

    # Diabetes
    if diabetes == "Yes":
      recommendations.append(
        "🩺 Keep blood sugar under control."
    )

    # Hypertension
    if hypertension == "Yes":
      recommendations.append(
        "❤️ Monitor your blood pressure regularly."
    )

    # Family History
    if family_history == "Yes":
      recommendations.append(
        "👨‍⚕️ Periodic lipid profile check-ups are recommended."
    )

    if len(recommendations) == 0:
      st.success(
        "🎉 Excellent! Your current lifestyle supports healthy lipid levels."
    )
    else:
      for item in recommendations:
        st.write("✔️", item)

    st.divider()

    st.header("⚠️ Medical Advice")

    if risk_score <= 2:

      st.success(
        "Continue your healthy lifestyle and repeat your lipid profile every year."
    )

    elif risk_score <= 5:

     st.warning(
        "Lifestyle modifications are recommended. Repeat your lipid profile within 3-6 months."
    )

    else:

     st.error(
        "Your results indicate a high cardiovascular risk. Please consult a healthcare professional."
    )

    st.divider()

   # =====================================
   # Health Score
   # =====================================

    st.header("❤️ Health Score")

    health_score = 100

    health_score -= risk_score * 10

    if bmi >= 25:
     health_score -= 5

    if smoker == "Current":
     health_score -= 10

    if diabetes == "Yes":
     health_score -= 10

    if hypertension == "Yes":
      health_score -= 10

    if exercise < 3:
      health_score -= 5

    if sleep < 6:
      health_score -= 5

    health_score = max(0, health_score)

    st.metric(
    label="Overall Health Score",
    value=f"{health_score}/100"
    )

    if health_score >= 85:

     st.success("🟢 Excellent Health Status")

    elif health_score >= 70:

      st.info("🟡 Good Health Status")

    elif health_score >= 50:

     st.warning("🟠 Moderate Health Status")

    else:

      st.error("🔴 High Health Risk")

    st.divider()

   # =====================================
   # Lipid Profile Chart
   # =====================================

    st.header("📊 Lipid Profile Chart")

    chart_data = pd.DataFrame({

    "Test": [
        "Total Cholesterol",
        "LDL",
        "HDL",
        "Triglycerides"
    ],

    "Value": [
        total_chol,
        ldl,
        hdl,
        triglycerides
    ]

    })

    st.bar_chart(
    chart_data,
    x="Test",
    y="Value"
    )

    st.divider()

    st.subheader("📈 Healthy Lipid Targets")

    st.write("🟢 Total Cholesterol : Less than 200 mg/dL")
    st.write("🟢 LDL : Less than 100 mg/dL")
    st.write("🟢 HDL : More than 60 mg/dL")
    st.write("🟢 Triglycerides : Less than 150 mg/dL")

    st.divider()

   # =====================================
   # PDF Report
   # =====================================
if st.session_state.analyzed:

    st.header("📄 Download Your Report")

    if st.button("Generate PDF Report"):

        pdf_file = generate_pdf(
            age,
            gender,
            bmi,
            total_chol,
            ldl,
            hdl,
            triglycerides,
            st.session_state.health_score,
            st.session_state.risk_level,
            st.session_state.recommendations
        )

        with open(pdf_file, "rb") as file:
            pdf_bytes = file.read()

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name="HealthVibe_Lipid_Report.pdf",
            mime="application/pdf"
        )
    