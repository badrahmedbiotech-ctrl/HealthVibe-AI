import streamlit as st

from components.auth import (
    create_users_table,
    register_user
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)

create_users_table()

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================
# HEADER
# ==========================================

role = st.session_state.get("role", "Patient")

st.markdown(f"""

<div style="text-align:center;padding-top:30px;">

<h1 style="color:#00C2FF;">
📝 Create {role} Account
</h1>

<p style="color:#94A3B8;">
Join HealthVibe AI
</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================
# FORM
# ==========================================

full_name = st.text_input("Full Name")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

confirm = st.text_input(
    "Confirm Password",
    type="password"
)

st.write("")

# ==========================================
# REGISTER
# ==========================================

if st.button(
    "Create Account",
    use_container_width=True
):

    if not full_name.strip():

        st.error("Enter your name")

    elif not email.strip():

        st.error("Enter email")

    elif password != confirm:

        st.error("Passwords do not match")

    elif len(password) < 6:

        st.error("Password must be at least 6 characters")

    else:

        success = register_user(

            full_name,

            email,

            password,

            role

        )

        if success:

            st.success("Account Created Successfully ✅")

            st.balloons()

            st.switch_page("pages/Login.py")

        else:

            st.error("Email already exists")

# ==========================================
# BACK
# ==========================================

st.divider()

if st.button(
    "⬅ Back To Login",
    use_container_width=True
):

    st.switch_page("pages/Login.py")

    