import streamlit as st


# ==========================================================
# LOGIN
# ==========================================================

def require_login():

    user = st.session_state.get("user")

    if user is None:

        st.warning("Please login first.")

        st.switch_page("pages/Login.py")

        st.stop()

    return user


# ==========================================================
# PATIENT
# ==========================================================

def require_patient():

    user = require_login()

    if user["role"] != "Patient":

        st.error("Access Denied")

        st.stop()

    return user


# ==========================================================
# DOCTOR
# ==========================================================

def require_doctor():

    user = require_login()

    if user["role"] != "Doctor":

        st.error("Access Denied")

        st.stop()

    return user


# ==========================================================
# ADMIN
# ==========================================================

def require_admin():

    user = require_login()

    if user["role"] != "Admin":

        st.error("Access Denied")

        st.stop()

    return user


# ==========================================================
# ADMIN OR DOCTOR
# ==========================================================

def require_admin_or_doctor():

    user = require_login()

    if user["role"] not in ["Admin", "Doctor"]:

        st.error("Access Denied")

        st.stop()

    return user