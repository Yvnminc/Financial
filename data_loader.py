#!/usr/bin/env python3
"""
Data loader for MMC financial data
"""
import pandas as pd
import numpy as np

def load_financial_data(filename):
    """Load and clean the financial data from Excel"""
    try:
        # Read the raw data
        df_raw = pd.read_excel(filename, sheet_name='MMC', header=None)
        
        # Print raw data to understand structure
        print("Raw data structure:")
        for i in range(10):  # Show first 10 rows
            print(f"Row {i}: {df_raw.iloc[i].tolist()}")
        
        # Find the header row (likely row with months)
        header_row = None
        data_start_row = None
        
        for i, row in df_raw.iterrows():
            row_values = [str(val).strip() if pd.notna(val) else '' for val in row]
            if 'July' in row_values or 'Financial Year' in row_values:
                if 'Financial Year' in row_values:
                    year_row = i
                elif 'July' in row_values:
                    header_row = i
                    data_start_row = i + 1
                    break
        
        print(f"\nHeader row found at: {header_row}")
        print(f"Data starts at row: {data_start_row}")
        
        if header_row is not None:
            # Extract column names
            columns = []
            for val in df_raw.iloc[header_row]:
                if pd.notna(val):
                    columns.append(str(val).strip())
                else:
                    columns.append('')
            
            # Extract data starting from data_start_row
            data_df = df_raw.iloc[data_start_row:].copy()
            data_df.columns = range(len(data_df.columns))
            
            # Create a clean dataframe
            clean_data = []
            for i, row in data_df.iterrows():
                row_data = {}
                account_name = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ''
                if account_name and account_name != 'nan' and account_name.strip():
                    row_data['Account'] = account_name.strip()
                    # Add monthly data
                    for j, col_name in enumerate(columns[2:], start=2):
                        if col_name and j < len(row):
                            try:
                                value = row.iloc[j]
                                if pd.notna(value) and str(value).strip() != '':
                                    # Try to convert to numeric
                                    try:
                                        row_data[col_name] = float(str(value).replace(',', '').replace('$', '').replace('(', '-').replace(')', ''))
                                    except ValueError:
                                        row_data[col_name] = str(value)
                                else:
                                    row_data[col_name] = 0.0
                            except (IndexError, AttributeError):
                                row_data[col_name] = 0.0
                    
                    if len(row_data) > 1:  # Only add if we have more than just the account name
                        clean_data.append(row_data)
            
            # Convert to DataFrame
            df_clean = pd.DataFrame(clean_data)
            return df_clean
        
        return None
        
    except Exception as e:
        print(f"Error loading financial data: {e}")
        return None

def test_load_financial_data():
    """Test function to load and examine financial data"""
    filename = "MMC - Monthly Financial Data.xlsx"
    df = load_financial_data(filename)
    
    if df is not None:
        print("\nCleaned financial data:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nData types:")
        print(df.dtypes)
    else:
        print("Failed to load financial data")

if __name__ == "__main__":
    test_load_financial_data() 