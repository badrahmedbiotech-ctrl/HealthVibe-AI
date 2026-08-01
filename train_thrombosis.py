import pandas as pd

import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# =====================================
# Load Dataset
# =====================================

DATASET_PATH = "dataset/thrombosis_filtered.csv"

df = pd.read_csv(DATASET_PATH)

print(df.head())
print(df.columns)

# =====================================
# Target Column
# =====================================

TARGET = "Thrombosis"

X = df.drop(columns=[TARGET, "SubjectID"])
X["Sex"] = X["Sex"].map({
    "M": 1,
    "F": 0
})
y = df[TARGET]

# =====================================
# Train Test Split
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =====================================
# SMOTE
# =====================================

smote = SMOTE(random_state=42)

X_train, y_train = smote.fit_resample(
    X_train,
    y_train
)
print("Before SMOTE:")
print(y.value_counts())

print("After SMOTE:")
print(pd.Series(y_train).value_counts())
# =====================================
# Scaling
# =====================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =====================================
# Model
# =====================================

model = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# =====================================
# Evaluation
# =====================================

pred = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, pred))

print("\nClassification Report:")
print(classification_report(y_test, pred))

# =====================================
# Save Model
# =====================================

Path("models").mkdir(exist_ok=True)

joblib.dump(model, "models/thrombosis_model.pkl")
joblib.dump(scaler, "models/thrombosis_scaler.pkl")

print("\nModel Saved Successfully ✅")