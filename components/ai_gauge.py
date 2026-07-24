import streamlit as st

def ai_gauge(probability):

    if probability is None:
        return

    percent = int(probability * 100)

    if percent < 40:
        color = "#22C55E"
        status = "LOW RISK"

    elif percent < 70:
        color = "#F59E0B"
        status = "MODERATE"

    else:
        color = "#EF4444"
        status = "HIGH RISK"

    st.markdown(f"""
    <div style="

    width:260px;
    height:260px;

    margin:auto;

    border-radius:50%;

    background:conic-gradient(
        {color} {percent*3.6}deg,
        #E5E7EB 0deg
    );

    display:flex;

    justify-content:center;

    align-items:center;

    ">

        <div style="

        width:200px;

        height:200px;

        background:#111827;

        border-radius:50%;

        display:flex;

        flex-direction:column;

        justify-content:center;

        align-items:center;

        ">

            <div style="font-size:52px;">
            🩺
            </div>

            <h1 style="color:white;margin:0;">
            {percent}%
            </h1>

            <p style="
            color:{color};
            font-size:20px;
            font-weight:bold;
            ">
            {status}
            </p>

        </div>

    </div>
    """, unsafe_allow_html=True)