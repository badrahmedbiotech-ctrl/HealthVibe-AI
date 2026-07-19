import streamlit as st

def recommendation(prediction):

    st.subheader("💡 Medical Recommendation")

    if prediction == 1:

        st.warning("""
### High Risk

• Visit an Internal Medicine doctor.

• Perform HbA1c Test.

• Monitor Blood Glucose.

• Reduce Sugar Intake.

• Exercise 30 minutes daily.

• Lose excess weight.

• Repeat laboratory tests.
""")

    else:

        st.success("""
### Healthy Lifestyle

• Continue healthy nutrition.

• Exercise regularly.

• Drink enough water.

• Annual Diabetes Screening.

• Maintain healthy body weight.
""")