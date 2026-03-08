import pandas as pd
from sqlalchemy import create_engine        #SQLAlchemy = bridge between Python and PostgreSQL, create_engine = creates connection to database

def get_engine():
    # Connect to PostgreSQL
    engine = create_engine(
        'postgresql://postgres:1234@localhost:5432/corp_card_fraud'             #Connect to PostgreSQL at my computer (localhost) port 5432 database corp_card_fraud using username postgres and my password
    )
    return engine

def load_raw_data(df, engine):
    df.to_sql(
        'raw_transactions',
        engine,
        if_exists='replace', #if table already has data,delete it and reload fresh
        index=False #no index col needed
    )
    print(f"Raw data loaded: {len(df)} rows")

def load_processed_data(df_transformed, engine):
    df_transformed.to_sql(
        'processed_transactions',
        engine,
        if_exists='replace',
        index=False
    )
    print(f"Processed data loaded: {len(df_transformed)} rows")

if __name__ == '__main__':
    from extract import extract_data
    from transform import transform_data

    # STEP 1 — EXTRACT
    df_raw = extract_data()

    # STEP 2 — LOAD RAW FIRST (before transform)
    engine = get_engine()
    load_raw_data(df_raw, engine)

    # STEP 3 — TRANSFORM
    df_processed = transform_data(df_raw)

    # STEP 4 — LOAD PROCESSED
    load_processed_data(df_processed, engine)

    print("\n ETL Load complete!")


    #python src/load.py
    #to check:
    # psql -U postgres -d corp_card_fraud
    # SELECT COUNT(*) FROM raw_transactions;
    # SELECT COUNT(*) FROM processed_transactions;
    # SELECT column_name FROM information_schema.columns  WHERE table_name = 'raw_transactions';
    # SELECT column_name FROM information_schema.columns  WHERE table_name = 'processed_transactions';