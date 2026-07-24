import streamlit as st

from components.database import (
    create_profile,
    get_profile,
    update_profile
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="My Medical Profile",
    page_icon="🩺",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================
# LOGIN CHECK
# ==========================================

if "user" not in st.session_state:

    st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.user

# ==========================================
# CREATE PROFILE IF NOT EXISTS
# ==========================================

create_profile(user["id"])

profile = get_profile(user["id"])


full_name = st.text_input(
    "👤 Full Name",
    value=profile["full_name"] or user["full_name"]
)

age = st.number_input(
    "🎂 Age",
    min_value=1,
    max_value=120,
    value=profile["age"] or 20
)

gender = st.selectbox(
    "⚧ Gender",
    ["Male", "Female"]
)

weight = st.number_input(
    "⚖ Weight (kg)",
    min_value=1.0,
    value=float(profile["weight"] or 70)
)

height = st.number_input(
    "📏 Height (cm)",
    min_value=1.0,
    value=float(profile["height"] or 170)
)

# ==========================================
# HEADER
# ==========================================

st.markdown(f"""

<div class="hero">

<h1>
👤 My Medical Profile
</h1>

<p>

Welcome

<b>{user["full_name"]}</b>

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================
# PERSONAL INFORMATION
# ==========================================

st.subheader("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    phone = st.text_input(
        "📞 Phone Number",
        value=profile["phone"] or ""
    )

    birth_date = st.text_input(
        "🎂 Birth Date",
        value=profile["birth_date"] or ""
    )

    blood_group = st.selectbox(

        "🩸 Blood Group",

        [

            "",
            "A+","A-",
            "B+","B-",
            "AB+","AB-",
            "O+","O-"

        ]

    )

with col2:

    address = st.text_input(
        "🏠 Address",
        value=profile["address"] or ""
    )

    smoking = st.selectbox(

        "🚬 Smoking",

        [

            "No",

            "Yes"

        ]

    )

    alcohol = st.selectbox(

        "🍺 Alcohol",

        [

            "No",

            "Yes"

        ]

    )

st.divider()

# ==========================================
# MEDICAL INFORMATION
# ==========================================

st.subheader("🩺 Medical Information")

col1, col2 = st.columns(2)

with col1:

    allergies = st.text_area(

        "🤧 Allergies",

        value=profile["allergies"] or "",

        height=120

    )

    chronic_diseases = st.text_area(

        "❤️ Chronic Diseases",

        value=profile["chronic_diseases"] or "",

        height=120

    )

with col2:

    medications = st.text_area(

        "💊 Current Medications",

        value=profile["medications"] or "",

        height=120

    )

    st.info(
        """
You can write one medication per line.

Example:

Metformin

Vitamin D

Aspirin
"""
    )

st.divider()

# ==========================================
# EMERGENCY CONTACT
# ==========================================

st.subheader("🚨 Emergency Contact")

col1, col2 = st.columns(2)

with col1:

    emergency_name = st.text_input(

        "Contact Name",

        value=profile["emergency_name"] or ""

    )

    emergency_relation = st.text_input(

        "Relationship",

        value=profile["emergency_relation"] or ""

    )

with col2:

    emergency_phone = st.text_input(

        "Phone Number",

        value=profile["emergency_phone"] or ""

    )

st.divider()

# ==========================================
# SAVE PROFILE
# ==========================================

if st.button(
    "💾 Save Medical Profile",
    use_container_width=True
):

    update_profile({

        "user_id": user["id"],

        "full_name": full_name,
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height,

        "phone": phone,
        "address": address,
        "birth_date": birth_date,
        "blood_group": blood_group,
        "smoking": smoking,
        "alcohol": alcohol,
        "allergies": allergies,
        "chronic_diseases": chronic_diseases,
        "medications": medications,
        "emergency_name": emergency_name,
        "emergency_phone": emergency_phone,
        "emergency_relation": emergency_relation

    })

    st.success("✅ Medical Profile Updated Successfully!")
    st.balloons()

    st.write("")

# ==========================================
# BACK BUTTON
# ==========================================

if st.button(

    "⬅ Back To Dashboard",

    use_container_width=True

):

    if user["role"] == "Doctor":

        st.switch_page("pages/doctor_db.py")

    else:

        st.switch_page("pages/Dashboard.py")