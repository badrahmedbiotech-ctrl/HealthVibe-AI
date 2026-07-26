import os
import streamlit as st
import pandas as pd
from fpdf import FPDF

from translations import get_text, get_lang_meta, DEFAULT_LANG

# مكتبات تشكيل الحروف العربية (reshaping) وترتيب الاتجاه (bidi) - ضرورية عشان
# الحروف العربية تظهر متصلة وبالاتجاه الصحيح جوه الـ PDF.
# pip install arabic-reshaper python-bidi
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SHAPING_AVAILABLE = True
except ImportError:
    ARABIC_SHAPING_AVAILABLE = False

# --- Language setup (same pattern used across the rest of the app) ---
if "lang" not in st.session_state:
    st.session_state["lang"] = DEFAULT_LANG

lang = st.session_state["lang"]
meta = get_lang_meta(lang)


def t(key: str) -> str:
    """Shortcut for get_text bound to the current session language."""
    return get_text(lang, key)


# --- خط الـ PDF (نفس أسلوب صفحة الجلطات) ---
# فولدر fonts موجود في جذر المشروع (HealthVibe-AI/fonts) مش جوه pages/,
# فلازم نطلع درجة واحدة لفوق من مكان الملف ده (اللي هو جوه pages/) عشان نوصله.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(PROJECT_ROOT, "fonts")
FONT_REGULAR_PATH = os.path.join(FONT_DIR, "Amiri-Regular.ttf")
FONT_BOLD_PATH = os.path.join(FONT_DIR, "Amiri-Bold.ttf")
PDF_FONTS_AVAILABLE = os.path.exists(FONT_REGULAR_PATH) and os.path.exists(FONT_BOLD_PATH)


def shape_ar(text: str) -> str:
    """يشكّل النص العربي ويرتبه من اليمين لليسار عشان يظهر سليم جوه الـ PDF."""
    if lang == "ar" and ARABIC_SHAPING_AVAILABLE:
        try:
            reshaped = arabic_reshaper.reshape(str(text))
            return get_display(reshaped)
        except Exception:
            return str(text)
    return str(text)


# ==========================
# PDF Generator Function
# ==========================
def generate_pdf(user_data, risk_level, health_score, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    if lang == "ar":
        if not PDF_FONTS_AVAILABLE:
            return None
        pdf.add_font("Amiri", "", FONT_REGULAR_PATH)
        pdf.add_font("Amiri", "B", FONT_BOLD_PATH)
        base_font = "Amiri"
    else:
        base_font = "Helvetica"

    align = "R" if lang == "ar" else "L"

    # 1. الهيدر
    pdf.set_font(base_font, "B", 24)
    pdf.set_text_color(26, 82, 118)
    pdf.cell(0, 15, shape_ar(t("pdf_app_name")), ln=1, align=align)

    pdf.set_font(base_font, "", 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 5, shape_ar(t("pdf_lipid_report_subtitle")), ln=1, align=align)

    pdf.ln(8)

    # 2. البيانات
    pdf.set_font(base_font, "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, shape_ar(t("pdf_patient_params_header")), ln=1, align=align)

    pdf.set_font(base_font, "", 11)
    pdf.set_text_color(60, 60, 60)
    for key, value in user_data.items():
        pdf.set_x(10)  # 🌟 السطر السحري عشان يرجع المؤشر لأول الشمال دايماً
        pdf.multi_cell(0, 7, shape_ar(f"- {key}: {value}"), align=align)

    pdf.ln(5)

    # 3. النتيجة
    pdf.set_font(base_font, "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, shape_ar(t("pdf_ai_eval_header")), ln=1, align=align)

    pdf.set_fill_color(240, 244, 248)
    pdf.set_text_color(26, 82, 118)
    pdf.set_draw_color(26, 82, 118)

    pdf.set_font(base_font, "B", 12)
    pdf.set_x(10)  # 🌟 نفس المبدأ هنا كمان قبل صندوق النتيجة
    pdf.multi_cell(
        180, 10,
        shape_ar(f"{t('pdf_lipid_overall_risk_label')}: {risk_level}    |    {t('pdf_lipid_health_score_label')}: {health_score}/100"),
        border=1, align="C", fill=True
    )
    pdf.ln(8)

    # 4. التوصيات
    pdf.set_font(base_font, "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, shape_ar(t("pdf_lipid_recs_label")), ln=1, align=align)

    pdf.set_font(base_font, "", 11)
    pdf.set_text_color(60, 60, 60)

    if recommendations:
        for rec in recommendations:
            pdf.set_x(10)
            pdf.multi_cell(180, 7, shape_ar(f"- {rec}"), align=align)
    else:
        pdf.set_x(10)
        pdf.multi_cell(180, 7, shape_ar(f"- {t('lipid_no_recs_msg')}"), align=align)

    return bytes(pdf.output())


# ==========================
# Streamlit Page
# ==========================

st.set_page_config(
    page_title="Lipid Profile Analyzer",
    page_icon=t("lipid_page_icon"),
    layout="wide"
)

# --- RTL / font support (نفس الأسلوب المستخدم في باقي صفحات المنصة) ---
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        direction: {meta['dir']};
        font-family: '{meta['font']}', sans-serif;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- زرار تبديل اللغة ---
top_col1, top_col2 = st.columns([5, 1])
with top_col2:
    if st.button(meta["switch_label"], key="lang_switch_lipid"):
        st.session_state["lang"] = "ar" if lang == "en" else "en"
        st.rerun()

if lang == "ar" and (not ARABIC_SHAPING_AVAILABLE or not PDF_FONTS_AVAILABLE):
    missing = []
    if not ARABIC_SHAPING_AVAILABLE:
        missing.append("`pip install arabic-reshaper python-bidi`")
    if not PDF_FONTS_AVAILABLE:
        missing.append(f"ملفات الخط `{FONT_REGULAR_PATH}` و `{FONT_BOLD_PATH}`")
    st.warning("⚠️ تقرير الـ PDF بالعربي محتاج: " + " و ".join(missing) + " — لحد ما تضيفهم مش هيتولد تقرير PDF بالعربي.")

st.title(t("lipid_hero_title"))
st.markdown(t("lipid_hero_desc"))

st.divider()


# ==========================
# Personal Information
# ==========================

st.subheader(t("personal_info"))

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(t("age"), min_value=1, max_value=120, value=30)
    gender = st.selectbox(t("gender"), [t("male"), t("female")])
    height = st.number_input(t("height"), min_value=100, max_value=250, value=170)

with col2:
    weight = st.number_input(t("weight"), min_value=20, max_value=250, value=70)
    smoker = st.selectbox(
        t("lipid_smoking_label"),
        [t("lipid_smoke_never"), t("lipid_smoke_former"), t("lipid_smoke_current")]
    )
    family_history = st.selectbox(t("lipid_family_history_label"), [t("no_option"), t("yes_option")])


# ==========================
# BMI
# ==========================

bmi = weight / ((height / 100) ** 2)

st.info(f"{t('lipid_calculated_bmi_label')} : {bmi:.2f}")

st.divider()

# ==========================
# Medical Conditions
# ==========================

st.subheader(t("lipid_medical_conditions_header"))

col1, col2 = st.columns(2)

with col1:
    diabetes = st.selectbox(t("lipid_diabetes_label"), [t("no_option"), t("yes_option")])
    hypertension = st.selectbox(t("lipid_hypertension_label"), [t("no_option"), t("yes_option")])

with col2:
    exercise = st.slider(t("lipid_exercise_label"), 0, 7, 3)
    sleep = st.slider(t("lipid_sleep_label"), 3, 12, 7)

st.divider()

# ==========================
# Lipid Profile
# ==========================

st.subheader(t("lipid_profile_header"))

col1, col2 = st.columns(2)

with col1:
    total_chol = st.number_input(t("lipid_total_chol_label"), 50, 500, 180)
    ldl = st.number_input(t("lipid_ldl_label"), 10, 300, 100)

with col2:
    hdl = st.number_input(t("lipid_hdl_label"), 10, 120, 55)
    triglycerides = st.number_input(t("lipid_trig_label"), 20, 600, 120)

st.divider()

analyze = st.button(t("lipid_analyze_button"), use_container_width=True)

if analyze:

    st.divider()
    st.header(t("lipid_results_header"))

    yes_label = t("yes_option")

    risk_score = 0

    # ==========================
    # Total Cholesterol
    # ==========================

    st.subheader(t("lipid_total_chol_section"))

    if total_chol < 200:
        st.success(t("lipid_chol_normal"))
    elif total_chol < 240:
        st.warning(t("lipid_chol_borderline"))
        risk_score += 1
    else:
        st.error(t("lipid_chol_high"))
        risk_score += 2

    # ==========================
    # LDL
    # ==========================

    st.subheader(t("lipid_ldl_section"))

    if ldl < 100:
        st.success(t("lipid_ldl_optimal"))
    elif ldl < 130:
        st.info(t("lipid_ldl_near_optimal"))
        risk_score += 1
    elif ldl < 160:
        st.warning(t("lipid_ldl_borderline"))
        risk_score += 2
    else:
        st.error(t("lipid_ldl_high"))
        risk_score += 3

    # ==========================
    # HDL
    # ==========================
    # (ملحوظة: تم حذف إعادة تصفير risk_score هنا لأنها كانت بتلغي نتيجة
    # الكوليسترول الكلي والـ LDL اللي اتحسبت فوق - ده كان الـ Bug الأساسي)

    st.subheader(t("lipid_hdl_section"))

    if hdl >= 60:
        st.success(t("lipid_hdl_excellent"))
    elif hdl >= 40:
        st.info(t("lipid_hdl_acceptable"))
    else:
        st.error(t("lipid_hdl_low"))
        risk_score += 2

    # ==========================
    # Triglycerides
    # ==========================

    st.subheader(t("lipid_trig_section"))

    if triglycerides < 150:
        st.success(t("lipid_trig_normal"))
    elif triglycerides < 200:
        st.warning(t("lipid_trig_borderline"))
        risk_score += 1
    elif triglycerides < 500:
        st.error(t("lipid_trig_high"))
        risk_score += 2
    else:
        st.error(t("lipid_trig_very_high"))
        risk_score += 3

    st.divider()
    st.header(t("lipid_overall_risk_header"))

    if risk_score <= 2:
        risk_level = t("lipid_risk_low")
        st.success(t("lipid_risk_low"))
    elif risk_score <= 5:
        risk_level = t("lipid_risk_moderate")
        st.warning(t("lipid_risk_moderate"))
    else:
        risk_level = t("lipid_risk_high")
        st.error(t("lipid_risk_high"))

    st.divider()

    # ==========================
    # Personalized Recommendations
    # ==========================

    st.header(t("lipid_recommendations_header"))
    recommendations = []

    if total_chol >= 200:
        recommendations.append(t("lipid_rec_chol"))

    if ldl >= 130:
        recommendations.append(t("lipid_rec_ldl"))

    if hdl < 40:
        recommendations.append(t("lipid_rec_hdl"))

    if triglycerides >= 150:
        recommendations.append(t("lipid_rec_trig"))

    if bmi >= 25:
        recommendations.append(t("lipid_rec_bmi"))

    if smoker == t("lipid_smoke_current"):
        recommendations.append(t("lipid_rec_smoking"))

    if exercise < 3:
        recommendations.append(t("lipid_rec_exercise"))

    if sleep < 6:
        recommendations.append(t("lipid_rec_sleep"))

    if diabetes == yes_label:
        recommendations.append(t("lipid_rec_diabetes"))

    if hypertension == yes_label:
        recommendations.append(t("lipid_rec_hypertension"))

    if family_history == yes_label:
        recommendations.append(t("lipid_rec_family_history"))

    if len(recommendations) == 0:
        st.success(t("lipid_no_recs_msg"))
    else:
        for item in recommendations:
            st.write("✔️", item)

    st.divider()

    st.header(t("lipid_medical_advice_header"))

    if risk_score <= 2:
        st.success(t("lipid_advice_low"))
    elif risk_score <= 5:
        st.warning(t("lipid_advice_moderate"))
    else:
        st.error(t("lipid_advice_high"))

    st.divider()

    # =====================================
    # Health Score
    # =====================================

    st.header(t("lipid_health_score_header"))

    health_score = 100
    health_score -= risk_score * 10

    if bmi >= 25:
        health_score -= 5
    if smoker == t("lipid_smoke_current"):
        health_score -= 10
    if diabetes == yes_label:
        health_score -= 10
    if hypertension == yes_label:
        health_score -= 10
    if exercise < 3:
        health_score -= 5
    if sleep < 6:
        health_score -= 5

    health_score = max(0, health_score)

    st.metric(label=t("lipid_health_score_metric_label"), value=f"{health_score}/100")

    if health_score >= 85:
        st.success(t("lipid_health_excellent"))
    elif health_score >= 70:
        st.info(t("lipid_health_good"))
    elif health_score >= 50:
        st.warning(t("lipid_health_moderate"))
    else:
        st.error(t("lipid_health_high_risk"))

    st.divider()

    # =====================================
    # Lipid Profile Chart
    # =====================================

    st.header(t("lipid_chart_header"))

    chart_data = pd.DataFrame({
        t("lipid_chart_test_col"): [
            t("lipid_total_chol_label"),
            t("lipid_ldl_label"),
            t("lipid_hdl_label"),
            t("lipid_trig_label"),
        ],
        t("lipid_chart_value_col"): [total_chol, ldl, hdl, triglycerides],
    })

    st.bar_chart(chart_data, x=t("lipid_chart_test_col"), y=t("lipid_chart_value_col"))

    st.divider()

    st.subheader(t("lipid_targets_header"))
    st.write(t("lipid_target_chol"))
    st.write(t("lipid_target_ldl"))
    st.write(t("lipid_target_hdl"))
    st.write(t("lipid_target_trig"))

    st.divider()

    # =====================================
    # PDF Report
    # =====================================

    st.header(t("lipid_download_header"))

    user_data = {
        t("pdf_lipid_age_label"): age,
        t("pdf_lipid_gender_label"): gender,
        t("pdf_lipid_bmi_label"): f"{bmi:.2f}",
        t("pdf_lipid_total_chol_label"): total_chol,
        t("pdf_lipid_ldl_label"): ldl,
        t("pdf_lipid_hdl_label"): hdl,
        t("pdf_lipid_trig_label"): triglycerides,
    }

    pdf_bytes = generate_pdf(user_data, risk_level, health_score, recommendations)

    if pdf_bytes is None:
        st.error(
            "❌ لا يمكن توليد تقرير PDF بالعربي لأن ملفات خط Amiri غير موجودة.\n\n"
            f"من فضلك ضيف الملفين التاليين:\n- {FONT_REGULAR_PATH}\n- {FONT_BOLD_PATH}"
        )
    else:
        st.download_button(
            label=t("lipid_download_pdf_button"),
            data=pdf_bytes,
            file_name="HealthVibe_Lipid_Report.pdf",
            mime="application/pdf",
        )