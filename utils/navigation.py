import streamlit as st
from pathlib import Path

# ==========================================
# SIDEBAR
# ==========================================

def sidebar():

    with st.sidebar:
     st.markdown("""
<div style="text-align:center;padding:15px 0;">
<h1 style="font-size:60px;">🩺</h1>
<h2 style="color:#00C2FF;">HealthVibe AI</h2>
</div>
""", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center">

        <h2 style="color:white;margin-top:5px;">
        HealthVibe AI
        </h2>

        <p style="color:#9CA3AF;font-size:14px;">
        Vibe Better, Live Better
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    username = st.session_state.get("username", "Guest")
    role = st.session_state.get("role", "User")

    st.info(f"""
👤 **{username}**


🩺 **{role}**
""")

    st.divider()

    st.markdown("### 🏠 Navigation")

    pages = [

            ("pages/Dashboard.py","🏠 Dashboard"),

            ("pages/Profile.py","👤 Profile"),

            ("pages/Patient_History.py","📋 Patient History"),

        ]

    st.markdown("### 🧬 Disease Prediction")

    pages += [

            ("pages/Diabetes.py", "🩸 Diabetes"),

            ("pages/Hypertension.py", "❤️ Hypertension"),

            ("pages/obesity.py", "⚖️ Obesity"),

            ("pages/lipid.py", "🫀 Lipid"),

            ("pages/thrombosis_app.py", "🧬 Thrombosis"),

            ("pages/Pulmonary_Fibrosis.py", "🫁 Pulmonary Fibrosis"),

            ("pages/CT_Scan_AI.py", "🩻 CT Scan AI"),

        ]

    st.markdown("### 🤖 AI")

    pages += [

            ("pages/chatbot.py", "🤖 AI Assistant"),

        ]

    st.markdown("### ⚙ More")

    pages += [

            ("pages/doctor_db.py", "👨‍⚕️ Doctor Dashboard"),

            ("pages/About.py", "ℹ️ About"),

        ]

        # ==========================
        # Navigation Buttons
        # ==========================

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

    st.markdown("### ⚡ System Status")

    st.success("🟢 AI Online")

    st.progress(100)

    st.caption("HealthVibe AI v2.0")

    st.divider()

        # ==========================
        # QUICK INFO
        # ==========================

    st.markdown("""
<div style="
background:#111827;
padding:15px;
border-radius:15px;
border:1px solid #1F2937;
">

<h4>💙 Health Tip</h4>

<p>
Drink enough water 💧<br>
Sleep 7–8 hours 😴<br>
Exercise regularly 🏃
</p>

</div>
""", unsafe_allow_html=True)

    st.divider()

        # ==========================
        # LOGOUT
        # ==========================

    if st.button(
            "🚪 Logout",
            type="primary",
            use_container_width=True
        ):

            st.session_state.clear()
            st.switch_page("app.py")

            st.markdown("""
<div style="
text-align:center;
margin-top:20px;
font-size:12px;
color:#6B7280;
">

© 2026 HealthVibe AI

<br>

Developed by <b>Badr Ahmed</b>

</div>
""", unsafe_allow_html=True)