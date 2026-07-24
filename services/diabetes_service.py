import joblib
import pandas as pd

model = joblib.load("models/diabetes_model.pkl")


def predict_diabetes(
    pregnancies,
    glucose,
    blood_pressure,
    skin_thickness,
    insulin,
    bmi,
    pedigree,
    age
):

    df = pd.DataFrame([[
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        pedigree,
        age
    ]], columns=[
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age"
    ])

    prediction = model.predict(df)[0]

    probability = None

    try:
        probability = model.predict_proba(df)[0][1]
    except Exception:
        pass

    return prediction, probability