import streamlit as st

from translations import get_text


def sidebar(lang=None):

    if lang is None:
        lang = st.session_state.get("lang", "en")

    with st.sidebar:

        st.markdown(f"""
        <div style="text-align:center;">

        <h1 style="
        color:#00C2FF;
        font-size:55px;
        margin-bottom:-15px;
        ">
        🩺
        </h1>

        <h2 style="color:white;">
        {get_text(lang, "app_title")}
        </h2>

        <p style="
        color:#94A3B8;
        margin-top:-10px;
        ">
        {get_text(lang, "sidebar_subtitle")}
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(f"### 📊 {get_text(lang, 'sidebar_status_header')}")

        st.success(f"🟢 {get_text(lang, 'sidebar_ai_online')}")

        st.info(get_text(lang, "sidebar_version"))

        st.divider()

        st.markdown(f"""
### 👨‍💻 {get_text(lang, "sidebar_developer_header")}

**Badr Ahmed**

{get_text(lang, "sidebar_developer_role1")}

{get_text(lang, "sidebar_developer_role2")}
""")

        st.divider()

        st.caption(get_text(lang, "sidebar_copyright"))


def hide_sidebar():

    st.markdown("""
    <style>

    section[data-testid="stSidebar"]{
        display:none;
    }

    div[data-testid="collapsedControl"]{
        display:none;
    }

    </style>
    """, unsafe_allow_html=True)