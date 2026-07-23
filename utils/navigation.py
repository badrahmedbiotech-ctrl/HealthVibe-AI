import streamlit as st
from pathlib import Path


# ==========================================
# SIDEBAR
# ==========================================

def sidebar():

    with st.sidebar:

        st.markdown("""
        <div style="text-align:center;">

        <h1 style="color:#00C2FF;font-size:55px;margin-bottom:-15px;">
        🩺
        </h1>

        <h2 style="color:white;">
        HealthVibe AI
        </h2>

        <p style="color:#94A3B8;margin-top:-10px;">
        AI Clinical Decision Support System
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ==========================
        # USER INFO
        # ==========================

        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "User")

        st.markdown(f"""
        ### 👤 Logged in

        **User:** {username}

        **Role:** {role}
        """)

        st.divider()

        # ==========================
        # NAVIGATION
        # ==========================

        st.markdown("## 🏥 AI Modules")

        pages = [
            ("pages/Dashboard.py", "🏠 Dashboard"),
            ("pages/Profile.py", "👤 My Profile"),
            ("pages/Diabetes.py", "🩸 Diabetes"),
            ("pages/Hypertension.py", "❤️ Hypertension"),
            ("pages/lipid.py", "🫀 Lipid"),
            ("pages/obesity.py", "⚖️ Obesity"),
            ("pages/Pulmonary_Fibrosis.py", "🫁 Pulmonary Fibrosis"),
            ("pages/thrombosis_app.py", "🩸 Thrombosis"),
            ("pages/doctor_db.py", "👨‍⚕️ Doctor Dashboard"),
            ("pages/About.py", "ℹ️ About"),
        ]

        for page, title in pages:

            if Path(page).exists():

                st.page_link(
                    page,
                    label=title,
                    use_container_width=True
                )

        st.divider()

        # ==========================
        # SYSTEM STATUS
        # ==========================

        st.markdown("## 📊 System Status")

        st.success("🟢 AI Online")

        st.progress(100)

        st.caption("Version 2.0")

        st.divider()

        # ==========================
        # DEVELOPER
        # ==========================

        st.markdown("""
        ## 👨‍💻 Developer

        **Badr Ahmed**

        Biotechnology Student

        AI • Bioinformatics • Data Science
        """)

        st.divider()

        # ==========================
        # LOGOUT
        # ==========================

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.switch_page("app.py")

        st.divider()

        st.caption("© 2026 HealthVibe AI")


# ==========================================
# HIDE SIDEBAR
# ==========================================

def hide_sidebar():

    st.markdown(
        """
        <style>

        section[data-testid="stSidebar"]{
            display:none;
        }

        div[data-testid="collapsedControl"]{
            display:none;
        }

        </style>
        """,
        unsafe_allow_html=True
    )