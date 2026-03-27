import pandas as pd
file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP (1) 2.xlsx'

df = pd.read_excel(file_path)
print("Analisando linhas com erro de conversão...")

for index, row in df.iterrows():
    raw_line = ";".join([str(x) for x in row.values if not pd.isna(x)])
    parts = raw_line.replace('"', '').split(';')
    
    # Se encontrarmos "COORDENADA EXATA" na posição errada, printamos a linha
    if "COORDENADA EXATA" in parts:
        pos = parts.index("COORDENADA EXATA")
        # Nas linhas normais, debería estar na 13. Se estiver em 11 ou 12, as coordenadas foram puxadas.
        if pos < 13:
            print(f"Linha {index+1}: 'COORDENADA EXATA' na posição {pos}. Total partes: {len(parts)}")
            print(f"Dados: {parts}\n")
    if index > 100: break # Olhar apenas os primeiros 100 por enquanto
