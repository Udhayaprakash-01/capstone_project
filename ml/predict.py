import joblib
import numpy as np

# ✅ Load trained model
model = joblib.load("ml/model.pkl")


def predict_usage_risk(features: dict):

    # ✅ Prepare input for model
    X = np.array([[
        features["avg_usage"],
        features["growth_rate"],
        features["variability"],
        features["peak_ratio"]
    ]])

    # ✅ Prediction
    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max()

    # ✅ Map labels
    mapping = {
        0: "LOW",
        1: "MEDIUM",
        2: "HIGH"
    }

    return {
        "congestion_risk": mapping[pred],
        "anomaly_flag": prob > 0.8,
        "score": float(prob)
    }