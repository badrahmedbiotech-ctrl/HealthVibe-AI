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
    page_icon="🔐",
    layout="centered"
)

create_users_table()

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================
# SESSION DEFAULTS
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "Patient"

if "email" not in st.session_state:
    st.session_state.email = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div style="text-align:center;padding-top:30px;">

<h1 style="color:#00C2FF;">
🩺 HealthVibe AI
</h1>

<h3>Login</h3>

<p style="color:#94A3B8;">
Welcome Back
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# ROLE
# ==========================================

role = st.radio(
    "Login As",
    ["Patient", "Doctor"],
    horizontal=True
)

st.write("")

# ==========================================
# LOGIN FORM
# ==========================================

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

remember = st.checkbox("Remember me")

st.write("")

# ==========================================
# LOGIN BUTTON
# ==========================================

if st.button(
    "🔐 Login",
    use_container_width=True
):

    user = login_user(email, password)

    if user is None:

        st.error("Invalid Email or Password")

    elif user["role"] != role:

        st.error(
            f"This account belongs to a {user['role']}."
        )

    else:

        st.session_state.logged_in = True

        # كامل بيانات المستخدم
        st.session_state.user = dict(user)

        # بيانات منفصلة
        st.session_state.user_id = user["id"]
        st.session_state.username = user["full_name"]
        st.session_state.email = user["email"]
        st.session_state.role = user["role"]

        st.success("Login Successful ✅")

        st.switch_page("pages/Dashboard.py")

# ==========================================
# REGISTER
# ==========================================

st.divider()

st.write("Don't have an account?")

if st.button(
    "📝 Create New Account",
    use_container_width=True
):

    st.session_state.role = role

    st.switch_page("pages/Register.py")