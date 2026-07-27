import streamlit as st


def init_preferences():

    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"

    if "language" not in st.session_state:
        st.session_state.language = "English"


def set_theme(theme):
    st.session_state.theme = theme


def set_language(language):
    st.session_state.language = language