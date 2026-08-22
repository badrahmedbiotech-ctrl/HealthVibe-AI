import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile

import numpy as np
import joblib

from utils.navigation import sidebar
from components.stepper import stepper

from components.database import (
    save_assessment,
    save_thrombosis
)
from components.branding import *
from components.colors import *
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

import translation
translation.init()
t = translation.t

# ==========================================================
# LANGUAGE / DIRECTION HELPER
# ==========================================================

def get_lang():
    # Try common translation module accessors first, fall back to session_state.
    for fn_name in ("get_lang", "get_language", "current_lang"):
        fn = getattr(translation, fn_name, None)
        if callable(fn):
            try:
                return fn()
            except Exception:
                pass
    return st.session_state.get("lang", "en")

IS_RTL = str(get_lang()).lower().startswith("ar")
DIR = "rtl" if IS_RTL else "ltr"

# ==========================================================
# LOAD CSS
# ==========================================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================================
# PAGE-LOCAL CSS (hero, cards, stepper, RTL)
# ==========================================================

st.markdown(
f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    direction: {DIR};
}}

.hv-card {{
    background: var(--secondary-background-color, #1c1f26);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,.15);
    transition: transform .15s ease, box-shadow .15s ease;
    text-align: {"right" if IS_RTL else "left"};
}}
.hv-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(0,0,0,.25);
}}

.hv-result-card {{
    border-radius: 20px;
    padding: 26px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,.2);
    margin-bottom: 12px;
}}
.hv-result-high {{ background: linear-gradient(135deg,#3a0000,#8B0000); color:#fff; }}
.hv-result-moderate {{ background: linear-gradient(135deg,#4a3b00,#B8860B); color:#fff; }}
.hv-result-low {{ background: linear-gradient(135deg,#003b1f,#0f9d58); color:#fff; }}

.hv-badge-risk {{
    display: inline-block;
    padding: 6px 18px;
    border-radius: 999px;
    background: rgba(255,255,255,.2);
    font-weight: 700;
    margin-top: 6px;
}}

.hv-footer {{
    text-align: center;
    padding: 24px;
}}

/* RTL fixes for native Streamlit widgets */
[dir="rtl"] label, .hv-rtl label {{
    text-align: right !important;
}}
{"div[data-testid='stMetric'] { text-align: right; }" if IS_RTL else ""}
{"div[data-testid='stMarkdownContainer'] { text-align: right; }" if IS_RTL else ""}
{"div[data-testid='stExpander'] { text-align: right; }" if IS_RTL else ""}
{"[data-testid='stHorizontalBlock'] { flex-direction: row-reverse; }" if IS_RTL else ""}
</style>
""",
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
# HERO (Diabetes-style card + progress bar) — top of page
# ==========================================================

progress = (st.session_state.page / 3) * 100

st.markdown(f"""
<div class="hero">

<h1>🩸 {t("Thrombosis Risk Prediction")}</h1>

<p>{t("AI Clinical Decision Support System")}</p>

<div style="margin-top:20px;height:10px;background:#1E293B;border-radius:20px;overflow:hidden;">

<div style="
width:{progress}%;
height:100%;
background:linear-gradient(90deg,#00C2FF,#2563EB);
">
</div>

</div>

<p style="margin-top:10px;">
{t("Step")} {st.session_state.page} / 3
</p>

</div>
""", unsafe_allow_html=True)

# Reuse the exact same stepper component Diabetes uses (Patient, Medical,
# Analysis, Result). Thrombosis only has 3 pages (page 3 runs analysis and
# shows the result together), so page 3 maps to stepper step 4.
_stepper_step = st.session_state.page if st.session_state.page < 3 else 4
stepper(_stepper_step)

st.write("")

# ==========================================================
# PDF REPORT
# (NOTE: FPDF default font is Latin-1 only, cannot render Arabic
# glyphs. This report always stays English regardless of language
# toggle unless a Unicode Arabic font is embedded.)
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
    temp.close()
    return temp.name

# ==========================================================
# PAGE 1
# ==========================================================

if st.session_state.page == 1:

    st.header(t("👤 Patient Information"))

    col1,col2 = st.columns(2)

    with col1:

        st.session_state.name = st.text_input(
            t("Patient Name"),
            value=st.session_state.name
        )

        st.session_state.age = st.number_input(
            t("Age"),
            1,
            120,
            value=st.session_state.age
        )

        st.session_state.gender = st.selectbox(
            t("Gender"),
            [
                t("Male"),
                t("Female")
            ],
            index=0 if st.session_state.gender=="Male" else 1
        )

    with col2:

        st.session_state.height = st.number_input(
            t("Height (cm)"),
            min_value=100,
            max_value=230,
            value=st.session_state.height
        )

        st.session_state.weight = st.number_input(
            t("Weight (kg)"),
            min_value=20,
            max_value=250,
            value=st.session_state.weight
        )

        st.session_state.d_dimer = st.number_input(
            t("D-Dimer (ng/mL)"),
            min_value=0.0,
            value=float(st.session_state.d_dimer)
        )

        blood_types = ["A+", "B+", "AB+", "O+", "A-", "B-", "AB-", "O-"]

        if st.session_state.blood_type not in blood_types:
            st.session_state.blood_type = "O+"

        st.session_state.blood_type = st.selectbox(
            t("Blood Type"),
            blood_types,
            index=blood_types.index(st.session_state.blood_type),
            key="blood_type_selec"
        )

    st.divider()

    if st.button(
        t("Next ➜"),
        use_container_width=True
    ):

        st.session_state.page = 2

        st.rerun()
# ==========================================================
# PAGE 2
# ==========================================================

if st.session_state.page == 2:

    st.header(t("🩺 Clinical Information"))

    c1,c2 = st.columns(2)

    with c1:

        st.session_state.swelling = st.selectbox(
            t("Leg Swelling"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.swelling=="No" else 1
        )

        st.session_state.pain = st.selectbox(
            t("Leg Pain"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.pain=="No" else 1
        )

        st.session_state.history = st.selectbox(
            t("Previous Blood Clot"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.history=="No" else 1
        )

        st.session_state.mobility = st.selectbox(
            t("Recent Immobility"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.mobility=="No" else 1
        )

        st.session_state.surgery = st.selectbox(
            t("Recent Surgery"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.surgery=="No" else 1
        )

    with c2:

        st.session_state.family_history = st.selectbox(
            t("Family History"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.family_history=="No" else 1
        )

        st.session_state.smoking = st.selectbox(
            t("Smoking"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.smoking=="No" else 1
        )

        st.session_state.hypertension = st.selectbox(
            t("Hypertension"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.hypertension=="No" else 1
        )

        st.session_state.diabetes = st.selectbox(
            t("Diabetes"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.diabetes=="No" else 1
        )

        st.session_state.cholesterol = st.selectbox(
            t("High Cholesterol"),
            [t("No"),t("Yes")],
            index=0 if st.session_state.cholesterol=="No" else 1
        )

    st.divider()

    left,right = st.columns(2)

    with left:

        if st.button(
            t("⬅ Back"),
            use_container_width=True
        ):

            st.session_state.page = 1
            st.rerun()

    with right:

        if st.button(
            f"🧠 {t('Predict')}",
            use_container_width=True
        ):

            st.session_state.page = 3
            st.rerun()

# ==========================================================
# PAGE 3
# ==========================================================

if st.session_state.page == 3:

    st.header(t("🤖 AI Prediction"))

    st.write(
        t("HealthVibe AI is analyzing your clinical data...")
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

        result = t("🔴 High Risk")

    else:

        result = t("🟢 Low Risk")

    st.session_state.risk_score = probability
    st.session_state.risk_result = result

    if probability >= 70:
        band_class = "hv-result-high"
        band_label = t("High Risk")
    elif probability >= 35:
        band_class = "hv-result-moderate"
        band_label = t("Moderate Risk")
    else:
        band_class = "hv-result-low"
        band_label = t("Low Risk")

    st.divider()

    # ==========================================
    # GAUGE
    # ==========================================

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=probability,

            title={"text": t("Risk %")},

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
        factors.append(t("High D-Dimer"))

    if st.session_state.swelling=="Yes":
        factors.append(t("Leg Swelling"))

    if st.session_state.pain=="Yes":
        factors.append(t("Leg Pain"))

    if st.session_state.history=="Yes":
        factors.append(t("Previous Thrombosis"))

    if st.session_state.mobility=="Yes":
        factors.append(t("Immobility"))

    if st.session_state.surgery=="Yes":
        factors.append(t("Recent Surgery"))

    if st.session_state.smoking=="Yes":
        factors.append(t("Smoking"))

    if st.session_state.hypertension=="Yes":
        factors.append(t("Hypertension"))

    if st.session_state.diabetes=="Yes":
        factors.append(t("Diabetes"))

    if st.session_state.cholesterol=="Yes":
        factors.append(t("High Cholesterol"))

    st.subheader(t("⚠ Risk Factors"))

    if len(factors)==0:

        st.success(t("No major risk factors detected."))

    else:

        for item in factors:

            st.warning(item)
            st.divider()

    # ==========================================
    # RECOMMENDATIONS (by risk band: Low / Moderate / High)
    # ==========================================

    st.subheader(t("💡 AI Recommendations"))

    if band_class == "hv-result-high":

        st.error(t("""
### High Risk

- Consult a vascular specialist immediately.
- Doppler Ultrasound is recommended.
- Avoid prolonged sitting.
- Maintain hydration.
- Follow physician instructions.
"""))

    elif band_class == "hv-result-moderate":

        st.warning(t("""
### Moderate Risk

- Schedule a follow-up with your physician.
- Increase light physical activity and mobility.
- Monitor for swelling or pain.
- Maintain hydration and a balanced diet.
- Repeat D-Dimer testing if symptoms persist.
"""))

    else:

        st.success(t("""
### Low Risk

- Continue regular physical activity.
- Maintain healthy body weight.
- Drink enough water.
- Avoid smoking.
- Keep regular follow-up if symptoms appear.
"""))

    st.divider()

    # ==========================================
    # PATIENT SUMMARY TABLE
    # ==========================================

    st.subheader(t("📋 Patient Summary"))

    summary_data = {

        t("Full Name"): st.session_state.name,
        t("Age"): st.session_state.age,
        t("Gender"): t(st.session_state.gender),
        t("Weight"): f"{st.session_state.weight} kg",
        t("Height"): f"{st.session_state.height} cm",
        t("Blood Type"): st.session_state.blood_type,
        t("D-Dimer"): st.session_state.d_dimer,
        t("Leg Swelling"): t(st.session_state.swelling),
        t("Leg Pain"): t(st.session_state.pain),
        t("Previous Blood Clot"): t(st.session_state.history),
        t("Recent Immobility"): t(st.session_state.mobility),
        t("Recent Surgery"): t(st.session_state.surgery),
        t("Family History"): t(st.session_state.family_history),
        t("Smoking"): t(st.session_state.smoking),
        t("Hypertension"): t(st.session_state.hypertension),
        t("Diabetes"): t(st.session_state.diabetes),
        t("High Cholesterol"): t(st.session_state.cholesterol),
        t("Prediction Result"): result,
        t("Risk Score (%)"): f"{probability:.1f}%"

    }

    summary_df = pd.DataFrame(
        {
            t("Field"): list(summary_data.keys()),
            t("Value"): list(summary_data.values())
        }
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # PDF REPORT (kept English - FPDF has no Arabic glyphs)
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

    if "High Risk" in result:
        st.error(f"🔴 {t('Result')}: {result}")
    elif "Moderate Risk" in result:
        st.warning(f"⚠️ {t('Result')}: {result}")
    else:
        st.success(f"🟢 {t('Result')}: {result}")

    st.divider()

    # ==========================================
    # ACTIONS: Back / Save Result / Download PDF
    # ==========================================

    col1, col2, col3 = st.columns(3)

    # ==========================
    # BACK
    # ==========================

    with col1:

        if st.button(
            t("⬅ Back"),
            use_container_width=True
        ):

            st.session_state.page = 2
            st.rerun()

    # ==========================
    # SAVE
    # ==========================

    with col2:

        if st.button(
            t("💾 Save Result"),
            use_container_width=True
        ):

            try:

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

                st.success(t("Saved Successfully ✅"))

            except Exception as e:

                st.error(f"{t('Database Error : ')}{e}")

    # ==========================
    # PDF
    # ==========================

    with col3:

        try:

            pdf_path = generate_pdf(report)

            with open(pdf_path,"rb") as file:

                st.download_button(
                    t("📄 Download PDF"),
                    data=file.read(),
                    file_name="HealthVibe_Thrombosis_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        except Exception as e:

            st.error(f"{t('PDF Error : ')}{e}")

    st.write("")

    if st.button(
        t("🏠 Back To Dashboard"),
        use_container_width=True
    ):

        st.switch_page("pages/Dashboard.py")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(f"""

<div class="hv-footer">

<h3 style="color:#00C2FF;">
HealthVibe AI
</h3>

<p style="color:gray;margin:2px 0;">
{t("Version")} 1.0 &nbsp;|&nbsp; {t("AI Model")}: Random Forest
</p>

<p style="color:gray;margin:2px 0;">
{t("Artificial Intelligence Disease Prediction Platform")}
</p>

<p style="color:gray;margin:2px 0;">
{t("Developed by ")}<b>Visionaries</b> &copy; 2026
</p>

</div>

""",unsafe_allow_html=True)