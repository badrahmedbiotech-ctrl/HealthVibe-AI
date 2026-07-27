import streamlit as st

from components.theme import apply_theme

from components.preferences import (
    init_preferences,
    set_theme,
    set_language
)

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="centered"
)

init_preferences()
apply_theme()

# أول مرة يفتح Settings
if "settings_page" not in st.session_state:
    st.session_state.settings_page = "home"

# ==========================
# الصفحة الرئيسية
# ==========================
if st.session_state.settings_page == "home":

    st.title("⚙️ Settings")

    if st.button("👤 My Profile", use_container_width=True):
        st.session_state.settings_page = "profile"
        st.rerun()

    if st.button("🌙 Appearance", use_container_width=True):
        st.session_state.settings_page = "appearance"
        st.rerun()

    if st.button("🌐 Language", use_container_width=True):
        st.session_state.settings_page = "language"
        st.rerun()

    if st.button("🔔 Notifications", use_container_width=True):
        st.session_state.settings_page = "notifications"
        st.rerun()

    if st.button("🤖 AI Assistant", use_container_width=True):
        st.session_state.settings_page = "ai"
        st.rerun()

    if st.button("🔒 Privacy & Security", use_container_width=True):
        st.session_state.settings_page = "privacy"
        st.rerun()

    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.settings_page = "about"
        st.rerun()

    if st.button("🚪 Log Out", use_container_width=True):
        st.session_state.settings_page = "logout"
        st.rerun()


# ==========================
# My Profile
# ==========================
elif st.session_state.settings_page == "profile":

    st.title("👤 My Profile")

    st.text_input(
        "Full Name",
        value=st.session_state.get("username", ""),
        disabled=True
    )

    st.text_input(
        "Email",
        value=st.session_state.get("email", ""),
        disabled=True
    )

    st.text_input(
        "Role",
        value=st.session_state.get("role", ""),
        disabled=True
    )

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()


# ==========================
# باقي الصفحات (مؤقتًا)
# ==========================
elif st.session_state.settings_page == "appearance":

    st.title("🌙 Appearance")

    theme = st.radio(
        "Choose Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )

    if st.button("Save Theme", use_container_width=True):
        set_theme(theme)
        st.success("Theme updated successfully ✅")

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()


elif st.session_state.settings_page == "language":

    st.title("🌐 Language")

    language = st.selectbox(
        "Choose Language",
        ["English", "العربية"],
        index=0 if st.session_state.language == "English" else 1
    )

    if st.button("Save Language", use_container_width=True):
        set_language(language)
        st.success("Language updated successfully ✅")

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()

elif st.session_state.settings_page == "notifications":

    st.title("🔔 Notifications")

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()


elif st.session_state.settings_page == "ai":

    st.title("🤖 AI Assistant")

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()


elif st.session_state.settings_page == "privacy":

    st.title("🔒 Privacy & Security")

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()


elif st.session_state.settings_page == "about":

    st.title("ℹ️ About")

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()


elif st.session_state.settings_page == "logout":

    st.title("🚪 Log Out")

    if st.button("Confirm Log Out"):
        st.session_state.clear()
        st.switch_page("pages/Login.py")

    if st.button("⬅️ Back"):
        st.session_state.settings_page = "home"
        st.rerun()