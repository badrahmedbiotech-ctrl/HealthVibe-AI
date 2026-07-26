import streamlit as st

def stepper(step):

    steps = [

        ("👤", "Patient"),
        ("🩺", "Medical"),
        ("📊", "Analysis"),
        ("🤖", "Result")

    ]

    cols = st.columns(len(steps))

    for i, (icon, title) in enumerate(steps):

        if i + 1 < step:

            color = "#22C55E"      # Green

        elif i + 1 == step:

            color = "#00C2FF"      # Blue

        else:

            color = "#64748B"      # Gray

        cols[i].markdown(f"""
<div style="text-align:center;">

<div style="
width:70px;
height:70px;
margin:auto;
border-radius:50%;
background:{color};
display:flex;
justify-content:center;
align-items:center;
font-size:32px;
color:white;
font-weight:bold;
">

{icon}

</div>

<h5 style="
margin-top:10px;
color:{color};
">

{title}

</h5>

</div>
""", unsafe_allow_html=True)