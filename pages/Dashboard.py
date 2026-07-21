import streamlit as st
from utils.navigation import sidebar

# ==========================
# SESSION PROTECTION
# ==========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="HealthVibe AI Dashboard",
    page_icon="🩺",
    layout="wide"
)

# ==========================
# LOAD CSS
# ==========================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================
# SIDEBAR
# ==========================

sidebar()

# ==========================
# HEADER
# ==========================

st.markdown(f"""
<div class="hero">

<h1>🩺 HealthVibe AI</h1>

<h3>
Welcome, {st.session_state.username}
</h3>

<p>
AI Clinical Decision Support System
</p>

</div>
""", unsafe_allow_html=True)

st.success("🟢 System Online")

st.write("")

# ==========================
# DASHBOARD METRICS
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Patients",
        value="1,254",
        delta="+23"
    )

with col2:
    st.metric(
        label="Predictions",
        value="8,421",
        delta="+112"
    )

with col3:
    st.metric(
        label="AI Accuracy",
        value="96.4%",
        delta="+0.3%"
    )

with col4:
    st.metric(
        label="Reports",
        value="5,014",
        delta="+44"
    )

st.write("")

# ==========================
# QUICK ACTIONS
# ==========================

st.subheader("🚀 Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):

        st.markdown("## 🩸 Diabetes Assessment")

        st.write("Predict diabetes risk using AI.")

        if st.button(
            "Open Assessment",
            use_container_width=True
        ):
            st.switch_page("pages/Diabetes.py")

with c2:
    with st.container(border=True):

        st.markdown("## 📂 Patient History")

        st.write("View previous patient records.")

        if st.button(
            "Open History",
            use_container_width=True
        ):
            st.info("Coming Soon")

with c3:
    with st.container(border=True):

        st.markdown("## 🩻 DICOM Viewer")

        st.write("View medical images.")

        if st.button(
            "Open Viewer",
            use_container_width=True
        ):
            st.info("Coming Soon")

st.write("")

# ==========================
# PLATFORM FEATURES
# ==========================

st.subheader("✨ Platform Features")

left, right = st.columns(2)

with left:

    st.checkbox("Doctor Login", value=True, disabled=True)

    st.checkbox("Patient Login", value=True, disabled=True)

    st.checkbox("AI Prediction", value=True, disabled=True)

    st.checkbox("Patient History", value=True, disabled=True)

    st.checkbox("Database", value=True, disabled=True)

with right:

    st.checkbox("OCR Analysis", value=False, disabled=True)

    st.checkbox("DICOM Viewer", value=False, disabled=True)

    st.checkbox("PDF Reports", value=False, disabled=True)

    st.checkbox("Mobile App", value=False, disabled=True)

    st.checkbox("API Integration", value=False, disabled=True)

st.write("")

# ==========================
# SYSTEM STATUS
# ==========================

st.divider()

st.subheader("📊 System Status")

st.progress(96)

st.success("HealthVibe AI is running normally.")

st.caption("Version 2.0")

# ==========================
# LOGOUT
# ==========================

st.divider()

if st.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.switch_page("app.py")

# ==========================
# FOOTER
# ==========================

st.write("")

st.markdown("""
<div class="footer">

<h2 style="color:#00C2FF;">
HealthVibe AI
</h2>

<p>
AI Clinical Decision Support System
</p>

<hr>

<p style="color:#94A3B8;">
Developed by <b>Badr Ahmed</b>
</p>

</div>
""", unsafe_allow_html=True)