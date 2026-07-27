import streamlit as st


def require_login():

    user = st.session_state.get("user")

    if user is None:

        st.warning("Please login first.")

        st.switch_page("pages/Login.py")

        st.stop()


def require_patient():

    require_login()

    user = st.session_state.get("user")

    if user["role"] != "Patient":

        st.error("Access Denied")

        st.stop()


def require_doctor():

    require_login()

    user = st.session_state.get("user")

    if user["role"] != "Doctor":

        st.error("Access Denied")

        st.stop()