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

import translation
translation.init()

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

st.markdown(f"""
<div class="hero">

<h1>{translation.t("👨‍⚕️ Doctors Management")}</h1>

<p>
{translation.t("Manage Doctors, Departments and Availability")}
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# LOAD DATA
# ==========================================

search = st.text_input(
    translation.t("🔍 Search Doctor"),
    placeholder=translation.t("Search by doctor's name...")
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
        translation.t("👨‍⚕️ Total Doctors"),
        doctors_count()
    )

with col2:
    st.metric(
        translation.t("🟢 Available"),
        available_doctors()
    )

with col3:
    unavailable = doctors_count() - available_doctors()

    st.metric(
        translation.t("🔴 Unavailable"),
        unavailable
    )

    # ==========================================
# ADD DOCTOR
# ==========================================

st.subheader(translation.t("➕ Add New Doctor"))

DEPARTMENTS = [
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

with st.form("doctor_form"):

    doctor_name = st.text_input(translation.t("Doctor Name"))

    department = st.selectbox(
        translation.t("Department"),
        DEPARTMENTS,
        format_func=translation.t
    )

    specialization = st.text_input(translation.t("Specialization"))

    years = st.number_input(
        translation.t("Years of Experience"),
        min_value=0,
        max_value=60,
        value=5
    )

    available = st.checkbox(
        translation.t("Available"),
        value=True
    )

    submit = st.form_submit_button(
        translation.t("💾 Save Doctor"),
        width="stretch"
    )

    if submit:

        if doctor_name.strip() == "":
            st.warning(translation.t("Doctor name is required."))

        else:

            add_doctor(
                doctor_name,
                department,
                specialization,
                years,
                available
            )

            st.success(translation.t("Doctor added successfully ✅"))
            st.rerun()

st.write("")

# ==========================================
# DOCTORS TABLE
# ==========================================

st.subheader(translation.t("👨‍⚕️ Doctors List"))

if len(df) == 0:

    st.info(translation.t("No doctors found."))

else:

    table = df.copy()

    if "available" in table.columns:

        table["available"] = table["available"].replace({
            1: translation.t("🟢 Available"),
            0: translation.t("🔴 Unavailable"),
            True: translation.t("🟢 Available"),
            False: translation.t("🔴 Unavailable")
        })

    table = table.rename(columns={
        "id": translation.t("ID"),
        "name": translation.t("Doctor Name"),
        "department": translation.t("Department"),
        "specialization": translation.t("Specialization"),
        "experience": translation.t("Experience"),
        "available": translation.t("Status"),
        "created_at": translation.t("Created")
    })

    st.dataframe(
        table,
        width="stretch",
        hide_index=True
    )

st.write("")

# ==========================================
# VIEW & EDIT DOCTOR
# ==========================================

if len(df) > 0:

    st.subheader(translation.t("✏️ View / Edit Doctor"))

    doctor_ids = df["id"].tolist()

    selected_id = st.selectbox(
        translation.t("Select Doctor"),
        doctor_ids
    )

    doctor = df[df["id"] == selected_id].iloc[0]

    with st.form("edit_doctor"):

        edit_name = st.text_input(
            translation.t("Doctor Name"),
            value=doctor["name"]
        )

        edit_department = st.text_input(
            translation.t("Department"),
            value=doctor["department"]
        )

        edit_specialization = st.text_input(
            translation.t("Specialization"),
            value=doctor["specialization"]
        )

        edit_experience = st.number_input(
            translation.t("Years of Experience"),
            min_value=0,
            max_value=60,
            value=int(doctor["experience"])
        )

        edit_available = st.checkbox(
            translation.t("Available"),
            value=bool(doctor["available"])
        )

        update_btn = st.form_submit_button(
            translation.t("💾 Update Doctor"),
            width="stretch"
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

            st.success(translation.t("Doctor updated successfully ✅"))
            st.rerun()

st.write("")

# ==========================================
# DELETE DOCTOR
# ==========================================

st.divider()

st.subheader(translation.t("🗑 Delete Doctor"))

if len(df) > 0:

    delete_id = st.selectbox(
        translation.t("Choose Doctor"),
        doctor_ids,
        key="delete_doctor"
    )

    confirm_delete = st.checkbox(
        translation.t("I confirm deleting this doctor")
    )

    if st.button(
        translation.t("Delete Doctor"),
        width="stretch",
        type="primary"
    ):

        if not confirm_delete:

            st.warning(translation.t("Please confirm deletion first."))

        else:

            delete_doctor(delete_id)

            st.success(translation.t("Doctor deleted successfully ✅"))

            st.rerun()

else:

    st.info(translation.t("No doctors available."))

st.write("")

# ==========================================
# DOCTOR STATISTICS
# ==========================================

st.divider()

st.subheader(translation.t("📊 Doctors Statistics"))

if len(df) > 0:

    total = len(df)

    available = len(df[df["available"] == 1])

    unavailable = total - available

    avg_exp = round(df["experience"].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            translation.t("👨‍⚕️ Total Doctors"),
            total
        )

    with c2:
        st.metric(
            translation.t("🟢 Available"),
            available
        )

    with c3:
        st.metric(
            translation.t("🔴 Unavailable"),
            unavailable
        )

    with c4:
        st.metric(
            translation.t("⭐ Avg Experience"),
            f"{avg_exp} {translation.t('Years')}"
        )

else:

    st.info(translation.t("No statistics available."))

st.write("")

# ==========================================
# CHARTS
# ==========================================

st.divider()

st.subheader(translation.t("📈 Doctors Analytics"))

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
            title=translation.t("Doctors by Department"),
            color="department"
        )

        fig.update_layout(
            xaxis_title=translation.t("Department"),
            yaxis_title=translation.t("Doctors")
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with right:

        status = pd.DataFrame({

            "Status": [
                translation.t("Available"),
                translation.t("🔴 Unavailable")
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
            title=translation.t("Availability Status")
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

st.write("")

# ==========================================
# EXPORT CSV
# ==========================================

st.divider()

st.subheader(translation.t("📄 Export Doctors Data"))

if len(df) > 0:

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label=translation.t("⬇ Download Doctors List"),

        data=csv,

        file_name="Doctors_List.csv",

        mime="text/csv",

        width="stretch"

    )

else:

    st.info(translation.t("No data available to export."))

st.write("")

# ==========================================
# QUICK SUMMARY
# ==========================================

st.divider()

st.subheader(translation.t("📌 Quick Summary"))

if len(df) > 0:

    st.success(
        f"{translation.t('Total Doctors : ')}{total}\n\n"
        f"{translation.t('Available Doctors : ')}{available}\n\n"
        f"{translation.t('Unavailable Doctors : ')}{unavailable}\n\n"
        f"{translation.t('Average Experience : ')}{avg_exp} {translation.t('Years')}"
    )

else:

    st.warning(translation.t("No doctors registered yet."))

# ==========================================
# FOOTER
# ==========================================

st.write("")
st.divider()

st.markdown(f"""

<div class="footer">

<h2 style="color:#00C2FF;">
{translation.t("HealthVibe AI")}
</h2>

<p>
{translation.t("Doctors Management System")}
</p>

<hr>

<p style="color:#94A3B8;">
{translation.t("Developed by ")}<b>Badr Ahmed</b>
</p>

</div>

""", unsafe_allow_html=True)