# Import all three functions from their files
from extract import extract_data
from transform import transform_data
from load import get_engine, load_raw_data, load_processed_data

def run_pipeline():
    print("=" * 50)
    print("STARTING ETL PIPELINE")
    print("=" * 50)

    # STEP 1 - EXTRACT
    print("\nStep 1: Extracting data...")
    df_raw = extract_data()

    # STEP 2 - LOAD RAW
    print("\nStep 2: Loading raw data to PostgreSQL...")
    engine = get_engine()
    load_raw_data(df_raw, engine)

    # STEP 3 - TRANSFORM
    print("\nStep 3: Transforming data...")
    df_processed = transform_data(df_raw)

    # STEP 4 - LOAD PROCESSED
    print("\nStep 4: Loading processed data to PostgreSQL...")
    load_processed_data(df_processed, engine)

    print("\n" + "=" * 50)
    print("ETL PIPELINE COMPLETE!")
    print("=" * 50)

if __name__ == '__main__':
    run_pipeline()


    #python src/pipeline.py