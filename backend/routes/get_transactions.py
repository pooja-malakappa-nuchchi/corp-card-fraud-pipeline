from fastapi import APIRouter
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://postgres:1234@localhost:5432/corp_card_fraud")
router = APIRouter()

@router.get("/transactions")
def get_all_transactions():
    df = pd.read_sql("SELECT * FROM processed_transactions LIMIT 100", engine)
    return df.to_dict(orient="records")