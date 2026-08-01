import streamlit as st

from utils.navigation import sidebar

from components.database import (
    get_patient_history,
    delete_history,
    delete_all_history
)

st.set_page_config(
    page_title="Patient History",
    page_icon="📋",
    layout="wide"
)

sidebar()

# ==========================================
# LOGIN CHECK
# ==========================================

if "user" not in st.session_state:
    st.switch_page("app.py")
    st.stop()

user = st.session_state["user"]

user_id = user["id"]
role = user.get("role", "Patient")

# ==========================================
# LOAD HISTORY
# ==========================================

history = get_patient_history(user_id)

# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">

<span class="hero-badge">
📋 Medical History
</span>

<h1>
My Assessments
</h1>

<p>
Review all previous AI predictions and reports.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# STATISTICS
# ==========================================

total_tests = len(history)

if total_tests > 0:

    latest = history.iloc[0]

    last_disease = latest["disease"]

    highest = history.loc[
        history["probability"].idxmax()
    ]

    highest_risk = f"{highest['probability']:.1f}%"

    most_tested = history["disease"].mode()[0]

else:

    last_disease = "--"
    highest_risk = "--"
    most_tested = "--"

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Tests", total_tests)

with c2:
    st.metric("Last Test", last_disease)

with c3:
    st.metric("Highest Risk", highest_risk)

with c4:
    st.metric("Most Tested", most_tested)

st.divider()

# ==========================================
# SEARCH & FILTERS
# ==========================================

st.subheader("🔍 Search & Filter")

col1, col2, col3 = st.columns(3)

with col1:

    search = st.text_input(
        "Search Disease"
    )

with col2:

    diseases = ["All"]

    if not history.empty:

        diseases += sorted(
            history["disease"].unique().tolist()
        )

    disease_filter = st.selectbox(
        "Disease",
        diseases
    )

with col3:

    sort_order = st.selectbox(
        "Sort By",
        [
            "Newest",
            "Oldest",
            "Highest Risk",
            "Lowest Risk"
        ]
    )

# ==========================================
# FILTER DATA
# ==========================================

filtered = history.copy()

if search:

    filtered = filtered[
        filtered["disease"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

if disease_filter != "All":

    filtered = filtered[
        filtered["disease"] == disease_filter
    ]

if sort_order == "Newest":

    filtered = filtered.sort_values(
        "created_at",
        ascending=False
    )

elif sort_order == "Oldest":

    filtered = filtered.sort_values(
        "created_at",
        ascending=True
    )

elif sort_order == "Highest Risk":

    filtered = filtered.sort_values(
        "probability",
        ascending=False
    )

elif sort_order == "Lowest Risk":

    filtered = filtered.sort_values(
        "probability",
        ascending=True
    )

# ==========================================
# EMPTY
# ==========================================

if filtered.empty:

    st.info("📭 No assessments found.")

    st.stop()

# ==========================================
# ACTIONS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🗑 Delete All History",
        width="stretch",
        type="secondary"
    ):

        delete_all_history(user_id)

        st.success("All Assessments Deleted Successfully")

        st.rerun()

with col2:

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(

        "📄 Download CSV",

        data=csv,

        file_name="HealthVibe_History.csv",

        mime="text/csv",

        width="stretch"

    )

st.divider()

# ==========================================
# MEDICAL CARDS
# ==========================================

st.subheader("📋 Assessment History")

for _, row in filtered.iterrows():

    with st.container(border=True):

        left, center, right = st.columns([5,2,2])

        with left:

            st.markdown(f"""
### 🩺 {row['disease']}

**Prediction:** {row['prediction']}

📅 {row['created_at']}
""")

        with center:

            st.metric(
                "Risk",
                f"{float(row['probability']):.1f}%"
            )

        with right:

            if st.button(
                "👁 View Details",
                key=f"view_{row['id']}"
            ):

                st.session_state.selected_assessment = row.to_dict()

            if st.button(
                "🗑 Delete",
                key=f"delete_{row['id']}"
            ):

                delete_history(row["id"])

                st.success("Assessment Deleted Successfully")

                st.rerun()

        st.write("")

# ==========================================
# DETAILS
# ==========================================

if "selected_assessment" in st.session_state:

    st.divider()

    st.subheader("📄 Assessment Details")

    item = st.session_state.selected_assessment

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Disease",
            item["disease"]
        )

        st.metric(
            "Prediction",
            item["prediction"]
        )

    with col2:

        st.metric(
            "Risk",
            f"{float(item['probability']):.1f}%"
        )
 
        st.metric(
            "Date",
            item["created_at"]
        )

    st.json(item)

    if st.button(
        "❌ Close Details"
    ):

        del st.session_state.selected_assessment

        st.rerun()     

    # ==========================================
# ANALYTICS
# ==========================================

st.divider()

st.subheader("📊 Assessment Analytics")

c1, c2 = st.columns(2)

with c1:

    disease_chart = (
        filtered["disease"]
        .value_counts()
    )

    st.bar_chart(disease_chart)

with c2:

    risk_chart = (
        filtered
        .groupby("disease")["probability"]
        .mean()
    )

    st.bar_chart(risk_chart)    