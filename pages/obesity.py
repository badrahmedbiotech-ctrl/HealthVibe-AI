import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    page_title="HealthVibe - Obesity",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Obesity Prediction")
st.write("Enter your information to predict your obesity level.")

# ======================
# Load Model
# ======================

model = joblib.load("models/obesity_model.pkl")

encoder = LabelEncoder()

prediction = None
result = None
confidence = None

# ======================
# Inputs
# ======================

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

age = st.number_input(
    "Age",
    min_value=1,
    max_value=100,
    value=25
)

height = st.number_input(
    "Height (meters)",
    min_value=1.00,
    max_value=2.50,
    value=1.70
)

weight = st.number_input(
    "Weight (kg)",
    min_value=20,
    max_value=250,
    value=70
)

bmi = weight / (height ** 2)

st.metric(
    "Current BMI",
    round(bmi,2)
)

family_history = st.selectbox(
    "Family history with overweight",
    ["yes","no"]
)

high_calorie = st.selectbox(
    "Frequent high calorie food",
    ["yes","no"]
)

vegetables = st.slider(
    "Vegetable Consumption",
    1,
    3,
    2
)

meals = st.slider(
    "Main Meals per Day",
    1,
    4,
    3
)

snacks = st.selectbox(
    "Food Between Meals",
    [
        "no",
        "Sometimes",
        "Frequently",
        "Always"
    ]
)

smoke = st.selectbox(
    "Smoking",
    [
        "yes",
        "no"
    ]
)

water = st.slider(
    "Water Intake",
    1.0,
    3.0,
    2.0
)

calories = st.selectbox(
    "Calories Monitoring",
    [
        "yes",
        "no"
    ]
)

activity = st.slider(
    "Physical Activity",
    0.0,
    3.0,
    1.0
)

technology = st.slider(
    "Technology Time",
    0.0,
    2.0,
    1.0
)

alcohol = st.selectbox(
    "Alcohol Consumption",
    [
        "no",
        "Sometimes",
        "Frequently"
    ]
)

transport = st.selectbox(
    "Transportation",
    [
        "Walking",
        "Bike",
        "Motorbike",
        "Automobile",
        "Public_Transportation"
    ]
)
# ======================
# Prediction
# ======================

if st.button("🔍 Predict"):

    gender_enc = encoder.fit_transform([gender])[0]
    family_enc = encoder.fit_transform([family_history])[0]
    high_calorie_enc = encoder.fit_transform([high_calorie])[0]
    snacks_enc = encoder.fit_transform([snacks])[0]
    smoke_enc = encoder.fit_transform([smoke])[0]
    calories_enc = encoder.fit_transform([calories])[0]
    alcohol_enc = encoder.fit_transform([alcohol])[0]
    transport_enc = encoder.fit_transform([transport])[0]

    data = pd.DataFrame([[
        gender_enc,
        age,
        height,
        weight,
        family_enc,
        high_calorie_enc,
        vegetables,
        meals,
        snacks_enc,
        smoke_enc,
        water,
        calories_enc,
        activity,
        technology,
        alcohol_enc,
        transport_enc
    ]], columns=[
        "Gender",
        "Age",
        "Height",
        "Weight",
        "Family history with overweight",
        "Frequent consumption of high-caloric food",
        "Frequency of vegetable consumption",
        "Number of main meals the person eats per day",
        "Consumption of food between meals",
        "SMOKE",
        "Daily water consumption",
        "Whether the person takes calorie supplements",
        "Physical activity frequency",
        "Time spent using technology",
        "Alcohol consumption",
        "Means of transportation used"
    ])

    prediction = model.predict(data)
    probability = model.predict_proba(data)[0]
    confidence = probability.max() * 100

    labels = {
        0: "Insufficient Weight",
        1: "Normal Weight",
        2: "Overweight Level I",
        3: "Overweight Level II",
        4: "Obesity Type I",
        5: "Obesity Type II",
        6: "Obesity Type III"
    }

    result = labels[int(prediction[0])]
    # ======================
# Prediction Summary
# ======================

if prediction is not None:

    st.divider()

    st.subheader("📊 Prediction Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⚖️ BMI",
            round(bmi, 2)
        )

    with col2:
        st.metric(
            "🧠 AI Prediction",
            result
        )

    with col3:
        st.metric(
            "🎯 Confidence",
            f"{confidence:.1f}%"
        )

    st.divider()

    # ======================
    # Risk Level
    # ======================

    if bmi < 25:
        risk = "🟢 Low"

    elif bmi < 30:
        risk = "🟠 Moderate"

    elif bmi < 35:
        risk = "🔴 High"

    else:
        risk = "🚨 Very High"

    st.subheader("❤️ Risk Level")

    st.info(risk)

    # ======================
    # BMI Status
    # ======================

    if bmi < 18.5:
        st.info("🟡 Underweight")

    elif bmi < 25:
        st.success("🟢 Healthy Weight")

    elif bmi < 30:
        st.warning("🟠 Overweight")

    elif bmi < 35:
        st.error("🔴 Obesity Class I")

    elif bmi < 40:
        st.error("🔴 Obesity Class II")

    else:
        st.error("🚨 Severe Obesity")
        # ======================
# Risk Factors
# ======================

    st.divider()

    st.subheader("⚠️ Risk Factors")

    risk_list = []

    if bmi >= 30:
        risk_list.append("⚖️ High BMI")

    if smoke == "yes":
        risk_list.append("🚬 Smoking")

    if family_history == "yes":
        risk_list.append("👨‍👩‍👧 Family History")

    if activity < 1:
        risk_list.append("🏃 Low Physical Activity")

    if water < 2:
        risk_list.append("💧 Low Water Intake")

    if high_calorie == "yes":
        risk_list.append("🍔 High Calorie Diet")

    if len(risk_list) == 0:
        st.success("✅ No Major Risk Factors")

    else:
        for item in risk_list:
            st.write("•", item)

# ======================
# Recommendations
# ======================

    st.divider()

    st.subheader("💡 Personalized Recommendations")

    if bmi < 18.5:

        st.info("🥛 Increase healthy calorie intake.")
        st.info("🍗 Eat more protein.")
        st.info("🏋️ Strength training is recommended.")

    elif bmi < 25:

        st.success("✅ Maintain your healthy lifestyle.")
        st.success("🥗 Balanced diet.")
        st.success("🏃 Continue exercising.")

    elif bmi < 30:

        st.warning("🥗 Reduce sugar and fast food.")
        st.warning("🚶 Walk at least 30 minutes daily.")
        st.warning("💧 Drink more water.")

    else:

        st.error("⚠️ Reduce high-calorie foods.")
        st.error("🏃 Exercise at least 150 minutes weekly.")
        st.error("🥦 Increase vegetables and fruits.")
        st.error("🩺 Consult a nutrition specialist.")
        # ======================
# Obesity Lab Analysis
# ======================

st.divider()

st.header("🧪 Obesity Lab Analysis")

hba1c = st.number_input(
    "HbA1c (%)",
    3.0, 15.0, 5.5
)

fbs = st.number_input(
    "Fasting Blood Sugar (mg/dL)",
    50, 300, 90
)

cholesterol = st.number_input(
    "Total Cholesterol (mg/dL)",
    100, 400, 180
)

ldl = st.number_input(
    "LDL Cholesterol (mg/dL)",
    20, 300, 90
)

hdl = st.number_input(
    "HDL Cholesterol (mg/dL)",
    10, 100, 50
)

triglycerides = st.number_input(
    "Triglycerides (mg/dL)",
    20, 500, 120
)

if st.button("🧪 Analyze Lab Results"):

    st.subheader("📋 Lab Report")

    # HbA1c
    if hba1c < 5.7:
        st.success("✅ HbA1c : Normal")
    elif hba1c < 6.5:
        st.warning("⚠️ HbA1c : Prediabetes")
    else:
        st.error("🔴 HbA1c : Diabetes")

    # FBS
    if fbs < 100:
        st.success("✅ Fasting Blood Sugar : Normal")
    elif fbs < 126:
        st.warning("⚠️ Fasting Blood Sugar : Prediabetes")
    else:
        st.error("🔴 Fasting Blood Sugar : High")

    # Cholesterol
    if cholesterol < 200:
        st.success("✅ Total Cholesterol : Normal")
    elif cholesterol < 240:
        st.warning("⚠️ Total Cholesterol : Borderline")
    else:
        st.error("🔴 Total Cholesterol : High")

    # LDL
    if ldl < 100:
        st.success("✅ LDL : Optimal")
    elif ldl < 160:
        st.warning("⚠️ LDL : Elevated")
    else:
        st.error("🔴 LDL : Very High")

    # HDL
    if hdl >= 60:
        st.success("✅ HDL : Excellent")
    elif hdl >= 40:
        st.warning("⚠️ HDL : Acceptable")
    else:
        st.error("🔴 HDL : Low")

    # Triglycerides
    if triglycerides < 150:
        st.success("✅ Triglycerides : Normal")
    elif triglycerides < 200:
        st.warning("⚠️ Triglycerides : Borderline High")
    else:
        st.error("🔴 Triglycerides : High")

    st.divider()

    st.subheader("💡 Overall Recommendation")

    if (
        hba1c < 5.7
        and fbs < 100
        and cholesterol < 200
        and ldl < 100
        and hdl >= 40
        and triglycerides < 150
    ):
        st.success("🎉 Your laboratory results are generally within the normal range.")

    else:
        st.warning(
            "⚠️ Some laboratory values are outside the normal range. Please consult your physician for further evaluation."
        )
        # ======================
# Footer
# ======================

st.divider()

st.caption("🏥 HealthVibe AI • Obesity Prediction Module")
