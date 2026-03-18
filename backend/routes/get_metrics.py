from fastapi import APIRouter

router = APIRouter()

@router.get("/metrics")
def get_metrics():
    return {
        "models": [
            {"name": "Logistic Regression", "precision": 0.05, "recall": 0.92, "f1": 0.10, "auc_roc": 0.9715, "training_time": "12s", "verdict": "poor"},
            {"name": "LinearSVC", "precision": 0.05, "recall": 0.92, "f1": 0.10, "auc_roc": 0.9742, "training_time": "20s", "verdict": "poor"},
            {"name": "Random Forest", "precision": 0.86, "recall": 0.83, "f1": 0.84, "auc_roc": 0.9845, "training_time": "103s", "verdict": "best"},
            {"name": "XGBoost", "precision": 0.54, "recall": 0.87, "f1": 0.66, "auc_roc": 0.9739, "training_time": "5s", "verdict": "medium"},
            {"name": "LightGBM", "precision": 0.10, "recall": 0.91, "f1": 0.19, "auc_roc": 0.9802, "training_time": "8s", "verdict": "medium"}
        ],
        "best_model": "Random Forest",
        "best_auc_roc": 0.9845
    }

@router.get("/metrics/confusion-matrix")
def get_confusion_matrix():
    return {
        "models": [
            {"name": "Logistic Regression", "tn": 55317, "fp": 1547, "fn": 8, "tp": 90},
            {"name": "LinearSVC", "tn": 55280, "fp": 1584, "fn": 8, "tp": 90},
            {"name": "Random Forest", "tn": 56851, "fp": 13, "fn": 17, "tp": 81},
            {"name": "XGBoost", "tn": 56791, "fp": 73, "fn": 13, "tp": 85},
            {"name": "LightGBM", "tn": 56096, "fp": 768, "fn": 9, "tp": 89}
        ]
    }