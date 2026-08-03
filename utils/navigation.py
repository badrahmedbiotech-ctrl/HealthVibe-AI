import streamlit as st
from pathlib import Path

import translation


def sidebar():

    with st.sidebar:

        # ==========================
        # LOGO
        # ==========================

        st.markdown("# 🩺")
        st.markdown("## HealthVibe AI")
        st.caption(translation.t("Clinical Decision Support Platform"))

        st.divider()

        # ==========================
        # USER CARD
        # ==========================

        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "Patient")

        st.info(f"""
👤 **{username}**

🩺 **{translation.t("Role:")}** {translation.t(role)}

🟢 **{translation.t("Status:")}** {translation.t("Online")}
""")

        st.divider()

        # ==========================
        # NAVIGATION
        # ==========================

        st.subheader(translation.t("📂 Navigation"))

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
                    label=translation.t(title),
                    width="stretch"
                )

        st.divider()

        # ==========================
        # SYSTEM STATUS
        # ==========================

        st.subheader(translation.t("⚡ System Status"))

        st.success(translation.t("🟢 AI Server"))
        st.success(translation.t("🟢 Database"))
        st.success(translation.t("🟢 Models Loaded"))

        st.divider()

        # ==========================
        # DAILY HEALTH TIP
        # ==========================

        st.subheader(translation.t("💙 Daily Health Tip"))

        tips = [
            "💧 Drink enough water",
            "🥗 Eat healthy meals",
            "🏃 Exercise at least 30 minutes",
            "😴 Sleep 7–8 hours",
        ]

        tips_md = "\n".join(f"- {translation.t(tip)}" for tip in tips)

        st.markdown(tips_md)

        st.divider()
                # ==========================
        # LOGOUT
        # ==========================

        if st.button(
            translation.t("🚪 Logout"),
            type="primary",
            width="stretch"
        ):
            st.session_state.clear()
            st.switch_page("app.py")