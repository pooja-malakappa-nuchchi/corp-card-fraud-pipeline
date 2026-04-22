# Corporate Credit Card Misuse Detection Using Machine Learning and ETL Pipeline

An end-to-end system that detects corporate credit card misuse using machine learning, supported by an ETL pipeline, REST API, and interactive dashboard.

## Problem

Organizations lose approximately 5% of annual revenue to fraud. Corporate credit card misuse is one of the most common types. Manual review of hundreds of thousands of transactions is not scalable. This project automates fraud detection using machine learning.

## Dataset

- **Source:** Credit Card Fraud Detection (ULB, Kaggle)
- **Size:** 284,807 transactions
- **Features:** 30 (V1-V28 PCA features, Amount_Scaled, Hour)
- **Class Distribution:** 99.83% legitimate, 0.17% fraud (492 cases)
- **Challenge:** Severe class imbalance handled using SMOTE

## System Architecture

```
CSV Data → Extract → Transform → Load → PostgreSQL
                                            ↓
React Dashboard ← FastAPI Backend ← ML Models (5 trained)
```

## Tech Stack

- **ETL Pipeline:** Python, pandas
- **Database:** PostgreSQL
- **ML Models:** scikit-learn, XGBoost, LightGBM
- **Backend:** FastAPI (7 REST endpoints)
- **Frontend:** React + Vite
- **Pipeline Orchestration:** Apache Airflow (DAG defined)

## Models Compared

| Model | Precision | Recall | F1 | AUC-ROC |
|-------|-----------|--------|----|---------|
| Logistic Regression | 0.05 | 0.92 | 0.10 | 0.9715 |
| LinearSVC | 0.05 | 0.92 | 0.10 | 0.9742 |
| **Random Forest** | **0.86** | **0.83** | **0.84** | **0.9845** |
| XGBoost | 0.54 | 0.87 | 0.66 | 0.9739 |
| LightGBM | 0.10 | 0.91 | 0.19 | 0.9802 |

**Best Model:** Random Forest (highest precision, F1, and AUC-ROC)

## Project Structure

```
corp-card-fraud-pipeline/
├── airflow/
│   └── dag_pipeline.py              # Airflow DAG for ETL orchestration
├── backend/
│   ├── main.py                      # FastAPI app entry point
│   ├── database.py                  # PostgreSQL connection
│   └── routes/
│       ├── __init__.py
│       ├── get_transactions.py      # Transaction endpoints (paginated)
│       ├── get_fraud.py             # Fraud filter endpoint
│       ├── get_metrics.py           # Model metrics endpoints
│       └── predict_transaction.py   # Prediction endpoint
├── data/
│   └── creditcard.csv               # Raw dataset (ULB Kaggle)
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main app with routing and dark mode
│   │   ├── App.css                  # Global styles (dark glass theme)
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Overview stats and charts
│   │   │   ├── Transactions.jsx     # Browse all transactions
│   │   │   ├── Predict.jsx          # Real-time prediction with popup
│   │   │   └── ModelResults.jsx     # Model comparison with card tabs
│   │   └── components/
│   │       ├── Navbar.jsx
│   │       └── Charts.jsx
│   ├── package.json
│   └── vite.config.js
├── models/
│   ├── random_forest.pkl            # Best model
│   ├── logistic_regression.pkl
│   ├── linear_svc.pkl
│   ├── xgboost.pkl
│   ├── lightgbm.pkl
│   ├── scaler.pkl                   # StandardScaler for Amount
│   └── v_medians.json               # V feature medians for prediction
├── notebooks/
│   ├── 01_exploration.ipynb         # Initial data exploration
│   ├── 02_EDA.ipynb                 # Exploratory data analysis
│   ├── 03_modeling.ipynb            # Model training and comparison
│   └── 04_evaluation.ipynb          # Evaluation and visualizations
├── presentations/
│   ├── Presented by Pooja.pdf       # Final presentation slides
│   └── Presented by Pooja.pptx
├── report/
│   ├── Project Update1/             # Literature review
│   ├── Project Update 2/            # Data and methodology
│   └── Project Update 3/            # Results and analysis
├── src/
│   ├── extract.py                   # Extract raw data from CSV
│   ├── transform.py                 # Feature engineering (Hour, Scale Amount)
│   ├── load.py                      # Load processed data to PostgreSQL
│   └── pipeline.py                  # Run full ETL pipeline
├── visualizations/                  # EDA charts (10 PNGs)
│   ├── amount_boxplot.png
│   ├── amount_distribution.png
│   ├── auc_roc_comparison.png
│   ├── class_distribution.png
│   ├── confusion_matrix.png
│   ├── fraud_by_hour.png
│   ├── fraud_percentage_by_hour.png
│   ├── roc_curve.png
│   ├── top_features.png
│   └── transactions_by_hour.png
├── .gitignore
└── README.md
```

## How to Run

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL installed and running

### Step 1: Clone the repo

```bash
git clone https://github.com/pooja-malakappa-nuchchi/corp-card-fraud-pipeline.git
cd corp-card-fraud-pipeline
```

### Step 1b: Download the dataset

The dataset is not included in this repo due to GitHub's file size limit (150MB). Download `creditcard.csv` from [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it in the `data/` folder:

```
data/creditcard.csv
```

### Step 2: Install Python dependencies

```bash
pip install fastapi uvicorn pandas scikit-learn xgboost lightgbm sqlalchemy psycopg2-binary joblib imbalanced-learn
```

### Step 3: Set up PostgreSQL

Create a database called `corp_card_fraud`:

```sql
CREATE DATABASE corp_card_fraud;
```

### Step 4: Run the ETL pipeline

This extracts data from CSV, engineers features (Hour, Amount_Scaled), and loads into PostgreSQL:

```bash
python src/pipeline.py
```

### Step 5: Train the models (optional, pre-trained models included)

```bash
# Open and run notebooks/03_modeling.ipynb in Jupyter
```

### Step 6: Start the FastAPI backend (Terminal 1)

```bash
python -m uvicorn backend.main:app --reload
```

Backend runs at http://localhost:8000. Check http://localhost:8000/docs for API documentation.

### Step 7: Start the React frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at http://localhost:5173.

### Step 8: Open the app

Open http://localhost:5173 in your browser. Make sure the backend is running before opening the frontend.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /transactions | All transactions (paginated, filterable) |
| GET | /transactions/test | Test transactions with all 30 features |
| GET | /transactions/fraud | Fraud transactions only |
| GET | /transactions/summary | Dashboard summary stats |
| POST | /predict | Predict fraud on a single transaction |
| GET | /metrics | All model performance metrics |
| GET | /metrics/confusion-matrix | Confusion matrices for all models |

## Dashboard Pages

- **Dashboard** — Overview with stat cards, fraud by hour chart, class distribution
- **Transactions** — Browse all 284,807 transactions with pagination and filtering
- **Predict** — Select any transaction, click Predict, see result compared to ground truth
- **Model Results** — Compare all 5 models, click model cards for detailed metrics and confusion matrix

## Author

Pooja Malakappa Nuchchi
MS Computer Science, Northeastern University (Roux Institute)