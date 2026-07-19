import streamlit as st

from components.auth import (
    create_users_table,
    create_default_admin,
    login,
)

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="centered"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


create_users_table()
create_default_admin()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.logged_in:

    st.switch_page("pages/Dashboard.py")

    st.markdown("""

<div class="hero">

<h1>🩺 HealthVibe AI</h1>

<p>
AI Clinical Decision Support System
</p>

</div>

""", unsafe_allow_html=True)

st.write("")

with st.container(border=True):

    st.subheader("🔐 Login")

    username = st.text_input(
        "Username",
        placeholder="Enter your username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    st.write("")

    login_btn = st.button(
        "Login",
        use_container_width=True
    )

    if login_btn:

     if username.strip() == "" or password.strip() == "":

        st.warning("Please enter username and password.")

    else:

        user = login(username, password)

        if user is None:

            st.error("Invalid username or password.")

        else:

            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]

            st.success("Login Successful ✅")

            st.rerun()

