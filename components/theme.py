import streamlit as st


def apply_theme():

    theme = st.session_state.get("theme", "Dark")

    if theme == "Dark":

        st.markdown("""
        <style>

        .stApp {
            background-color: #0B1220;
            color: white;
        }

        </style>
        """, unsafe_allow_html=True)


    else:

        st.markdown("""
        <style>

        .stApp {
            background-color: white;
            color: black;
        }

        </style>
        """, unsafe_allow_html=True)