import streamlit as st

from components.auth import create_users_table
from components.language import apply_language
from translations import get_text
# تهيئة متغيرات الـ session لمنع الـ AttributeError
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None
st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🏥",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("""

<div style="text-align:center;padding-top:50px;">

<h1 style="font-size:55px;color:#00C2FF;">
🏥 HealthVibe AI
</h1>

<h3 style="color:white;">
AI Clinical Decision Support Platform
</h3>

<p style="color:#94A3B8;font-size:20px;">
Choose how you want to continue
</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2 = st.columns(2)

with col1:

    st.markdown("## 👤 Patient")

    st.write("Access your medical dashboard")

    if st.button(
        "Continue as Patient",
        use_container_width=True
    ):

        st.session_state.role = "Patient"

        st.switch_page("pages/Login.py")

with col2:

    st.markdown("## 👨‍⚕️ Doctor")

    st.write("Access your doctor dashboard")

    if st.button(
        "Continue as Doctor",
        use_container_width=True
    ):

        st.session_state.role = "Doctor"

        st.switch_page("pages/Login.py")
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
chatbot_page = st.Page("pages/chatbot.py", title=get_text(lang, "chatbot"), icon="💬") # أو الاسم المضبوط للملف عندك جوه pages
diabetes_page = st.Page("pages/Diabetes.py", title=get_text(lang, "nav_diabetes"), icon="🩸")
# heart_page = st.Page("pages/Heart_Disease.py", ...)
hypertension_page = st.Page("pages/Hypertension.py", title=get_text(lang, "nav_hypertension"), icon="🩸")
lipid_page = st.Page("pages/lipid.py", title=get_text(lang, "nav_lipid"), icon="🧪")
obesity_page = st.Page("pages/obesity.py", title=get_text(lang, "nav_obesity"), icon="⚖️")
pf_page = st.Page("pages/Pulmonary_Fibrosis.py", title=get_text(lang, "nav_pulmonary_fibrosis"), icon="🫁")
ct_page = st.Page("pages/CT_Scan_AI.py", title=get_text(lang, "nav_ct_scan"), icon="🩻")
thrombosis_page = st.Page("pages/thrombosis_app.py", title=get_text(lang, "nav_thrombosis"), icon="🩸")
history_page = st.Page("pages/Patient_History.py", title=get_text(lang, "nav_patient_history"), icon="📋")
about_page = st.Page("pages/About.py", title=get_text(lang, "nav_about"), icon="ℹ")

pages = [
    login_page,
    home_page,
    dashboard_page,
    chatbot_page,
    diabetes_page,
    hypertension_page,
    lipid_page,
    obesity_page,
    pf_page,
    ct_page,
    thrombosis_page,
    history_page,
    about_page,
]

pg = st.navigation(pages, position="sidebar")

pg.run()