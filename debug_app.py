#!/usr/bin/env python3
"""Test script to verify CSV reading"""

import pandas as pd

def test_csv_reading():
    """Test reading the emails.csv file"""
    
    print("=== READING emails.csv ===")
    
    try:
        # Read the CSV file
        df = pd.read_csv('emails.csv')
        
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print()
        
        print("=== FIRST 3 ROWS (raw) ===")
        print(df.head(3))
        print()
        
        print("=== FIRST ROW AS DICT ===")
        first_row = df.iloc[0].to_dict()
        for key, value in first_row.items():
            print(f"{key}: '{value}'")
        print()
        
        print("=== CHECKING DATA TYPES ===")
        print(df.dtypes)
        print()
        
        # Test converting to records (like your Flask app does)
        records = df.head(3).to_dict('records')
        print("=== FIRST RECORD AS USED BY FLASK ===")
        if records:
            first_record = records[0]
            print(f"ID: {first_record['id']} (should be 1)")
            print(f"Sender: {first_record['sender']} (should be john.doe@example.com)")
            print(f"Subject: {first_record['subject']} (should be Meeting Schedule)")
            print(f"Body: {first_record['body'][:50]}... (should start with 'Hi team')")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_csv_reading()