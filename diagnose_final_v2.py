import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'

try:
    with open(file_path, 'r', encoding='latin1') as f:
        l1 = f.readline().replace('"', '').strip().split(';')
        l2 = f.readline().replace('"', '').strip().split(';')
        
        print(f"{'IDX':<5} | {'HEADER':<30} | {'DATA'}")
        print("-" * 80)
        for i in range(max(len(l1), len(l2))):
            h = l1[i] if i < len(l1) else "N/A"
            d = l2[i] if i < len(l2) else "N/A"
            print(f"{i:<5} | {h:<30} | {d}")

except Exception as e:
    print(f"Error: {e}")
