import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

from components.language import apply_language
from translations import get_text

st.set_page_config(
    page_title="HealthVibe - Obesity",
    page_icon="⚖️",
    layout="wide"
)

lang = apply_language()

st.title(get_text(lang, "obesity_page_title"))
st.write(get_text(lang, "obesity_page_subtitle"))

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
# ملحوظة: قيم الاختيارات (value) لازم تفضل زي ما هي بالإنجليزي لأن الموديل
# اتدرب عليها كده بالظبط. بنستخدم format_func بس عشان نعرض النص المترجم
# للمستخدم من غير ما نغيّر القيمة الحقيقية اللي بتتبعت للموديل.

gender = st.selectbox(
    get_text(lang, "gender"),
    ["Male", "Female"],
    format_func=lambda v: get_text(lang, "male") if v == "Male" else get_text(lang, "female")
)

age = st.number_input(
    get_text(lang, "age"),
    min_value=1,
    max_value=100,
    value=25
)

height = st.number_input(
    get_text(lang, "height_m_label"),
    min_value=1.00,
    max_value=2.50,
    value=1.70
)

weight = st.number_input(
    get_text(lang, "weight"),
    min_value=20,
    max_value=250,
    value=70
)

bmi = weight / (height ** 2)

st.metric(
    get_text(lang, "current_bmi_label"),
    round(bmi, 2)
)

family_history = st.selectbox(
    get_text(lang, "family_history_label"),
    ["yes", "no"],
    format_func=lambda v: get_text(lang, "yes_option") if v == "yes" else get_text(lang, "no_option")
)

high_calorie = st.selectbox(
    get_text(lang, "high_calorie_label"),
    ["yes", "no"],
    format_func=lambda v: get_text(lang, "yes_option") if v == "yes" else get_text(lang, "no_option")
)

vegetables = st.slider(
    get_text(lang, "vegetables_label"),
    1,
    3,
    2
)

meals = st.slider(
    get_text(lang, "meals_label"),
    1,
    4,
    3
)

snacks_map = {
    "no": get_text(lang, "no_option"),
    "Sometimes": get_text(lang, "snack_sometimes"),
    "Frequently": get_text(lang, "snack_frequently"),
    "Always": get_text(lang, "snack_always"),
}
snacks = st.selectbox(
    get_text(lang, "snacks_label"),
    list(snacks_map.keys()),
    format_func=lambda v: snacks_map[v]
)

smoke = st.selectbox(
    get_text(lang, "smoke_label"),
    ["yes", "no"],
    format_func=lambda v: get_text(lang, "yes_option") if v == "yes" else get_text(lang, "no_option")
)

water = st.slider(
    get_text(lang, "water_label"),
    1.0,
    3.0,
    2.0
)

calories = st.selectbox(
    get_text(lang, "calories_monitor_label"),
    ["yes", "no"],
    format_func=lambda v: get_text(lang, "yes_option") if v == "yes" else get_text(lang, "no_option")
)

activity = st.slider(
    get_text(lang, "activity_label"),
    0.0,
    3.0,
    1.0
)

technology = st.slider(
    get_text(lang, "technology_label"),
    0.0,
    2.0,
    1.0
)

alcohol_map = {
    "no": get_text(lang, "no_option"),
    "Sometimes": get_text(lang, "alcohol_sometimes"),
    "Frequently": get_text(lang, "alcohol_frequently"),
}
alcohol = st.selectbox(
    get_text(lang, "alcohol_label"),
    list(alcohol_map.keys()),
    format_func=lambda v: alcohol_map[v]
)

transport_map = {
    "Walking": get_text(lang, "transport_walking"),
    "Bike": get_text(lang, "transport_bike"),
    "Motorbike": get_text(lang, "transport_motorbike"),
    "Automobile": get_text(lang, "transport_automobile"),
    "Public_Transportation": get_text(lang, "transport_public"),
}
transport = st.selectbox(
    get_text(lang, "transport_label"),
    list(transport_map.keys()),
    format_func=lambda v: transport_map[v]
)

# ======================
# Prediction
# ======================

if st.button(get_text(lang, "predict_button")):

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
        0: get_text(lang, "obesity_level_0"),
        1: get_text(lang, "obesity_level_1"),
        2: get_text(lang, "obesity_level_2"),
        3: get_text(lang, "obesity_level_3"),
        4: get_text(lang, "obesity_level_4"),
        5: get_text(lang, "obesity_level_5"),
        6: get_text(lang, "obesity_level_6"),
    }

    result = labels[int(prediction[0])]

# ======================
# Prediction Summary
# ======================

if prediction is not None:

    st.divider()

    st.subheader(get_text(lang, "prediction_summary_header"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            get_text(lang, "bmi_label"),
            round(bmi, 2)
        )

    with col2:
        st.metric(
            get_text(lang, "ai_prediction_metric"),
            result
        )

    with col3:
        st.metric(
            get_text(lang, "confidence_metric"),
            f"{confidence:.1f}%"
        )

    st.divider()

    # ======================
    # Risk Level
    # ======================

    if bmi < 25:
        risk = get_text(lang, "obesity_risk_low")
    elif bmi < 30:
        risk = get_text(lang, "obesity_risk_moderate")
    elif bmi < 35:
        risk = get_text(lang, "obesity_risk_high")
    else:
        risk = get_text(lang, "obesity_risk_very_high")

    st.subheader(get_text(lang, "risk_level_header"))
    st.info(risk)

    # ======================
    # BMI Status
    # ======================

    if bmi < 18.5:
        st.info(get_text(lang, "bmi_underweight"))
    elif bmi < 25:
        st.success(get_text(lang, "bmi_healthy"))
    elif bmi < 30:
        st.warning(get_text(lang, "bmi_overweight"))
    elif bmi < 35:
        st.error(get_text(lang, "bmi_obesity_1"))
    elif bmi < 40:
        st.error(get_text(lang, "bmi_obesity_2"))
    else:
        st.error(get_text(lang, "bmi_severe_obesity"))

    # ======================
    # Risk Factors
    # ======================

    st.divider()

    st.subheader(get_text(lang, "risk_factors_header"))

    risk_list = []

    if bmi >= 30:
        risk_list.append(get_text(lang, "risk_factor_bmi"))

    if smoke == "yes":
        risk_list.append(get_text(lang, "risk_factor_smoking"))

    if family_history == "yes":
        risk_list.append(get_text(lang, "risk_factor_family"))

    if activity < 1:
        risk_list.append(get_text(lang, "risk_factor_activity"))

    if water < 2:
        risk_list.append(get_text(lang, "risk_factor_water"))

    if high_calorie == "yes":
        risk_list.append(get_text(lang, "risk_factor_calorie"))

    if len(risk_list) == 0:
        st.success(get_text(lang, "no_major_risk_factors"))
    else:
        for item in risk_list:
            st.write("•", item)

    # ======================
    # Recommendations
    # ======================

    st.divider()

    st.subheader(get_text(lang, "personalized_recommendations_header"))

    if bmi < 18.5:
        st.info(get_text(lang, "rec_underweight_1"))
        st.info(get_text(lang, "rec_underweight_2"))
        st.info(get_text(lang, "rec_underweight_3"))

    elif bmi < 25:
        st.success(get_text(lang, "rec_healthy_1"))
        st.success(get_text(lang, "rec_healthy_2"))
        st.success(get_text(lang, "rec_healthy_3"))

    elif bmi < 30:
        st.warning(get_text(lang, "rec_overweight_1"))
        st.warning(get_text(lang, "rec_overweight_2"))
        st.warning(get_text(lang, "rec_overweight_3"))

    else:
        st.error(get_text(lang, "rec_obese_1"))
        st.error(get_text(lang, "rec_obese_2"))
        st.error(get_text(lang, "rec_obese_3"))
        st.error(get_text(lang, "rec_obese_4"))

# ======================
# Obesity Lab Analysis
# ======================

st.divider()

st.header(get_text(lang, "lab_analysis_header"))

hba1c = st.number_input(
    get_text(lang, "hba1c_label"),
    3.0, 15.0, 5.5
)

fbs = st.number_input(
    get_text(lang, "fbs_label"),
    50, 300, 90
)

cholesterol = st.number_input(
    get_text(lang, "cholesterol_label"),
    100, 400, 180
)

ldl = st.number_input(
    get_text(lang, "ldl_label"),
    20, 300, 90
)

hdl = st.number_input(
    get_text(lang, "hdl_label"),
    10, 100, 50
)

triglycerides = st.number_input(
    get_text(lang, "triglycerides_label"),
    20, 500, 120
)

if st.button(get_text(lang, "analyze_lab_button")):

    st.subheader(get_text(lang, "lab_report_header"))

    # HbA1c
    if hba1c < 5.7:
        st.success(get_text(lang, "hba1c_normal"))
    elif hba1c < 6.5:
        st.warning(get_text(lang, "hba1c_prediabetes"))
    else:
        st.error(get_text(lang, "hba1c_diabetes"))

    # FBS
    if fbs < 100:
        st.success(get_text(lang, "fbs_normal"))
    elif fbs < 126:
        st.warning(get_text(lang, "fbs_prediabetes"))
    else:
        st.error(get_text(lang, "fbs_high"))

    # Cholesterol
    if cholesterol < 200:
        st.success(get_text(lang, "chol_normal"))
    elif cholesterol < 240:
        st.warning(get_text(lang, "chol_borderline"))
    else:
        st.error(get_text(lang, "chol_high"))

    # LDL
    if ldl < 100:
        st.success(get_text(lang, "ldl_optimal"))
    elif ldl < 160:
        st.warning(get_text(lang, "ldl_elevated"))
    else:
        st.error(get_text(lang, "ldl_very_high"))

    # HDL
    if hdl >= 60:
        st.success(get_text(lang, "hdl_excellent"))
    elif hdl >= 40:
        st.warning(get_text(lang, "hdl_acceptable"))
    else:
        st.error(get_text(lang, "hdl_low"))

    # Triglycerides
    if triglycerides < 150:
        st.success(get_text(lang, "trig_normal"))
    elif triglycerides < 200:
        st.warning(get_text(lang, "trig_borderline"))
    else:
        st.error(get_text(lang, "trig_high"))

    st.divider()

    st.subheader(get_text(lang, "overall_recommendation_header"))

    if (
        hba1c < 5.7
        and fbs < 100
        and cholesterol < 200
        and ldl < 100
        and hdl >= 40
        and triglycerides < 150
    ):
        st.success(get_text(lang, "lab_results_normal_msg"))
    else:
        st.warning(get_text(lang, "lab_results_abnormal_msg"))

# ======================
# Footer
# ======================

st.divider()

st.caption(get_text(lang, "obesity_footer_caption"))