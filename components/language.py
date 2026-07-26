import streamlit as st

from translations import get_lang_meta


def apply_language():
    """
    - بتقرا/تهيّئ اللغة الحالية من st.session_state (افتراضي: en).
    - بتطبّق اتجاه الصفحة (RTL/LTR) والخط المناسب على حسب اللغة.
    - بترسم زرار تبديل اللغة مرة واحدة بس في كل rerun — حتى لو
      الدالة دي اتنادت من أكتر من ملف في نفس الـ rerun (زي app.py
      وبعدها الصفحة اللي st.navigation() بيشغّلها). ده اللي كان
      بيسبب StreamlitDuplicateElementKey لأن كل نداية كانت بترسم
      زرار جديد بنفس الـ key.
    """

    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"

    lang = st.session_state["lang"]
    meta = get_lang_meta(lang)

    st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        direction: {meta["dir"]};
    }}
    .stApp {{
        font-family: '{meta["font"]}', sans-serif;
    }}
    </style>
    """, unsafe_allow_html=True)

    # الحارس اللي بيمنع رسم الزرار أكتر من مرة في نفس الـ rerun.
    # لازم يترجع False من جديد في أول كل rerun -- وده بيحصل في
    # app.py (شوف الملف) لأنه أول ملف بيتنفذ دايمًا.
    if not st.session_state.get("_lang_btn_rendered", False):

        st.session_state["_lang_btn_rendered"] = True

        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button(meta["switch_label"], key="lang_switch_btn"):
                st.session_state["lang"] = "ar" if lang == "en" else "en"
                st.rerun()

    return lang