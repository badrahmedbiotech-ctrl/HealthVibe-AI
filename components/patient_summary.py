import streamlit as st
import pandas as pd

def patient_summary(data):

    st.subheader("📋 Patient Summary")

    df = pd.DataFrame({

        "Feature": data.keys(),

        "Value": data.values()

    })

    st.dataframe(
        df,
        use_container_width=True
    )