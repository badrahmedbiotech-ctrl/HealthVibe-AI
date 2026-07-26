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

        pages = [

            ("pages/Login.py","🔑 Login"),

            ("pages/Register.py","📝 Register"),

            ("pages/Profile.py","👤 My Profile"),

            ("pages/Dashboard.py","🏠 Dashboard"),

        ]

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

            st.session_state.clear()

            st.switch_page("app.py")