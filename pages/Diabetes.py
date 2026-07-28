import streamlit as st

from components.auth_guard import require_patient

require_patient()

import joblib
import pandas as pd

# ==========================
# LOGIN CHECK
# ==========================

if "user" not in st.session_state:
    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state["user"]

from components.database import get_profile

profile = get_profile(user["id"])

if profile is None:
    st.warning("Please complete your profile first.")
    st.switch_page("pages/Profile.py")
    st.stop()

from utils.navigation import sidebar
from components.database import get_profile
from components.stepper import stepper
from components.result_card import result_card
from components.recommendation import recommendation
from components.patient_summary import patient_summary
from components.ai_gauge import ai_gauge
from components.loading_animation import ai_loading
from components.pdf_report import create_pdf

from components.database import (
    create_tables,
    save_patient
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩸",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================
# MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("models/diabetes_model.pkl")

model = load_model()

create_tables()

# ==========================================
# SESSION
# ==========================================

if "step" not in st.session_state:
    st.session_state.step = 1

if "patient" not in st.session_state:
    st.session_state.patient = {}

if "saved" not in st.session_state:
    st.session_state.saved = False

# ==========================================
# PREMIUM HERO
# ==========================================

progress = (st.session_state.step / 4) * 100

st.markdown(f"""
<div class="hero">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
flex-wrap:wrap;
gap:30px;
">

<div>

<h1>
🩸 Diabetes Prediction
</h1>

<p>
AI Clinical Decision Support System
</p>

<br>

<div style="
background:rgba(255,255,255,.08);
height:10px;
border-radius:20px;
overflow:hidden;
width:320px;
">

<div style="
width:{progress}%;
height:100%;
background:linear-gradient(90deg,#00C2FF,#2563EB);
">
</div>

</div>

<p style="margin-top:10px;">
Assessment Progress : Step {st.session_state.step} of 4
</p>

</div>

<div style="
font-size:95px;
">
🩸
</div>

</div>

</div>
""", unsafe_allow_html=True)

stepper(st.session_state.step)

st.write("")

# ==========================================
# STEP 1
# ==========================================

if st.session_state.step == 1:

    st.markdown("## 👤 Patient Information")
    st.caption("Basic information loaded automatically from your profile.")

    name = profile["full_name"] or ""
    age = profile["age"] or 20
    gender = profile["gender"] or "Male"
    weight = profile["weight"] or 70.0
    height = profile["height"] or 170.0

    st.success("✅ Patient information loaded from your profile.")
    m1, m2, m3 = st.columns(3)

    with m1:
      st.metric("Age", age)

    with m2:
      st.metric("Weight", f"{weight} kg")

    with m3:
      st.metric("Height", f"{height} cm")

    st.write("")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Full Name", value=name, disabled=True)
        st.number_input("Age", value=int(age), disabled=True)
        st.text_input("Gender", value=gender, disabled=True)

    with col2:
        st.number_input("Weight (kg)", value=float(weight), disabled=True)
        st.number_input("Height (cm)", value=float(height), disabled=True)

    st.write("")

    if st.button(
        "Next ➜",
        key="next_step1",
        use_container_width=True
    ):

        st.session_state.patient["name"] = name
        st.session_state.patient["age"] = age
        st.session_state.patient["gender"] = gender
        st.session_state.patient["weight"] = weight
        st.session_state.patient["height"] = height

        st.session_state.step = 2
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
# ==========================================
# STEP 2
# ==========================================

elif st.session_state.step == 2:

    st.subheader("🩺 Medical Information")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    pregnancies = st.number_input(
        "Pregnancies",
        min_value=0,
        max_value=20,
        value=st.session_state.patient.get("pregnancies", 0)
    )

    glucose = st.number_input(
        "Glucose",
        min_value=50,
        max_value=300,
        value=st.session_state.patient.get("glucose", 120)
    )

    blood_pressure = st.number_input(
        "Blood Pressure",
        min_value=40,
        max_value=200,
        value=st.session_state.patient.get("blood_pressure", 70)
    )

    insulin = st.number_input(
        "Insulin",
        min_value=0,
        max_value=900,
        value=st.session_state.patient.get("insulin", 80)
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back",
            key="back_step2",
            use_container_width=True
        ):
            st.session_state.step = 1
            st.rerun()

    with col2:

        if st.button(
            "Next ➜",
            key="next_step2",
            use_container_width=True
        ):

            st.session_state.patient["pregnancies"] = pregnancies
            st.session_state.patient["glucose"] = glucose
            st.session_state.patient["blood_pressure"] = blood_pressure
            st.session_state.patient["insulin"] = insulin

            st.session_state.step = 3
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)



# ==========================================
# STEP 3
# ==========================================
elif st.session_state.step == 3:

    st.subheader("📊 Additional Measurements")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    skin_thickness = st.number_input(
        "Skin Thickness",
        min_value=0,
        max_value=100,
        value=st.session_state.patient.get("skin_thickness", 20)
    )

    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=70.0,
        value=st.session_state.patient.get("bmi", 25.0)
    )

    pedigree = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        max_value=3.0,
        value=st.session_state.patient.get("pedigree", 0.500),
        format="%.3f"
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back",
            key="back_step3",
            use_container_width=True
        ):
            st.session_state.step = 2
            st.rerun()

    with col2:

        if st.button(
            "🤖 Analyze with AI",
            key="analyze_ai",
            use_container_width=True
        ):

            st.session_state.patient["pregnancies"] = pregnancies
            st.session_state.patient["glucose"] = glucose
            st.session_state.patient["blood_pressure"] = blood_pressure
            st.session_state.patient["skin_thickness"] = skin_thickness
            st.session_state.patient["insulin"] = insulin
            st.session_state.patient["bmi"] = bmi
            st.session_state.patient["pedigree"] = pedigree
            st.session_state.patient["age"] = age

            st.session_state.step = 4
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 4
# ==========================================

elif st.session_state.step == 4:

    st.markdown("""
    <div class="hero">

    <h1>🤖 AI Analysis Result</h1>

    <p>
    Your prediction has been successfully generated using our AI model.
    </p>

    </div>
    """, unsafe_allow_html=True)


    patient = st.session_state.patient

    input_data = pd.DataFrame(
    [[
        patient.get("pregnancies", 0),
        patient.get("glucose", 120),
        patient.get("blood_pressure", 70),
        patient.get("skin_thickness", 20),
        patient.get("insulin", 80),
        patient.get("bmi", 25.0),
        patient.get("pedigree", 0.5),
        patient.get("age", 20)
    ]],
    columns=[
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age"
    ]
)


    ai_loading()


    prediction = model.predict(input_data)[0]


    try:
        probability = model.predict_proba(input_data)[0][1]

    except Exception:
        probability = 0



    patient["prediction"] = int(prediction)
    patient["probability"] = float(probability)



    if not st.session_state.saved:

        patient["user_id"] = st.session_state.user["id"]

        try:
          save_patient(patient)
        except Exception as e:
          st.warning(f"Patient record was not saved: {e}")

        st.session_state.saved = True



    st.success("Analysis Completed Successfully ✅")

    st.balloons()



    ai_gauge(probability)



    st.write("")


    # ==============================
    # RESULT CARD
    # ==============================

    st.markdown("""
    <div class="card">

    <h2>🩺 Prediction Result</h2>

    </div>
    """, unsafe_allow_html=True)


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Risk Status",
            "Positive" if prediction else "Negative"
        )


    with col2:

        st.metric(
            "AI Confidence",
            f"{probability*100:.1f}%"
        )



    st.write("")


    # ==============================
    # PATIENT SUMMARY
    # ==============================

    st.markdown("""
    <div class="card">

    <h2>👤 Patient Summary</h2>

    </div>
    """, unsafe_allow_html=True)



    patient_summary({

        "Full Name": patient["name"],
        "Age": patient["age"],
        "Gender": patient["gender"],
        "Weight (kg)": patient["weight"],
        "Height (cm)": patient["height"],
        "Pregnancies": patient["pregnancies"],
        "Glucose": patient["glucose"],
        "Blood Pressure": patient["blood_pressure"],
        "Skin Thickness": patient["skin_thickness"],
        "Insulin": patient["insulin"],
        "BMI": patient["bmi"],
        "Pedigree": patient["pedigree"]

    })



    st.write("")
    st.divider()



    # ==============================
    # MEDICAL REPORT
    # ==============================

    st.markdown("""
    <div class="card">

    <h2>📄 Medical Report</h2>

    <p>
    Download your complete AI-generated medical report.
    </p>

    </div>
    """, unsafe_allow_html=True)



    pdf_file = create_pdf(patient)



    with open(pdf_file, "rb") as pdf:

        st.download_button(

            "⬇ Download PDF Report",

            data=pdf,

            file_name=pdf_file,

            mime="application/pdf",

            use_container_width=True

        )



    st.write("")
    st.divider()



    # ==============================
    # ACTION BUTTONS
    # ==============================


    st.markdown("""
    <div class="card">

    <h2>⚡ Quick Actions</h2>

    <p>
    Start a new prediction or edit your data.
    </p>

    </div>
    """, unsafe_allow_html=True)



    col1, col2 = st.columns(2)



    with col1:

        if st.button(
            "⬅ Back",
            key="back_step4",
            use_container_width=True
        ):

            st.session_state.step = 3
            st.rerun()



    with col2:

        if st.button(
            "🔄 New Assessment",
            key="new_assessment",
            use_container_width=True
        ):

            st.session_state.step = 1
            st.session_state.patient = {}
            st.session_state.saved = False

            st.rerun()