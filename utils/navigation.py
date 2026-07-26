import streamlit as st

from translations import get_text

# ==========================================
# SIDEBAR
# ==========================================

def sidebar(lang=None):

    if lang is None:
        lang = st.session_state.get("lang", "en")

    with st.sidebar:

        st.markdown(f"""
        <div style="text-align:center;">

        <h1 style="color:#00C2FF;font-size:55px;margin-bottom:-15px;">
        🩺
        </h1>

        <h2 style="color:white;">
        {get_text(lang, "app_title")}
        </h2>

        <p style="color:#94A3B8;margin-top:-10px;">
        AI Clinical Decision Support System
        <p style="
        color:#94A3B8;
        margin-top:-10px;
        ">
        {get_text(lang, "sidebar_subtitle")}
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.divider()

        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "User")

        st.markdown(f"""
        ### 👤 Logged in

        **User:** {username}

        **Role:** {role}
        """)

        st.divider()

        # ==========================
        # MAIN
        # ==========================

        st.markdown("## 🏠 Main")
        st.markdown(f"### 📊 {get_text(lang, 'sidebar_status_header')}")

        st.success(f"🟢 {get_text(lang, 'sidebar_ai_online')}")
        
        ("pages/Login.py","🔑 Login"),

        ("pages/Register.py","📝 Register"),

        ("pages/Profile.py","👤 My Profile"),

        ("pages/Dashboard.py","🏠 Dashboard"),

        

        # ==========================
        # DISEASES
        # ==========================

        st.markdown("## 🧬 Disease Prediction")

        pages += [

            ("pages/Diabetes.py","🩸 Diabetes"),

            ("pages/Hypertension.py","❤️ Hypertension"),

            ("pages/lipid.py","🫀 Lipid"),

            ("pages/obesity.py","⚖️ Obesity"),

            ("pages/thrombosis_app.py","🩸 Thrombosis"),

            ("pages/Pulmonary_Fibrosis.py","🫁 Pulmonary Fibrosis"),

            ("pages/CT_Scan_AI.py","🩻 CT Scan"),

        ]

        # ==========================
        # EXTRA
        # ==========================

        st.markdown("## 📋 Other")

        pages += [

            ("pages/Patient_History.py","📋 Patient History"),

            ("pages/doctor_db.py","👨‍⚕️ Doctor Dashboard"),

            ("pages/About.py","ℹ️ About"),

        ]

        # ==========================

        for page, title in pages:

            if Path(page).exists():

                st.page_link(
                    page,
                    label=title,
                    use_container_width=True
                )

        st.divider()

        st.success("🟢 AI Online")

        st.progress(100)

        st.caption("Version 2.0")

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
           st.info(get_text(lang, "sidebar_version"))

        st.divider()

        st.markdown(f"""
### 👨‍💻 {get_text(lang, "sidebar_developer_header")}

            st.session_state.clear()

            st.switch_page("app.py")
{get_text(lang, "sidebar_developer_role1")}

{get_text(lang, "sidebar_developer_role2")}
""")

        st.divider()

        st.caption(get_text(lang, "sidebar_copyright"))


def hide_sidebar():

    st.markdown("""
    <style>

    section[data-testid="stSidebar"]{
        display:none;
    }

    div[data-testid="collapsedControl"]{
        display:none;
    }

    </style>
    """, unsafe_allow_html=True)
