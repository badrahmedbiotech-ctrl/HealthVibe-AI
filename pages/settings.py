import streamlit as st
from utils.navigation import sidebar

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import translation
translation.init()

# ==========================================
# CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================
# LOGIN
# ==========================================

if "logged_in" not in st.session_state:
    st.switch_page("app.py")
    st.stop()

user = st.session_state.user

username = user["username"]
role = user["role"]

# ==========================================
# HERO
# ==========================================

st.markdown(f"""
<div class="hero">

<span class="hero-badge">
⚙️ {translation.t("⚙️ System Settings")}
</span>

<div style="display:flex;justify-content:space-between;align-items:center;">

<div>

<h1>
{translation.t("Settings")}
</h1>

<p>

{translation.t("Welcome")} {username}

</p>

</div>

<div style="font-size:95px;">
⚙️
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# ACCOUNT SETTINGS
# ==========================================

st.subheader(translation.t("👤 Account Settings"))

c1, c2 = st.columns(2)

with c1:

    st.text_input(
        translation.t("Username"),
        value=username,
        disabled=True
    )

    st.text_input(
        translation.t("Role"),
        value=role,
        disabled=True
    )

with c2:

    email = st.text_input(
        translation.t("Email"),
        value=st.session_state.user.get("email", ""),
        disabled=True
    )

    st.text_input(
        translation.t("Status"),
        value=translation.t("Active"),
        disabled=True
    )

st.divider()

# ==========================================
# SYSTEM SETTINGS
# ==========================================

st.subheader(translation.t("⚙️ Preferences"))

dark_mode = st.toggle(
    translation.t("Dark Mode"),
    value=True
)

notifications = st.toggle(
    translation.t("Enable Notifications"),
    value=True
)

ai_recommendation = st.toggle(
    translation.t("AI Recommendations"),
    value=True
)

language = st.selectbox(
    translation.t("Language"),
    [
        "English",
        "Arabic"
    ],
    format_func=translation.t
)

st.divider()

st.write("")

# ==========================================
# ACCOUNT SETTINGS
# ==========================================

st.subheader(translation.t("👤 Account Settings"))

c1, c2 = st.columns(2)

with c1:

    st.text_input(
        translation.t("Username"),
        value=username,
        disabled=True
    )

    st.text_input(
        translation.t("Role"),
        value=role,
        disabled=True
    )

with c2:

    email = st.text_input(
        translation.t("Email"),
        value=st.session_state.user.get("email", ""),
        disabled=True
    )

    st.text_input(
        translation.t("Status"),
        value=translation.t("Active"),
        disabled=True
    )

st.divider()

# ==========================================
# SYSTEM SETTINGS
# ==========================================

st.subheader(translation.t("⚙️ Preferences"))

dark_mode = st.toggle(
    translation.t("Dark Mode"),
    value=True
)

notifications = st.toggle(
    translation.t("Enable Notifications"),
    value=True
)

ai_recommendation = st.toggle(
    translation.t("AI Recommendations"),
    value=True
)

language = st.selectbox(
    translation.t("Language"),
    [
        "English",
        "Arabic"
    ],
    format_func=translation.t
)

st.divider()