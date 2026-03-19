from fastapi import APIRouter
import joblib       # loads saved .pkl model files
import numpy as np  # converts features list to numpy array
import os           # builds file paths cross-platform

router = APIRouter()

# Load Random Forest model
# __file__ = current file location
# ../../ = go up 2 folders to project root
model_path = os.path.join(os.path.dirname(__file__), '../../models/random_forest.pkl')

# Load model ONCE when server starts
# Stays in memory — no reload every request
model = joblib.load(model_path)

@router.post("/predict")
# POST because React is SENDING data to server
def predict(data: dict):
    # data = entire transaction row sent from React
    # Contains V1-V28, Hour, Amount_Scaled, Class

    # Get V1-V28 features directly from transaction row
    v_features = [float(data.get(f'V{i}', 0)) for i in range(1, 29)]

    # Get Hour directly from transaction row
    hour = int(data.get('Hour', 0))

    # Get Amount_Scaled directly from transaction row
    # Already scaled by ETL pipeline — no rescaling needed!
    amount_scaled = float(data.get('Amount_Scaled', 0))

    # Build complete 30 feature array
    # Order must match training data:
    # V1-V28, Hour, Amount_Scaled
    features = v_features + [hour, amount_scaled]

    # Convert to 2D numpy array
    # reshape(1, -1) = 1 row, 30 columns
    # Model expects 2D input not 1D list
    features_array = np.array(features).reshape(1, -1)

    # Get prediction — 0=Legitimate, 1=Fraud
    prediction = model.predict(features_array)[0]

    # Get fraud probability (0.0 to 1.0)
    # [0] = first row, [1] = fraud probability
    probability = model.predict_proba(features_array)[0][1]

    # Get actual label from transaction row
    # Used to compare prediction vs reality in UI
    actual = data.get('Class', None)

    # Build response
    result = {
        "prediction": int(prediction),
        "result": "Fraud" if prediction == 1 else "Legitimate",
        "fraud_probability": round(float(probability), 4),
        "model_used": "Random Forest"
    }

    # Add actual label if available
    # React shows: "Predicted: Fraud | Actual: Fraud ✅"
    if actual is not None:
        result["actual"] = int(actual)
        result["actual_label"] = "Fraud" if int(actual) == 1 else "Legitimate"
        result["correct"] = int(prediction) == int(actual)

    return result