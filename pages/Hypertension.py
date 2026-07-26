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

from translations import get_text, get_lang_meta, DEFAULT_LANG

# Arabic shaping support for the PDF (reshape + right-to-left reorder)
# pip install arabic-reshaper python-bidi
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SHAPING_AVAILABLE = True
except ImportError:
    ARABIC_SHAPING_AVAILABLE = False

# ================= LANG SETUP =================
if "lang" not in st.session_state:
    st.session_state.lang = DEFAULT_LANG

lang = st.session_state.lang


def t(key):
    return get_text(lang, key)


def switch_lang():
    st.session_state.lang = "ar" if st.session_state.lang == "en" else "en"


meta = get_lang_meta(lang)

# ================= OPTION -> TRANSLATION KEY MAPS =================
# Every selectbox/multiselect keeps its ORIGINAL canonical English option
# list untouched (so all downstream comparisons/adjustments/PDF logic stay
# exactly as before) - we only change what's *displayed* via format_func.
OPTION_LABELS = {
    "Male": "male", "Female": "female",
    "Yes": "yes_option", "No": "no_option",

    "Office / Desk Job": "ht_occ_office",
    "IT / Software": "ht_occ_it",
    "Teacher": "ht_occ_teacher",
    "Healthcare Worker": "ht_occ_healthcare",
    "Driver / Transport": "ht_occ_driver",
    "Military / Police / Security": "ht_occ_military",
    "Construction / Manual Labor": "ht_occ_construction",
    "Sales / Customer Service": "ht_occ_sales",
    "Business Owner / Executive": "ht_occ_business",
    "Student": "ht_occ_student",
    "Homemaker": "ht_occ_homemaker",
    "Unemployed / Retired": "ht_occ_unemployed",
    "Other (please specify)": "ht_other_specify_option",

    "Kidney Disease": "ht_disease_kidney",
    "Thyroid Disorder": "ht_disease_thyroid",
    "Heart Disease": "ht_disease_heart",
    "Creatinine (mg/dL)": "ht_unit_creatinine",
    "Underactive (Hypothyroidism)": "ht_thyroid_under",
    "Overactive (Hyperthyroidism)": "ht_thyroid_over",
    "Not sure / Other": "ht_not_sure_other",
    "Coronary Artery Disease": "ht_heart_cad",
    "Heart Failure": "ht_heart_failure",
    "Arrhythmia (irregular heartbeat)": "ht_heart_arrhythmia",
    "Valve Disease": "ht_heart_valve",

    "Normal": "ht_bph_normal",
    "Low (Hypotension)": "ht_bph_low",
    "Borderline Low (before hypotension)": "ht_bph_borderline_low",
    "Prehypertension (borderline high)": "ht_bph_prehypertension",
    "High (Hypertension)": "ht_bph_high",
    "Other / Not sure": "ht_bph_other",

    "Hypertension": "hypertension_checkbox",
    "Diabetes": "diabetes_checkbox",
    "Stroke": "ht_stroke",

    "Sedentary (little to no exercise)": "ht_act_sedentary",
    "Light (1-2 times/week)": "ht_act_light",
    "Moderate (3-4 times/week)": "ht_act_moderate",
    "Active (5+ times/week)": "ht_act_active",

    "Low": "ht_level_low",
    "Moderate": "ht_level_moderate",
    "High": "ht_level_high",
    "Very High": "ht_level_very_high",

    "Less than 5 hours": "ht_sleep_lt5",
    "5-6 hours": "ht_sleep_5to6",
    "7-8 hours": "ht_sleep_7to8",
    "More than 8 hours": "ht_sleep_gt8",

    "Never": "ht_alcohol_never",
    "Occasionally": "ht_alcohol_occasionally",
    "Regularly": "ht_alcohol_regularly",

    "I know the exact number": "ht_hr_mode_exact",
    "Not sure — let me estimate": "ht_hr_mode_estimate",
    "Slow (below 60 bpm)": "ht_hr_slow",
    "Normal (60–100 bpm)": "ht_hr_normal_bpm",
    "Fast (above 100 bpm)": "ht_hr_fast",

    "Headache": "ht_symptom_headache",
    "Dizziness": "ht_symptom_dizziness",
    "Blurred vision": "ht_symptom_blurred_vision",
    "Chest pain": "ht_symptom_chest_pain",
    "Shortness of breath": "ht_symptom_shortness_breath",
    "Nosebleeds": "ht_symptom_nosebleeds",
    "Fatigue": "ht_symptom_fatigue",
    "Palpitations": "ht_symptom_palpitations",
}


def disp(value):
    """Translated display text for a canonical English option value.
    Free-text the user typed (not in the map) passes through unchanged."""
    key = OPTION_LABELS.get(value)
    return t(key) if key else value


# ================= EMAIL CONFIGURATION =================
def _get_email_credentials():
    try:
        return st.secrets["EMAIL_USER"], st.secrets["EMAIL_APP_PASSWORD"]
    except Exception:
        return "", ""


SENDER_EMAIL, SENDER_APP_PASSWORD = _get_email_credentials()
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# ==========================================================

st.set_page_config(page_title="Hypertension Assessment - HealthVibe AI", layout="wide", page_icon="🩸")

# ================= THEME (+ RTL/LTR + FONT FROM translations.py) =================
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        direction: {meta['dir']};
        font-family: '{meta['font']}', sans-serif;
    }}
    .main {{ background-color: #0e1117; }}
    .block-container {{ padding-top: 2rem; }}
    .hv-header {{ font-size: 34px; font-weight: 800; color: #f1f5f9; margin-bottom: 2px; }}
    .hv-sub {{ color: #94a3b8; font-size: 15px; margin-bottom: 20px; }}
    .hv-card {{
        background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px; padding: 22px 24px; margin-bottom: 18px;
    }}
    .hv-card h4 {{ color: #e2e8f0; margin-top: 0; margin-bottom: 14px; font-size: 18px; }}
    .stButton>button {{
        background: linear-gradient(90deg, #06b6d4, #2563eb) !important; color: white !important;
        border: none !important; border-radius: 10px !important; padding: 11px 26px !important;
        font-size: 16px !important; font-weight: 700 !important; width: 100%; transition: 0.25s ease;
    }}
    .stButton>button:hover {{ opacity: 0.9; transform: translateY(-1px); }}
    .result-card {{
        background: rgba(30, 41, 59, 0.6); border-radius: 14px; padding: 26px;
        text-align: center; border-top: 4px solid #e11d48;
    }}
    .result-card.safe {{ border-top: 4px solid #10b981; }}
    .rec-box {{ border-radius: 10px; padding: 18px; margin-top: 12px; line-height: 1.7; }}
    .badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-right: 6px; }}
    .badge-model {{ background: rgba(37, 99, 235, 0.2); color: #60a5fa; }}
    .badge-info {{ background: rgba(148, 163, 184, 0.15); color: #94a3b8; }}
    .step-label {{ color: #60a5fa; font-weight: 700; font-size: 13px; letter-spacing: 1px; }}
    </style>
""", unsafe_allow_html=True)

# ================= LANGUAGE SWITCH BUTTON =================
top_l, top_r = st.columns([6, 1])
with top_r:
    st.button(meta["switch_label"], on_click=switch_lang, key="lang_switch_btn_hypertension")

# ================= LOAD MODEL & FEATURE ORDER =================
MODEL_PATH = os.path.join("models", "hypertension_model.pkl")
FEATURES_PATH = os.path.join("models", "trained_features.pkl")

if not all(os.path.exists(p) for p in [MODEL_PATH, FEATURES_PATH]):
    st.error(t("ht_model_missing_error"))
    st.stop()


@st.cache_resource
def load_assets():
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
    return model, features


model, MODEL_FEATURES = load_assets()

# ---- Canonical (English) option lists - UNCHANGED from the original logic ----
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

DISEASES_EXTRA = {
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
# Note: drug names are kept as their standard English/Latin pharmaceutical
# names (common practice even in Arabic-language medical apps).

ACTIVITY_TYPES = [  # (emoji, translation_key, canonical_value)
    ("🚶", "ht_activity_walking", "Walking"),
    ("🏃", "ht_activity_running", "Running"),
    ("🚴", "ht_activity_cycling", "Cycling"),
    ("🏋️", "ht_activity_weight_training", "Weight training"),
    ("🧘", "ht_activity_yoga", "Yoga"),
    ("⚽", "ht_activity_football", "Football"),
    ("🏊", "ht_activity_swimming", "Swimming"),
    ("🎾", "ht_activity_tennis", "Tennis"),
    ("🤸", "ht_other_specify_option", "Other"),
]
ACT_VALUES = [val for _, _, val in ACTIVITY_TYPES]


def act_display(value):
    for emoji, key, val in ACTIVITY_TYPES:
        if val == value:
            return f"{emoji} {t(key)}"
    return value


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


def recommendations_for(final_prediction):
    """Build the (translated) recommendation block for the given result (0/1)."""
    if final_prediction == 1:
        return {
            "title": t("ht_rec_high_title"),
            "bg": "#3f1723", "border": "#7f1d3a", "title_color": "#fda4af", "text_color": "#fecdd3",
            "items": [t("ht_rec_high_item1"), t("ht_rec_high_item2"), t("ht_rec_high_item3"), t("ht_rec_high_item4")],
        }
    return {
        "title": t("ht_rec_low_title"),
        "bg": "#0f2e22", "border": "#16513c", "title_color": "#6ee7b7", "text_color": "#a7f3d0",
        "items": [t("ht_rec_low_item1"), t("ht_rec_low_item2"), t("ht_rec_low_item3"), t("ht_rec_low_item4")],
    }


# ================= SESSION STATE =================
STEP_KEYS = ["ht_step_personal_info", "ht_step_blood_pressure", "ht_step_symptoms", "ht_step_medical_history",
             "ht_step_medications", "ht_step_lifestyle_vitals", "ht_step_lab_uploads", "ht_step_report"]
if "step" not in st.session_state:
    st.session_state.step = 0
if "a" not in st.session_state:
    st.session_state.a = {}
if "result" not in st.session_state:
    st.session_state.result = None


def go_next():
    st.session_state.step = min(st.session_state.step + 1, len(STEP_KEYS) - 1)


def go_back():
    st.session_state.step = max(st.session_state.step - 1, 0)


a = st.session_state.a

st.markdown(f"<div class='hv-header'>{t('hypertension_title')}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='hv-sub'>{t('ht_subtitle')}</div>", unsafe_allow_html=True)
st.progress(st.session_state.step / (len(STEP_KEYS) - 1))
st.markdown(
    f"<div class='step-label'>{t('ht_step_word')} {st.session_state.step + 1} / {len(STEP_KEYS)} — "
    f"{t(STEP_KEYS[st.session_state.step]).upper()}</div><br>",
    unsafe_allow_html=True,
)

step = st.session_state.step

# ---------------- STEP 0: Personal Info ----------------
if step == 0:
    st.markdown(f"<div class='hv-card'><h4>{t('personal_info')}</h4>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        a["full_name"] = st.text_input(t("full_name"), value=a.get("full_name", ""))
        a["age"] = st.number_input(t("age"), min_value=18, max_value=110, value=a.get("age", 45), step=1)
        a["email"] = st.text_input(t("ht_email_hint_label"), value=a.get("email", ""))
    with c2:
        gender_default = a.get("gender", "Male")
        gender_idx = 0 if gender_default == "Male" else 1
        a["gender"] = st.selectbox(t("gender"), ["Male", "Female"], index=gender_idx, format_func=disp)
        a["weight_kg"] = st.number_input(t("weight"), min_value=20.0, max_value=250.0, value=a.get("weight_kg", 75.0), step=0.5)
    with c3:
        occ_default = a.get("occupation_choice", OCCUPATIONS[0])
        occ_idx = OCCUPATIONS.index(occ_default) if occ_default in OCCUPATIONS else 0
        a["occupation_choice"] = st.selectbox(t("occupation_label"), OCCUPATIONS, index=occ_idx, format_func=disp)
        if a["occupation_choice"] == "Other (please specify)":
            a["occupation_custom"] = st.text_input(t("ht_please_specify_occupation"), value=a.get("occupation_custom", ""))
        a["height_cm"] = st.number_input(t("height"), min_value=100.0, max_value=230.0, value=a.get("height_cm", 170.0), step=0.5)

    bmi = a["weight_kg"] / ((a["height_cm"] / 100) ** 2)
    a["bmi"] = bmi
    st.info(f"{t('ht_bmi_auto_msg')} **{bmi:.1f}**")
    st.markdown("</div>", unsafe_allow_html=True)
    st.button(t("next"), on_click=go_next)

# ---------------- STEP 1: Blood Pressure ----------------
elif step == 1:
    st.markdown(f"<div class='hv-card'><h4>{t('ht_bp_reading_header')}</h4>", unsafe_allow_html=True)
    st.caption(t("ht_bp_caption"))
    c1, c2 = st.columns(2)
    with c1:
        a["sysBP"] = st.number_input(t("ht_systolic_label"), min_value=70, max_value=260, value=a.get("sysBP", 120), step=1)
    with c2:
        a["diaBP"] = st.number_input(t("ht_diastolic_label"), min_value=40, max_value=160, value=a.get("diaBP", 80), step=1)

    if a["sysBP"] >= 140 or a["diaBP"] >= 90:
        category = t("ht_cat_high")
    elif a["sysBP"] >= 120 or a["diaBP"] >= 80:
        category = t("ht_cat_pre")
    else:
        category = t("ht_cat_normal")
    st.info(f"{t('ht_ref_category_prefix')} **{category}**")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='hv-card'><h4>{t('ht_bp_history_header')} "
        f"<span class='badge badge-info'>{t('ht_badge_reference_only')}</span></h4>",
        unsafe_allow_html=True,
    )
    st.caption(t("ht_bp_history_caption"))
    bp_hist_default = a.get("bp_history", BP_HISTORY_OPTIONS[0])
    bp_hist_idx = BP_HISTORY_OPTIONS.index(bp_hist_default) if bp_hist_default in BP_HISTORY_OPTIONS else 0
    a["bp_history"] = st.selectbox(t("ht_usual_bp_pattern_label"), BP_HISTORY_OPTIONS, index=bp_hist_idx, format_func=disp)
    if a["bp_history"] == "Other / Not sure":
        c1, c2 = st.columns(2)
        with c1:
            a["bp_history_sys"] = st.number_input(t("ht_expected_systolic_label"), min_value=70, max_value=260, value=a.get("bp_history_sys", 120), step=1)
        with c2:
            a["bp_history_dia"] = st.number_input(t("ht_expected_diastolic_label"), min_value=40, max_value=160, value=a.get("bp_history_dia", 80), step=1)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button(t("back"), on_click=go_back)
    c2.button(t("next"), on_click=go_next)

# ---------------- STEP 2: Symptoms ----------------
elif step == 2:
    st.markdown(
        f"<div class='hv-card'><h4>{t('ht_symptoms_header')} "
        f"<span class='badge badge-model'>{t('ht_badge_affects_score')}</span></h4>",
        unsafe_allow_html=True,
    )
    a["symptoms"] = st.multiselect(t("ht_select_symptoms_label"), SYMPTOM_OPTIONS, default=a.get("symptoms", []), format_func=disp)
    a["other_symptoms"] = st.text_input(t("ht_other_symptoms_label"), value=a.get("other_symptoms", ""))
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button(t("back"), on_click=go_back)
    c2.button(t("next"), on_click=go_next)

# ---------------- STEP 3: Medical History ----------------
elif step == 3:
    st.markdown(f"<div class='hv-card'><h4>{t('ht_medical_history_header')}</h4>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        diab_default = a.get("diabetes", "No")
        a["diabetes"] = st.selectbox(t("ht_has_diabetes_label"), ["No", "Yes"], index=["No", "Yes"].index(diab_default), format_func=disp)
        if a["diabetes"] == "Yes":
            a["glucose"] = st.number_input(t("ht_fasting_glucose_label"), min_value=40, max_value=400, value=a.get("glucose", 120), step=1)
        else:
            a.setdefault("glucose", 90)
        a["totChol"] = st.number_input(t("cholesterol_label"), min_value=100, max_value=400, value=a.get("totChol", 200), step=1)
    with c2:
        hr_mode_default = a.get("heartRate_mode", "I know the exact number")
        hr_mode_opts = ["I know the exact number", "Not sure — let me estimate"]
        a["heartRate_mode"] = st.radio(
            t("ht_resting_hr_label"), hr_mode_opts,
            index=hr_mode_opts.index(hr_mode_default) if hr_mode_default in hr_mode_opts else 0,
            horizontal=True, format_func=disp,
        )
        if a["heartRate_mode"] == "I know the exact number":
            a["heartRate"] = st.number_input(t("ht_resting_hr_bpm_label"), min_value=40, max_value=200, value=a.get("heartRate", 75), step=1)
        else:
            hr_opts = ["Slow (below 60 bpm)", "Normal (60–100 bpm)", "Fast (above 100 bpm)"]
            hr_map = {"Slow (below 60 bpm)": 55, "Normal (60–100 bpm)": 75, "Fast (above 100 bpm)": 110}
            hr_choice_default = a.get("heartRate_choice", hr_opts[1])
            hr_choice_idx = hr_opts.index(hr_choice_default) if hr_choice_default in hr_opts else 1
            a["heartRate_choice"] = st.selectbox(t("ht_hr_describe_label"), hr_opts, index=hr_choice_idx, format_func=disp)
            a["heartRate"] = hr_map[a["heartRate_choice"]]

    st.markdown(f"<br>**{t('ht_other_conditions_label')}**", unsafe_allow_html=True)
    a.setdefault("diseases", {})
    for disease, meta_d in DISEASES_EXTRA.items():
        c1, c2, c3 = st.columns([1.2, 1, 1.5])
        disease_info = a["diseases"].get(disease, {})
        with c1:
            has_it = st.selectbox(disp(disease), ["No", "Yes"], key=f"dis_{disease}",
                                   index=["No", "Yes"].index(disease_info.get("has", "No")), format_func=disp)
        value = None
        dtype = None
        if has_it == "Yes" and meta_d["unit"]:
            with c2:
                value = st.number_input(disp(meta_d["unit"]), min_value=0.0, value=float(disease_info.get("value") or 0.0), key=f"val_{disease}")
        elif has_it == "Yes" and meta_d.get("type_options"):
            with c2:
                type_opts = meta_d["type_options"]
                default_type = disease_info.get("type", type_opts[0])
                dtype = st.selectbox(t("ht_type_label"), type_opts,
                                      index=type_opts.index(default_type) if default_type in type_opts else 0,
                                      key=f"type_{disease}", format_func=disp)
                if dtype == "Not sure / Other":
                    dtype = st.text_input(t("ht_please_specify_label"), value=disease_info.get("type_custom", ""), key=f"typecustom_{disease}")
        lab_file = None
        if has_it == "Yes":
            with c3:
                lab_file = st.file_uploader(
                    f"{t('ht_upload_lab_prefix')} {disp(disease)} {t('ht_lab_report_optional_suffix')}",
                    type=["png", "jpg", "jpeg", "pdf"], key=f"file_{disease}",
                )
        a["diseases"][disease] = {"has": has_it, "value": value, "type": dtype, "file": lab_file}

    a["other_conditions"] = st.text_area(t("ht_other_medical_conditions_label"), value=a.get("other_conditions", ""), height=120)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='hv-card'><h4>{t('ht_family_history_header')} "
        f"<span class='badge badge-info'>{t('ht_badge_reference_only')}</span></h4>",
        unsafe_allow_html=True,
    )
    st.caption(t("ht_family_caption"))
    a["family_history"] = st.multiselect(t("ht_family_history_multiselect_label"), FAMILY_HISTORY_OPTIONS, default=a.get("family_history", []), format_func=disp)
    a["family_history_other"] = st.text_input(t("ht_family_history_other_label"), value=a.get("family_history_other", ""))
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button(t("back"), on_click=go_back)
    c2.button(t("next"), on_click=go_next)

# ---------------- STEP 4: Medications ----------------
elif step == 4:
    st.markdown(f"<div class='hv-card'><h4>{t('ht_medications_header')}</h4>", unsafe_allow_html=True)
    bp_meds_default = a.get("bp_meds", "No")
    a["bp_meds"] = st.selectbox(t("ht_taking_bp_meds_label"), ["No", "Yes"],
                                 index=["No", "Yes"].index(bp_meds_default), format_func=disp)
    if a["bp_meds"] == "Yes":
        med_default = a.get("med_choice", MEDICATION_NAME_OPTIONS[0])
        med_idx = MEDICATION_NAME_OPTIONS.index(med_default) if med_default in MEDICATION_NAME_OPTIONS else 0
        # Drug names stay in their standard form; only the trailing "Other" option is translated.
        a["med_choice"] = st.selectbox(
            t("ht_medication_name_label"), MEDICATION_NAME_OPTIONS, index=med_idx,
            format_func=lambda v: t("ht_other_specify_option") if v == "Other (please specify)" else v,
        )
        if a["med_choice"] == "Other (please specify)":
            a["med_custom"] = st.text_input(t("ht_type_medication_name_label"), value=a.get("med_custom", ""))
        c1, c2 = st.columns(2)
        with c1:
            a["med_photo_upload"] = st.file_uploader(t("ht_upload_med_photo_label"), type=["png", "jpg", "jpeg"])
        with c2:
            a["med_photo_camera"] = st.camera_input(t("ht_take_photo_now_label"))
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button(t("back"), on_click=go_back)
    c2.button(t("next"), on_click=go_next)

# ---------------- STEP 5: Lifestyle & Vitals ----------------
elif step == 5:
    st.markdown(f"<div class='hv-card'><h4>{t('ht_smoking_alcohol_header')}</h4>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        smoker_default = a.get("currentSmoker", "No")
        a["currentSmoker"] = st.selectbox(t("ht_currently_smoke_label"), ["No", "Yes"],
                                           index=["No", "Yes"].index(smoker_default), format_func=disp)
        if a["currentSmoker"] == "Yes":
            a["cigsPerDay"] = st.number_input(t("ht_cigs_per_day_label"), min_value=0, max_value=80, value=a.get("cigsPerDay", 5), step=1)
        else:
            a["cigsPerDay"] = 0
    with c2:
        alcohol_default = a.get("alcohol", "Never")
        a["alcohol"] = st.selectbox(t("alcohol_label"), ["Never", "Occasionally", "Regularly"],
                                     index=["Never", "Occasionally", "Regularly"].index(alcohol_default), format_func=disp)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='hv-card'><h4>{t('ht_physical_activity_header')}</h4>", unsafe_allow_html=True)
    activity_level_default = a.get("activity_level", ACTIVITY_LEVELS[0])
    activity_level_idx = ACTIVITY_LEVELS.index(activity_level_default) if activity_level_default in ACTIVITY_LEVELS else 0
    a["activity_level"] = st.selectbox(t("ht_activity_level_label"), ACTIVITY_LEVELS, index=activity_level_idx, format_func=disp)

    if a["activity_level"] != ACTIVITY_LEVELS[0]:
        default_vals = [v for v in a.get("activity_types", []) if v in ACT_VALUES]
        a["activity_types"] = st.multiselect(t("ht_activity_types_label"), ACT_VALUES, default=default_vals, format_func=act_display)
        if "Other" in a["activity_types"]:
            a["activity_other"] = st.text_input(t("ht_specify_activity_label"), value=a.get("activity_other", ""))
    else:
        a["activity_types"] = []
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='hv-card'><h4>{t('ht_stress_sleep_diet_header')}</h4>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        stress_default = a.get("stress_level", STRESS_LEVELS[0])
        a["stress_level"] = st.selectbox(t("ht_stress_level_label"), STRESS_LEVELS, index=STRESS_LEVELS.index(stress_default), format_func=disp)
    with c2:
        sleep_default = a.get("avg_sleep", SLEEP_OPTIONS[2])
        sleep_idx = SLEEP_OPTIONS.index(sleep_default) if sleep_default in SLEEP_OPTIONS else 2
        a["avg_sleep"] = st.selectbox(t("ht_average_sleep_label"), SLEEP_OPTIONS, index=sleep_idx, format_func=disp)
    with c3:
        salt_default = a.get("salt_intake", SALT_OPTIONS[0])
        a["salt_intake"] = st.selectbox(t("ht_salt_intake_label"), SALT_OPTIONS, index=SALT_OPTIONS.index(salt_default), format_func=disp)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button(t("back"), on_click=go_back)
    c2.button(t("next"), on_click=go_next)

# ---------------- STEP 6: Additional Lab Uploads ----------------
elif step == 6:
    st.markdown(
        f"<div class='hv-card'><h4>{t('ht_lab_uploads_header')} "
        f"<span class='badge badge-info'>{t('ht_badge_reference_only')}</span></h4>",
        unsafe_allow_html=True,
    )
    a["extra_labs_text"] = st.text_area(t("ht_extra_labs_label"), value=a.get("extra_labs_text", ""))
    c1, c2 = st.columns(2)
    with c1:
        a["extra_files_upload"] = st.file_uploader(t("ht_upload_extra_files_label"), type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    with c2:
        a["extra_files_camera"] = st.camera_input(t("ht_camera_lab_label"))
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button(t("back"), on_click=go_back)
    c2.button(t("next"), on_click=go_next)

# ---------------- STEP 7: Report ----------------
elif step == 7:
    st.markdown(f"<div class='hv-card'><h4>{t('ht_ready_analyze_header')}</h4>", unsafe_allow_html=True)
    st.write(t("ht_review_info_msg"))
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.button(t("back"), on_click=go_back)
    analyze_clicked = c2.button(t("ht_analyze_generate_button"))

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
        # Reason labels are built already-translated (baked in at analysis time,
        # same as the PDF/report language for this run).
        adjustments = []
        for disease, meta_d in DISEASES_EXTRA.items():
            info = a["diseases"].get(disease, {})
            if info.get("has") == "Yes":
                pts = meta_d["points"]
                if meta_d["unit"] and info.get("value") and meta_d["high"] and info["value"] >= meta_d["high"]:
                    pts += 3
                label = disp(disease)
                if info.get("type"):
                    label = f"{disp(disease)} ({disp(info['type'])})"
                adjustments.append((label, pts))

        n_symptoms = len([s for s in a.get("symptoms", []) if s])
        if n_symptoms:
            adjustments.append((f"{t('ht_reported_symptoms_prefix')} ({n_symptoms})", min(n_symptoms * 2, 10)))

        if a["occupation_choice"] in HIGH_STRESS_OCCUPATIONS:
            adjustments.append((t("ht_high_stress_occupation"), 3))

        if a["alcohol"] == "Regularly":
            adjustments.append((t("ht_regular_alcohol"), 4))
        elif a["alcohol"] == "Occasionally":
            adjustments.append((t("ht_occasional_alcohol"), 2))

        # -- Blood pressure history --
        bp_history = a.get("bp_history")
        if bp_history == "High (Hypertension)":
            adjustments.append((t("ht_self_reported_high_bp"), 3))
        elif bp_history == "Prehypertension (borderline high)":
            adjustments.append((t("ht_self_reported_borderline_bp"), 1))
        elif bp_history == "Other / Not sure":
            sys_o, dia_o = a.get("bp_history_sys"), a.get("bp_history_dia")
            if sys_o and dia_o:
                if sys_o >= 140 or dia_o >= 90:
                    adjustments.append((t("ht_reported_usual_bp_hypertension"), 3))
                elif sys_o >= 120 or dia_o >= 80:
                    adjustments.append((t("ht_reported_usual_bp_prehypertension"), 1))

        # -- Family history --
        for fam in a.get("family_history", []):
            adjustments.append((f"{t('ht_family_history_of_prefix')} {disp(fam)}", FAMILY_HISTORY_POINTS.get(fam, 2)))

        # -- Physical activity --
        if a.get("activity_level") == ACTIVITY_LEVELS[0]:
            adjustments.append((t("ht_sedentary_lifestyle"), 3))
        elif a.get("activity_level") == ACTIVITY_LEVELS[1]:
            adjustments.append((t("ht_low_physical_activity"), 1))

        # -- Stress --
        if a.get("stress_level") == "High":
            adjustments.append((t("ht_high_stress_level"), 2))
        elif a.get("stress_level") == "Very High":
            adjustments.append((t("ht_very_high_stress_level"), 4))

        # -- Sleep --
        if a.get("avg_sleep") == "Less than 5 hours":
            adjustments.append((t("ht_insufficient_sleep"), 3))
        elif a.get("avg_sleep") == "5-6 hours":
            adjustments.append((t("ht_below_average_sleep"), 1))

        # -- Salt intake --
        if a.get("salt_intake") == "High":
            adjustments.append((t("ht_high_salt_intake"), 3))
        elif a.get("salt_intake") == "Moderate":
            adjustments.append((t("ht_moderate_salt_intake"), 1))

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
        st.markdown(f"<h3 style='color:#94a3b8;margin-top:0;'>{t('ht_predicted_result_label')}</h3>", unsafe_allow_html=True)
        if r["final_prediction"] == 1:
            st.markdown(f"<h2 style='color:#f87171;font-weight:800;'>{t('ht_high_risk_result')}</h2>", unsafe_allow_html=True)
            st.metric(t("ht_overall_risk_score_label"), f"{r['final_risk']:.1f}%")
        else:
            st.markdown(f"<h2 style='color:#34d399;font-weight:800;'>{t('ht_normal_low_risk_result')}</h2>", unsafe_allow_html=True)
            st.metric(t("ht_overall_stability_score_label"), f"{100 - r['final_risk']:.1f}%")
        st.caption(
            f"{t('ht_ai_base_estimate_label')}: {r['ml_risk']:.1f}% • "
            f"{t('ht_clinical_adjustment_label')}: +{r['total_adjustment']:.0f} {t('ht_pts_word')}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with res_col2:
        rec = recommendations_for(r["final_prediction"])
        items_html = "".join(f"<li style='margin-bottom:8px;'>{item}</li>" for item in rec["items"])
        st.markdown(f"""
        <div class='hv-card' style='border-right:4px solid #2563eb;'>
            <h4>{t('ht_medical_recommendations_header')}</h4>
            <div class='rec-box' style='background-color:{rec["bg"]};border:1px solid {rec["border"]};'>
                <strong style='color:{rec["title_color"]};font-size:16px;'>{rec["title"]}</strong>
                <ul style='margin-top:10px;color:{rec["text_color"]};padding-right:20px;'>{items_html}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if r["adjustments"]:
        st.markdown(f"<div class='hv-card'><h4>{t('ht_contributed_factors_header')}</h4>", unsafe_allow_html=True)
        for label, pts in r["adjustments"]:
            st.write(f"• {label}: **+{pts} {t('ht_pts_word')}**")
        st.caption(t("ht_transparent_caption"))
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption(t("ht_disclaimer_caption"))

    def build_pdf():
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        from reportlab.lib import colors

        from pdf_fonts import get_pdf_fonts

        # ---- Color palette (kept consistent with the app's blue/teal theme) ----
        PRIMARY = colors.HexColor("#2563eb")
        TEAL = colors.HexColor("#06b6d4")
        DANGER = colors.HexColor("#e11d48")
        SUCCESS = colors.HexColor("#10b981")
        DARK = colors.HexColor("#1e293b")
        GRAY = colors.HexColor("#475569")
        LIGHT_BG = colors.HexColor("#f1f5f9")
        WHITE = colors.white

        # ---- Arabic-capable font (Amiri, shared registration) ----
        font_reg, font_bold, fonts_available = get_pdf_fonts(lang)

        if lang == "ar" and (not fonts_available or not ARABIC_SHAPING_AVAILABLE):
            st.warning(
                "⚠️ Arabic PDF needs `pip install arabic-reshaper python-bidi` and "
                "`fonts/Amiri-Regular.ttf` + `fonts/Amiri-Bold.ttf` next to this page."
            )

        def shape_ar(text):
            if lang == "ar" and ARABIC_SHAPING_AVAILABLE:
                try:
                    return get_display(arabic_reshaper.reshape(str(text)))
                except Exception:
                    return str(text)
            return str(text)

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4
        y = [height]

        LEFT_X, RIGHT_X = 2 * cm, width - 2 * cm
        NEAR_X = RIGHT_X if lang == "ar" else LEFT_X   # main text starts here
        FAR_X = LEFT_X if lang == "ar" else RIGHT_X    # secondary text (opposite side)

        def draw_near(text, yy, size=10.5, bold=False, color=None):
            c.setFillColor(color or GRAY)
            c.setFont(font_bold if bold else font_reg, size)
            if lang == "ar":
                c.drawRightString(NEAR_X, yy, shape_ar(text))
            else:
                c.drawString(NEAR_X, yy, text)

        def draw_far(text, yy, size=9, color=None):
            c.setFillColor(color or WHITE)
            c.setFont(font_reg, size)
            if lang == "ar":
                c.drawString(FAR_X, yy, shape_ar(text))
            else:
                c.drawRightString(FAR_X, yy, text)

        def new_page_if_needed(min_y=2.5 * cm):
            if y[0] < min_y:
                c.showPage()
                y[0] = height - 2 * cm

        def header_band():
            c.setFillColor(PRIMARY)
            c.rect(0, height - 3 * cm, width, 3 * cm, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(font_bold, 20)
            if lang == "ar":
                c.drawRightString(RIGHT_X, height - 1.7 * cm, shape_ar(t("app_title")))
            else:
                c.drawString(LEFT_X, height - 1.7 * cm, "HealthVibe AI")
            c.setFont(font_reg, 11)
            if lang == "ar":
                c.drawRightString(RIGHT_X, height - 2.4 * cm, shape_ar(t("ht_pdf_report_subtitle")))
            else:
                c.drawString(LEFT_X, height - 2.4 * cm, t("ht_pdf_report_subtitle"))
            c.setFont(font_reg, 9)
            gen_text = f"{t('ht_pdf_generated_label')}: {r['generated_at']}"
            if lang == "ar":
                c.drawString(LEFT_X, height - 1.7 * cm, shape_ar(gen_text))
            else:
                c.drawRightString(RIGHT_X, height - 1.7 * cm, gen_text)
            y[0] = height - 3.7 * cm

        def section_title(text):
            new_page_if_needed(3 * cm)
            draw_near(text, y[0], size=13, bold=True, color=PRIMARY)
            y[0] -= 6
            c.setStrokeColor(TEAL)
            c.setLineWidth(1.2)
            c.line(LEFT_X, y[0], RIGHT_X, y[0])
            y[0] -= 16

        def body_line(text, size=10.5, gap=15, color=None, bold=False):
            new_page_if_needed()
            draw_near(text, y[0], size=size, bold=bold, color=color or DARK)
            y[0] -= gap

        def result_banner():
            new_page_if_needed(4.5 * cm)
            is_high = r["final_prediction"] == 1
            box_color = DANGER if is_high else SUCCESS
            label = t("report_high_risk") if is_high else t("ht_pdf_normal_low_risk")
            c.setFillColor(box_color)
            c.roundRect(LEFT_X, y[0] - 2.2 * cm, width - 4 * cm, 2.2 * cm, 8, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(font_bold, 17)
            c.drawCentredString(width / 2, y[0] - 1.05 * cm, shape_ar(f"{label}  —  {r['final_risk']:.1f}%"))
            c.setFont(font_reg, 9.5)
            caption = (
                f"{t('ht_ai_base_estimate_label')}: {r['ml_risk']:.1f}%   |   "
                f"{t('ht_clinical_adjustment_label')}: +{r['total_adjustment']:.0f} {t('ht_pts_word')}"
            )
            c.drawCentredString(width / 2, y[0] - 1.7 * cm, shape_ar(caption))
            y[0] -= 2.7 * cm

        # ================= HEADER =================
        header_band()

        # ================= RESULT =================
        section_title(t("ht_pdf_section_result"))
        result_banner()

        # ================= PATIENT INFO =================
        section_title(t("ht_pdf_section_patient_info"))
        body_line(f"{t('ht_pdf_name_label')}: {a.get('full_name') or '-'}     {t('age')}: {a.get('age')}     {t('gender')}: {disp(a.get('gender'))}")
        body_line(f"{t('bmi_label')}: {a.get('bmi', 0):.1f}", gap=20)

        # ================= BLOOD PRESSURE & LABS =================
        section_title(t("ht_pdf_section_bp_labs"))
        body_line(f"{t('ht_pdf_reading_label')}: {a.get('sysBP')}/{a.get('diaBP')} mmHg     {t('ht_pdf_cholesterol_label')}: {a.get('totChol')} mg/dL")
        glucose_line = f"{t('ht_pdf_glucose_label')}: {a.get('glucose')} mg/dL" if a.get("diabetes") == "Yes" else f"{t('ht_pdf_glucose_label')}: {t('ht_pdf_glucose_na')}"
        body_line(f"{glucose_line}     {t('ht_pdf_heart_rate_label')}: {a.get('heartRate')} bpm")
        bp_hist_line = disp(a.get("bp_history", "-"))
        if a.get("bp_history") == "Other / Not sure":
            bp_hist_line = f"{t('ht_pdf_other_expected_prefix')}{a.get('bp_history_sys', '-')}/{a.get('bp_history_dia', '-')} mmHg)"
        body_line(f"{t('ht_pdf_bp_history_label')}: {bp_hist_line}", gap=20)

        # ================= SYMPTOMS =================
        section_title(t("ht_pdf_section_symptoms"))
        symptoms_line = ", ".join(disp(s) for s in a.get("symptoms", [])) or t("ht_pdf_none_reported")
        body_line(symptoms_line, gap=20)

        # ================= MEDICAL HISTORY =================
        section_title(t("ht_pdf_section_medical_history"))
        med_display = ""
        if a.get("bp_meds") == "Yes":
            med_display = a.get("med_custom") if a.get("med_choice") == "Other (please specify)" and a.get("med_custom") else a.get("med_choice", "")
        body_line(
            f"{t('diabetes_checkbox')}: {disp(a.get('diabetes'))}     {t('ht_pdf_bp_medication_label')}: {disp(a.get('bp_meds'))}"
            + (f" ({med_display})" if med_display else "")
        )
        for disease in DISEASES_EXTRA:
            info = a["diseases"].get(disease, {})
            if info.get("has") == "Yes":
                extra = f" ({info['value']})" if info.get("value") else (f" ({disp(info['type'])})" if info.get("type") else "")
                body_line(f"  •  {disp(disease)}: {t('yes_option')}{extra}")
        fam_history = ", ".join(disp(f) for f in a.get("family_history", [])) or t("ht_pdf_none_reported")
        if a.get("family_history_other"):
            fam_history += f"; {a.get('family_history_other')}"
        body_line(f"{t('ht_pdf_family_history_label')}: {fam_history}", gap=20)

        # ================= LIFESTYLE & VITALS =================
        section_title(t("ht_pdf_section_lifestyle_vitals"))
        body_line(
            f"{t('ht_pdf_smoking_label')}: {disp(a.get('currentSmoker'))} "
            f"({a.get('cigsPerDay', 0)} {t('ht_pdf_cigs_per_day_unit')})     "
            f"{t('ht_pdf_alcohol_label')}: {disp(a.get('alcohol'))}"
        )
        body_line(f"{t('ht_pdf_activity_level_label')}: {disp(a.get('activity_level', '-'))}")
        if a.get("activity_types"):
            activity_line = ", ".join(act_display(v) for v in a.get("activity_types", []))
            if "Other" in a.get("activity_types", []) and a.get("activity_other"):
                activity_line += f" ({a.get('activity_other')})"
            body_line(f"{t('ht_pdf_activity_types_label')}: {activity_line}")
        body_line(
            f"{t('ht_pdf_stress_label')}: {disp(a.get('stress_level', '-'))}     "
            f"{t('ht_pdf_sleep_label')}: {disp(a.get('avg_sleep', '-'))}     "
            f"{t('ht_pdf_salt_label')}: {disp(a.get('salt_intake', '-'))}",
            gap=20,
        )

        # ================= CLINICAL FACTORS ADJUSTMENT =================
        if r.get("adjustments"):
            section_title(t("ht_pdf_section_adjustment"))
            for label_txt, pts in r["adjustments"]:
                body_line(f"  •  {label_txt}: +{pts} {t('ht_pts_word')}", gap=14)
            y[0] -= 6

        # ================= DISCLAIMER =================
        new_page_if_needed(2.5 * cm)
        c.setFillColor(LIGHT_BG)
        c.roundRect(LEFT_X, y[0] - 1.6 * cm, width - 4 * cm, 1.6 * cm, 6, fill=1, stroke=0)
        c.setFillColor(GRAY)
        c.setFont(font_reg, 9)
        if lang == "ar":
            c.drawRightString(RIGHT_X - 0.3 * cm, y[0] - 0.7 * cm, shape_ar(t("ht_pdf_disclaimer_line1")))
            c.drawRightString(RIGHT_X - 0.3 * cm, y[0] - 1.15 * cm, shape_ar(t("ht_pdf_disclaimer_line2")))
        else:
            c.drawString(2.3 * cm, y[0] - 0.7 * cm, t("ht_pdf_disclaimer_line1"))
            c.drawString(2.3 * cm, y[0] - 1.15 * cm, t("ht_pdf_disclaimer_line2"))
        y[0] -= 2.2 * cm

        # ================= LAB IMAGES =================
        images = []
        for disease, info in a.get("diseases", {}).items():
            if info.get("file") is not None and info["file"].type.startswith("image"):
                images.append((f"{disp(disease)} {t('ht_pdf_lab_suffix')}", info["file"]))
        if a.get("extra_files_upload"):
            for f in a["extra_files_upload"]:
                if f.type.startswith("image"):
                    images.append((t("ht_pdf_additional_lab"), f))
        if a.get("extra_files_camera") is not None:
            images.append((t("ht_pdf_camera_capture"), a["extra_files_camera"]))

        if images:
            c.showPage()
            y[0] = height - 2 * cm
            section_title(t("ht_pdf_section_lab_images"))
            for label_img, f in images:
                try:
                    img = ImageReader(f)
                    body_line(label_img, 11, bold=True, gap=14)
                    new_page_if_needed(6.5 * cm)
                    c.drawImage(img, LEFT_X, y[0] - 6 * cm, width=8 * cm, height=6 * cm, preserveAspectRatio=True)
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
            st.download_button(t("ht_download_pdf_button"), data=pdf_bytes,
                                file_name=f"hypertension_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf")
        except Exception as e:
            st.warning(f"{t('ht_pdf_gen_error_prefix')} ({e}). {t('ht_pdf_install_reportlab_hint')}")

    with pdf_col2:
        if st.button(t("ht_send_email_button")):
            recipient_email = a.get("email", "").strip()
            if not recipient_email or "@" not in recipient_email:
                st.error(t("ht_invalid_email_error"))
            elif not SENDER_EMAIL or not SENDER_APP_PASSWORD:
                st.warning(t("ht_email_not_configured_warning"))
            else:
                try:
                    pdf_bytes_for_email = build_pdf()
                    msg = MIMEMultipart()
                    msg["From"] = SENDER_EMAIL
                    msg["To"] = recipient_email
                    msg["Subject"] = t("ht_email_subject")
                    body = (
                        f"{t('ht_email_greeting_prefix')} {a.get('full_name') or ''},\n\n"
                        f"{t('ht_email_body_line1')}\n\n"
                        f"{t('ht_email_body_line2')}\n\n"
                        f"{t('ht_email_signature')}"
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

                    st.success(f"{t('ht_email_sent_prefix')} {recipient_email}!")
                except Exception as e:
                    st.error(f"{t('ht_email_send_error_prefix')} {e}")