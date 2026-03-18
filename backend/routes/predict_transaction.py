from fastapi import APIRouter
import joblib
import numpy as np
import os

router = APIRouter()

model_path = os.path.join(os.path.dirname(__file__), '../../models/random_forest.pkl')
model = joblib.load(model_path)

@router.post("/predict")
def predict(data: dict):
    features = data.get("features")
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)[0]
    probability = model.predict_proba(features_array)[0][1]
    return {
        "prediction": int(prediction),
        "result": "Fraud" if prediction == 1 else "Legitimate",
        "fraud_probability": round(float(probability), 4),
        "model_used": "Random Forest"
    }