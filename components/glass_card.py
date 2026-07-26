import streamlit as st

def open_card():
    st.markdown("""
    <style>
    .glass-card{
        background:rgba(255,255,255,.06);
        backdrop-filter:blur(18px);
        border:1px solid rgba(255,255,255,.08);
        border-radius:20px;
        padding:30px;
        box-shadow:0 10px 30px rgba(0,0,0,.25);
        margin-top:20px;
        margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True)

def close_card():
    pass