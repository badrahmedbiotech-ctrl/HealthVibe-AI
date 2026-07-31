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
⚙️ System Settings
</span>

<div style="display:flex;justify-content:space-between;align-items:center;">

<div>

<h1>
Settings
</h1>

<p>

Welcome {username}

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

st.subheader("👤 Account Settings")

c1, c2 = st.columns(2)

with c1:

    st.text_input(
        "Username",
        value=username,
        disabled=True
    )

    st.text_input(
        "Role",
        value=role,
        disabled=True
    )

with c2:

    email = st.text_input(
        "Email",
        value=st.session_state.user.get("email", ""),
        disabled=True
    )

    st.text_input(
        "Status",
        value="Active",
        disabled=True
    )

st.divider()

# ==========================================
# SYSTEM SETTINGS
# ==========================================

st.subheader("⚙️ Preferences")

dark_mode = st.toggle(
    "Dark Mode",
    value=True
)

notifications = st.toggle(
    "Enable Notifications",
    value=True
)

ai_recommendation = st.toggle(
    "AI Recommendations",
    value=True
)

language = st.selectbox(
    "Language",
    [
        "English",
        "Arabic"
    ]
)

st.divider()

st.write("")

# ==========================================
# ACCOUNT SETTINGS
# ==========================================

st.subheader("👤 Account Settings")

c1, c2 = st.columns(2)

with c1:

    st.text_input(
        "Username",
        value=username,
        disabled=True
    )

    st.text_input(
        "Role",
        value=role,
        disabled=True
    )

with c2:

    email = st.text_input(
        "Email",
        value=st.session_state.user.get("email", ""),
        disabled=True
    )

    st.text_input(
        "Status",
        value="Active",
        disabled=True
    )

st.divider()

# ==========================================
# SYSTEM SETTINGS
# ==========================================

st.subheader("⚙️ Preferences")

dark_mode = st.toggle(
    "Dark Mode",
    value=True
)

notifications = st.toggle(
    "Enable Notifications",
    value=True
)

ai_recommendation = st.toggle(
    "AI Recommendations",
    value=True
)

language = st.selectbox(
    "Language",
    [
        "English",
        "Arabic"
    ]
)

st.divider()