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
    save_thrombosis,
    get_profile
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

# ==========================================================
# CHECK LOGIN FIRST (قبل كل شيء)
# ==========================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")
    st.stop()

sidebar()

# ==========================================================
# LOAD PATIENT PROFILE
# ==========================================================

user = st.session_state.get("user", {})
user_id = user.get("id")

profile = get_profile(user_id) if user_id else None

if profile:
    profile = dict(profile)

    # Load patient data automatically
    st.session_state.name = profile.get("full_name") or user.get("full_name", "")
    st.session_state.age = int(profile.get("age") or 45)
    st.session_state.gender = profile.get("gender") or "Male"
    st.session_state.weight = float(profile.get("weight") or 70)
    st.session_state.height = float(profile.get("height") or 170)
    st.session_state.blood_type = profile.get("blood_group") or "O+"

    # Optional: automatically use profile smoking status
    st.session_state.smoking = profile.get("smoking") or "No"

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

        # FIX: st.session_state.gender is stored as the raw English value
        # ("Male"/"Female") coming from the profile, but the selectbox
        # options are translated. Compare/derive against the translated
        # label so the correct option is pre-selected in any language,
        # and always store back the canonical English value ("Male"/
        # "Female") so downstream comparisons (page 3, model input,
        # BMI/report) stay consistent regardless of UI language.
        gender_options = [t("Male"), t("Female")]
        current_gender_label = t("Male") if st.session_state.gender == "Male" else t("Female")

        gender_choice = st.selectbox(
            t("Gender"),
            gender_options,
            index=gender_options.index(current_gender_label)
        )

        st.session_state.gender = "Male" if gender_choice == t("Male") else "Female"

        st.session_state.height = st.number_input(
            t("Height (cm)"),
            min_value=100.0,
            max_value=230.0,
            value=float(st.session_state.height)
        )

    with col2:

        st.session_state.weight = st.number_input(
            t("Weight (kg)"),
            min_value=20.0,
            max_value=250.0,
            value=float(st.session_state.weight)
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
            key="blood_type_select"
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

elif st.session_state.page == 2:

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
            t("Predict ➜"),
            use_container_width=True
        ):

            st.session_state.page = 3
            st.rerun()

# ==========================================================
# PAGE 3
# ==========================================================

elif st.session_state.page == 3:

    st.header(t("🤖 AI Prediction"))

    st.write(
        t("HealthVibe AI is analyzing your clinical data...")
    )

    st.divider()

    # ==========================================
    # PREPARE DATA + COMBINED RISK ASSESSMENT
    # ==========================================
    # IMPORTANT (why the scoring was rebuilt):
    # The trained Random Forest model only "sees" 5 raw features:
    # Age, Gender, Height, Weight and D-Dimer. It has NO visibility
    # into the 9 real clinical risk factors collected on Page 2
    # (previous DVT, recent surgery, immobility, swelling, pain,
    # family history, smoking, hypertension, diabetes) or into BMI.
    #
    # The previous version blended 60% model / 40% clinical score.
    # Because the model can't see the clinical picture at all, that
    # weighting let a weak/uninformed model output cap or dilute the
    # result even for patients with a textbook high-risk profile
    # (e.g. previous DVT + recent surgery + immobility + very high
    # D-Dimer could still land in "Moderate" instead of "High" if the
    # model happened to output a low probability). That is not
    # clinically defensible.
    #
    # Fix: the transparent, clinically-weighted score (modeled loosely
    # on the Wells DVT criteria + D-Dimer) is now the PRIMARY driver
    # (75%) since it is the only part of the pipeline that actually
    # reflects the patient's real symptoms and history. The trained
    # model is kept as a minor supporting signal (25%) rather than the
    # dominant one. BMI (obesity is an established DVT risk factor)
    # is now included, since height/weight were being collected but
    # never actually used as a risk factor before.

    gender = 1 if st.session_state.gender == "Male" else 0

    X = np.array([[
        float(st.session_state.age),
        float(gender),
        float(st.session_state.height),
        float(st.session_state.weight),
        float(st.session_state.d_dimer)
    ]], dtype=float)

    # Model probability (secondary/supporting signal only)
    X_scaled = scaler.transform(X)
    model_probability = float(model.predict_proba(X_scaled)[0][1] * 100)
    model_probability = float(np.clip(model_probability, 0, 100))

    # ------------------------------------------
    # BMI (obesity is a recognized DVT risk factor,
    # but height/weight were collected and never used for this)
    # ------------------------------------------
    height_m = max(float(st.session_state.height), 1.0) / 100.0
    BMI = round(float(st.session_state.weight) / (height_m ** 2), 1)

    if BMI >= 30:
        bmi_points = 6.0
    elif BMI >= 25:
        bmi_points = 3.0
    else:
        bmi_points = 0.0

    # ------------------------------------------
    # Clinical risk score (0-100)
    # ------------------------------------------
    # Transparent weights for the risk factors shown in the UI.
    # These sum to 100 at maximum (86 clinical checkboxes + 14 D-Dimer),
    # BMI can add a further 3-6 points, clipped at 100 overall.
    risk_weights = {
        "swelling": 12,
        "pain": 8,
        "history": 18,
        "mobility": 10,
        "surgery": 12,
        "family_history": 8,
        "smoking": 5,
        "hypertension": 5,
        "diabetes": 5,
        "cholesterol": 3
    }

    clinical_points = 0.0
    clinical_points += risk_weights["swelling"] if st.session_state.swelling == t("Yes") else 0
    clinical_points += risk_weights["pain"] if st.session_state.pain == t("Yes") else 0
    clinical_points += risk_weights["history"] if st.session_state.history == t("Yes") else 0
    clinical_points += risk_weights["mobility"] if st.session_state.mobility == t("Yes") else 0
    clinical_points += risk_weights["surgery"] if st.session_state.surgery == t("Yes") else 0
    clinical_points += risk_weights["family_history"] if st.session_state.family_history == t("Yes") else 0
    clinical_points += risk_weights["smoking"] if st.session_state.smoking == t("Yes") else 0
    clinical_points += risk_weights["hypertension"] if st.session_state.hypertension == t("Yes") else 0
    clinical_points += risk_weights["diabetes"] if st.session_state.diabetes == t("Yes") else 0
    clinical_points += risk_weights["cholesterol"] if st.session_state.cholesterol == t("Yes") else 0
    clinical_points += bmi_points

    # D-Dimer contribution.
    # 500 ng/mL is used as a common screening reference here; the exact
    # clinical cutoff depends on the assay and clinical context.
    d_dimer = float(st.session_state.d_dimer)

    if d_dimer <= 500:
        d_dimer_points = 0.0
    elif d_dimer <= 1000:
        d_dimer_points = 7.0
    elif d_dimer <= 2000:
        d_dimer_points = 10.0
    else:
        d_dimer_points = 14.0

    clinical_points += d_dimer_points
    clinical_score = float(np.clip(clinical_points, 0, 100))

    # ------------------------------------------
    # Final risk probability
    # ------------------------------------------
    # The trained model only sees 5 raw features (age, gender, height,
    # weight, D-Dimer) and has NO visibility into the 9 real clinical
    # risk factors or BMI. In practice this means it can (and does)
    # output a low probability even for a textbook high-risk patient
    # (e.g. previous DVT + recent surgery + immobility + active
    # swelling/pain) - blending it into the decision, even at a
    # reduced weight, still pulled genuinely high-risk cases below the
    # High Risk threshold. Since the model cannot be trusted to move
    # the result in a clinically sound direction, it is no longer part
    # of the decision at all. The final probability is now the
    # transparent clinical score itself - fully explainable from the
    # patient's own answers, and guaranteed to move monotonically with
    # the risk factors entered. The model's output is still computed
    # and shown separately in the report as a supporting AI signal,
    # but it never overrides the clinical picture.
    probability = float(np.clip(clinical_score, 0, 100))

    # Use ONE classification rule for the whole page.
    # Do not use model.predict() for the label because it can disagree
    # with the probability thresholds shown by the UI.
    if probability >= 70:
        result = t("🔴 High Risk")
    elif probability >= 35:
        result = t("🟡 Moderate Risk")
    else:
        result = t("🟢 Low Risk")

    st.session_state.risk_score = probability
    st.session_state.risk_result = result

    # ==========================================
    # SAVE RESULT
    # ==========================================

    if not st.session_state.saved_result:

        user = st.session_state.get("user", {})
        
        if user and user.get("id"):
            assessment_id = save_assessment(

                user["id"],

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

    if BMI >= 25:
        factors.append(t("Elevated BMI"))

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

        "BMI": BMI,

        "Blood Type":st.session_state.blood_type,

        "D-Dimer": st.session_state.d_dimer,
        "Leg Swelling": st.session_state.swelling,
        "Leg Pain": st.session_state.pain,
        "Previous Blood Clot": st.session_state.history,
        "Recent Immobility": st.session_state.mobility,
        "Recent Surgery": st.session_state.surgery,
        "Family History": st.session_state.family_history,
        "Smoking": st.session_state.smoking,
        "Hypertension": st.session_state.hypertension,
        "Diabetes": st.session_state.diabetes,
        "High Cholesterol": st.session_state.cholesterol,
        "AI Model Probability": f"{model_probability:.1f}%",
        "Clinical Risk Score": f"{clinical_score:.1f}/100",
        "Final Risk Probability": f"{probability:.1f}%",
        "Prediction": result

    }

    pdf_path = generate_pdf(report)

    with open(pdf_path,"rb") as file:

        st.download_button(

            t("📄 Download Report"),
            file,
            file_name="HealthVibe_Thrombosis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # ==========================================
    # RESULT STATUS DISPLAY
    # ==========================================

    result_status = band_label

    if "High Risk" in result_status:
        st.error(f"🔴 Result: {result_status}")
    elif "Moderate Risk" in result_status:
        st.warning(f"⚠️ Result: {result_status}")
    else:
        st.success(f"🟢 Result: {result_status}")

    st.divider()

    # ==========================================
    # QUICK ACTIONS
    # ==========================================

    d1, d2, d3 = st.columns([1, 2, 1])

    with d2:
        if st.button(
            t("🏠 Dashboard"),
            use_container_width=True,
            key="thrombosis_dashboard_button"
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