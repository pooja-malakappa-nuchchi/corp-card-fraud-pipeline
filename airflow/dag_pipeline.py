from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path so we can import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

# Default settings for all tasks
default_args = {
    'owner': 'pooja',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
# Runs daily — in production this would process new transaction data each day
dag = DAG(
    'corp_card_fraud_etl',
    default_args=default_args,
    description='ETL pipeline for corporate credit card fraud detection',
    schedule_interval='@daily',
    catchup=False,
)

# Task 1: Extract raw data from CSV
def run_extract(**kwargs):
    df = extract_data()
    # Save to temp location for next task
    df.to_csv('/tmp/extracted_data.csv', index=False)
    print(f"Extracted {len(df)} rows")
    return len(df)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=run_extract,
    dag=dag,
)

# Task 2: Transform — engineer features, scale amount
def run_transform(**kwargs):
    import pandas as pd
    df = pd.read_csv('/tmp/extracted_data.csv')
    df_transformed = transform_data(df)
    df_transformed.to_csv('/tmp/transformed_data.csv', index=False)
    print(f"Transformed {len(df_transformed)} rows")
    print(f"Columns: {df_transformed.columns.tolist()}")
    return len(df_transformed)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=run_transform,
    dag=dag,
)

# Task 3: Load into PostgreSQL
def run_load(**kwargs):
    import pandas as pd
    df = pd.read_csv('/tmp/transformed_data.csv')
    load_data(df)
    print(f"Loaded {len(df)} rows into PostgreSQL")
    return len(df)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=run_load,
    dag=dag,
)

# Task 4: Validate — check data was loaded correctly
def run_validate(**kwargs):
    import pandas as pd
    from sqlalchemy import create_engine
    engine = create_engine("postgresql://postgres:1234@localhost:5432/corp_card_fraud")
    
    # Check row count
    count = pd.read_sql("SELECT COUNT(*) as cnt FROM processed_transactions", engine).iloc[0]['cnt']
    print(f"Validation: {count} rows in database")
    
    # Check class distribution
    dist = pd.read_sql('SELECT "Class", COUNT(*) as cnt FROM processed_transactions GROUP BY "Class"', engine)
    print(f"Class distribution:\n{dist}")
    
    # Check no null values
    nulls = pd.read_sql('SELECT COUNT(*) as cnt FROM processed_transactions WHERE "Hour" IS NULL', engine).iloc[0]['cnt']
    if nulls > 0:
        raise ValueError(f"Found {nulls} null values in Hour column!")
    
    print("Validation passed!")
    return count

validate_task = PythonOperator(
    task_id='validate_data',
    python_callable=run_validate,
    dag=dag,
)

# Define task order: extract -> transform -> load -> validate
extract_task >> transform_task >> load_task >> validate_task