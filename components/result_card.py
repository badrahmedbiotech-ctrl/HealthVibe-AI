import streamlit as st

def result_card(prediction, probability=None):

    if prediction == 1:
        color = "#EF4444"
        status = "HIGH RISK"
        title = "High Risk of Diabetes"
        icon = "⚠️"
    else:
        color = "#22C55E"
        status = "LOW RISK"
        title = "Low Risk of Diabetes"
        icon = "🩺"

    percent = 0
    if probability is not None:
        percent = round(probability * 100, 1)

    st.markdown("## 🤖 AI Prediction")

    st.markdown(f"""
<div style="
background:rgba(255,255,255,.06);
backdrop-filter:blur(18px);
border:1px solid rgba(255,255,255,.08);
border-radius:20px;
padding:30px;
box-shadow:0 10px 30px rgba(0,0,0,.25);
">

<div style="
width:220px;
height:220px;
margin:auto;
border-radius:50%;
background:conic-gradient({color} {percent*3.6}deg,#374151 0deg);
display:flex;
justify-content:center;
align-items:center;
">

<div style="
width:170px;
height:170px;
background:#111827;
border-radius:50%;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
">

<div style="font-size:45px;">
{icon}
</div>

<h1 style="margin:0;color:white;">
{percent}%
</h1>

<p style="
color:{color};
font-weight:bold;
font-size:18px;
margin:0;
">
{status}
</p>

</div>
</div>

<br>

<div style="
padding:18px;
border-radius:15px;
background:rgba(255,255,255,.05);
font-size:22px;
font-weight:bold;
color:white;
text-align:center;
">
{title}
</div>

</div>
""", unsafe_allow_html=True)