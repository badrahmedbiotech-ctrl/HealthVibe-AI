import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.divider()

        if st.button("💬 AI Assistant", use_container_width=True):
            st.switch_page("pages/chatbot.py")