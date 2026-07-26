import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("=" * 60)
print("Training HealthVibe Obesity Model")
print("=" * 60)

# ===========================
# Load Dataset
# ===========================
df = pd.read_csv("datasets/clean_obesity_dataset.csv")

# حذف الأعمدة الوصفية
df = df.drop(columns=[
    "Frequency of vegetable consumption Classes",
    "Number of main meals the person eats per day Classes",
    "Daily water consumption Classes",
    "Physical activity frequency Classes",
    "Time spent using technology Classes"
])

print(df.shape)

# ===========================
# Convert Text to Numbers
# ===========================
encoder = LabelEncoder()

for col in df.columns:
    if df[col].dtype == "object" or str(df[col].dtype) == "string" or str(df[col].dtype) == "str":
        df[col] = encoder.fit_transform(df[col].astype(str))

# ===========================
# Features & Target
# ===========================
target = "Obesity level class"

X = df.drop(columns=[target])
y = df[target]

# ===========================
# Split Dataset
# ===========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ===========================
# Train Model
# ===========================
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42
)

model.fit(X_train, y_train)

# ===========================
# Evaluate
# ===========================
pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("\nAccuracy :", acc)

# ===========================
# Save Model
# ===========================
joblib.dump(model, "models/obesity_model.pkl")

print("\nObesity Model Saved Successfully")