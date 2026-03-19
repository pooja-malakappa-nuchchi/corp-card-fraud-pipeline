import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os
import json

def transform_data(df):
    print("Starting transformation...")

    #  # STEP 1 — SAFETY CLEANING (Not needed as data is clean already, no null values, no datatype changes needed)
    
    # # Remove duplicates
    # before = len(df)
    # df = df.drop_duplicates()
    # after = len(df)
    # print(f"✅ Duplicates removed: {before - after} rows dropped")
    
    # # Handle missing values
    # missing = df.isnull().sum().sum()
    # if missing > 0:
    #     print(f"⚠️ Found {missing} missing values — filling...")
    #     num_cols = df.select_dtypes(include=[np.number]).columns
    #     df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    #     print("✅ Missing values filled with median")
    # else:
    #     print("✅ No missing values found!")

    # # Fix data types
    # df['Class'] = df['Class'].astype(int)
    # print("✅ Data types verified")
    #==================================================
    
    # Step 1 — Engineer Hour feature
    df['Hour'] = (df['Time'] / 3600) % 24
    df['Hour'] = df['Hour'].astype(int)
    print("Hour feature engineered")
    
    # Step 2 — Scale Amount column
    scaler = StandardScaler()
    df['Amount_Scaled'] = scaler.fit_transform(df[['Amount']])
    # fit_transform does:
    # 1. Calculates mean 
    # 2. Calculates std 
    # 3. Applies (value - mean) / std to every row
    print(" Amount scaled")

    # Save scaler so predict_transaction.py can use same scaling
    # When new dataset comes in, scaler updates automatically i.e., New dataset has different transactions Different amounts, different patterns
    # So, based on input, New mean and std will be calculated
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print("Scaler saved to models/scaler.pkl")

    # Save V1-V28 medians
    # When new dataset comes → medians recalculate automatically!
    v_cols = [f'V{i}' for i in range(1, 29)]
    v_medians = df[v_cols].median().tolist()
    medians_path = os.path.join(base_dir, 'models', 'v_medians.json')
    with open(medians_path, 'w') as f:
        json.dump(v_medians, f)
    print("V medians saved to models/v_medians.json")

# New data arrives
# transform.py runs on NEW data
# scaler.fit_transform(df[['Amount']]) --> (fits on NEW data, calculates NEW mean and std, saves NEW scaler.pkl)        ↓
# predict_transaction.py loads NEW scaler.pkl uses NEW mean and std automatically 
    
    # Step 3 — Drop original Time and Amount columns
    # (replaced by Hour and Amount_Scaled)
    df = df.drop(['Time', 'Amount'], axis=1)
    print(" Unnecessary columns dropped")
    
    print(f"\nTransformed data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    return df

if __name__ == '__main__':
    from extract import extract_data
    df = extract_data()
    df_transformed = transform_data(df)


#scaled_value = (original_value - mean) / std
#Mean = sum of all values / count
#Std= calculated by .describe 
    #python src/transform.py