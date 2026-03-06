#Load raw CSV from data/ folder into a pandas dataframe
import pandas as pd
import os

def extract_data():
    # Get the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'creditcard.csv')
    
    # load CSV into dataframe
    df = pd.read_csv(data_path)
    
    print(f"Data extracted successfully!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    return df

if __name__ == '__main__':
    df = extract_data()


#Instructions for myself:
#==========================
#cd corp-card-fraud-pipeline
#python src/extract.py