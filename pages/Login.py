import streamlit as st

from components.branding import LOGO

st.image(
    "assets/logo.jpg",
    width=180
)

from components.auth import (
    create_users_table,
    login_user
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HealthVibe AI | Login",
    page_icon=str(LOGO),
    layout="centered",
    initial_sidebar_state="collapsed"
)

import translation

translation.init()
t = translation.t

create_users_table()

from components.auth import create_admin

create_admin()

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("""
<style>

#MainMenu{
    visibility:hidden;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

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

st.markdown(
    '<div class="login-card">',
    unsafe_allow_html=True
)

st.markdown("""
<div style="text-align:center;">

    <h1 style="font-size:70px;">
        🩺
    </h1>

    <h2 style="color:#00C2FF;">
        HealthVibe AI
    </h2>

</div>
""", unsafe_allow_html=True)


st.markdown(
    f'<div class="title">{t("HealthVibe AI")}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{t("Welcome Back")}</div>',
    unsafe_allow_html=True
)


# ==========================================
# ROLE
# ==========================================

role = st.radio(
    t("Login As"),
    ["Patient", "Doctor", "Admin"],
    format_func=t,
    horizontal=True
)


# ==========================================
# EMAIL
# ==========================================

email = st.text_input(
    t("📧 Email"),
    placeholder=t("Enter your email")
)


# ==========================================
# PASSWORD
# ==========================================

password = st.text_input(
    t("🔒 Password"),
    type="password",
    placeholder=t("Enter your password")
)


remember = st.checkbox(
    t("Remember me")
)


# ==========================================
# LOGIN
# ==========================================

st.write("")

if st.button(
    t("🚀 Login"),
    width="stretch"
):

    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if not email.strip() or not password:

        st.warning(
            t("Please enter your email and password.")
        )

        st.stop()


    # --------------------------------------
    # LOGIN USER
    # --------------------------------------

    user = login_user(
        email.strip(),
        password
    )


    # --------------------------------------
    # INVALID LOGIN
    # --------------------------------------

    if user is None:

        st.error(
            t("❌ Invalid Email or Password")
        )

    # --------------------------------------
    # WRONG ROLE
    # --------------------------------------

    elif user["role"] != role:

        st.error(
            t(
                "This account belongs to a {role}."
            ).format(
                role=t(user["role"])
            )
        )

    # --------------------------------------
    # SUCCESS
    # --------------------------------------

    else:

        st.session_state.logged_in = True

        st.session_state.user = dict(user)

        st.session_state.user_id = user["id"]

        st.session_state.username = user["full_name"]

        st.session_state.email = user["email"]

        st.session_state.role = user["role"]


        st.success(
            t("✅ Login Successful")
        )

        st.balloons()


        # ==================================
        # ROLE BASED REDIRECT
        # ==================================

        if user["role"] == "Admin":

            st.switch_page(
                "pages/Admin_Dashboard.py"
            )

        elif user["role"] == "Doctor":

            st.switch_page(
                "pages/Doctor_Dashboard.py"
            )

        else:

            st.switch_page(
                "pages/Dashboard.py"
            )


# ==========================================
# REGISTER
# ==========================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="text-align:center;color:#94A3B8;">
        {t("Don't have an account?")}
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# REGISTER BUTTON
# ==========================================

if role == "Admin":

    st.info(
        "Admin accounts cannot be created from public registration."
    )

else:

    if st.button(
        t("📝 Create New Account"),
        width="stretch"
    ):

        st.session_state.role = role

        st.switch_page(
            "pages/Register.py"
        )


# ==========================================
# CLOSE CARD
# ==========================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)