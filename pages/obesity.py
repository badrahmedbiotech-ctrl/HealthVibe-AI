import streamlit as st
import pandas as pd
import joblib
import os

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="HealthVibe AI - Obesity",
    page_icon="⚖️",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

default_values = {

    "page": 1,
    "analyzed": False,

    "prediction": "",
    "confidence": 0,

    "health_score": 0,
    "risk_level": "",

    "recommendations": [],

}


for key, value in default_values.items():

    if key not in st.session_state:
        st.session_state[key] = value



# ==================================================
# LOAD MODEL
# ==================================================

model = joblib.load(
    "models/obesity_model.pkl"
)



# ==================================================
# PDF GENERATOR
# ==================================================

def generate_pdf(
        age,
        gender,
        bmi,
        prediction,
        confidence,
        risk_level,
        health_score,
        recommendations
):

    file_name = "HealthVibe_Obesity_Report.pdf"


    doc = SimpleDocTemplate(
        file_name
    )


    styles = getSampleStyleSheet()


    content = []


    content.append(
        Paragraph(
            "<b>HealthVibe AI</b>",
            styles["Title"]
        )
    )


    content.append(
        Paragraph(
            "Obesity Prediction Report",
            styles["Heading1"]
        )
    )


    content.append(
        Paragraph(
            f"Age : {age}",
            styles["BodyText"]
        )
    )


    content.append(
        Paragraph(
            f"Gender : {gender}",
            styles["BodyText"]
        )
    )


    content.append(
        Paragraph(
            f"BMI : {bmi:.2f}",
            styles["BodyText"]
        )
    )


    content.append(
        Paragraph(
            f"AI Prediction : {prediction}",
            styles["BodyText"]
        )
    )


    content.append(
        Paragraph(
            f"Confidence : {confidence:.1f}%",
            styles["BodyText"]
        )
    )


    content.append(
        Paragraph(
            f"Risk Level : {risk_level}",
            styles["BodyText"]
        )
    )


    content.append(
        Paragraph(
            f"Health Score : {health_score}/100",
            styles["BodyText"]
        )
    )


    content.append(
        Paragraph(
            "Recommendations:",
            styles["Heading2"]
        )
    )


    for item in recommendations:

        content.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )


    doc.build(content)


    return file_name




# ==================================================
# HEADER
# ==================================================

st.title(
    "⚖️ HealthVibe AI - Obesity Analyzer"
)


st.write(
    "AI-based obesity prediction and personalized health assessment."
)



st.divider()



# ==================================================
# PAGE INDICATOR
# ==================================================

st.progress(
    st.session_state.page / 5
)


st.caption(
    f"Step {st.session_state.page} of 5"
)



# ==================================================
# PAGE 1
# ==================================================

if st.session_state.page == 1:


    st.header(
        "👤 Personal Information"
    )


    col1, col2 = st.columns(2)



    with col1:


        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )


        age = st.number_input(
            "Age",
            1,
            100,
            25
        )


        height = st.number_input(
            "Height (meters)",
            1.0,
            2.5,
            1.70
        )



    with col2:


        weight = st.number_input(
            "Weight (kg)",
            20,
            250,
            70
        )


        family_history = st.selectbox(
            "Family history with overweight",
            [
                "yes",
                "no"
            ]
        )



        smoke = st.selectbox(
            "Smoking",
            [
                "yes",
                "no"
            ]
        )



    bmi = weight / (height ** 2)



    st.metric(
        "Current BMI",
        round(bmi,2)
    )



    st.session_state.age = age
    st.session_state.gender = gender
    st.session_state.height = height
    st.session_state.weight = weight
    st.session_state.bmi = bmi
    st.session_state.family_history = family_history
    st.session_state.smoke = smoke



# ==================================================
# NAVIGATION
# ==================================================

st.divider()


col1, col2 = st.columns(2)



with col1:

    if st.session_state.page > 1:

        if st.button(
            "⬅️ Back",
            use_container_width=True
        ):

            st.session_state.page -= 1

            st.rerun()



with col2:


    if st.session_state.page < 5:

        if st.button(
            "Next ➡️",
            use_container_width=True
        ):

            st.session_state.page += 1

            st.rerun()
            # ==================================================
# PAGE 2
# ==================================================

if st.session_state.page == 2:


    st.header(
        "🥗 Lifestyle & Daily Habits"
    )


    col1, col2 = st.columns(2)



    with col1:


        high_calorie = st.selectbox(
            "Frequent high calorie food",
            [
                "yes",
                "no"
            ]
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



        water = st.slider(
            "Daily Water Intake",
            1.0,
            3.0,
            2.0
        )



    with col2:


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



    # Save Data

    st.session_state.high_calorie = high_calorie
    st.session_state.vegetables = vegetables
    st.session_state.meals = meals
    st.session_state.snacks = snacks
    st.session_state.water = water
    st.session_state.calories = calories
    st.session_state.activity = activity
    st.session_state.technology = technology
    st.session_state.alcohol = alcohol
    st.session_state.transport = transport




# ==================================================
# PAGE 3
# ==================================================

if st.session_state.page == 3:


    st.header(
        "⚖️ AI Obesity Prediction"
    )


    st.info(
        "The AI model analyzes your lifestyle and body information."
    )



    if st.button(
        "🔍 Predict Obesity Level",
        use_container_width=True
    ):



        # ================================
        # Encoding
        # ================================


        gender_map = {
            "Male":0,
            "Female":1
        }


        yes_no_map = {
            "no":0,
            "yes":1
        }


        snacks_map = {

            "no":0,
            "Sometimes":1,
            "Frequently":2,
            "Always":3

        }


        alcohol_map = {

            "no":0,
            "Sometimes":1,
            "Frequently":2

        }


        transport_map = {

            "Walking":0,
            "Bike":1,
            "Motorbike":2,
            "Automobile":3,
            "Public_Transportation":4

        }



        input_data = pd.DataFrame([{

            "Gender":
            gender_map[st.session_state.gender],


            "Age":
            st.session_state.age,


            "Height":
            st.session_state.height,


            "Weight":
            st.session_state.weight,


            "Family history with overweight":
            yes_no_map[st.session_state.family_history],


            "Frequent consumption of high-caloric food":
            yes_no_map[st.session_state.high_calorie],


            "Frequency of vegetable consumption":
            st.session_state.vegetables,


            "Number of main meals the person eats per day":
            st.session_state.meals,


            "Consumption of food between meals":
            snacks_map[st.session_state.snacks],


            "SMOKE":
            yes_no_map[st.session_state.smoke],


            "Daily water consumption":
            st.session_state.water,


            "Whether the person takes calorie supplements":
            yes_no_map[st.session_state.calories],


            "Physical activity frequency":
            st.session_state.activity,


            "Time spent using technology":
            st.session_state.technology,


            "Alcohol consumption":
            alcohol_map[st.session_state.alcohol],


            "Means of transportation used":
            transport_map[st.session_state.transport]

        }])



        prediction_value = model.predict(
            input_data
        )



        probability = model.predict_proba(
            input_data
        )[0]



        confidence = probability.max()*100



        labels = {

            0:"Insufficient Weight",
            1:"Normal Weight",
            2:"Overweight Level I",
            3:"Overweight Level II",
            4:"Obesity Type I",
            5:"Obesity Type II",
            6:"Obesity Type III"

        }



        st.session_state.prediction = labels[
            int(prediction_value[0])
        ]


        st.session_state.confidence = confidence



        st.session_state.analyzed = True



        st.success(
            "Prediction completed successfully."
        )



    if st.session_state.analyzed:


        st.divider()


        col1,col2,col3 = st.columns(3)



        with col1:

            st.metric(
                "BMI",
                round(st.session_state.bmi,2)
            )


        with col2:

            st.metric(
                "AI Prediction",
                st.session_state.prediction
            )


        with col3:

            st.metric(
                "Confidence",
                f"{st.session_state.confidence:.1f}%"
            )
            # ==================================================
# PAGE 4
# ==================================================

if st.session_state.page == 4:


    st.header(
        "❤️ Health Risk Assessment"
    )


    bmi = st.session_state.bmi


    risk_score = 0



    # ================================
    # BMI Risk
    # ================================


    st.subheader(
        "⚖️ BMI Status"
    )


    if bmi < 18.5:

        st.info(
            "🟡 Underweight"
        )

        risk_score += 1


    elif bmi < 25:

        st.success(
            "🟢 Healthy Weight"
        )


    elif bmi < 30:

        st.warning(
            "🟠 Overweight"
        )

        risk_score += 2


    elif bmi < 35:

        st.error(
            "🔴 Obesity Class I"
        )

        risk_score += 3


    elif bmi < 40:

        st.error(
            "🔴 Obesity Class II"
        )

        risk_score += 4


    else:

        st.error(
            "🚨 Severe Obesity"
        )

        risk_score += 5



    st.divider()



    # ================================
    # Risk Factors
    # ================================


    st.subheader(
        "⚠️ Risk Factors"
    )


    risk_factors = []



    if bmi >= 30:

        risk_factors.append(
            "⚖️ High BMI"
        )


    if st.session_state.smoke == "yes":

        risk_factors.append(
            "🚬 Smoking"
        )


    if st.session_state.family_history == "yes":

        risk_factors.append(
            "👨‍👩‍👧 Family history of overweight"
        )


    if st.session_state.activity < 1:

        risk_factors.append(
            "🏃 Low Physical Activity"
        )


    if st.session_state.water < 2:

        risk_factors.append(
            "💧 Low Water Intake"
        )


    if st.session_state.high_calorie == "yes":

        risk_factors.append(
            "🍔 High Calorie Diet"
        )



    if len(risk_factors) == 0:


        st.success(
            "✅ No major risk factors detected"
        )


    else:


        for factor in risk_factors:

            st.write(
                "•",
                factor
            )



    st.divider()



    # ================================
    # Overall Risk Level
    # ================================


    st.subheader(
        "🎯 Overall Risk Level"
    )



    if risk_score <= 1:


        risk_level = "Low Risk"

        st.success(
            "🟢 Low Risk"
        )



    elif risk_score <= 3:


        risk_level = "Moderate Risk"

        st.warning(
            "🟡 Moderate Risk"
        )



    else:


        risk_level = "High Risk"

        st.error(
            "🔴 High Risk"
        )



    st.session_state.risk_level = risk_level



    st.divider()



    # ================================
    # Health Score
    # ================================


    st.header(
        "❤️ Health Score"
    )


    health_score = 100



    health_score -= risk_score * 10



    if st.session_state.smoke == "yes":

        health_score -= 10



    if st.session_state.activity < 1:

        health_score -= 5



    if st.session_state.water < 2:

        health_score -= 5



    if st.session_state.high_calorie == "yes":

        health_score -= 5



    health_score = max(
        0,
        health_score
    )



    st.session_state.health_score = health_score



    st.metric(
        "Overall Health Score",
        f"{health_score}/100"
    )



    if health_score >= 85:


        st.success(
            "🟢 Excellent Health Status"
        )


    elif health_score >= 70:


        st.info(
            "🟡 Good Health Status"
        )


    elif health_score >= 50:


        st.warning(
            "🟠 Moderate Health Status"
        )


    else:


        st.error(
            "🔴 High Health Risk"
        )



    st.divider()



    # ================================
    # Recommendations
    # ================================


    st.header(
        "💡 Personalized Recommendations"
    )


    recommendations = []



    if bmi >= 25:

        recommendations.append(
            "🥗 Reduce high calorie foods and sugary drinks."
        )


    if st.session_state.activity < 3:

        recommendations.append(
            "🏃 Aim for at least 150 minutes of exercise weekly."
        )


    if st.session_state.water < 2:

        recommendations.append(
            "💧 Increase daily water intake."
        )


    if st.session_state.vegetables < 3:

        recommendations.append(
            "🥦 Increase vegetables and fiber intake."
        )


    if st.session_state.smoke == "yes":

        recommendations.append(
            "🚭 Stop smoking to reduce health risks."
        )


    if st.session_state.high_calorie == "yes":

        recommendations.append(
            "🍎 Choose healthier food alternatives."
        )



    if len(recommendations) == 0:


        recommendations.append(
            "🎉 Maintain your healthy lifestyle."
        )



    st.session_state.recommendations = recommendations



    for item in recommendations:

        st.write(
            "✔️",
            item
        )
        # ==================================================
# PAGE 5
# ==================================================

if st.session_state.page == 5:


    st.header(
        "🧪 Obesity Related Lab Analysis"
    )


    st.write(
        "Analyze important metabolic parameters related to obesity."
    )



    col1, col2 = st.columns(2)



    with col1:


        hba1c = st.number_input(
            "HbA1c (%)",
            3.0,
            15.0,
            5.5
        )


        fbs = st.number_input(
            "Fasting Blood Sugar (mg/dL)",
            50,
            300,
            90
        )


        cholesterol = st.number_input(
            "Total Cholesterol (mg/dL)",
            100,
            400,
            180
        )



    with col2:


        ldl = st.number_input(
            "LDL Cholesterol (mg/dL)",
            20,
            300,
            90
        )


        hdl = st.number_input(
            "HDL Cholesterol (mg/dL)",
            10,
            100,
            50
        )


        triglycerides = st.number_input(
            "Triglycerides (mg/dL)",
            20,
            500,
            120
        )



    if st.button(
        "🧪 Analyze Laboratory Results",
        use_container_width=True
    ):


        st.divider()


        st.subheader(
            "📋 Laboratory Report"
        )



        # HbA1c

        if hba1c < 5.7:

            st.success(
                "✅ HbA1c : Normal"
            )


        elif hba1c < 6.5:

            st.warning(
                "⚠️ HbA1c : Prediabetes Range"
            )


        else:

            st.error(
                "🔴 HbA1c : Diabetes Range"
            )



        # FBS

        if fbs < 100:

            st.success(
                "✅ Fasting Blood Sugar : Normal"
            )


        elif fbs < 126:

            st.warning(
                "⚠️ Fasting Blood Sugar : Prediabetes"
            )


        else:

            st.error(
                "🔴 Fasting Blood Sugar : High"
            )



        # Cholesterol

        if cholesterol < 200:

            st.success(
                "✅ Total Cholesterol : Normal"
            )


        elif cholesterol < 240:

            st.warning(
                "⚠️ Total Cholesterol : Borderline High"
            )


        else:

            st.error(
                "🔴 Total Cholesterol : High"
            )



        # LDL

        if ldl < 100:

            st.success(
                "✅ LDL : Optimal"
            )


        elif ldl < 160:

            st.warning(
                "⚠️ LDL : Elevated"
            )


        else:

            st.error(
                "🔴 LDL : Very High"
            )



        # HDL

        if hdl >= 60:

            st.success(
                "✅ HDL : Excellent"
            )


        elif hdl >= 40:

            st.info(
                "🟡 HDL : Acceptable"
            )


        else:

            st.error(
                "🔴 HDL : Low"
            )



        # Triglycerides

        if triglycerides < 150:

            st.success(
                "✅ Triglycerides : Normal"
            )


        elif triglycerides < 200:

            st.warning(
                "⚠️ Triglycerides : Borderline High"
            )


        else:

            st.error(
                "🔴 Triglycerides : High"
            )



        st.divider()



        st.subheader(
            "💡 Medical Recommendation"
        )



        if (
            hba1c < 5.7
            and fbs < 100
            and cholesterol < 200
            and ldl < 100
            and hdl >= 40
            and triglycerides < 150
        ):


            st.success(
                "🎉 Your laboratory results are generally within normal range."
            )


        else:


            st.warning(
                "⚠️ Some laboratory values need medical follow-up."
            )



    st.divider()



    # ==================================================
    # CHARTS
    # ==================================================


    st.header(
        "📊 Health Visualization"
    )


    chart_data = pd.DataFrame({

        "Parameter":[

            "BMI",
            "Health Score"

        ],

        "Value":[

            st.session_state.bmi,
            st.session_state.health_score

        ]

    })


    st.bar_chart(
        chart_data,
        x="Parameter",
        y="Value"
    )



    st.divider()



    st.subheader(
        "📈 Healthy Targets"
    )


    st.write(
        "🟢 BMI : 18.5 - 24.9"
    )


    st.write(
        "🟢 HbA1c : Less than 5.7%"
    )


    st.write(
        "🟢 Fasting Blood Sugar : Less than 100 mg/dL"
    )


    st.write(
        "🟢 LDL : Less than 100 mg/dL"
    )


    st.write(
        "🟢 Triglycerides : Less than 150 mg/dL"
    )
    # ==================================================
# PDF REPORT
# ==================================================

if st.session_state.page == 5 and st.session_state.analyzed:

    st.divider()

    st.header("📄 Download Your Health Report")

    if st.button(
        "Generate PDF Report",
        use_container_width=True
    ):

        pdf_file = generate_pdf(

            age=st.session_state.age,
            gender=st.session_state.gender,
            bmi=st.session_state.bmi,

            prediction=st.session_state.prediction,
            confidence=st.session_state.confidence,

            risk_level=st.session_state.risk_level,
            health_score=st.session_state.health_score,

            recommendations=st.session_state.recommendations

        )


        with open(pdf_file, "rb") as file:

            pdf_bytes = file.read()


        st.download_button(

            label="⬇️ Download PDF",

            data=pdf_bytes,

            file_name="HealthVibe_Obesity_Report.pdf",

            mime="application/pdf",

            use_container_width=True

        )



# ==================================================
# FINAL SUMMARY
# ==================================================

if st.session_state.page == 5 and st.session_state.analyzed:

    st.divider()

    st.header("📋 Final Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "BMI",
            round(st.session_state.bmi, 2)
        )

        st.metric(
            "Health Score",
            f"{st.session_state.health_score}/100"
        )

    with col2:

        st.metric(
            "AI Prediction",
            st.session_state.prediction
        )

        st.metric(
            "Risk Level",
            st.session_state.risk_level
        )



# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🏥 HealthVibe AI • Obesity Prediction Module"
)
