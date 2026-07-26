from pathlib import Path
import streamlit as st
from translations import get_text

def sidebar(lang=None):
    if lang is None:
        lang = st.session_state.get("lang", "en")
    # 1. تجهيز قائمة الصفحات (تستخدم كأزواج: مسار الملف والعنوان)
    main_pages = [
        ("pages/1_Home.py", f"🏠 {get_text(lang, 'nav_home')}"),
        ("app.py", "🔑 Login"),  # 👈 التعديل هنا: التوجيه للملف الرئيسي app.py بدلاً من pages/Login.py
        ("pages/Register.py", "📝 Register"),
        ("pages/Profile.py", "👤 My Profile"),
        ("pages/Dashboard.py", "🏠 Dashboard"),
    ]

    disease_pages = [
        ("pages/Diabetes.py", "🩸 Diabetes"),
        ("pages/Hypertension.py", "❤️ Hypertension"),
        ("pages/lipid.py", "🫀 Lipid"),
        ("pages/obesity.py", "⚖️ Obesity"),
        ("pages/thrombosis_app.py", "🩸 Thrombosis"),
        ("pages/Pulmonary_Fibrosis.py", "🫁 Pulmonary Fibrosis"),
        ("pages/CT_Scan_AI.py", "🩻 CT Scan"),
    ]

    other_pages = [
        ("pages/Patient_History.py", "📋 Patient History"),
        ("pages/doctor_db.py", "👨‍⚕️ Doctor Dashboard"),
        ("pages/About.py", "ℹ️ About"),
    ]

    # 2. بناء المكونات داخل الـ Sidebar
    with st.sidebar:
        # Header
        st.markdown(
            f"""
            <div style="text-align:center;">
                <h1 style="color:#00C2FF;font-size:55px;margin-bottom:-15px;">🩺</h1>
                <h2 style="color:white;">{get_text(lang, "app_title")}</h2>
                <p style="color:#94A3B8;margin-top:-10px;">AI Clinical Decision Support System</p>
                <p style="color:#94A3B8;margin-top:-10px;">{get_text(lang, "sidebar_subtitle")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # User Info
        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "User")

        st.markdown(
            f"""
            ### 👤 Logged in
            **User:** {username}  
            **Role:** {role}
            """
        )

        st.divider()

        # Main Navigation
st.markdown("## 🏠 Main")
for page, title in main_pages:
    if Path(page).exists():
        st.page_link(page, label=title, use_container_width=True)
st.divider()

        # Disease Prediction Navigation
st.markdown("## 🧬 Disease Prediction")
for page, title in disease_pages:
            if Path(page).exists():
                st.page_link(page, label=title, use_container_width=True)

st.divider()

        # Other Navigation
st.markdown("## 📋 Other")
for page, title in other_pages:
            if Path(page).exists():
                st.page_link(page, label=title, use_container_width=True)

st.divider()

        # Status & System Info
st.markdown(f"### 📊 {get_text(lang, 'sidebar_status_header')}")
st.success(f"🟢 {get_text(lang, 'sidebar_ai_online')}")
st.progress(100)
st.caption(get_text(lang, "sidebar_version"))

st.divider()

        # Developer Info
st.markdown(
            f"""
            ### 👨‍💻 {get_text(lang, "sidebar_developer_header")}
            {get_text(lang, "sidebar_developer_role1")}
            {get_text(lang, "sidebar_developer_role2")}
            """
        )

st.divider()

        # Logout Button
if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("app.py")
            st.caption(get_text(lang, "sidebar_copyright"))


def hide_sidebar():
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        div[data-testid="collapsedControl"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
