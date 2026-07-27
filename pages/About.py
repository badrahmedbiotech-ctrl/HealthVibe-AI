import streamlit as st

st.set_page_config(page_title="About HealthVibe", page_icon="💙")

st.title("💙 About HealthVibe AI")

st.markdown("""
Welcome to *HealthVibe AI*.

HealthVibe AI is an intelligent healthcare platform that combines Artificial Intelligence and medical data analysis to support both patients and healthcare professionals.

Our platform provides:

- Early disease prediction
- Personalized health insights
- AI-powered medical assistance
- Automated medical reports
- Continuous patient monitoring

within one integrated healthcare ecosystem.
""")

st.divider()

st.header("🌍 Vision")

st.write("""
To become a leading AI-powered healthcare platform that transforms preventive medicine by enabling early disease detection, intelligent clinical decision support, and continuous patient monitoring.

HealthVibe aims to make healthcare more accessible, personalized, and data-driven, empowering both patients and healthcare professionals to improve health outcomes through innovative technology.
""")

st.divider()

st.header("🎯 Mission")

st.write("""
Our mission is to transform preventive healthcare by developing an intelligent platform that connects Artificial Intelligence with medical expertise.

HealthVibe helps patients understand their health risks through early disease prediction while enabling healthcare professionals to monitor patients, generate comprehensive medical reports, and make data-driven clinical decisions.

We strive to improve healthcare accessibility, reduce diagnostic delays, and promote healthier lives through innovative digital technology.
""")

st.divider()

st.header("⭐ Core Values")

col1, col2 = st.columns(2)

with col1:
    st.success("🩺 Early Disease Detection")
    st.success("🤖 AI-Powered Healthcare")
    st.success("📄 Smart Medical Reports")

with col2:
    st.success("👨‍⚕️ Clinical Decision Support")
    st.success("❤️ Patient-Centered Care")
    st.success("🌍 Innovation & Accessibility")