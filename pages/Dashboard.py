import streamlit as st

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
# 🩺 HealthVibe AI

### AI Powered Diabetes Management Platform

---

""")

st.success("System Online ✅")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Patients",
        "1,254",
        "+23"
    )

with col2:
    st.metric(
        "Predictions",
        "8,421",
        "+112"
    )

with col3:
    st.metric(
        "AI Accuracy",
        "96.4%",
        "+0.3%"
    )

with col4:
    st.metric(
        "Reports",
        "5,014",
        "+44"
    )

    st.write("")
st.subheader("🚀 Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("## 🩸 Diabetes Assessment")
        st.write("Predict diabetes risk using AI.")
        if st.button("Open Assessment", use_container_width=True):
            st.switch_page("pages/Diabetes.py")

with c2:
    with st.container(border=True):
        st.markdown("## 📂 Patient History")
        st.write("View previous patient records.")
        if st.button("Open History", use_container_width=True):
            st.info("Coming Soon")

with c3:
    with st.container(border=True):
        st.markdown("## 🩻 DICOM Viewer")
        st.write("View Medical Images.")
        if st.button("Open Viewer", use_container_width=True):
            st.info("Coming Soon")

            st.write("")
st.subheader("✨ Platform Features")

col1, col2 = st.columns(2)

with col1:

    st.checkbox("✅ Doctor Login", value=True, disabled=True)

    st.checkbox("✅ Patient Login", value=True, disabled=True)

    st.checkbox("✅ AI Prediction", value=True, disabled=True)

    st.checkbox("✅ Patient History", value=True, disabled=True)

    st.checkbox("✅ Database", value=True, disabled=True)

with col2:

    st.checkbox("🚧 OCR Analysis", value=False, disabled=True)

    st.checkbox("🚧 DICOM Viewer", value=False, disabled=True)

    st.checkbox("🚧 PDF Reports", value=False, disabled=True)

    st.checkbox("🚧 Mobile App", value=False, disabled=True)

    st.checkbox("🚧 API Integration", value=False, disabled=True)

    st.write("")
st.divider()

st.subheader("📊 System Status")

st.progress(96)

st.success("HealthVibe AI is running normally.")

st.caption("Version 1.0.0")