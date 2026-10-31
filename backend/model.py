import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "Crop_recommendation.csv")
if not os.path.exists(CSV_PATH):
    CSV_PATH = os.path.join(BASE_DIR, "..", "Crop_recommendation.csv")

print(f"Loading dataset from: {CSV_PATH}")
df = pd.read_csv(CSV_PATH)

# Features: N, P, K, temperature, humidity, ph, rainfall
X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
y = df["label"]

# 80/20 train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
print("Training Random Forest Classifier (100 estimators)...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred) * 100
print(f"✅ Accuracy on Test Set: {acc:.2f}%")

# Save model
output_model_path = os.path.join(BASE_DIR, "model.pkl")
with open(output_model_path, "wb") as f:
    pickle.dump(model, f)
print(f"✅ Model serialized and saved to: {output_model_path}")
