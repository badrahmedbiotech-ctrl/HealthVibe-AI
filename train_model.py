import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# قراءة الداتا
df = pd.read_csv("diabetes.csv")

# تقسيم البيانات
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# Train / Test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# إنشاء الموديل
model = LogisticRegression(max_iter=1000)

# التدريب
model.fit(X_train, y_train)

# حفظ الموديل
joblib.dump(model, "models/diabetes_model.pkl")

print("Model trained successfully!")