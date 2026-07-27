import streamlit as st
from components.language import apply_language
from translations import get_text

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="wide"
)

lang = apply_language()

st.title(get_text(lang, "home_title"))

st.markdown(f"""
{get_text(lang, "home_welcome_header")}

{get_text(lang, "home_intro")}

{get_text(lang, "home_modules_header")}

- {get_text(lang, "home_module_heart")}
- {get_text(lang, "home_module_diabetes")}
- {get_text(lang, "home_module_pf")}
- {get_text(lang, "home_module_ct")}

---

{get_text(lang, "home_features_header")}

{get_text(lang, "home_feature_ai_diagnosis")}

{get_text(lang, "home_feature_reports")}

{get_text(lang, "home_feature_risk")}

{get_text(lang, "home_feature_dashboard")}

{get_text(lang, "home_feature_easy")}

---

{get_text(lang, "home_developed_by")}
""")

st.success(get_text(lang, "home_ready_msg"))