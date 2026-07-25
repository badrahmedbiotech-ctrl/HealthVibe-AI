import streamlit as st
from components.language import apply_language
from translations import get_text

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

lang = apply_language()

st.markdown(f"""
# 🩺 HealthVibe AI

### {get_text(lang, "dashboard_subtitle")}

---

""")

st.success(get_text(lang, "system_online"))

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        get_text(lang, "metric_patients"),
        "1,254",
        "+23"
    )

with col2:
    st.metric(
        get_text(lang, "metric_predictions"),
        "8,421",
        "+112"
    )

with col3:
    st.metric(
        get_text(lang, "metric_accuracy"),
        "96.4%",
        "+0.3%"
    )

with col4:
    st.metric(
        get_text(lang, "metric_reports"),
        "5,014",
        "+44"
    )

    st.write("")
st.subheader(get_text(lang, "quick_actions_header"))

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown(f"## {get_text(lang, 'diabetes_assessment_title')}")
        st.write(get_text(lang, "diabetes_assessment_desc"))
        if st.button(get_text(lang, "open_assessment_button"), use_container_width=True):
            st.switch_page("pages/Diabetes.py")

with c2:
    with st.container(border=True):
        st.markdown(f"## {get_text(lang, 'patient_history_title')}")
        st.write(get_text(lang, "patient_history_desc"))
        if st.button(get_text(lang, "open_history_button"), use_container_width=True):
            st.info(get_text(lang, "coming_soon"))

with c3:
    with st.container(border=True):
        st.markdown(f"## {get_text(lang, 'dicom_viewer_title')}")
        st.write(get_text(lang, "dicom_viewer_desc"))
        if st.button(get_text(lang, "open_viewer_button"), use_container_width=True):
            st.info(get_text(lang, "coming_soon"))

            st.write("")
st.subheader(get_text(lang, "platform_features_header"))

col1, col2 = st.columns(2)

with col1:

    st.checkbox(get_text(lang, "feature_doctor_login"), value=True, disabled=True)

    st.checkbox(get_text(lang, "feature_patient_login"), value=True, disabled=True)

    st.checkbox(get_text(lang, "feature_ai_prediction"), value=True, disabled=True)

    st.checkbox(get_text(lang, "feature_patient_history"), value=True, disabled=True)

    st.checkbox(get_text(lang, "feature_database"), value=True, disabled=True)

with col2:

    st.checkbox(get_text(lang, "feature_ocr"), value=False, disabled=True)

    st.checkbox(get_text(lang, "feature_dicom"), value=False, disabled=True)

    st.checkbox(get_text(lang, "feature_pdf_reports"), value=False, disabled=True)

    st.checkbox(get_text(lang, "feature_mobile_app"), value=False, disabled=True)

    st.checkbox(get_text(lang, "feature_api_integration"), value=False, disabled=True)

    st.write("")
st.divider()

st.subheader(get_text(lang, "system_status_header"))

st.progress(96)

st.success(get_text(lang, "system_running"))

st.caption(get_text(lang, "version_label"))