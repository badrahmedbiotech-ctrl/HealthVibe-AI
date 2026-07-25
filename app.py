import streamlit as st

from components.auth import (
    create_users_table,
    create_default_admin,
    login,
)

from components.language import apply_language
from translations import get_text

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="centered"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


create_users_table()
create_default_admin()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

# ============================================================
# جديد: بنصفّر الحارس ده هنا (أول حاجة بتتنفذ في كل rerun) عشان
# apply_language() ترسم زرار تبديل اللغة مرة واحدة بس، حتى لو
# اتنادت تاني جوه الصفحة اللي st.navigation() هيشغّلها.
# ============================================================
st.session_state["_lang_btn_rendered"] = False

lang = apply_language()


def render_login():
    # ملاحظة: نفس فورم اللوجين القديم، لكن دلوقتي جوه دالة عشان
    # تتحط كـ st.Page — كده st.navigation() بيفضل شغال دايمًا
    # (مهما كانت حالة تسجيل الدخول) وStreamlit ميرجعش للتنقل
    # التلقائي المبني على أسماء الملفات.

    st.markdown(f"""
    <div class="hero">
        <h1>🩺 {get_text(lang, "app_title")}</h1>
        <p>AI Clinical Decision Support System</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    with st.container(border=True):

        st.subheader("🔐 " + get_text(lang, "login_header"))

        username = st.text_input(
            get_text(lang, "username"),
            placeholder=get_text(lang, "username_placeholder")
        )

        password = st.text_input(
            get_text(lang, "password"),
            type="password",
            placeholder=get_text(lang, "password_placeholder")
        )

        st.write("")

        login_btn = st.button(
            get_text(lang, "login_button"),
            use_container_width=True
        )

        if login_btn:
            if username.strip() == "" or password.strip() == "":
                st.warning(get_text(lang, "enter_username_password"))
            else:
                user = login(username, password)

                if user is None:
                    st.error(get_text(lang, "invalid_credentials"))
                else:
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.session_state.role = user[3]

                    st.success(get_text(lang, "login_success"))
                    st.rerun()


# ============================================================
# جديد: الشريط الجانبي بقى ظاهر دايمًا (مسجل دخول أو لأ)،
# وكل عناوين الصفحات بتتترجم فورًا من get_text() على حسب اللغة.
# صفحة اللوجين نفسها بقت واحدة من صفحات القايمة بدل ما تكون
# منفصلة أو مخفية.
# ============================================================

login_page = st.Page(render_login, title=get_text(lang, "login_header"), icon="🔐", default=not st.session_state.logged_in)
home_page = st.Page("pages/1_Home.py", title=get_text(lang, "nav_home"), icon="🏠", default=st.session_state.logged_in)
dashboard_page = st.Page("pages/Dashboard.py", title=get_text(lang, "nav_dashboard"), icon="📊")
diabetes_page = st.Page("pages/Diabetes.py", title=get_text(lang, "nav_diabetes"), icon="🩸")
heart_page = st.Page("pages/Heart_Disease.py", title=get_text(lang, "nav_heart_disease"), icon="❤️")
hypertension_page = st.Page("pages/Hypertension.py", title=get_text(lang, "nav_hypertension"), icon="🩸")
lipid_page = st.Page("pages/lipid.py", title=get_text(lang, "nav_lipid"), icon="🧪")
obesity_page = st.Page("pages/obesity.py", title=get_text(lang, "nav_obesity"), icon="⚖️")
pf_page = st.Page("pages/Pulmonary_Fibrosis.py", title=get_text(lang, "nav_pulmonary_fibrosis"), icon="🫁")
ct_page = st.Page("pages/CT_Scan_AI.py", title=get_text(lang, "nav_ct_scan"), icon="🩻")
breast_page = st.Page("pages/Breast_Cancer.py", title=get_text(lang, "nav_breast_cancer"), icon="🎗")
thrombosis_page = st.Page("pages/thrombosis_app.py", title=get_text(lang, "nav_thrombosis"), icon="🩸")
history_page = st.Page("pages/Patient_History.py", title=get_text(lang, "nav_patient_history"), icon="📋")
about_page = st.Page("pages/About.py", title=get_text(lang, "nav_about"), icon="ℹ")

pages = [
    login_page,
    home_page,
    dashboard_page,
    diabetes_page,
    heart_page,
    hypertension_page,
    lipid_page,
    obesity_page,
    pf_page,
    ct_page,
    breast_page,
    thrombosis_page,
    history_page,
    about_page,
]

pg = st.navigation(pages, position="sidebar")

pg.run()