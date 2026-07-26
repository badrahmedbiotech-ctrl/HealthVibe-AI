import streamlit as st


def require_login():
    if not st.session_state.get("logged_in", False):
        st.warning("Please login first.")
        st.stop()


def require_patient():
    require_login()
    user = st.session_state.get("user") or {}
    role = (
        user.get("role", "")
        if isinstance(user, dict)
        else st.session_state.get("role", "")
    )
    if str(role).lower() != "patient":
        st.error("Access Denied: Patient access required.")
        st.stop()


def require_doctor():
    require_login()
    user = st.session_state.get("user") or {}
    role = (
        user.get("role", "")
        if isinstance(user, dict)
        else st.session_state.get("role", "")
    )
    if str(role).lower() != "doctor":
        st.error("Access Denied: Doctor access required.")
        st.stop()