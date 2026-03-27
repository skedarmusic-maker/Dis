import pandas as pd
file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\BASE END.xlsx'

df = pd.read_excel(file_path)
print(df.head(10).to_string())
