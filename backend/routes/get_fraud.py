from fastapi import APIRouter
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://postgres:1234@localhost:5432/corp_card_fraud")
router = APIRouter()

@router.get("/transactions/fraud")
#GET endpoint at /transactions/fraud : When React calls this it Returns ONLY fraud transactions (Class = 1 means fraud)

def get_fraud_transactions():
    df = pd.read_sql('SELECT * FROM processed_transactions WHERE "Class" = 1', engine)
    #WHERE "Class" = 1 means only return rows where Class = 1, whcih is only fraud transactions!

    return df.to_dict(orient="records")
    # Converts to JSON for React

@router.get("/transactions/summary")
def get_summary():
    total = pd.read_sql("SELECT COUNT(*) as total FROM processed_transactions", engine).iloc[0]['total']
    fraud = pd.read_sql('SELECT COUNT(*) as fraud FROM processed_transactions WHERE "Class" = 1', engine).iloc[0]['fraud']
    return {
    "total_transactions": int(total),
    # int() converts numpy int to Python int
    # FastAPI needs Python int for JSON 

    "fraud_transactions": int(fraud),
    # 492

    "legitimate_transactions": int(total - fraud),
    # 284807 - 492 = 284315

    "fraud_percentage": round((fraud/total)*100, 2)
    # (492/284807) * 100 = 0.17%
    # round(0.172..., 2) = 0.17
}