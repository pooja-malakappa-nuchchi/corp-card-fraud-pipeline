from fastapi import APIRouter
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://postgres:1234@localhost:5432/corp_card_fraud")
router = APIRouter()

@router.get("/transactions/fraud")
def get_fraud_transactions():
    df = pd.read_sql('SELECT * FROM processed_transactions WHERE "Class" = 1', engine)
    return df.to_dict(orient="records")

@router.get("/transactions/summary")
def get_summary():
    total = pd.read_sql("SELECT COUNT(*) as total FROM processed_transactions", engine).iloc[0]['total']
    fraud = pd.read_sql('SELECT COUNT(*) as fraud FROM processed_transactions WHERE "Class" = 1', engine).iloc[0]['fraud']
    return {
        "total_transactions": int(total),
        "fraud_transactions": int(fraud),
        "legitimate_transactions": int(total - fraud),
        "fraud_percentage": round((fraud/total)*100, 2)
    }