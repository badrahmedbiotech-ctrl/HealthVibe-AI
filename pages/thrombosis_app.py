import os
import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
import io
import plotly.graph_objects as go
from utils.sidebar import render_sidebar

from translations import get_text, get_lang_meta, DEFAULT_LANG

# --- Streamlit Page Config (يجب أن تكون في بداية الكود) ---
st.set_page_config(page_title="Thrombosis Assessment", page_icon="🩸")

# مكتبات تشكيل الحروف العربية (reshaping) وترتيب الاتجاه (bidi)
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SHAPING_AVAILABLE = True
except ImportError:
    ARABIC_SHAPING_AVAILABLE = False

# --- Language setup ---
if "lang" not in st.session_state:
    st.session_state["lang"] = DEFAULT_LANG

lang = st.session_state["lang"]
meta = get_lang_meta(lang)


def t(key: str) -> str:
    """Shortcut for get_text bound to the current session language."""
    return get_text(lang, key)


# --- خط الـ PDF ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(PROJECT_ROOT, "fonts")
FONT_REGULAR_PATH = os.path.join(FONT_DIR, "Amiri-Regular.ttf")
FONT_BOLD_PATH = os.path.join(FONT_DIR, "Amiri-Bold.ttf")
PDF_FONTS_AVAILABLE = os.path.exists(FONT_REGULAR_PATH) and os.path.exists(FONT_BOLD_PATH)


def shape_ar(text: str) -> str:
    """تشكيل ورص النصوص العربية للـ PDF."""
    if lang == "ar" and ARABIC_SHAPING_AVAILABLE:
        try:
            reshaped = arabic_reshaper.reshape(str(text))
            return get_display(reshaped)
        except Exception:
            return str(text)
    return str(text)


def generate_pdf(user_data, result, recommendations, medications):
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
    pdf.cell(0, 5, shape_ar(t("pdf_report_subtitle_thrombosis")), ln=1, align=align)

    pdf.ln(8)

    # 2. البيانات
    pdf.set_font(base_font, "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, shape_ar(t("pdf_patient_params_header")), ln=1, align=align)

    pdf.set_font(base_font, "", 11)
    pdf.set_text_color(60, 60, 60)
    for key, value in user_data.items():
        pdf.set_x(10)
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
    pdf.set_x(10)
    pdf.multi_cell(180, 10, shape_ar(f"{t('pdf_result_status_label')}: {result}"), border=1, align="C", fill=True)
    pdf.ln(8)

    # 4. الأدوية المقترحة
    pdf.set_font(base_font, "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, shape_ar(t("pdf_meds_header")), ln=1, align=align)
    pdf.set_font(base_font, "", 11)
    pdf.set_text_color(60, 60, 60)
    for med in medications:
        pdf.set_x(10)
        pdf.multi_cell(180, 7, shape_ar(f"- {med}"), align=align)

    pdf.ln(5)

    # 5. التوصيات
    pdf.set_font(base_font, "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, shape_ar(t("pdf_recs_header")), ln=1, align=align)

    pdf.set_font(base_font, "", 11)
    pdf.set_text_color(60, 60, 60)

    if isinstance(recommendations, list):
        for rec in recommendations:
            pdf.set_x(10)
            pdf.multi_cell(180, 7, shape_ar(f"- {rec}"), align=align)
    else:
        pdf.set_x(10)
        pdf.multi_cell(180, 7, shape_ar(f"- {str(recommendations)}"), align=align)

    return bytes(pdf.output())


# --- UI Styling & Sidebar ---
render_sidebar()

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
    if st.button(meta["switch_label"], key="lang_switch_thrombosis"):
        st.session_state["lang"] = "ar" if lang == "en" else "en"
        st.rerun()

st.title(t("thrombosis_title"))
st.write(t("thrombosis_desc"))

if lang == "ar" and (not ARABIC_SHAPING_AVAILABLE or not PDF_FONTS_AVAILABLE):
    missing = []
    if not ARABIC_SHAPING_AVAILABLE:
        missing.append("`pip install arabic-reshaper python-bidi`")
    if not PDF_FONTS_AVAILABLE:
        missing.append(f"ملفات الخط `{FONT_REGULAR_PATH}` و `{FONT_BOLD_PATH}`")
    st.warning("⚠️ تقرير الـ PDF بالعربي محتاج: " + " و ".join(missing) + " — لحد ما تضيفهم مش هيتولد تقرير PDF بالعربي.")

# --- استمارة البيانات ---
with st.form("thrombosis_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(t("age"), min_value=1, max_value=120, value=45)
        d_dimer = st.number_input(t("ddimer_label"), min_value=0.0, value=250.0, help=t("ddimer_help"))
        swelling = st.selectbox(t("swelling_label"), [t("no_option"), t("yes_option")])
    with col2:
        pain = st.selectbox(t("pain_label"), [t("no_option"), t("yes_option")])
        history = st.selectbox(t("history_label"), [t("no_option"), t("yes_option")])
        mobility = st.selectbox(t("mobility_label"), [t("no_option"), t("yes_option")])

    submit = st.form_submit_button(t("analyze_risk_button"))

if submit:
    yes_label = t("yes_option")

    # حساب الـ Risk Score
    risk_score = 0
    if d_dimer > 500:
        risk_score += 2
    if swelling == yes_label:
        risk_score += 1
    if pain == yes_label:
        risk_score += 1
    if history == yes_label:
        risk_score += 2
    if mobility == yes_label:
        risk_score += 1
    if age > 60:
        risk_score += 1

    # إعداد بيانات الـ Explainable AI (XAI)
    features = []
    contributions = []
    if d_dimer > 500:
        features.append(t("feature_elevated_ddimer"))
        contributions.append(2)
    if swelling == yes_label:
        features.append(t("feature_leg_swelling"))
        contributions.append(1)
    if pain == yes_label:
        features.append(t("feature_leg_pain"))
        contributions.append(1)
    if history == yes_label:
        features.append(t("feature_previous_history"))
        contributions.append(2)
    if mobility == yes_label:
        features.append(t("feature_prolonged_immobility"))
        contributions.append(1)
    if age > 60:
        features.append(t("feature_age_over_60"))
        contributions.append(1)

    if not features:
        features.append(t("feature_no_risk_factors"))
        contributions.append(0)

    user_data = {
        t("age"): age,
        t("ddimer_data_label"): f"{d_dimer} ng/mL",
        t("swelling_label"): swelling,
        t("pain_label"): pain,
        t("history_label"): history,
        t("mobility_label"): mobility,
    }

    # تحديد درجة الخطورة
    if d_dimer < 500:
        if history == yes_label and swelling == yes_label:
            result = t("result_moderate_clinical")
            result_status_key = "moderate"
        else:
            result = t("result_low_negative")
            result_status_key = "low"
    else:
        if history == yes_label or swelling == yes_label or pain == yes_label or mobility == yes_label:
            result = t("result_high_positive")
            result_status_key = "high"
        else:
            result = t("result_moderate_elevated")
            result_status_key = "moderate"

    st.write("---")
    st.subheader(t("analysis_results_header"))

    # 1. Gauge Chart
    percentage_value = min((risk_score / 8) * 100, 100)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': t("gauge_title"), 'font': {'size': 18}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "white"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 35], 'color': "#1a9850"},
                {'range': [35, 70], 'color': "#fdae61"},
                {'range': [70, 100], 'color': "#d73027"},
            ],
        }
    ))

    fig_gauge.update_layout(
        template="plotly_dark",
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(fig_gauge, use_container_width=True)

    # عرض النتيجة الملونة
    if result_status_key == "high":
        st.error(f"🔴 {t('result_label')}: {result}")
    elif result_status_key == "moderate":
        st.warning(f"⚠️ {t('result_label')}: {result}")
    else:
        st.success(f"🟢 {t('result_label')}: {result}")

    # 2. XAI Bar Chart
    st.write("---")
    st.subheader(t("decision_explanation_header"))
    st.write(t("decision_explanation_desc"))

    fig_bar = go.Figure(go.Bar(
        x=contributions,
        y=features,
        orientation='h',
        marker=dict(
            color=contributions,
            colorscale='Reds',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1),
        )
    ))

    fig_bar.update_layout(
        xaxis_title=t("risk_weight_axis"),
        yaxis_title=t("patient_parameters_axis"),
        template="plotly_dark",
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # 3. الأدوية والتوصيات
    if result_status_key == "high":
        meds = [t("med_high_1"), t("med_high_2"), t("med_high_3")]
        recs = [t("rec_high_1"), t("rec_high_2"), t("rec_high_3"), t("rec_high_4")]
    elif result_status_key == "moderate":
        meds = [t("med_mod_1"), t("med_mod_2")]
        recs = [t("rec_mod_1"), t("rec_mod_2"), t("rec_mod_3")]
    else:
        meds = [t("med_low_1"), t("med_low_2"), t("med_low_3")]
        recs = [t("rec_low_1"), t("rec_low_2"), t("rec_low_3"), t("rec_low_4")]

    st.write("---")
    st.write(t("suggested_meds_header"))
    for m in meds:
        st.write(f"- {m}")

    st.write(t("recommendations_label"))
    for r in recs:
        st.write(f"- {r}")

    # 4. زر تحميل הـ PDF
    pdf_bytes = generate_pdf(user_data, result, recs, meds)

    if pdf_bytes is None:
        st.error(
            "❌ لا يمكن توليد تقرير PDF بالعربي لأن ملفات خط Amiri غير موجودة.\n\n"
            f"من فضلك ضيف الملفين التاليين:\n- {FONT_REGULAR_PATH}\n- {FONT_BOLD_PATH}"
        )
    else:
        st.download_button(
            label=t("download_pdf_thrombosis_button"),
            data=pdf_bytes,
            file_name="Thrombosis_AI_Report.pdf",
            mime="application/pdf",
        )