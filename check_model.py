import joblib

print("=================================")

features = joblib.load("models/trained_features.pkl")

print(features)

print(type(features))

print("=================================")