import streamlit as st
from components.branding import *
from components.auth import (
    create_users_table,
    register_user
)

st.set_page_config(
    page_title="HealthVibe AI | Register",
    page_icon=str(LOGO),
    layout="centered",
    initial_sidebar_state="collapsed"
)

create_users_table()

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>

#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

.stApp{
background:#0B1120;
}

.block-container{
max-width:500px;
padding-top:2rem;
}

.register-card{
background:#111827;
padding:35px;
border-radius:24px;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 10px 40px rgba(0,0,0,.35);
}

.title{
text-align:center;
font-size:34px;
font-weight:700;
color:white;
margin-bottom:5px;
}

.subtitle{
text-align:center;
color:#94A3B8;
margin-bottom:30px;
}

.stButton>button{
width:100%;
height:50px;
border-radius:14px;
border:none;
font-size:18px;
font-weight:600;
background:linear-gradient(90deg,#10B981,#2563EB);
color:white;
transition:.3s;
}

.stButton>button:hover{
transform:scale(1.02);
}

[data-testid="stTextInput"] input{
background:#1F2937;
color:white;
border-radius:12px;
border:1px solid #374151;
height:48px;
}

</style>
""", unsafe_allow_html=True)

role = st.session_state.get("role","Patient")

st.markdown('<div class="register-card">',unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding-bottom:15px;">
    <h1 style="font-size:70px;">🩺</h1>
    <h2 style="color:#00C2FF;">HealthVibe AI</h2>
</div>
""", unsafe_allow_html=True)

st.markdown(
'<div class="title">Create Account</div>',
unsafe_allow_html=True
)

st.markdown(
f'<div class="subtitle">Register as {role}</div>',
unsafe_allow_html=True
)

full_name = st.text_input(
    "👤 Full Name",
    placeholder="Enter your full name"
)

email = st.text_input(
    "📧 Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "🔒 Password",
    type="password",
    placeholder="Create password"
)

confirm = st.text_input(
    "🔒 Confirm Password",
    type="password",
    placeholder="Confirm password"
)

st.write("")

if st.button(
    "🚀 Create Account",
    width="stretch"
):

    if not full_name.strip():

        st.error("Please enter your name.")

    elif not email.strip():

        st.error("Please enter your email.")

    elif password != confirm:

        st.error("Passwords do not match.")

    elif len(password) < 6:

        st.error("Password must be at least 6 characters.")

    else:

        success = register_user(

            full_name,

            email,

            password,

            role

        )

        if success:

            st.success("✅ Account Created Successfully")

            st.balloons()

            st.switch_page("pages/Login.py")

        else:

            st.error("This email already exists.")

st.markdown("<br>",unsafe_allow_html=True)

st.markdown(
"""
<div style="text-align:center;color:#94A3B8;">
Already have an account?
</div>
""",
unsafe_allow_html=True
)

if st.button(
    "🔐 Login",
    width="stretch"
):
    st.switch_page("pages/Login.py")

st.markdown("</div>",unsafe_allow_html=True)