import pandas as pd
file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP (1) 2.xlsx'

df = pd.read_excel(file_path)
raw_line = ";".join([str(x) for x in df.iloc[0].values if not pd.isna(x)])
parts = raw_line.replace('"', '').split(';')
for i, p in enumerate(parts):
    print(f"{i}: {p}")
