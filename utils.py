def calculate_bmi(weight, height):
    """
    Calculate BMI from weight (kg) and height (cm)
    """

    height = height / 100
    bmi = weight / (height ** 2)

    return round(bmi, 2)


def get_risk_level(probability):

    if probability < 0.30:
        return "🟢 Low Risk"

    elif probability < 0.70:
        return "🟡 Moderate Risk"

    else:
        return "🔴 High Risk"


def get_recommendation(probability):

    if probability < 0.30:

        return [
            "Maintain a healthy lifestyle.",
            "Exercise regularly.",
            "Eat a balanced diet.",
            "Check blood glucose periodically."
        ]

    elif probability < 0.70:

        return [
            "Monitor your blood glucose.",
            "Reduce sugar intake.",
            "Increase physical activity.",
            "Consult your doctor if needed."
        ]

    else:

        return [
            "Consult your physician immediately.",
            "Perform an HbA1c test.",
            "Follow a medical nutrition plan.",
            "Maintain regular follow-up."
        ]