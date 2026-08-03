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
# OPTIONAL: get_patient_profile
# ----------------------------------------------------------
# لازم تضيف الدالة دي في components/database.py عشان الـ
# Auto-fill يشتغل فعليًا. لو مش موجودة لسه، الكود مش هيكسر
# وهيشتغل بالوضع القديم (المستخدم يدخل كل حاجة يدوي).
#
# شكل مقترح للدالة في components/database.py:
#
# def get_patient_profile(user_id):
#     """
#     يرجع dict لبيانات المريض الأساسية لو موجود، أو None.
#     مثال:
#     return {
#         "name": "...",
#         "age": 30,
#         "gender": "Male",
#         "height": 175,
#         "weight": 80,
#         "blood_type": "O+",
#         "diabetes": "No",
#         "hypertension": "No",
#         "smoking": "No",
#     }
#     """
#     ...
# ==========================================================

try:
    from components.database import get_patient_profile
except ImportError:

    def get_patient_profile(user_id):
        return None

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
# BLOOD TYPES (with Rh factor)
# ==========================================================

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

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

    "blood_type":"O+",

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

    "saved_result":False,

    "profile_loaded":False,

    "patient_found":False

}

for key,value in defaults.items():

    if key not in st.session_state:

        st.session_state[key]=value

# ==========================================================
# AUTO-FILL PATIENT PROFILE FROM DATABASE
# ==========================================================

if not st.session_state.profile_loaded:

    patient = get_patient_profile(st.session_state.user["id"])

    if patient:

        st.session_state.name = patient.get("name", st.session_state.name)
        st.session_state.age = patient.get("age", st.session_state.age)
        st.session_state.gender = patient.get("gender", st.session_state.gender)
        st.session_state.height = patient.get("height", st.session_state.height)
        st.session_state.weight = patient.get("weight", st.session_state.weight)

        bt = patient.get("blood_type", st.session_state.blood_type)
        st.session_state.blood_type = bt if bt in BLOOD_TYPES else st.session_state.blood_type

        st.session_state.diabetes = patient.get("diabetes", st.session_state.diabetes)
        st.session_state.hypertension = patient.get("hypertension", st.session_state.hypertension)
        st.session_state.smoking = patient.get("smoking", st.session_state.smoking)

        st.session_state.patient_found = True

    else:

        st.session_state.patient_found = False

    st.session_state.profile_loaded = True

# ==========================================================
# PDF REPORT
# ==========================================================

def generate_pdf(data, alerts=None, medical_override=None):

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

    # ------------------------------
    # CLINICAL ALERTS SECTION
    # ------------------------------

    if alerts:

        pdf.ln(6)

        pdf.set_font("Arial","B",14)

        pdf.cell(0, 10, "Clinical Alerts", ln=True)

        pdf.set_font("Arial","",12)

        severity_label = {
            "critical": "[CRITICAL]",
            "moderate": "[MODERATE]",
            "mild": "[MILD]"
        }

        for _, label, severity in alerts:

            tag = severity_label.get(severity, "")

            pdf.cell(0, 8, f"{tag} {label}", ln=True)

    # ------------------------------
    # MEDICAL OVERRIDE WARNING
    # ------------------------------

    if medical_override:

        pdf.ln(6)

        pdf.set_font("Arial","B",13)

        pdf.cell(0, 10, "Medical Attention Notice", ln=True)

        pdf.set_font("Arial","",12)

        pdf.multi_cell(0, 7, medical_override)

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

    if st.session_state.patient_found:

        st.success("✅ تم العثور على بيانات المريض تلقائيًا من قاعدة البيانات")

        col1,col2 = st.columns(2)

        with col1:
            st.markdown(f"**👤 الاسم:** {st.session_state.name}")
            st.markdown(f"**🎂 العمر:** {st.session_state.age}")
            st.markdown(f"**⚧ النوع:** {st.session_state.gender}")
            st.markdown(f"**🩸 فصيلة الدم:** {st.session_state.blood_type}")

        with col2:
            st.markdown(f"**📏 الطول:** {st.session_state.height} cm")
            st.markdown(f"**⚖ الوزن:** {st.session_state.weight} kg")
            st.markdown(f"**🍬 السكري:** {st.session_state.diabetes}")
            st.markdown(f"**💢 ضغط الدم:** {st.session_state.hypertension}")

        with st.expander("✏️ تعديل البيانات يدويًا (لو فيه خطأ)"):

            ecol1,ecol2 = st.columns(2)

            with ecol1:

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
                    ["Male","Female"],
                    index=0 if st.session_state.gender=="Male" else 1
                )

            with ecol2:

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

                st.session_state.blood_type = st.selectbox(
                    "Blood Type",
                    BLOOD_TYPES,
                    index=BLOOD_TYPES.index(st.session_state.blood_type)
                )

        st.markdown("### 🆕 بيانات الفحص الحالي (Thrombosis)")

        st.session_state.d_dimer = st.number_input(
            "D-Dimer (ng/mL)",
            min_value=0.0,
            value=float(st.session_state.d_dimer)
        )

    else:

        st.info("ℹ️ لم يتم العثور على بيانات محفوظة لهذا المريض — من فضلك أدخل البيانات يدويًا")

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
                BLOOD_TYPES,
                index=BLOOD_TYPES.index(st.session_state.blood_type)
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
    # CLINICAL ALERTS (severity-tagged)
    # ==========================================
    # each item: (key, label, severity) -> severity in
    # {"critical", "moderate", "mild"}
    # ==========================================

    alerts = []

    swelling_yes = st.session_state.swelling == "Yes"
    pain_yes = st.session_state.pain == "Yes"
    history_yes = st.session_state.history == "Yes"
    mobility_yes = st.session_state.mobility == "Yes"
    surgery_yes = st.session_state.surgery == "Yes"

    # --- Critical combinations (possible active clot signs) ---

    if swelling_yes and pain_yes:
        alerts.append((
            "swelling_pain_combo",
            "تورم وألم بالساق معًا — علامة محتملة لجلطة نشطة",
            "critical"
        ))

    if st.session_state.d_dimer > 500 and (swelling_yes or pain_yes):
        alerts.append((
            "d_dimer_symptomatic",
            "ارتفاع D-Dimer مصحوب بأعراض سريرية",
            "critical"
        ))
    elif st.session_state.d_dimer > 500:
        alerts.append((
            "d_dimer_high",
            "ارتفاع D-Dimer",
            "moderate"
        ))

    if history_yes and (swelling_yes or pain_yes):
        alerts.append((
            "history_recurrence",
            "تاريخ سابق لجلطة مع أعراض حالية — احتمال تكرار",
            "critical"
        ))
    elif history_yes:
        alerts.append((
            "history_only",
            "تاريخ سابق للإصابة بجلطة",
            "moderate"
        ))

    if (mobility_yes or surgery_yes) and (swelling_yes or pain_yes):
        alerts.append((
            "postop_immobility_symptomatic",
            "قلة حركة/جراحة حديثة مع أعراض — علامات تستدعي تقييم عاجل",
            "critical"
        ))
    else:
        if mobility_yes:
            alerts.append(("mobility", "قلة الحركة مؤخرًا", "moderate"))
        if surgery_yes:
            alerts.append(("surgery", "جراحة حديثة", "moderate"))

    # --- Moderate / background risk factors ---

    if st.session_state.family_history == "Yes":
        alerts.append(("family_history", "تاريخ عائلي للإصابة بجلطات", "moderate"))

    # --- Mild / general risk factors ---

    if st.session_state.smoking == "Yes":
        alerts.append(("smoking", "التدخين", "mild"))

    if st.session_state.hypertension == "Yes":
        alerts.append(("hypertension", "ضغط الدم المرتفع", "mild"))

    if st.session_state.diabetes == "Yes":
        alerts.append(("diabetes", "السكري", "mild"))

    if st.session_state.cholesterol == "Yes":
        alerts.append(("cholesterol", "ارتفاع الكوليسترول", "mild"))

    critical_alerts = [a for a in alerts if a[2] == "critical"]
    moderate_alerts = [a for a in alerts if a[2] == "moderate"]
    mild_alerts = [a for a in alerts if a[2] == "mild"]

    st.subheader("⚠ Clinical Alerts")

    if not alerts:

        st.success("لا توجد تنبيهات سريرية حالية ✅")

    else:

        for _, label, _ in critical_alerts:
            st.error(f"🔴 {label}")

        for _, label, _ in moderate_alerts:
            st.warning(f"🟠 {label}")

        for _, label, _ in mild_alerts:
            st.info(f"🟡 {label}")

    st.divider()

    # ==========================================
    # RECOMMENDATIONS (with medical override)
    # ==========================================

    st.subheader("💡 AI Recommendations")

    medical_override_text = None

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

        if critical_alerts:

            medical_override_text = (
                "Despite the AI model indicating Low Risk, the patient shows "
                "clinical alerts consistent with a possible active thrombosis. "
                "Urgent clinical evaluation and a Doppler Ultrasound are "
                "recommended regardless of the AI probability score."
            )

            st.warning(f"""
### ⚠️ تنبيه طبي هام

نتيجة الذكاء الاصطناعي **منخفضة الخطورة**، لكن فيه أعراض/علامات سريرية حرجة
ظاهرة عند المريض ({", ".join([label for _, label, _ in critical_alerts])}).

**يُنصح بشدة بمراجعة طبيب الأوعية الدموية وعمل Doppler Ultrasound فورًا،
بغض النظر عن نتيجة النموذج.**
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

    pdf_path = generate_pdf(report, alerts=alerts, medical_override=medical_override_text)

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
