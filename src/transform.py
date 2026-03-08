import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

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