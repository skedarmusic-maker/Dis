import pandas as pd
file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\BASE END.xlsx'

try:
    df = pd.read_excel(file_path)
    print("Columns in BASE END.xlsx:")
    print(df.columns.tolist())
    print("\nFirst row sample:")
    print(df.iloc[0].to_dict())
    
except Exception as e:
    print(f"Error: {e}")
