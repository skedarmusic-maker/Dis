import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'

try:
    with open(file_path, 'r', encoding='latin1') as f:
        l1 = f.readline().replace('"', '').strip().split(';')
        l2 = f.readline().replace('"', '').strip().split(';')
        
        print("COL_IDX | HEADER_VAL | DATA_VAL")
        print("-" * 50)
        for i in range(max(len(l1), len(l2))):
            h = l1[i] if i < len(l1) else "N/A"
            d = l2[i] if i < len(l2) else "N/A"
            print(f"{i:7} | {h[:20]:20} | {d[:20]:20}")

except Exception as e:
    print(f"Error: {e}")
