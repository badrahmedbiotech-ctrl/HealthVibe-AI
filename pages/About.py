import streamlit as st
import translation
from utils.navigation import sidebar
st.set_page_config(page_title="About HealthVibe", page_icon="💙")

translation.init()
sidebar()
IS_AR = st.session_state.get("lang", "en") == "ar"
# ==========================================================
# PAGE-LOCAL RTL CSS (only injected when Arabic is active —
# does not touch English/LTR rendering at all)
# ==========================================================

if IS_AR:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            direction: rtl;
        }

        /* Every markdown/write block on this page (intro, vision,
           mission paragraphs + their bullet lists) */
        [data-testid="stMarkdownContainer"] {
            direction: rtl;
            text-align: right !important;
        }

        [data-testid="stMarkdownContainer"] ul,
        [data-testid="stMarkdownContainer"] ol {
            direction: rtl;
            text-align: right !important;
            padding-right: 1.4em;
            padding-left: 0;
            margin-right: 0;
        }

        [data-testid="stMarkdownContainer"] li {
            direction: rtl;
            text-align: right !important;
        }

        /* st.success() core-values cards */
        [data-testid="stAlertContainer"],
        [data-testid="stAlertContentContainer"] {
            direction: rtl;
            text-align: right !important;
        }

        h1, h2, h3, p {
            direction: rtl;
            text-align: right !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def rtl_header(text: str, level: str = "h1"):
    """Render a header as raw HTML with dir='rtl' when Arabic is active,
    otherwise fall back to the normal Streamlit header (unchanged LTR)."""
    if IS_AR:
        st.markdown(
            f'<{level} dir="rtl" style="text-align:right;">{text}</{level}>',
            unsafe_allow_html=True
        )
    elif level == "h1":
        st.title(text)
    else:
        st.header(text)


# ==========================================================
# TITLE
# ==========================================================

rtl_header(translation.t("💙 About HealthVibe AI"), "h1")

st.markdown(translation.t("about_intro"))

st.divider()

rtl_header(translation.t("🌍 Vision"), "h2")

st.write(translation.t("about_vision"))

st.divider()

rtl_header(translation.t("🎯 Mission"), "h2")

st.write(translation.t("about_mission"))

st.divider()

rtl_header(translation.t("⭐ Core Values"), "h2")

col1, col2 = st.columns(2)

with col1:
    st.success(translation.t("🩺 Early Disease Detection"))
    st.success(translation.t("🤖 AI-Powered Healthcare"))
    st.success(translation.t("📄 Smart Medical Reports"))

with col2:
    st.success(translation.t("👨‍⚕️ Clinical Decision Support"))
    st.success(translation.t("❤️ Patient-Centered Care"))
    st.success(translation.t("🌍 Innovation & Accessibility"))