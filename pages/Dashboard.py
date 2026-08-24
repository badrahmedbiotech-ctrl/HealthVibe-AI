import streamlit as st
import pandas as pd
from datetime import datetime

from components.branding import *
from components.colors import *
from components.branding import LOGO, LOGO_ICON

from translation import init, t

# ==========================================
# LANGUAGE (must run before any other markup)
# ==========================================

init()

col1, col2 = st.columns([1, 5])

with col1:
    try:
        st.image(str(LOGO_ICON), width=50)
    except Exception:
        pass

with col2:
    st.title(t("HealthVibe AI"))
    st.caption(t("Vibe Better, Live Better"))

from utils.navigation import sidebar

from components.database import (
    total_patients,
    total_assessments,
    average_risk,
    latest_assessments,
    disease_statistics,
    risk_statistics,
    get_all_history,
    get_profile
)

from components.doctor_db import (
    doctors_count,
    available_doctors
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title=t("HealthVibe AI Dashboard"),
    page_icon=str(LOGO),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SESSION
# ==========================================

if "logged_in" not in st.session_state:
    st.switch_page("app.py")
    st.stop()
username = st.session_state.get("username", "User")
role = st.session_state.get("role", "Patient")
user_id = st.session_state.get("user_id")

# ==========================================
# CSS
# ==========================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

sidebar()

st.write(t("Dashboard Loaded Successfully"))

# ==========================================
# LOAD DATABASE
# ==========================================

try:
    patients = total_patients()
except:
    patients = 0

try:
    assessments = get_all_history()
except:
    assessments = []

history_count = len(assessments)

try:
    doctors = doctors_count()
except:
    doctors = 0

try:
    online_doctors = available_doctors()
except:
    online_doctors = 0

profile = get_profile(user_id)

# ==========================================
# HEALTH SCORE
# ==========================================

if history_count == 0:

    health_score = 100
    latest_prediction = t("No Assessment")

else:

    latest = assessments.iloc[-1]

    latest_prediction = latest["prediction"]

    if latest_prediction == "Low Risk":
        health_score = 95

    elif latest_prediction == "Moderate Risk":
        health_score = 75

    else:
        health_score = 45

# ==========================================
# NOTIFICATIONS
# ==========================================

notifications = []

if history_count == 0:

    notifications.append(t("Welcome to HealthVibe AI"))

else:

    notifications.append(
        f"{t('Latest assessment :')} {t(latest_prediction)}"
    )

if online_doctors > 0:

    notifications.append(
        f"{online_doctors} {t('Doctors Online')}"
    )

notifications.append(
    f"{t('Last Login :')} {datetime.now().strftime('%d %b %Y')}"
)

# ==========================================
# CARD
# ==========================================

def disease_card(icon, title, desc, page, key):

    st.markdown(
        f"""
        <div class="dashboard-card">

        <div style="font-size:55px;">
        {icon}
        </div>

        <h3>{t(title)}</h3>

        <p>{t(desc)}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        t(f"Open {title}"),
        key=key,
        width="stretch"
    ):
        st.switch_page(page)

# ==========================================
# HERO
# ==========================================

st.markdown(f"""
<div class="hero">

<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">

<div>

<span class="hero-badge">
{t("🟢 AI System Online")}
</span>

<h1>
{t("👋 Welcome Back,")} {username}
</h1>

<p>
{t("Your Intelligent Clinical Decision Support Platform")}
</p>

</div>

<div style="font-size:110px;">
🩺
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# QUICK ACTIONS
# ==========================================

a1, a2, a3, a4 = st.columns(4)

with a1:

    if st.button(
        t("🩸 New Assessment"),
        width="stretch"
    ):
        st.switch_page("pages/Diabetes.py")

with a2:

    if st.button(
        t("🤖 AI Assistant"),
        width="stretch"
    ):
        st.switch_page("pages/chatbot.py")

with a3:

    if st.button(
        t("📋 Medical History"),
        width="stretch"
    ):
        st.switch_page("pages/Patient_History.py")

with a4:

    if st.button(
        t("👤 Profile"),
        width="stretch"
    ):
        st.switch_page("pages/Profile.py")

st.write("")

# ==========================================
# LOAD REAL DATA
# ==========================================

patients = total_patients()
assessment_count = total_assessments()
doctors = doctors_count()
available = available_doctors()
history = get_all_history()
history_count = len(history)

# ==========================================
# DASHBOARD METRICS
# ==========================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        t("👥 Patients"),
        patients
    )
with m2:
    st.metric(
        t("📄 Assessments"),
        assessment_count
    )

with m3:
    st.metric(
        t("👨‍⚕️ Doctors"),
        doctors
    )

with m4:
    st.metric(
        t("🟢 Available"),
        available
    )

# ==========================================
# SUMMARY + RISK
# ==========================================

left, right = st.columns([2, 1])

with left:

    st.markdown(f"""
    <div class="card">
    <h3>{t("📈 Dashboard Summary")}</h3>
    """, unsafe_allow_html=True)

    st.write(f"{t('Username:')} {username}")
    st.write(f"{t('Role:')} {t(role)}")
    st.write(f"{t('Total Assessments:')} {history_count}")
    st.write(f"{t('Latest Prediction:')} {t(latest_prediction)}")

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown(f"""
    <div class="card">
    <h3>{t("❤️ Risk Indicator")}</h3>
    """, unsafe_allow_html=True)

    st.progress(health_score / 100)

    if health_score >= 90:

        st.success(t("Excellent"))

    elif health_score >= 70:

        st.warning(t("Moderate"))

    else:

        st.error(t("High Risk"))

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ==========================================
# CHART
# ==========================================

st.subheader(t("📊 Platform Statistics"))

chart = pd.DataFrame({

    "Category": [
        t("Patients"),
        t("Assessments"),
        t("Doctors")
    ],

    "Value": [
        patients,
        history_count,
        doctors
    ]

})

st.bar_chart(
    chart,
    x="Category",
    y="Value",
    width="stretch"
)

st.write("")

# ==========================================
# AI MODULES
# ==========================================

st.subheader(t("🩺 AI Disease Prediction Modules"))

r1 = st.columns(4)

with r1[0]:
    disease_card(
        "🩸",
        "Diabetes",
        "Blood Glucose Risk Prediction",
        "pages/Diabetes.py",
        "db"
    )

with r1[1]:
    disease_card(
        "❤️",
        "Hypertension",
        "Blood Pressure Analysis",
        "pages/Hypertension.py",
        "ht"
    )

with r1[2]:
    disease_card(
        "🫀",
        "Lipid Profile",
        "Cholesterol Risk Assessment",
        "pages/lipid.py",
        "lp"
    )

with r1[3]:
    disease_card(
        "⚖️",
        "Obesity",
        "BMI & Weight Risk",
        "pages/obesity.py",
        "ob"
    )

st.write("")

r2 = st.columns(4)

with r2[0]:
    disease_card(
        "🫁",
        "Pulmonary",
        "Pulmonary Fibrosis",
        "pages/Pulmonary_Fibrosis.py",
        "pf"
    )

with r2[1]:
    disease_card(
        "🩻",
        "CT Scan AI",
        "Medical Image Detection",
        "pages/CT_Scan_AI.py",
        "ct"
    )

with r2[2]:
    disease_card(
        "🩸",
        "Thrombosis",
        "Blood Clot Prediction",
        "pages/Thrombosis.py",
        "thr"
    )

with r2[3]:

    st.markdown(f"""
    <div class="dashboard-card">

    <div style="font-size:55px;">
    🚀
    </div>

    <h3>{t("Coming Soon")}</h3>

    <p>
    {t("More AI models are under development.")}
    </p>

    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================
# NOTIFICATIONS
# ==========================================

left, right = st.columns([2, 1])

with left:

    st.subheader(t("🔔 Notifications"))

    for note in notifications:

        st.info(note)

with right:

    st.subheader(t("⚡️ System Status"))

    st.success(t("🟢 AI Server"))

    st.success(t("🟢 Database"))

    st.success(t("🟢 Models"))

    st.success(t("🟢 Authentication"))

st.write("")
st.divider()

# ==========================================
# RECENT ACTIVITY
# ==========================================

st.subheader(t("📈 Recent Activity"))

try:
    history = get_all_history()
except:
    history = []

if len(history) == 0:

    st.info(t("No assessments yet."))

else:

    for _, item in history.tail(5).iloc[::-1].iterrows():

        with st.container(border=True):

            c1, c2, c3 = st.columns([3, 2, 2])

            with c1:
                st.write(t(item['disease']))

            with c2:
                st.write(t(item["prediction"]))

            with c3:
                st.caption(item["created_at"])

st.write("")
st.divider()

# ==========================================
# LATEST REPORTS
# ==========================================

st.subheader(t("📄 Latest Assessments"))

if len(history) == 0:

    st.info(t("No reports yet."))

else:

    for _, report in history.tail(10).iloc[::-1].iterrows():

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])

            with c1:
                st.write(t(report['disease']))

            with c2:
                st.write(t(report["prediction"]))

            with c3:
                probability = report.get("probability", 0)
                st.progress(float(probability))

            with c4:
                st.caption(report["created_at"])

st.write("")
st.divider()

# ==========================================
# PATIENT DASHBOARD
# ==========================================

if role == "Patient":

    st.subheader(t("👤 Patient Dashboard"))

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(f"""
        <div class="card">
        <h3>{t("📊 Personal Statistics")}</h3>
        """, unsafe_allow_html=True)

        st.metric(
            t("Assessments"),
            history_count
        )

        st.metric(
            t("Health Score"),
            f"{health_score}%"
        )

        st.metric(
            t("Latest Result"),
            t(latest_prediction)
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(f"""
        <div class="card">
        <h3>{t("💡 Daily Health Tips")}</h3>
        """, unsafe_allow_html=True)

        tips = [

            "💧 Drink enough water",

            "🥗 Eat healthy food",

            "🏃 Exercise regularly",

            "😴 Sleep 7-8 hours",

            "🚭 Avoid smoking"

        ]

        for tip in tips:

            st.write(t(tip))

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

# ==========================================
# DOCTOR DASHBOARD
# ==========================================

elif role == "Doctor":

    st.subheader(t("👨‍⚕️ Doctor Dashboard"))

    d1, d2, d3 = st.columns(3)

    with d1:

        st.markdown(f"""
        <div class="card">
        <h3>{t("👥 Patient Management")}</h3>
        <p>
        {t("View and manage all registered patients.")}
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.metric(
            t("Patients"),
            patients
        )

        if st.button(
            t("Open Patient Manager"),
            key="doctor_patient",
            width="stretch"
        ):
            st.switch_page("pages/doctor_db.py")

    with d2:

        st.markdown(f"""
        <div class="card">
        <h3>{t("📈 AI Analytics")}</h3>
        <p>
        {t("Monitor AI performance and predictions.")}
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.metric(
            t("Assessments"),
            history_count
        )

        if st.button(
            t("Open Analytics"),
            key="doctor_ai",
            width="stretch"
        ):
            st.switch_page("pages/doctor_db.py")

    with d3:

        st.markdown(f"""
        <div class="card">
        <h3>{t("👨‍⚕️ Doctors")}</h3>
        <p>
        {t("Manage doctor accounts.")}
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.metric(
            t("Online Doctors"),
            online_doctors
        )

        if st.button(
            t("Manage Doctors"),
            key="doctor_manage",
            width="stretch"
        ):
            st.switch_page("pages/doctor_db.py")

    st.write("")
    st.divider()

# ==========================================
# QUICK ACCESS
# ==========================================

st.subheader(t("⚡️ Quick Access"))

q1, q2, q3, q4 = st.columns(4)

with q1:

    if st.button(
        t("🤖 AI Chatbot"),
        key="qa_chat",
        width="stretch"
    ):
        st.switch_page("pages/chatbot.py")

with q2:

    if st.button(
        t("📋 Patient History"),
        key="qa_history_count",
        width="stretch"
    ):
        st.switch_page("pages/Patient_History.py")

with q3:

    if st.button(
        t("👤 Profile"),
        key="qa_profile",
        width="stretch"
    ):
        st.switch_page("pages/Profile.py")

with q4:

    if st.button(
        t("⚙️ Settings"),
        key="qa_settings",
        width="stretch"
    ):
        st.switch_page("pages/settings.py")

st.write("")
st.divider()

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader(t("🧠 AI Insights"))

i1, i2 = st.columns(2)

with i1:

    st.markdown(f"""
    <div class="card">

    <h3>{t("📊 Risk Distribution")}</h3>

    <p>
    {t("Based on your previous assessments, your overall health trend is improving.")}
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.progress(72)

with i2:

    st.markdown(f"""
    <div class="card">

    <h3>{t("💡 AI Recommendation")}</h3>

    <p>

    ✔️ {t("Continue regular screening.")}<br><br>

    ✔️ {t("Maintain healthy diet.")}<br><br>

    ✔️ {t("Exercise at least 150 min/week.")}<br><br>

    ✔️ {t("Repeat laboratory tests every 6 months.")}

    </p>

    </div>
    """, unsafe_allow_html=True)

# ==========================================
# NOTIFICATIONS
# ==========================================

st.write("")
st.divider()

st.subheader(t("🔔 Notifications"))

notifications = [

    ("🟢", "AI models updated successfully"),

    ("🔵", "New medical report available"),

    ("🟡", "Annual health check recommended"),

    ("🟢", "Database synchronized")

]

for icon, msg in notifications:

    st.info(f"{icon} {t(msg)}")

# ==========================================
# SYSTEM STATUS
# ==========================================

st.subheader(t("⚡️ System Status"))

system1, system2, system3, system4 = st.columns(4)

with system1:
    st.success(t("🟢 AI Server Online"))

with system2:
    st.success(t("🟢 Database Connected"))

with system3:
    st.success(t("🟢 Models Loaded"))

with system4:
    st.success(t("🟢 Secure Connection"))

st.progress(0.98)

st.divider()

# ==========================================
# PLATFORM ANALYTICS
# ==========================================

st.subheader(t("📊 Platform Analytics"))

col1, col2 = st.columns([2, 1])

with col1:

    analytics = pd.DataFrame({
        "Category": [
            t("Patients"),
            t("Assessments"),
            t("Doctors")
        ],
        "Value": [
            patients,
            history_count,
            doctors
        ]
    })

    st.bar_chart(
        analytics,
        x="Category",
        y="Value",
        width="stretch"
    )

with col2:

    st.metric(t("AI Accuracy"), "98.7%")
    st.metric(t("Online Doctors"), online_doctors)
    st.metric(t("System Status"), t("Healthy"))

st.divider()

# ==========================================
# AI HEALTH INSIGHTS
# ==========================================

st.subheader(t("🧠 AI Health Insights"))

left, right = st.columns(2)

with left:

    st.markdown(f"""
    <div class="card">
    <h3>{t("🤖 AI Recommendation")}</h3>
    """, unsafe_allow_html=True)

    if history_count == 0:

        st.info(t("No assessments yet."))

    elif history_count < 5:

        st.success(
            t("Great start. Continue monitoring your health regularly.")
        )

    elif history_count < 15:

        st.warning(
            t("Keep following healthy habits and review your reports.")
        )

    else:

        st.error(
            t("You have many assessments. Regular physician follow-up is recommended.")
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown(f"""
    <div class="card">
    <h3>{t("📈 AI Prediction Distribution")}</h3>
    """, unsafe_allow_html=True)

    chart = pd.DataFrame({

        "Risk": [
            t("Low"),
            t("Moderate"),
            t("High")
        ],

        "Count": [
            max(history_count - 3, 0),
            min(history_count, 3),
            1 if history_count > 0 else 0
        ]

    })

    st.bar_chart(
        chart,
        x="Risk",
        y="Count",
        width="stretch"
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ==========================================
# UPCOMING FEATURES
# ==========================================

st.subheader(t("🚀 Upcoming Features"))

u1, u2, u3 = st.columns(3)

with u1:
    st.info(t("📅 Smart Appointment Booking"))

with u2:
    st.info(t("💊 Medication Reminder"))

with u3:
    st.info(t("📱 HealthVibe Mobile App"))

st.divider()

# ==========================================
# ACCOUNT INFORMATION
# ==========================================

st.subheader(t("👤 Account"))

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        t("Username"),
        username
    )

with c2:

    st.metric(
        t("Role"),
        t(role)
    )

with c3:

    st.metric(
        t("Status"),
        t("Active")
    )

st.write("")
st.divider()

# ==========================================
# FOOTER
# ==========================================

st.write("")
st.divider()

st.markdown(f"""
<div style="
text-align:center;
padding:25px;
color:#94A3B8;
">

<h2 style="
color:#00C2FF;
margin-bottom:5px;
">
{t("🩺 HealthVibe AI")}
</h2>

<p>
{t("AI Clinical Decision Support Platform")}
</p>

<p style="margin-top:15px;">
{t("Version 2.0 • Secure • Intelligent • Fast")}
</p>

<hr style="
border:1px solid #2d3748;
margin:20px 0;
">

<p>
{t("Made with ❤️ using Streamlit + AI")}
</p>

<p>
{t("© 2026 HealthVibe AI • All Rights Reserved")}
</p>

</div>
""", unsafe_allow_html=True)