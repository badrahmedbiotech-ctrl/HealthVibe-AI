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

import translation
translation.init()

create_users_table()

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

role = st.session_state.get("role", "Patient")

st.markdown(
    '<div class="register-card">',
    unsafe_allow_html=True
)

st.markdown(
f"""
<div style="text-align:center;padding-bottom:15px;">
    <h1 style="font-size:70px;">🩺</h1>
    <h2 style="color:#00C2FF;">
        {translation.t("HealthVibe AI")}
    </h2>
</div>
""",
unsafe_allow_html=True
)

st.markdown(
    f'<div class="title">{translation.t("Create Account")}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">'
    f'{translation.t("Register as ")}{translation.t(role)}'
    f'</div>',
    unsafe_allow_html=True
)

full_name = st.text_input(
    translation.t("👤 Full Name"),
    placeholder=translation.t("Enter your full name")
)

email = st.text_input(
    translation.t("📧 Email"),
    placeholder=translation.t("Enter your email")
)

password = st.text_input(
    translation.t("🔒 Password"),
    type="password",
    placeholder=translation.t("Create password")
)

confirm = st.text_input(
    translation.t("🔒 Confirm Password"),
    type="password",
    placeholder=translation.t("Confirm password")
)

st.write("")

if st.button(
    translation.t("🚀 Create Account"),
    width="stretch"
):

    if not full_name.strip():

        st.error(
            translation.t("Please enter your name.")
        )

    elif not email.strip():

        st.error(
            translation.t("Please enter your email.")
        )

    elif password != confirm:

        st.error(
            translation.t("Passwords do not match.")
        )

    elif len(password) < 6:

        st.error(
            translation.t(
                "Password must be at least 6 characters."
            )
        )

    else:

        success = register_user(
            full_name.strip(),
            email.strip(),
            password,
            role
        )

        if success:

            st.success(
                translation.t(
                    "✅ Account Created Successfully"
                )
            )

            st.balloons()

            st.switch_page(
                "pages/Login.py"
            )

        else:

            st.error(
                translation.t(
                    "This email already exists."
                )
            )

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
f"""
<div style="text-align:center;color:#94A3B8;">
    {translation.t("Already have an account?")}
</div>
""",
unsafe_allow_html=True
)

if st.button(
    translation.t("🔐 Login"),
    width="stretch"
):

    st.switch_page(
        "pages/Login.py"
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)