import streamlit as st
import time

def ai_loading():

    status = st.empty()

    progress = st.progress(0)

    steps = [

        ("🩸 Reading Patient Data...",20),

        ("🧠 Running AI Model...",45),

        ("📊 Calculating Risk Score...",70),

        ("💡 Generating Recommendation...",90),

        ("✅ Finalizing Report...",100)

    ]

    for text,value in steps:

        status.markdown(f"""

        ## {text}

        """,unsafe_allow_html=True)

        progress.progress(value)

        time.sleep(0.7)

    status.empty()

    progress.empty()