import streamlit as st
import pandas as pd
from datetime import datetime

from utils.navigation import sidebar

from components.database import (
    total_patients,
    get_all_history,
    get_profile,
    create_profile,
    update_profile
)

from components.doctor_db import (
    doctors_count,
    available_doctors
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="My Medical Profile",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

# ==========================================
# SESSION CHECK
# ==========================================

if "logged_in" not in st.session_state:
    st.switch_page("app.py")
    st.stop()

user = st.session_state.get("user", {})

user_id = user.get("id")
user_name = user.get("full_name", "")
full_name_user = user.get("full_name", "")
role = user.get("role", "Patient")
# ==========================================
# LOAD PROFILE
# ==========================================

create_profile(user_id)

profile = get_profile(user_id)

if profile:
    profile = dict(profile)
else:
    profile = {}
# ==========================================
# SAFE VALUES
# ==========================================

full_name = profile.get("full_name") or full_name_user

age = int(profile.get("age") or 20)

gender = profile.get("gender") or "Male"

weight = float(profile.get("weight") or 70)

height = float(profile.get("height") or 170)

phone = profile.get("phone") or ""

address = profile.get("address") or ""

birth_date = profile.get("birth_date") or ""

blood_group = profile.get("blood_group") or ""

smoking = profile.get("smoking") or "No"

alcohol = profile.get("alcohol") or "No"

allergies = profile.get("allergies") or ""

chronic_diseases = profile.get("chronic_diseases") or ""

medications = profile.get("medications") or ""

emergency_name = profile.get("emergency_name") or ""

emergency_phone = profile.get("emergency_phone") or ""

emergency_relation = profile.get("emergency_relation") or ""

# ==========================================
# HERO
# ==========================================

st.markdown(f"""
<div class="hero">

<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">

<div>

<span class="hero-badge">
🟢 Medical Profile
</span>

<h1>
👤 {full_name}
</h1>

<p>
Manage your medical information securely
</p>

</div>

<div style="font-size:100px;">
🩺
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# QUICK INFO
# ==========================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Age", age)

with m2:
    st.metric("Gender", gender)

with m3:
    st.metric("Weight", f"{weight} kg")

with m4:
    st.metric("Height", f"{height} cm")

st.write("")
st.divider()

# ==========================================
# PERSONAL INFORMATION
# ==========================================

st.subheader("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    full_name = st.text_input(
        "Full Name",
        value=full_name
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=age
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"],
        index=0 if gender == "Male" else 1
    )

    birth_date = st.text_input(
        "Birth Date",
        value=birth_date
    )

with col2:

    phone = st.text_input(
        "Phone Number",
        value=phone
    )

    address = st.text_input(
        "Address",
        value=address
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        value=weight
    )

    height = st.number_input(
        "Height (cm)",
        min_value=1.0,
        value=height
    )

st.write("")
st.divider()

# ==========================================
# MEDICAL INFORMATION
# ==========================================

st.subheader("🩺 Medical Information")

left, right = st.columns(2)

with left:

    blood_group = st.selectbox(
        "Blood Group",
        [
            "",
            "A+","A-",
            "B+","B-",
            "AB+","AB-",
            "O+","O-"
        ],
        index=[
            "",
            "A+","A-",
            "B+","B-",
            "AB+","AB-",
            "O+","O-"
        ].index(blood_group if blood_group in [
            "",
            "A+","A-",
            "B+","B-",
            "AB+","AB-",
            "O+","O-"
        ] else "")
    )

    smoking = st.selectbox(
        "Smoking",
        ["No", "Yes"],
        index=0 if smoking == "No" else 1
    )

    alcohol = st.selectbox(
        "Alcohol",
        ["No", "Yes"],
        index=0 if alcohol == "No" else 1
    )

with right:

    allergies = st.text_area(
        "Allergies",
        value=allergies,
        height=120
    )

    chronic_diseases = st.text_area(
        "Chronic Diseases",
        value=chronic_diseases,
        height=120
    )

st.write("")

medications = st.text_area(
    "Current Medications",
    value=medications,
    height=120
)

st.divider()

# ==========================================
# EMERGENCY CONTACT
# ==========================================

st.subheader("🚨 Emergency Contact")

c1, c2 = st.columns(2)

with c1:

    emergency_name = st.text_input(
        "Contact Name",
        value=emergency_name
    )

    emergency_relation = st.text_input(
        "Relationship",
        value=emergency_relation
    )

with c2:

    emergency_phone = st.text_input(
        "Phone Number",
        value=emergency_phone
    )

st.write("")
st.divider()

# ==========================================
# SAVE PROFILE
# ==========================================

st.subheader("💾 Save Changes")

if st.button(
    "💾 Save Medical Profile",
    use_container_width=True
):

    update_profile({

        "user_id": user_id,

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

    st.success("✅ Medical Profile Updated Successfully")

    st.balloons()

st.write("")
st.divider()

# ==========================================
# PROFILE SUMMARY
# ==========================================

st.subheader("📊 Profile Summary")

s1, s2, s3 = st.columns(3)

with s1:

    st.metric(
        "Profile Completion",
        "100%"
    )

with s2:

    st.metric(
        "Blood Group",
        blood_group if blood_group else "--"
    )

with s3:

    bmi = round(weight / ((height / 100) ** 2), 1)

    st.metric(
        "BMI",
        bmi
    )

st.write("")

if bmi < 18.5:

    st.info("⚠ Underweight")

elif bmi < 25:

    st.success("✅ Normal Weight")

elif bmi < 30:

    st.warning("⚠ Overweight")

else:

    st.error("🔴 Obesity")

st.divider()

# ==========================================
# QUICK ACTIONS
# ==========================================

st.subheader("⚡ Quick Actions")

b1, b2 = st.columns(2)

with b1:

    if st.button(
        "🏠 Back To Dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/Dashboard.py")

with b2:

    if st.button(
        "📋 View Medical History",
        use_container_width=True
    ):
        st.switch_page("pages/Patient_History.py")

st.write("")
st.divider()

# ==========================================
# HEALTH TIPS
# ==========================================

st.subheader("💡 Personalized Health Tips")

tips = []

if bmi < 18.5:
    tips = [
        "🥛 Increase healthy calories.",
        "🍗 Eat more protein.",
        "🏋️ Start resistance training."
    ]

elif bmi < 25:
    tips = [
        "🥗 Maintain your balanced diet.",
        "🚶 Walk daily.",
        "💧 Stay hydrated."
    ]

elif bmi < 30:
    tips = [
        "🏃 Increase physical activity.",
        "🍟 Reduce fast food.",
        "🥦 Eat more vegetables."
    ]

else:
    tips = [
        "👨‍⚕️ Consult your physician.",
        "🥗 Follow a weight-loss diet.",
        "🚶 Exercise regularly."
    ]

for tip in tips:
    st.success(tip)

st.write("")
st.divider()

# ==========================================
# ACCOUNT INFO
# ==========================================

st.subheader("🔐 Account")

a1, a2, a3 = st.columns(3)

with a1:
    st.metric("Name", full_name_user)

with a2:
    st.metric("Email", user.get("email", ""))

with a3:
    st.metric("Role", role)
st.write("")
st.divider()

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div style="
text-align:center;
padding:25px;
color:#94A3B8;
">

<h2 style="color:#00C2FF;">
🩺 HealthVibe AI
</h2>

<p>
Your Complete AI Healthcare Platform
</p>

<hr style="margin:20px 0;">

<p>
Made with ❤️ using Streamlit & AI
</p>

<p>
© 2026 HealthVibe AI
</p>

</div>
""", unsafe_allow_html=True)