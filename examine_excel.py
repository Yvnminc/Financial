#!/usr/bin/env python3
"""
Script to examine the structure of the Excel file
"""
import pandas as pd
import numpy as np

def examine_excel_file(filename):
    """Examine the Excel file and print its structure"""
    try:
        # Read Excel file
        excel_file = pd.ExcelFile(filename)
        
        print(f"Excel file: {filename}")
        print(f"Sheet names: {excel_file.sheet_names}")
        print("=" * 50)
        
        # Examine each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"\nSheet: {sheet_name}")
            df = pd.read_excel(filename, sheet_name=sheet_name)
            
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print("\nFirst 5 rows:")
            print(df.head())
            print("\nData types:")
            print(df.dtypes)
            print("\nInfo:")
            print(df.info())
            print("=" * 50)
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")

def test_examine_excel():
    """Test function to examine the Excel file"""
    filename = "MMC - Monthly Financial Data.xlsx"
    examine_excel_file(filename)

if __name__ == "__main__":
    test_examine_excel() 