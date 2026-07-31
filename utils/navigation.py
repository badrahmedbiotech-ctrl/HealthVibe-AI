import streamlit as st
from pathlib import Path


def sidebar():

    with st.sidebar:

        # ==========================
        # LOGO
        # ==========================

        st.markdown("# 🩺")
        st.markdown("## HealthVibe AI")
        st.caption("Clinical Decision Support Platform")

        st.divider()

        # ==========================
        # USER CARD
        # ==========================

        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "Patient")

        st.info(f"""
👤 **{username}**

🩺 **Role:** {role}

🟢 **Status:** Online
""")

        st.divider()

        # ==========================
        # NAVIGATION
        # ==========================

        st.subheader("📂 Navigation")

        pages = [
            ("pages/Dashboard.py", "🏠 Dashboard"),
            ("pages/Profile.py", "👤 Profile"),
            ("pages/Patient_History.py", "📋 Patient History"),

            ("pages/Diabetes.py", "🩸 Diabetes"),
            ("pages/Hypertension.py", "❤️ Hypertension"),
            ("pages/obesity.py", "⚖️ Obesity"),
            ("pages/lipid.py", "🫀 Lipid"),
            ("pages/thrombosis_app.py", "🧬 Thrombosis"),
            ("pages/Pulmonary_Fibrosis.py", "🫁 Pulmonary AI"),
            ("pages/CT_Scan_AI.py", "🩻 CT Analysis"),

            ("pages/chatbot.py", "🤖 AI Assistant"),

            ("pages/doctor_db.py", "👨‍⚕️ Doctor Dashboard"),
            ("pages/About.py", "ℹ️ About"),
        ]
                # ==========================
        # PAGE LINKS
        # ==========================

        for page, title in pages:

            if Path(page).exists():

                st.page_link(
                    page,
                    label=title,
                    width="stretch"
                )

        st.divider()

        # ==========================
        # SYSTEM STATUS
        # ==========================

        st.subheader("⚡ System Status")

        st.success("🟢 AI Server")
        st.success("🟢 Database")
        st.success("🟢 Models Loaded")

        st.divider()

        # ==========================
        # DAILY HEALTH TIP
        # ==========================

        st.subheader("💙 Daily Health Tip")

        st.markdown("""
- 💧 Drink enough water
- 🥗 Eat healthy meals
- 🏃 Exercise at least 30 minutes
- 😴 Sleep 7–8 hours
""")

        st.divider()
                # ==========================
        # LOGOUT
        # ==========================

        if st.button(
            "🚪 Logout",
            type="primary",
            width="stretch"
        ):
            st.session_state.clear()
            st.switch_page("app.py")