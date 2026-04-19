from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import get_transactions, get_fraud, predict_transaction, get_metrics

app = FastAPI(title="Corp Card Misuse Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_transactions.router)
app.include_router(get_fraud.router)
app.include_router(predict_transaction.router)
app.include_router(get_metrics.router)

@app.get("/")
def home():
    return {"message": "Corp Card Misuse Detection API is running!"}