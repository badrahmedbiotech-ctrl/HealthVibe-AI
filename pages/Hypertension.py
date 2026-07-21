import streamlit as st
import os
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders as email_encoders
from datetime import datetime
import pandas as pd
import joblib

# ================= EMAIL CONFIGURATION =================
# البيانات دي بتتقرا من ملف .streamlit/secrets.toml (مش مكتوبة هنا في الكود)،
# عشان تقدري ترفعي/تشاركي الملف ده من غير ما الباسورد يبان لحد.
#
# لازم يكون عندك ملف .streamlit/secrets.toml فيه:
#        EMAIL_USER = "your_email@gmail.com"
#        EMAIL_PASS = "الكود المكون من 16 حرف من غير مسافات"
SENDER_EMAIL = st.secrets["EMAIL_USER"]
SENDER_APP_PASSWORD = st.secrets["EMAIL_PASS"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# ==========================================================

st.set_page_config(page_title="Hypertension Assessment - HealthVibe AI", layout="wide", page_icon="🩸")

# ================= THEME =================
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .block-container { padding-top: 2rem; }
    .hv-header { font-size: 34px; font-weight: 800; color: #f1f5f9; margin-bottom: 2px; }
    .hv-sub { color: #94a3b8; font-size: 15px; margin-bottom: 20px; }
    .hv-card {
        background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px; padding: 22px 24px; margin-bottom: 18px;
    }
    .hv-card h4 { color: #e2e8f0; margin-top: 0; margin-bottom: 14px; font-size: 18px; }
    .stButton>button {
        background: linear-gradient(90deg, #06b6d4, #2563eb) !important; color: white !important;
        border: none !important; border-radius: 10px !important; padding: 11px 26px !important;
        font-size: 16px !important; font-weight: 700 !important; width: 100%; transition: 0.25s ease;
    }
    .stButton>button:hover { opacity: 0.9; transform: translateY(-1px); }
    .result-card {
        background: rgba(30, 41, 59, 0.6); border-radius: 14px; padding: 26px;
        text-align: center; border-top: 4px solid #e11d48;
    }
    .result-card.safe { border-top: 4px solid #10b981; }
    .rec-box { border-radius: 10px; padding: 18px; margin-top: 12px; line-height: 1.7; }
    .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-right: 6px; }
    .badge-model { background: rgba(37, 99, 235, 0.2); color: #60a5fa; }
    .badge-info { background: rgba(148, 163, 184, 0.15); color: #94a3b8; }
    .step-label { color: #60a5fa; font-weight: 700; font-size: 13px; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# ================= LOAD MODEL & FEATURE ORDER =================
MODEL_PATH = os.path.join("models", "hypertension_model.pkl")
FEATURES_PATH = os.path.join("models", "trained_features.pkl")

if not all(os.path.exists(p) for p in [MODEL_PATH, FEATURES_PATH]):
    st.error("⚠️ Model or feature files are missing. Please run train_hypertension.py first.")
    st.stop()

@st.cache_resource
def load_assets():
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
    return model, features

model, MODEL_FEATURES = load_assets()

OCCUPATIONS = [
    "Office / Desk Job", "IT / Software", "Teacher", "Healthcare Worker",
    "Driver / Transport", "Military / Police / Security", "Construction / Manual Labor",
    "Sales / Customer Service", "Business Owner / Executive", "Student",
    "Homemaker", "Unemployed / Retired", "Other (please specify)",
]
HIGH_STRESS_OCCUPATIONS = {
    "Healthcare Worker", "Driver / Transport", "Military / Police / Security",
    "Construction / Manual Labor", "Business Owner / Executive",
}

DISEASES_EXTRA = {  # not seen by the trained model -> informational + rule-based adjustment only
    "Kidney Disease": {"unit": "Creatinine (mg/dL)", "high": 1.3, "points": 8, "type_options": None},
    "Thyroid Disorder": {"unit": None, "high": None, "points": 3,
                          "type_options": ["Underactive (Hypothyroidism)", "Overactive (Hyperthyroidism)", "Not sure / Other"]},
    "Heart Disease": {"unit": None, "high": None, "points": 10,
                       "type_options": ["Coronary Artery Disease", "Heart Failure", "Arrhythmia (irregular heartbeat)", "Valve Disease", "Not sure / Other"]},
}

MEDICATION_NAME_OPTIONS = [
    "Lisinopril (ACE Inhibitor)", "Enalapril (ACE Inhibitor)", "Losartan (ARB)", "Valsartan (ARB)",
    "Amlodipine (Calcium Channel Blocker)", "Metoprolol (Beta Blocker)", "Atenolol (Beta Blocker)",
    "Bisoprolol (Beta Blocker)", "Hydrochlorothiazide (Diuretic)", "Furosemide (Diuretic)",
    "Other (please specify)",
]

ACTIVITY_TYPES = [
    ("🚶 Walking", "Walking"), ("🏃 Running / Jogging", "Running"), ("🚴 Cycling", "Cycling"),
    ("🏋️ Weight training", "Weight training"), ("🧘 Yoga / Stretching", "Yoga"),
    ("⚽ Football", "Football"), ("🏊 Swimming", "Swimming"), ("🎾 Tennis / Racket sports", "Tennis"),
    ("🤸 Other (please specify)", "Other"),
]

SYMPTOM_OPTIONS = ["Headache", "Dizziness", "Blurred vision", "Chest pain",
                    "Shortness of breath", "Nosebleeds", "Fatigue", "Palpitations"]

BP_HISTORY_OPTIONS = [
    "Normal",
    "Low (Hypotension)",
    "Borderline Low (before hypotension)",
    "Prehypertension (borderline high)",
    "High (Hypertension)",
    "Other / Not sure",
]

FAMILY_HISTORY_OPTIONS = ["Hypertension", "Diabetes", "Heart Disease", "Stroke", "Kidney Disease"]
FAMILY_HISTORY_POINTS = {"Hypertension": 3, "Heart Disease": 3, "Diabetes": 2, "Stroke": 3, "Kidney Disease": 2}

ACTIVITY_LEVELS = [
    "Sedentary (little to no exercise)",
    "Light (1-2 times/week)",
    "Moderate (3-4 times/week)",
    "Active (5+ times/week)",
]

STRESS_LEVELS = ["Low", "Moderate", "High", "Very High"]
SLEEP_OPTIONS = ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"]
SALT_OPTIONS = ["Low", "Moderate", "High"]

RECOMMENDATIONS = {
    1: {
        "title": "⚠️ Important guidance for managing high blood pressure risk",
        "bg": "#3f1723", "border": "#7f1d3a", "title_color": "#fda4af", "text_color": "#fecdd3",
        "items": [
            "Reduce sodium intake: avoid added salt, pickles, processed and fast food.",
            "Monitor daily: check and log your blood pressure twice a day.",
            "Improve lifestyle: 30 minutes of brisk activity daily, stay well hydrated.",
            "See a specialist: confirm these results with lab tests and a treatment plan.",
        ],
    },
    0: {
        "title": "✅ Guidance to keep your blood pressure healthy and stable",
        "bg": "#0f2e22", "border": "#16513c", "title_color": "#6ee7b7", "text_color": "#a7f3d0",
        "items": [
            "Follow a DASH-style diet: vegetables, fresh fruit, whole grains, lean protein.",
            "Manage stress: get enough sleep and practice relaxation exercises.",
            "Protect your heart: avoid smoking and excess caffeine.",
            "Keep up annual preventive checkups.",
        ],
    },
}

# ================= SESSION STATE =================
STEPS = ["Personal Info", "Blood Pressure", "Symptoms", "Medical History", "Medications",
         "Lifestyle & Vitals", "Additional Lab Uploads", "Report"]
if "step" not in st.session_state:
    st.session_state.step = 0
if "a" not in st.session_state:
    st.session_state.a = {}
if "result" not in st.session_state:
    st.session_state.result = None

def go_next():
    st.session_state.step = min(st.session_state.step + 1, len(STEPS) - 1)

def go_back():
    st.session_state.step = max(st.session_state.step - 1, 0)

a = st.session_state.a

st.markdown("<div class='hv-header'>🩸 Hypertension Risk Assessment</div>", unsafe_allow_html=True)
st.markdown("<div class='hv-sub'>A complete, step-by-step AI-powered blood pressure risk evaluation.</div>", unsafe_allow_html=True)
st.progress(st.session_state.step / (len(STEPS) - 1))
st.markdown(f"<div class='step-label'>STEP {st.session_state.step + 1} / {len(STEPS)} — {STEPS[st.session_state.step].upper()}</div><br>", unsafe_allow_html=True)

step = st.session_state.step

# ---------------- STEP 0: Personal Info ----------------
if step == 0:
    st.markdown("<div class='hv-card'><h4>👤 Personal Information</h4>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        a["full_name"] = st.text_input("Full Name", value=a.get("full_name", ""))
        a["age"] = st.number_input("Age", min_value=18, max_value=110, value=a.get("age", 45), step=1)
        a["email"] = st.text_input("Email (to receive your PDF report)", value=a.get("email", ""))
    with c2:
        gender_default = a.get("gender", "Male")
        a["gender"] = st.selectbox("Gender", ["Male", "Female"], index=["Male", "Female"].index(gender_default))
        a["weight_kg"] = st.number_input("Weight (kg)", min_value=20.0, max_value=250.0, value=a.get("weight_kg", 75.0), step=0.5)
    with c3:
        occ_default = a.get("occupation_choice", OCCUPATIONS[0])
        occ_idx = OCCUPATIONS.index(occ_default) if occ_default in OCCUPATIONS else 0
        a["occupation_choice"] = st.selectbox("Occupation", OCCUPATIONS, index=occ_idx)
        if a["occupation_choice"] == "Other (please specify)":
            a["occupation_custom"] = st.text_input("Please specify your occupation", value=a.get("occupation_custom", ""))
        a["height_cm"] = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=a.get("height_cm", 170.0), step=0.5)

    bmi = a["weight_kg"] / ((a["height_cm"] / 100) ** 2)
    a["bmi"] = bmi
    st.info(f"📐 Your BMI is automatically calculated: **{bmi:.1f}**")
    st.markdown("</div>", unsafe_allow_html=True)
    st.button("Next →", on_click=go_next)

# ---------------- STEP 1: Blood Pressure ----------------
elif step == 1:
    st.markdown("<div class='hv-card'><h4>🩺 Blood Pressure Reading</h4>", unsafe_allow_html=True)
    st.caption("Please enter your most recent measurement.")
    c1, c2 = st.columns(2)
    with c1:
        a["sysBP"] = st.number_input("Systolic (top number, mmHg)", min_value=70, max_value=260, value=a.get("sysBP", 120), step=1)
    with c2:
        a["diaBP"] = st.number_input("Diastolic (bottom number, mmHg)", min_value=40, max_value=160, value=a.get("diaBP", 80), step=1)

    if a["sysBP"] >= 140 or a["diaBP"] >= 90:
        category = "High Blood Pressure (Hypertension range)"
    elif a["sysBP"] >= 120 or a["diaBP"] >= 80:
        category = "Prehypertension range"
    else:
        category = "Normal range"
    st.info(f"Reference category based on standard guidelines: **{category}**")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hv-card'><h4>📈 Blood Pressure History <span class='badge badge-info'>reference only</span></h4>", unsafe_allow_html=True)
    st.caption("How has your blood pressure usually been over time — not just today's reading?")
    bp_hist_default = a.get("bp_history", BP_HISTORY_OPTIONS[0])
    bp_hist_idx = BP_HISTORY_OPTIONS.index(bp_hist_default) if bp_hist_default in BP_HISTORY_OPTIONS else 0
    a["bp_history"] = st.selectbox("Usual blood pressure pattern", BP_HISTORY_OPTIONS, index=bp_hist_idx)
    if a["bp_history"] == "Other / Not sure":
        c1, c2 = st.columns(2)
        with c1:
            a["bp_history_sys"] = st.number_input("Your expected/usual systolic (if known)", min_value=70, max_value=260, value=a.get("bp_history_sys", 120), step=1)
        with c2:
            a["bp_history_dia"] = st.number_input("Your expected/usual diastolic (if known)", min_value=40, max_value=160, value=a.get("bp_history_dia", 80), step=1)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go_back)
    c2.button("Next →", on_click=go_next)

# ---------------- STEP 2: Symptoms ----------------
elif step == 2:
    st.markdown("<div class='hv-card'><h4>🤕 Current Symptoms <span class='badge badge-model'>affects your risk score</span></h4>", unsafe_allow_html=True)
    a["symptoms"] = st.multiselect("Select any symptoms you currently experience", SYMPTOM_OPTIONS, default=a.get("symptoms", []))
    a["other_symptoms"] = st.text_input("Other symptoms (optional)", value=a.get("other_symptoms", ""))
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go_back)
    c2.button("Next →", on_click=go_next)

# ---------------- STEP 3: Medical History ----------------
elif step == 3:
    st.markdown("<div class='hv-card'><h4>📋 Medical History</h4>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        diab_default = a.get("diabetes", "No")
        a["diabetes"] = st.selectbox("Do you have diabetes?", ["No", "Yes"], index=["No", "Yes"].index(diab_default))
        if a["diabetes"] == "Yes":
            a["glucose"] = st.number_input("Fasting Glucose (mg/dL)", min_value=40, max_value=400, value=a.get("glucose", 120), step=1)
        else:
            a.setdefault("glucose", 90)
        a["totChol"] = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=a.get("totChol", 200), step=1)
    with c2:
        hr_mode_default = a.get("heartRate_mode", "I know the exact number")
        hr_mode_opts = ["I know the exact number", "Not sure — let me estimate"]
        a["heartRate_mode"] = st.radio("Resting Heart Rate", hr_mode_opts,
                                        index=hr_mode_opts.index(hr_mode_default) if hr_mode_default in hr_mode_opts else 0,
                                        horizontal=True)
        if a["heartRate_mode"] == "I know the exact number":
            a["heartRate"] = st.number_input("Resting Heart Rate (bpm)", min_value=40, max_value=200, value=a.get("heartRate", 75), step=1)
        else:
            hr_opts = ["Slow (below 60 bpm)", "Normal (60–100 bpm)", "Fast (above 100 bpm)"]
            hr_map = {"Slow (below 60 bpm)": 55, "Normal (60–100 bpm)": 75, "Fast (above 100 bpm)": 110}
            hr_choice_default = a.get("heartRate_choice", hr_opts[1])
            hr_choice_idx = hr_opts.index(hr_choice_default) if hr_choice_default in hr_opts else 1
            a["heartRate_choice"] = st.selectbox("Roughly how would you describe it?", hr_opts, index=hr_choice_idx)
            a["heartRate"] = hr_map[a["heartRate_choice"]]

    st.markdown("<br>**Other conditions**", unsafe_allow_html=True)
    a.setdefault("diseases", {})
    for disease, meta in DISEASES_EXTRA.items():
        c1, c2, c3 = st.columns([1.2, 1, 1.5])
        disease_info = a["diseases"].get(disease, {})
        with c1:
            has_it = st.selectbox(disease, ["No", "Yes"], key=f"dis_{disease}",
                                   index=["No", "Yes"].index(disease_info.get("has", "No")))
        value = None
        dtype = None
        if has_it == "Yes" and meta["unit"]:
            with c2:
                value = st.number_input(meta["unit"], min_value=0.0, value=float(disease_info.get("value") or 0.0), key=f"val_{disease}")
        elif has_it == "Yes" and meta.get("type_options"):
            with c2:
                type_opts = meta["type_options"]
                default_type = disease_info.get("type", type_opts[0])
                dtype = st.selectbox("Type", type_opts, index=type_opts.index(default_type) if default_type in type_opts else 0, key=f"type_{disease}")
                if dtype == "Not sure / Other":
                    dtype = st.text_input("Please specify", value=disease_info.get("type_custom", ""), key=f"typecustom_{disease}")
        lab_file = None
        if has_it == "Yes":
            with c3:
                lab_file = st.file_uploader(f"Upload {disease} lab report (optional)", type=["png", "jpg", "jpeg", "pdf"], key=f"file_{disease}")
        a["diseases"][disease] = {"has": has_it, "value": value, "type": dtype, "file": lab_file}

    a["other_conditions"] = st.text_area("Other medical conditions (optional)", value=a.get("other_conditions", ""), height=120)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hv-card'><h4>👪 Family & Medical History <span class='badge badge-info'>reference only</span></h4>", unsafe_allow_html=True)
    st.caption("Does anyone in your immediate family (parents/siblings) have any of the following?")
    a["family_history"] = st.multiselect("Family history", FAMILY_HISTORY_OPTIONS, default=a.get("family_history", []))
    a["family_history_other"] = st.text_input("Other family medical history (optional)", value=a.get("family_history_other", ""))
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go_back)
    c2.button("Next →", on_click=go_next)

# ---------------- STEP 4: Medications ----------------
elif step == 4:
    st.markdown("<div class='hv-card'><h4>💊 Medications</h4>", unsafe_allow_html=True)
    bp_meds_default = a.get("bp_meds", "No")
    a["bp_meds"] = st.selectbox("Are you currently taking any blood pressure medication?", ["No", "Yes"],
                                 index=["No", "Yes"].index(bp_meds_default))
    if a["bp_meds"] == "Yes":
        med_default = a.get("med_choice", MEDICATION_NAME_OPTIONS[0])
        med_idx = MEDICATION_NAME_OPTIONS.index(med_default) if med_default in MEDICATION_NAME_OPTIONS else 0
        a["med_choice"] = st.selectbox("Medication name (optional, for your record)", MEDICATION_NAME_OPTIONS, index=med_idx)
        if a["med_choice"] == "Other (please specify)":
            a["med_custom"] = st.text_input("Please type the medication name", value=a.get("med_custom", ""))
        c1, c2 = st.columns(2)
        with c1:
            a["med_photo_upload"] = st.file_uploader("Or upload a photo of the medication box", type=["png", "jpg", "jpeg"])
        with c2:
            a["med_photo_camera"] = st.camera_input("Or take a photo now")
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go_back)
    c2.button("Next →", on_click=go_next)

# ---------------- STEP 5: Lifestyle & Vitals ----------------
elif step == 5:
    st.markdown("<div class='hv-card'><h4>🚬 Smoking & Alcohol</h4>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        smoker_default = a.get("currentSmoker", "No")
        a["currentSmoker"] = st.selectbox("Do you currently smoke?", ["No", "Yes"],
                                           index=["No", "Yes"].index(smoker_default))
        if a["currentSmoker"] == "Yes":
            a["cigsPerDay"] = st.number_input("Cigarettes per day", min_value=0, max_value=80, value=a.get("cigsPerDay", 5), step=1)
        else:
            a["cigsPerDay"] = 0
    with c2:
        alcohol_default = a.get("alcohol", "Never")
        a["alcohol"] = st.selectbox("Alcohol consumption", ["Never", "Occasionally", "Regularly"],
                                     index=["Never", "Occasionally", "Regularly"].index(alcohol_default))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hv-card'><h4>🏃 Physical Activity</h4>", unsafe_allow_html=True)
    activity_level_default = a.get("activity_level", ACTIVITY_LEVELS[0])
    activity_level_idx = ACTIVITY_LEVELS.index(activity_level_default) if activity_level_default in ACTIVITY_LEVELS else 0
    a["activity_level"] = st.selectbox("Physical Activity Level", ACTIVITY_LEVELS, index=activity_level_idx)

    if a["activity_level"] != ACTIVITY_LEVELS[0]:
        activity_labels = [label for label, _ in ACTIVITY_TYPES]
        default_labels = [lbl for lbl in a.get("activity_types_display", []) if lbl in activity_labels]
        a["activity_types_display"] = st.multiselect(
            "What type(s) of activity do you do? (pick all that apply)", activity_labels, default=default_labels
        )
        a["activity_types"] = [val for label, val in ACTIVITY_TYPES if label in a["activity_types_display"]]
        if "Other" in a["activity_types"]:
            a["activity_other"] = st.text_input("Please specify the activity/sport name", value=a.get("activity_other", ""))
    else:
        a["activity_types_display"] = []
        a["activity_types"] = []
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hv-card'><h4>🧠 Stress, Sleep & Diet</h4>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        stress_default = a.get("stress_level", STRESS_LEVELS[0])
        a["stress_level"] = st.selectbox("Stress Level", STRESS_LEVELS, index=STRESS_LEVELS.index(stress_default))
    with c2:
        sleep_default = a.get("avg_sleep", SLEEP_OPTIONS[2])
        sleep_idx = SLEEP_OPTIONS.index(sleep_default) if sleep_default in SLEEP_OPTIONS else 2
        a["avg_sleep"] = st.selectbox("Average Sleep", SLEEP_OPTIONS, index=sleep_idx)
    with c3:
        salt_default = a.get("salt_intake", SALT_OPTIONS[0])
        a["salt_intake"] = st.selectbox("Salt Intake", SALT_OPTIONS, index=SALT_OPTIONS.index(salt_default))
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go_back)
    c2.button("Next →", on_click=go_next)

# ---------------- STEP 6: Additional Lab Uploads ----------------
elif step == 6:
    st.markdown("<div class='hv-card'><h4>🧪 Additional Lab Uploads <span class='badge badge-info'>reference only</span></h4>", unsafe_allow_html=True)
    a["extra_labs_text"] = st.text_area("Any other lab values you'd like to record (optional)", value=a.get("extra_labs_text", ""))
    c1, c2 = st.columns(2)
    with c1:
        a["extra_files_upload"] = st.file_uploader("Upload additional lab photos/files", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    with c2:
        a["extra_files_camera"] = st.camera_input("Or take a photo of a lab result")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go_back)
    c2.button("Next →", on_click=go_next)

# ---------------- STEP 7: Report ----------------
elif step == 7:
    st.markdown("<div class='hv-card'><h4>✅ Ready to Analyze</h4>", unsafe_allow_html=True)
    st.write("Review your information using the Back button if needed, then generate your report.")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go_back)
    analyze_clicked = c2.button("🔍 Analyze and Generate Report")

    if analyze_clicked:
        male = 1 if a["gender"] == "Male" else 0
        current_smoker = 1 if a["currentSmoker"] == "Yes" else 0
        bp_meds = 1 if a["bp_meds"] == "Yes" else 0
        diabetes = 1 if a["diabetes"] == "Yes" else 0

        pulse_pressure = a["sysBP"] - a["diaBP"]
        mean_arterial_pressure = a["diaBP"] + (pulse_pressure / 3)
        age_bmi = a["age"] * a["bmi"]
        smoking_load = current_smoker * a["cigsPerDay"]

        row = {
            "male": male, "age": a["age"], "currentSmoker": current_smoker, "cigsPerDay": a["cigsPerDay"],
            "BPMeds": bp_meds, "diabetes": diabetes, "totChol": a["totChol"], "sysBP": a["sysBP"],
            "diaBP": a["diaBP"], "BMI": a["bmi"], "heartRate": a["heartRate"], "glucose": a["glucose"],
            "pulse_pressure": pulse_pressure, "mean_arterial_pressure": mean_arterial_pressure,
            "age_bmi": age_bmi, "smoking_load": smoking_load,
        }
        input_df = pd.DataFrame([row])[MODEL_FEATURES]

        ml_prediction = int(model.predict(input_df)[0])
        ml_risk = float(model.predict_proba(input_df)[0][1] * 100)

        # ---- Rule-based clinical adjustment for factors outside the model ----
        adjustments = []
        for disease, meta in DISEASES_EXTRA.items():
            info = a["diseases"].get(disease, {})
            if info.get("has") == "Yes":
                pts = meta["points"]
                if meta["unit"] and info.get("value") and meta["high"] and info["value"] >= meta["high"]:
                    pts += 3
                label = disease
                if info.get("type"):
                    label = f"{disease} ({info['type']})"
                adjustments.append((label, pts))

        n_symptoms = len([s for s in a.get("symptoms", []) if s])
        if n_symptoms:
            adjustments.append((f"Reported symptoms ({n_symptoms})", min(n_symptoms * 2, 10)))

        if a["occupation_choice"] in HIGH_STRESS_OCCUPATIONS:
            adjustments.append(("High-stress occupation", 3))

        if a["alcohol"] == "Regularly":
            adjustments.append(("Regular alcohol consumption", 4))
        elif a["alcohol"] == "Occasionally":
            adjustments.append(("Occasional alcohol consumption", 2))

        # -- Blood pressure history --
        bp_history = a.get("bp_history")
        if bp_history == "High (Hypertension)":
            adjustments.append(("Self-reported history of high blood pressure", 3))
        elif bp_history == "Prehypertension (borderline high)":
            adjustments.append(("Self-reported borderline high blood pressure history", 1))
        elif bp_history == "Other / Not sure":
            sys_o, dia_o = a.get("bp_history_sys"), a.get("bp_history_dia")
            if sys_o and dia_o:
                if sys_o >= 140 or dia_o >= 90:
                    adjustments.append(("Reported usual BP in hypertension range", 3))
                elif sys_o >= 120 or dia_o >= 80:
                    adjustments.append(("Reported usual BP in prehypertension range", 1))

        # -- Family history --
        for fam in a.get("family_history", []):
            adjustments.append((f"Family history of {fam}", FAMILY_HISTORY_POINTS.get(fam, 2)))

        # -- Physical activity --
        if a.get("activity_level") == ACTIVITY_LEVELS[0]:
            adjustments.append(("Sedentary lifestyle", 3))
        elif a.get("activity_level") == ACTIVITY_LEVELS[1]:
            adjustments.append(("Low physical activity", 1))

        # -- Stress --
        if a.get("stress_level") == "High":
            adjustments.append(("High stress level", 2))
        elif a.get("stress_level") == "Very High":
            adjustments.append(("Very high stress level", 4))

        # -- Sleep --
        if a.get("avg_sleep") == "Less than 5 hours":
            adjustments.append(("Insufficient sleep (<5 hrs)", 3))
        elif a.get("avg_sleep") == "5-6 hours":
            adjustments.append(("Below-average sleep (5-6 hrs)", 1))

        # -- Salt intake --
        if a.get("salt_intake") == "High":
            adjustments.append(("High salt intake", 3))
        elif a.get("salt_intake") == "Moderate":
            adjustments.append(("Moderate salt intake", 1))

        total_adjustment = min(sum(p for _, p in adjustments), 25)
        final_risk = max(0.0, min(100.0, ml_risk + total_adjustment))
        final_prediction = 1 if final_risk >= 50 else 0

        st.session_state.result = {
            "ml_prediction": ml_prediction, "ml_risk": ml_risk,
            "adjustments": adjustments, "total_adjustment": total_adjustment,
            "final_risk": final_risk, "final_prediction": final_prediction,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

# ================= RESULTS =================
if st.session_state.result:
    r = st.session_state.result
    st.markdown("<hr style='border-color:#1e293b;margin:30px 0;'>", unsafe_allow_html=True)

    res_col1, res_col2 = st.columns([1, 2])
    with res_col1:
        card_class = "result-card" if r["final_prediction"] == 1 else "result-card safe"
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#94a3b8;margin-top:0;'>Predicted Result</h3>", unsafe_allow_html=True)
        if r["final_prediction"] == 1:
            st.markdown("<h2 style='color:#f87171;font-weight:800;'>High Risk ⚠️</h2>", unsafe_allow_html=True)
            st.metric("Overall Risk Score", f"{r['final_risk']:.1f}%")
        else:
            st.markdown("<h2 style='color:#34d399;font-weight:800;'>Normal / Low Risk ✅</h2>", unsafe_allow_html=True)
            st.metric("Overall Stability Score", f"{100 - r['final_risk']:.1f}%")
        st.caption(f"AI model base estimate: {r['ml_risk']:.1f}% • Clinical factors adjustment: +{r['total_adjustment']:.0f} pts")
        st.markdown("</div>", unsafe_allow_html=True)

    with res_col2:
        rec = RECOMMENDATIONS[r["final_prediction"]]
        items_html = "".join(f"<li style='margin-bottom:8px;'>{item}</li>" for item in rec["items"])
        st.markdown(f"""
        <div class='hv-card' style='border-right:4px solid #2563eb;'>
            <h4>📋 Medical Recommendations</h4>
            <div class='rec-box' style='background-color:{rec["bg"]};border:1px solid {rec["border"]};'>
                <strong style='color:{rec["title_color"]};font-size:16px;'>{rec["title"]}</strong>
                <ul style='margin-top:10px;color:{rec["text_color"]};padding-right:20px;'>{items_html}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if r["adjustments"]:
        st.markdown("<div class='hv-card'><h4>🧮 What contributed to your Clinical Factors adjustment</h4>", unsafe_allow_html=True)
        for label, pts in r["adjustments"]:
            st.write(f"• {label}: **+{pts} pts**")
        st.caption("Transparent, rule-based addition (capped at +25 pts), combined with — not a replacement for — the trained AI model's estimate.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("⚕️ This tool provides an AI-based estimate and is not a substitute for professional medical diagnosis. Please consult a doctor for confirmation.")

    def build_pdf():
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        from reportlab.lib import colors

        # ---- Color palette (kept consistent with the app's blue/teal theme) ----
        PRIMARY = colors.HexColor("#2563eb")
        TEAL = colors.HexColor("#06b6d4")
        DANGER = colors.HexColor("#e11d48")
        SUCCESS = colors.HexColor("#10b981")
        DARK = colors.HexColor("#1e293b")
        GRAY = colors.HexColor("#475569")
        LIGHT_BG = colors.HexColor("#f1f5f9")
        WHITE = colors.white

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4
        y = [height]  # mutable container so nested helpers can update it

        def new_page_if_needed(min_y=2.5 * cm):
            if y[0] < min_y:
                c.showPage()
                y[0] = height - 2 * cm

        def header_band():
            c.setFillColor(PRIMARY)
            c.rect(0, height - 3 * cm, width, 3 * cm, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(2 * cm, height - 1.7 * cm, "HealthVibe AI")
            c.setFont("Helvetica", 11)
            c.drawString(2 * cm, height - 2.4 * cm, "Hypertension Risk Assessment Report")
            c.setFont("Helvetica", 9)
            c.drawRightString(width - 2 * cm, height - 1.7 * cm, f"Generated: {r['generated_at']}")
            y[0] = height - 3.7 * cm

        def section_title(text):
            new_page_if_needed(3 * cm)
            c.setFillColor(PRIMARY)
            c.setFont("Helvetica-Bold", 13)
            c.drawString(2 * cm, y[0], text)
            y[0] -= 6
            c.setStrokeColor(TEAL)
            c.setLineWidth(1.2)
            c.line(2 * cm, y[0], width - 2 * cm, y[0])
            y[0] -= 16
            c.setFillColor(DARK)

        def body_line(text, size=10.5, gap=15, color=None, bold=False):
            new_page_if_needed()
            c.setFillColor(color or GRAY)
            c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
            c.drawString(2 * cm, y[0], text)
            y[0] -= gap

        def result_banner():
            new_page_if_needed(4.5 * cm)
            is_high = r["final_prediction"] == 1
            box_color = DANGER if is_high else SUCCESS
            label = "HIGH RISK" if is_high else "NORMAL / LOW RISK"
            c.setFillColor(box_color)
            c.roundRect(2 * cm, y[0] - 2.2 * cm, width - 4 * cm, 2.2 * cm, 8, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 17)
            c.drawCentredString(width / 2, y[0] - 1.05 * cm, f"{label}  —  {r['final_risk']:.1f}%")
            c.setFont("Helvetica", 9.5)
            c.drawCentredString(
                width / 2, y[0] - 1.7 * cm,
                f"AI model base estimate: {r['ml_risk']:.1f}%   |   Clinical factors adjustment: +{r['total_adjustment']:.0f} pts"
            )
            y[0] -= 2.7 * cm

        # ================= HEADER =================
        header_band()

        # ================= RESULT =================
        section_title("Result")
        result_banner()

        # ================= PATIENT INFO =================
        section_title("Patient Information")
        body_line(f"Name: {a.get('full_name') or '-'}     Age: {a.get('age')}     Gender: {a.get('gender')}")
        body_line(f"BMI: {a.get('bmi', 0):.1f}", gap=20)

        # ================= BLOOD PRESSURE & LABS =================
        section_title("Blood Pressure & Labs")
        body_line(f"Reading: {a.get('sysBP')}/{a.get('diaBP')} mmHg     Cholesterol: {a.get('totChol')} mg/dL")
        glucose_line = f"Glucose: {a.get('glucose')} mg/dL" if a.get("diabetes") == "Yes" else "Glucose: not applicable (no diabetes reported)"
        body_line(f"{glucose_line}     Heart rate: {a.get('heartRate')} bpm")
        bp_hist_line = a.get("bp_history", "-")
        if bp_hist_line == "Other / Not sure":
            bp_hist_line = f"Other (Expected ~{a.get('bp_history_sys', '-')}/{a.get('bp_history_dia', '-')} mmHg)"
        body_line(f"Blood pressure history: {bp_hist_line}", gap=20)

        # ================= SYMPTOMS =================
        section_title("Symptoms")
        body_line(", ".join(a.get("symptoms", [])) or "None reported", gap=20)

        # ================= MEDICAL HISTORY =================
        section_title("Medical History")
        med_display = ""
        if a.get("bp_meds") == "Yes":
            med_display = a.get("med_custom") if a.get("med_choice") == "Other (please specify)" and a.get("med_custom") else a.get("med_choice", "")
        body_line(f"Diabetes: {a.get('diabetes')}     BP medication: {a.get('bp_meds')}" + (f" ({med_display})" if med_display else ""))
        for disease in DISEASES_EXTRA:
            info = a["diseases"].get(disease, {})
            if info.get("has") == "Yes":
                extra = f" ({info['value']})" if info.get("value") else (f" ({info['type']})" if info.get("type") else "")
                body_line(f"  •  {disease}: Yes{extra}")
        fam_history = ", ".join(a.get("family_history", [])) or "None reported"
        if a.get("family_history_other"):
            fam_history += f"; {a.get('family_history_other')}"
        body_line(f"Family history: {fam_history}", gap=20)

        # ================= LIFESTYLE & VITALS =================
        section_title("Lifestyle & Vitals")
        body_line(f"Smoking: {a.get('currentSmoker')} ({a.get('cigsPerDay', 0)} cigs/day)     Alcohol: {a.get('alcohol')}")
        body_line(f"Physical activity level: {a.get('activity_level', '-')}")
        if a.get("activity_types_display"):
            activity_line = ", ".join(a.get("activity_types_display", []))
            if "Other" in a.get("activity_types", []) and a.get("activity_other"):
                activity_line += f" ({a.get('activity_other')})"
            body_line(f"Activity type(s): {activity_line}")
        body_line(f"Stress level: {a.get('stress_level', '-')}     Sleep: {a.get('avg_sleep', '-')}     Salt intake: {a.get('salt_intake', '-')}", gap=20)

        # ================= CLINICAL FACTORS ADJUSTMENT =================
        if r.get("adjustments"):
            section_title("What Contributed to the Clinical Factors Adjustment")
            for label_txt, pts in r["adjustments"]:
                body_line(f"  •  {label_txt}: +{pts} pts", gap=14)
            y[0] -= 6

        # ================= DISCLAIMER =================
        new_page_if_needed(2.5 * cm)
        c.setFillColor(LIGHT_BG)
        c.roundRect(2 * cm, y[0] - 1.6 * cm, width - 4 * cm, 1.6 * cm, 6, fill=1, stroke=0)
        c.setFillColor(GRAY)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(2.3 * cm, y[0] - 0.7 * cm,
                     "This tool provides an AI-based estimate and is not a substitute for professional")
        c.drawString(2.3 * cm, y[0] - 1.15 * cm,
                     "medical diagnosis. Please consult a doctor for confirmation.")
        y[0] -= 2.2 * cm

        # ================= LAB IMAGES =================
        images = []
        for disease, info in a.get("diseases", {}).items():
            if info.get("file") is not None and info["file"].type.startswith("image"):
                images.append((f"{disease} lab", info["file"]))
        if a.get("extra_files_upload"):
            for f in a["extra_files_upload"]:
                if f.type.startswith("image"):
                    images.append(("Additional lab", f))
        if a.get("extra_files_camera") is not None:
            images.append(("Camera capture", a["extra_files_camera"]))

        if images:
            c.showPage()
            y[0] = height - 2 * cm
            section_title("Attached Lab Images (for doctor's reference)")
            for label_img, f in images:
                try:
                    img = ImageReader(f)
                    body_line(label_img, 11, bold=True, gap=14)
                    new_page_if_needed(6.5 * cm)
                    c.drawImage(img, 2 * cm, y[0] - 6 * cm, width=8 * cm, height=6 * cm, preserveAspectRatio=True)
                    y[0] -= 6.5 * cm
                except Exception:
                    pass

        c.save()
        buf.seek(0)
        return buf

    pdf_col1, pdf_col2 = st.columns(2)
    with pdf_col1:
        try:
            pdf_bytes = build_pdf()
            st.download_button("⬇️ Download PDF Report", data=pdf_bytes,
                                file_name=f"hypertension_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf")
        except Exception as e:
            st.warning(f"Could not generate PDF ({e}). Make sure 'reportlab' is installed: pip install reportlab")

    with pdf_col2:
        if st.button("📧 Send Report to My Email"):
            recipient_email = a.get("email", "").strip()
            if not recipient_email or "@" not in recipient_email:
                st.error("Please go back to Step 1 and enter a valid email address.")
            else:
                try:
                    pdf_bytes_for_email = build_pdf()
                    msg = MIMEMultipart()
                    msg["From"] = SENDER_EMAIL
                    msg["To"] = recipient_email
                    msg["Subject"] = "Your HealthVibe AI Hypertension Risk Report"
                    body = (
                        f"Hi {a.get('full_name') or ''},\n\n"
                        "Please find attached your Hypertension Risk Assessment report.\n\n"
                        "This is an AI-based estimate and not a substitute for professional medical advice.\n\n"
                        "— HealthVibe AI"
                    )
                    msg.attach(MIMEText(body, "plain"))

                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(pdf_bytes_for_email.read())
                    email_encoders.encode_base64(part)
                    part.add_header("Content-Disposition", "attachment; filename=hypertension_report.pdf")
                    msg.attach(part)

                    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                        server.starttls()
                        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
                        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())

                    st.success(f"✅ Report sent successfully to {recipient_email}!")
                except Exception as e:
                    st.error(f"Could not send the email. Error: {e}")