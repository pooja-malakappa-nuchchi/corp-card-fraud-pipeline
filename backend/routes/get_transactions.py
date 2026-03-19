from fastapi import APIRouter, Query  
# APIRouter = create grouped routes
# Query = lets us accept URL parameters like ?page=1&limit=20

from sqlalchemy import create_engine  
# creates PostgreSQL connection
import pandas as pd                   
# reads SQL results into dataframe

# PostgreSQL connection string
# format: postgresql://username:password@host:port/database
engine = create_engine("postgresql://postgres:1234@localhost:5432/corp_card_fraud")

router = APIRouter()  # creates router for transaction endpoints

@router.get("/transactions")
# Main transactions endpoint
# Supports pagination and filtering
# React calls: GET /transactions?page=1&limit=20&filter=fraud
def get_all_transactions(
    page: int = Query(default=1),      # which page? default=1
    limit: int = Query(default=20),    # rows per page? default=20
    filter: str = Query(default="all") # all/fraud/legitimate
):
    # Calculate how many rows to skip
    # Page 1: skip 0, Page 2: skip 20, Page 3: skip 40
    offset = (page - 1) * limit

    # Build WHERE clause based on filter
    if filter == "fraud":
        where = 'WHERE "Class" = 1'      # only fraud rows
    elif filter == "legitimate":
        where = 'WHERE "Class" = 0'      # only legitimate rows
    else:
        where = ''                        # all rows

    # Fetch transactions with pagination
    # LIMIT = how many rows to return
    # OFFSET = how many rows to skip
    query = f'SELECT * FROM processed_transactions {where} LIMIT {limit} OFFSET {offset}'
    df = pd.read_sql(query, engine)

    # Get total count for pagination calculation
    count_query = f'SELECT COUNT(*) as total FROM processed_transactions {where}'
    total = pd.read_sql(count_query, engine).iloc[0]['total']

    return {
        "transactions": df.to_dict(orient="records"),  # list of transaction dicts
        "total": int(total),                            # total matching rows
        "page": page,                                   # current page
        "limit": limit,                                 # rows per page
        "total_pages": int(total // limit) + 1         # total pages available
    }

@router.get("/transactions/test")
# Used specifically for Predict page
# Returns transactions with ALL 30 features
# React uses these to send to /predict endpoint
def get_test_transactions(
    page: int = Query(default=1),   # which page
    limit: int = Query(default=20)  # rows per page
):
    # Calculate offset for pagination
    offset = (page - 1) * limit

    # Fetch transactions — no filter, all rows
    query = f'SELECT * FROM processed_transactions LIMIT {limit} OFFSET {offset}'
    df = pd.read_sql(query, engine)

    # Get total count
    total = pd.read_sql(
        "SELECT COUNT(*) as total FROM processed_transactions",
        engine
    ).iloc[0]['total']

    return {
        "transactions": df.to_dict(orient="records"),  # all 30 features included
        "total": int(total),
        "page": page,
        "total_pages": int(total // limit) + 1
    }