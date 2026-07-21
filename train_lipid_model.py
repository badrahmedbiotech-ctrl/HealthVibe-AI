import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("="*60)
print("Training HealthVibe Lipid Model")
print("="*60)

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("datasets/clean_lipid_dataset.csv")

# الأعمدة المستخدمة

features = [
    "age",
    "sex",
    "cholesterol_total",
    "ldl",
    "hdl",
    "triglycerides",
    "fasting_blood_sugar",
    "hba1c",
    "bmi",
    "resting_bp_systolic",
    "smoker_status"
]

X = df[features]

y = df["Lipid_Risk"]

# ==========================
# Encoding
# ==========================

encoder = LabelEncoder()

X["sex"] = encoder.fit_transform(X["sex"])

X["smoker_status"] = encoder.fit_transform(X["smoker_status"])

# ==========================
# Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================
# Model
# ==========================

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================
# Evaluation
# ==========================

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("\nAccuracy :", acc)

# ==========================
# Save
# ==========================

joblib.dump(model, "models/lipid_model.pkl")

print("\nLipid Model Saved Successfully")