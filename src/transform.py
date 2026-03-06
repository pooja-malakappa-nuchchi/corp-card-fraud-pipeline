import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def transform_data(df):
    print("Starting transformation...")
    
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