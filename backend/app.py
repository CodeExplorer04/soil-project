import os
import pickle
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
CSV_PATH = os.path.join(BASE_DIR, "Crop_recommendation.csv")
if not os.path.exists(CSV_PATH):
    CSV_PATH = os.path.join(BASE_DIR, "..", "Crop_recommendation.csv")

model = None


def get_or_train_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
                print("✅ Pre-trained model.pkl loaded successfully.")
                return model
        except Exception as e:
            print(f"Failed to load model.pkl ({e}), retraining...")

    if os.path.exists(CSV_PATH):
        print(f"🌱 Training Crop Recommendation model from {CSV_PATH}...")
        df = pd.read_csv(CSV_PATH)
        X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
        y = df["label"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)
        print("✅ Model trained and saved as model.pkl!")
        return model
    else:
        print("⚠️ Warning: Crop_recommendation.csv not found!")
        return None


# Initialize model on startup
model = get_or_train_model()

# Path to frontend
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))


@app.route("/")
def home():
    if os.path.exists(os.path.join(FRONTEND_DIR, "index.html")):
        return send_from_directory(FRONTEND_DIR, "index.html")
    return jsonify({"message": "Soil Project Crop Recommendation API", "status": "online"})


@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return jsonify({"error": "Not found"}), 404


@app.route("/predict", methods=["POST"])
def predict():
    global model
    if model is None:
        model = get_or_train_model()
    if model is None:
        return jsonify({"error": "Model not available"}), 500

    data = request.get_json() or {}
    try:
        features = [
            float(data["N"]),
            float(data["P"]),
            float(data["K"]),
            float(data["temperature"]),
            float(data["humidity"]),
            float(data["ph"]),
            float(data["rainfall"])
        ]
        prediction = model.predict([features])[0]
        return jsonify({
            "prediction": prediction,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
