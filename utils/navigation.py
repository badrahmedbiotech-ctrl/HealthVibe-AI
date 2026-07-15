import streamlit as st
from pathlib import Path

def sidebar():

    with st.sidebar:

        st.markdown("""
        <div style="text-align:center;">

        <h1 style="
        color:#00C2FF;
        font-size:55px;
        margin-bottom:-15px;
        ">
        🩺
        </h1>

        <h2 style="
        color:white;
        ">
        HealthVibe AI
        </h2>

        <p style="
        color:#94A3B8;
        margin-top:-10px;
        ">
        AI Clinical Decision Support System
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("### 🏥 AI Modules")

        pages = [

            ("app.py","🏠 Dashboard"),

            ("pages/Diabetes.py","🩸 Diabetes"),

            ("pages/Heart_Disease.py","❤️ Heart Disease"),

            ("pages/Pulmonary_Fibrosis.py","🫁 Pulmonary Fibrosis"),

            ("pages/CT_Scan_AI.py","🩻 Lung CT Scan"),

            ("pages/Breast_Cancer.py","🎗 Breast Cancer"),

            ("pages/About.py","ℹ About")

        ]

        for page,title in pages:

            if Path(page).exists():

                st.page_link(page,label=title)

        st.divider()

        st.markdown("""
        ### 📊 System Status
        """)

        st.success("🟢 AI Online")

        st.info("Version 2.0")

        st.divider()

        st.markdown("""
        ### 👨‍💻 Developer

        **Badr Ahmed**

        Biotechnology Student

        AI & Bioinformatics
        """)

        st.divider()

        st.caption("© 2026 HealthVibe AI")