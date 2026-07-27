import streamlit as st
from components.auth import (
    create_users_table,
    login_user
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HealthVibe AI | Login",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

create_users_table()

# ==========================================
# LOAD CSS
# ==========================================

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
max-width:480px;
padding-top:2rem;
}

.login-card{
background:#111827;
padding:35px;
border-radius:24px;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 10px 40px rgba(0,0,0,.35);
}

.title{
text-align:center;
font-size:36px;
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
transition:0.3s;
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

[data-testid="stRadio"]{
padding-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION
# ==========================================

defaults = {
    "logged_in": False,
    "user": None,
    "username": "",
    "role": "Patient",
    "email": "",
    "user_id": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================
# LOGIN CARD
# ==========================================

st.markdown('<div class="login-card">', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;">
    <h1 style="font-size:70px;">🩺</h1>
    <h2 style="color:#00C2FF;">HealthVibe AI</h2>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">HealthVibe AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Welcome Back</div>',
    unsafe_allow_html=True
)

role = st.radio(
    "Login As",
    ["Patient", "Doctor"],
    horizontal=True
)

email = st.text_input(
    "📧 Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "🔒 Password",
    type="password",
    placeholder="Enter your password"
)

remember = st.checkbox("Remember me")

# ==========================================
# LOGIN BUTTON
# ==========================================

st.write("")

if st.button(
    "🚀 Login",
    use_container_width=True
):

    user = login_user(email, password)

    if user is None:

        st.error("❌ Invalid Email or Password")

    elif user["role"] != role:

        st.error(
            f"This account belongs to a {user['role']}."
        )

    else:

        st.session_state.logged_in = True

        st.session_state.user = dict(user)

        st.session_state.user_id = user["id"]
        st.session_state.username = user["full_name"]
        st.session_state.email = user["email"]
        st.session_state.role = user["role"]

        st.success("✅ Login Successful")

        st.balloons()

        st.switch_page("pages/Dashboard.py")


st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
"""
<div style="text-align:center;color:#94A3B8;">
Don't have an account?
</div>
""",
unsafe_allow_html=True
)

if st.button(
    "📝 Create New Account",
    use_container_width=True
):

    st.session_state.role = role

    st.switch_page("pages/Register.py")


st.markdown("</div>", unsafe_allow_html=True)