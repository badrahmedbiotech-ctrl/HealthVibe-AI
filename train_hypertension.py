import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import joblib
import os

print("🔄 1. جاري تحميل الداتا سيت الطبية المعتمدة (Framingham)...")
df = pd.read_csv("dataset/hypertension_dataset.csv")
df.columns = df.columns.str.strip()

print("🧬 2. تطبيق هندسة الميزات (Feature Engineering) لرفع الدقة...")
df['pulse_pressure'] = df['sysBP'] - df['diaBP']
df['mean_arterial_pressure'] = df['diaBP'] + (df['pulse_pressure'] / 3)
df['age_bmi'] = df['age'] * df['BMI']
df['smoking_load'] = df['currentSmoker'] * df['cigsPerDay'].fillna(0)

X = df.drop(columns=['Risk'])
y = df['Risk']

print(f"      عدد الصفوف المستخدمة (بالكامل، من غير حذف أي فراغات): {len(X):,}")

print("⚖️ 3. تقسيم البيانات بشكل متوازن (Stratified Split)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("⚙️ 4. ضبط الموديل (HistGradientBoostingClassifier + موازنة الفئات)...")
hgb = HistGradientBoostingClassifier(random_state=42, class_weight='balanced')
param_grid = {
    'max_iter': [50, 100, 150],
    'max_depth': [5, 10, None],
    'learning_rate': [0.01, 0.05, 0.1]
}
grid_search = GridSearchCV(estimator=hgb, param_grid=param_grid, cv=3, n_jobs=-1, scoring='accuracy', verbose=0)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1])

print("\n" + "=" * 50)
print("🎯 نتيجة الموديل النهائي")
print("=" * 50)
print(f"✅ Accuracy: {accuracy * 100:.2f}%")
print(f"✅ AUC Score: {auc:.3f}  (كل ما اقترب من 1.0 كل ما كان أفضل)")
print(f"⚙️ أفضل إعدادات: {grid_search.best_params_}")
print("=" * 50)
print("\n📋 تقرير التقييم التفصيلي:")
print(classification_report(y_test, y_pred, target_names=["Low Risk", "High Risk"]))

os.makedirs("models", exist_ok=True)
joblib.dump(best_model, "models/hypertension_model.pkl")
joblib.dump(X.columns.tolist(), "models/trained_features.pkl")
joblib.dump({}, "models/hypertension_model_encoders.pkl")

print("💾 عظيييم! تم تدريب وحفظ الموديل النظيف والأعمدة المحدثة في مجلد 'models/'!")