import streamlit as st
import pandas as pd
import plotly.express as px

from components.auth_guard import require_doctor

require_doctor()

from utils.navigation import sidebar

from components.doctor_db import (
    create_doctors_table,
    add_doctor,
    get_doctors,
    search_doctor,
    delete_doctor,
    update_doctor,
    doctors_count,
    available_doctors
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Doctors",
    page_icon="👨‍⚕️",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

create_doctors_table()

# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">

<h1>👨‍⚕️ Doctors Management</h1>

<p>
Manage Doctors, Departments and Availability
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# LOAD DATA
# ==========================================

search = st.text_input(
    "🔍 Search Doctor",
    placeholder="Search by doctor's name..."
)

if search:
    df = search_doctor(search)
else:
    df = get_doctors()

# ==========================================
# DASHBOARD
# ==========================================

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👨‍⚕️ Total Doctors",
        doctors_count()
    )

with col2:
    st.metric(
        "🟢 Available",
        available_doctors()
    )

with col3:
    unavailable = doctors_count() - available_doctors()

    st.metric(
        "🔴 Unavailable",
        unavailable
    )

    # ==========================================
# ADD DOCTOR
# ==========================================

st.subheader("➕ Add New Doctor")

with st.form("doctor_form"):

    doctor_name = st.text_input("Doctor Name")

    department = st.selectbox(
        "Department",
        [
            "Internal Medicine",
            "Cardiology",
            "Neurology",
            "Radiology",
            "Pulmonology",
            "Oncology",
            "Endocrinology",
            "Pediatrics",
            "Orthopedics",
            "General Surgery"
        ]
    )

    specialization = st.text_input("Specialization")

    years = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=60,
        value=5
    )

    available = st.checkbox(
        "Available",
        value=True
    )

    submit = st.form_submit_button(
        "💾 Save Doctor",
        use_container_width=True
    )

    if submit:

        if doctor_name.strip() == "":
            st.warning("Doctor name is required.")

        else:

            add_doctor(
                doctor_name,
                department,
                specialization,
                years,
                available
            )

            st.success("Doctor added successfully ✅")
            st.rerun()

st.write("")

# ==========================================
# DOCTORS TABLE
# ==========================================

st.subheader("👨‍⚕️ Doctors List")

if len(df) == 0:

    st.info("No doctors found.")

else:

    table = df.copy()

    if "available" in table.columns:

        table["available"] = table["available"].replace({
            1: "🟢 Available",
            0: "🔴 Unavailable",
            True: "🟢 Available",
            False: "🔴 Unavailable"
        })

    table = table.rename(columns={
        "id": "ID",
        "name": "Doctor Name",
        "department": "Department",
        "specialization": "Specialization",
        "experience": "Experience",
        "available": "Status",
        "created_at": "Created"
    })

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

st.write("")

# ==========================================
# VIEW & EDIT DOCTOR
# ==========================================

if len(df) > 0:

    st.subheader("✏️ View / Edit Doctor")

    doctor_ids = df["id"].tolist()

    selected_id = st.selectbox(
        "Select Doctor",
        doctor_ids
    )

    doctor = df[df["id"] == selected_id].iloc[0]

    with st.form("edit_doctor"):

        edit_name = st.text_input(
            "Doctor Name",
            value=doctor["name"]
        )

        edit_department = st.text_input(
            "Department",
            value=doctor["department"]
        )

        edit_specialization = st.text_input(
            "Specialization",
            value=doctor["specialization"]
        )

        edit_experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=60,
            value=int(doctor["experience"])
        )

        edit_available = st.checkbox(
            "Available",
            value=bool(doctor["available"])
        )

        update_btn = st.form_submit_button(
            "💾 Update Doctor",
            use_container_width=True
        )

        if update_btn:

            update_doctor(
                selected_id,
                edit_name,
                edit_department,
                edit_specialization,
                edit_experience,
                edit_available
            )

            st.success("Doctor updated successfully ✅")
            st.rerun()

st.write("")

# ==========================================
# DELETE DOCTOR
# ==========================================

st.divider()

st.subheader("🗑 Delete Doctor")

if len(df) > 0:

    delete_id = st.selectbox(
        "Choose Doctor",
        doctor_ids,
        key="delete_doctor"
    )

    confirm_delete = st.checkbox(
        "I confirm deleting this doctor"
    )

    if st.button(
        "Delete Doctor",
        use_container_width=True,
        type="primary"
    ):

        if not confirm_delete:

            st.warning("Please confirm deletion first.")

        else:

            delete_doctor(delete_id)

            st.success("Doctor deleted successfully ✅")

            st.rerun()

else:

    st.info("No doctors available.")

st.write("")

# ==========================================
# DOCTOR STATISTICS
# ==========================================

st.divider()

st.subheader("📊 Doctors Statistics")

if len(df) > 0:

    total = len(df)

    available = len(df[df["available"] == 1])

    unavailable = total - available

    avg_exp = round(df["experience"].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "👨‍⚕️ Total Doctors",
            total
        )

    with c2:
        st.metric(
            "🟢 Available",
            available
        )

    with c3:
        st.metric(
            "🔴 Unavailable",
            unavailable
        )

    with c4:
        st.metric(
            "⭐ Avg Experience",
            f"{avg_exp} Years"
        )

else:

    st.info("No statistics available.")

st.write("")

# ==========================================
# CHARTS
# ==========================================

st.divider()

st.subheader("📈 Doctors Analytics")

if len(df) > 0:

    left, right = st.columns(2)

    with left:

        dep = (
            df.groupby("department")
            .size()
            .reset_index(name="Doctors")
        )

        fig = px.bar(
            dep,
            x="department",
            y="Doctors",
            title="Doctors by Department",
            color="department"
        )

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Doctors"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        status = pd.DataFrame({

            "Status": [
                "Available",
                "Unavailable"
            ],

            "Count": [
                len(df[df["available"] == 1]),
                len(df[df["available"] == 0])
            ]

        })

        fig2 = px.pie(
            status,
            values="Count",
            names="Status",
            hole=0.55,
            title="Availability Status"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

st.write("")

# ==========================================
# EXPORT CSV
# ==========================================

st.divider()

st.subheader("📄 Export Doctors Data")

if len(df) > 0:

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="⬇ Download Doctors List",

        data=csv,

        file_name="Doctors_List.csv",

        mime="text/csv",

        use_container_width=True

    )

else:

    st.info("No data available to export.")

st.write("")

# ==========================================
# QUICK SUMMARY
# ==========================================

st.divider()

st.subheader("📌 Quick Summary")

if len(df) > 0:

    st.success(f"""
Total Doctors : {total}

Available Doctors : {available}

Unavailable Doctors : {unavailable}

Average Experience : {avg_exp} Years
""")

else:

    st.warning("No doctors registered yet.")

# ==========================================
# FOOTER
# ==========================================

st.write("")
st.divider()

st.markdown("""

<div class="footer">

<h2 style="color:#00C2FF;">
HealthVibe AI
</h2>

<p>
Doctors Management System
</p>

<hr>

<p style="color:#94A3B8;">
Developed by <b>Badr Ahmed</b>
</p>

</div>

""", unsafe_allow_html=True)