import pandas as pd
import sys

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP (1) 2.xlsx'

try:
    df = pd.read_excel(file_path)
    print("Columns found in XLSX:")
    print(df.columns.tolist())
    print("\nFirst row sample:")
    print(df.iloc[0].to_dict())
    
except Exception as e:
    print(f"Error reading XLSX: {e}")
    print("Trying to suggest alternative...")
