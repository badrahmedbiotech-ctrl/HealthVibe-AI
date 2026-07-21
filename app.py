import streamlit as st

from components.auth import (
    create_users_table,
    create_default_admin,
    login
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="centered"
)

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================
# DATABASE
# ==========================================

create_users_table()
create_default_admin()

# ==========================================
# SESSION
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# ==========================================
# REDIRECT
# ==========================================

if st.session_state.logged_in:
    st.switch_page("pages/Dashboard.py")

# ==========================================
# HERO
# ==========================================

st.markdown("""

<div class="hero">

<h1>🩺 HealthVibe AI</h1>

<p>
AI Clinical Decision Support System
</p>

</div>

""", unsafe_allow_html=True)

st.write("")


# ==========================================
# LOGIN CARD
# ==========================================

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

        # Validation
        if username.strip() == "" or password.strip() == "":

            st.warning("Please enter your username and password.")

        else:

            user = login(
                username=username,
                password=password
            )

            if user is None:

                st.error("❌ Invalid username or password.")

            else:

                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]

                st.success(f"Welcome {user['username']} 👋")

                st.rerun()

# ==========================================
# FOOTER
# ==========================================

st.write("")
st.markdown("---")

st.caption(
    "© 2026 HealthVibe AI • Secure Authentication System"
)