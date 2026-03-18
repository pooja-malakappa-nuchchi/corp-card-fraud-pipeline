from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware 
# CORS = Cross Origin Resource Sharing
#CORSMiddleware - Asks Browser to Allow React to call FastAPI even through the origins of React and FAST API is different.

from routes import get_transactions, get_fraud, predict_transaction, get_metrics

# Create FastAPI app
app = FastAPI(title="Corp Card Misuse Detection API")

# Allow React frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React runs on 3000
    allow_methods=["*"],  #allow GET, POST, PUT, DELETE...
    allow_headers=["*"],  
)

# Register all routes
app.include_router(get_transactions.router) #Registers get_transactions.py routes into the main app. So atht, FastAPI will know all endpoints defined in get_transactions.py
app.include_router(get_fraud.router)
app.include_router(predict_transaction.router)
app.include_router(get_metrics.router)

# Test endpoint
@app.get("/")
#app.get = HTTP GET request ; "/" = URL path
def home():
    return {"message": "Corp Card Misuse Detection API is running!"}


#==============================================================================
#  FastAPI() - Creates the API app 
#  CORSMiddlewar - Allows React to call this API 
#  include_router - Registers each route file 
#  @app.get("/") - Test endpoint to check if API works 



