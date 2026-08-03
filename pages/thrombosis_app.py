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
# PAGE-LOCAL CSS (hero, cards, RTL)
# ==========================================================

st.markdown(
f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    direction: {DIR};
}}

.hv-hero {{
    background: linear-gradient(135deg, #0F2027 0%, #2C5364 60%, #00C2FF 100%);
    border-radius: 18px;
    padding: 36px 32px;
    color: #fff;
    text-align: {"right" if IS_RTL else "left"};
    margin-bottom: 18px;
}}
.hv-hero h1 {{
    margin: 8px 0 4px 0;
    font-size: 2rem;
}}
.hv-hero p {{
    opacity: .9;
    font-size: 1rem;
    margin: 0;
}}
.hv-badge {{
    display: inline-block;
    background: rgba(255,255,255,.15);
    border: 1px solid rgba(255,255,255,.35);
    padding: 6px 14px;
    border-radius: 999px;
    font-size: .85rem;
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

   HEAD
  origin/main
with st.form("thrombosis_form"):
    col1, col2 = st.columns(2)

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
# UI HELPER: DASHBOARD CARD
# ==========================================================

def render_card(col, icon, label, value):
    with col:
        st.markdown(
            f"""
            <div class="hv-card">
                <div style="font-size:1.6rem;">{icon}</div>
                <div style="opacity:.7;font-size:.85rem;margin-top:4px;">{label}</div>
                <div style="font-size:1.2rem;font-weight:700;margin-top:2px;">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================================
# HERO
# ==========================================================

st.markdown(
f"""
<div class="hv-hero">

<span class="hv-badge">
🩸 {t("AI Disease Screening")}
</span>

<h1>
{t("Thrombosis Risk Prediction")}
</h1>

<p>
{t("Artificial Intelligence Based Blood Clot Screening System")}
</p>

</div>
""",
unsafe_allow_html=True
)

# ==========================================================
# DASHBOARD
# ==========================================================

st.subheader(t("📊 AI Dashboard"))

m1,m2,m3,m4 = st.columns(4)

render_card(m1, "🩸", t("Disease"), t("Thrombosis"))
render_card(m2, "🤖", t("AI Model"), "Random Forest")
render_card(m3, "⚠", t("Risk Factors"), "10")
render_card(m4, "🟢", t("Status"), t("Ready"))

st.divider()

# ==========================================================
# PAGE 1
# ==========================================================

if st.session_state.page == 1:

    st.header(t("👤 Patient Information"))

    col1,col2 = st.columns(2)

    origin/main
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

      HEAD
if submit:
     HEAD

    # 1. 
    origin/main
    risk_score = 0
    features = []
    contributions = []

        st.session_state.height = st.number_input(
            t("Height (cm)"),
            min_value=100,
            max_value=230,
            value=st.session_state.height
        )
        origin/main
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

        st.session_state.blood_type = st.selectbox(
            t("Blood Type"),
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

    st.caption(t("Step 1 / 3"))

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

    st.progress(66)

    st.caption(t("Step 2 / 3"))

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
            t("Analyze ➜"),
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
    # RESULT CARD (display-only risk band, does NOT touch model output)
    # ==========================================

    if probability >= 70:
        band_class = "hv-result-high"
        band_label = t("High Risk")
    elif probability >= 35:
        band_class = "hv-result-moderate"
        band_label = t("Moderate Risk")
    else:
        band_class = "hv-result-low"
        band_label = t("Low Risk")

    st.markdown(
        f"""
        <div class="hv-result-card {band_class}">
            <div style="font-size:1rem;opacity:.85;">{t("AI Prediction Result")}</div>
            <div style="font-size:2.2rem;font-weight:800;margin:6px 0;">{probability:.1f}%</div>
            <div class="hv-badge-risk">{band_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    m1,m2 = st.columns(2)

    with m1:

        st.metric(

            t("Risk Probability"),

            f"{probability:.1f}%"

        )

    with m2:

        st.metric(

            t("Prediction"),

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

    pdf_path = generate_pdf(report)

    with open(pdf_path,"rb") as file:

        st.download_button(

            t("📄 Download Report"),

     HEAD

     origin/main
    if "High Risk" in result_status:
        st.error(f"🔴 Result: {result_status}")
    elif "Moderate Risk" in result_status:
        st.warning(f"⚠️ Result: {result_status}")
    else:
        st.success(f"🟢 Result: {result_status}")

            file,
       origin/main

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

            t("⬅ Back"),

            use_container_width=True

        ):

            st.session_state.page = 2

            st.rerun()

    with c2:

        if st.button(

            t("🏠 Dashboard"),

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
{t("Developed by ")}<b>Badr Ahmed</b> &copy; 2026
</p>

</div>

""",unsafe_allow_html=True)