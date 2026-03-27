import sys
import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'
output_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\supabase_import.sql'

def clean_name(name):
    # Manual mapping for the specific garbage in this CSV
    mapping = {
        'Cï¾ƒæ³¥IGO PDV': 'codigo_pdv',
        'NOME PDV': 'nome_pdv',
        'RAZï¾ƒã‚° SOCIAL': 'razao_social',
        'STATUS': 'status',
        'ENDEREï¾ƒï¿½O': 'endereco',
        'BAIRRO': 'bairro',
        'CIDADE': 'cidade',
        'UF': 'uf',
        'CEP': 'cep',
        'RESPONSï¾ƒã€ƒEL': 'responsavel',
        'COORDENADA': 'coordenada_1',
        'PRECISï¾ƒã‚° NO SISTEMA': 'coordenada_2',
        'REDE': 'rede',
        'BANDEIRA': 'bandeira',
        'CANAL': 'canal',
        'REGIï¾ƒã‚°': 'regiao',
        'CLUSTER': 'cluster',
        'ROTA': 'rota',
        'GRUPO DE CLIENTES': 'grupo_clientes',
        'CERCA ELETRï¾ƒå¹´ICA': 'cerca_eletronica',
        'MIX': 'mix',
        'TIPO DE PDV': 'tipo_pdv',
        'NOME DO SHOPPING': 'nome_shopping'
    }
    
    name_upper = name.strip().upper()
    if name_upper in mapping:
        return mapping[name_upper]
        
    # Fallback normalization
    name = name_upper.replace('ï¾ƒæ³¥', 'O').replace('ï¾ƒã‚°', 'AO').replace('ï¾ƒï¿½', 'O').replace('ï¾ƒã€ƒ', 'VE').replace('ï¾ƒå¹´', 'ON')
    name = re.sub(r'[^A-Z0-9]', '_', name)
    return name.lower().strip('_')

try:
    with open(file_path, 'r', encoding='latin1') as f, open(output_path, 'w', encoding='utf-8') as out:
        header_raw = f.readline().strip()
        raw_headers = header_raw.split(';')
        
        headers = []
        for x in raw_headers:
            x = x.strip('" ')
            if not x: continue
            h = clean_name(x)
            headers.append(h)
            
        # Ensure unique headers
        seen = {}
        unique_headers = []
        for h in headers:
            if h in seen:
                seen[h] += 1
                unique_headers.append(f"{h}_{seen[h]}")
            else:
                seen[h] = 0
                unique_headers.append(h)
        
        headers = unique_headers

        out.write(f"-- Script de Importacao de Dados - Rota Disney\n")
        out.write(f"CREATE TABLE IF NOT EXISTS lojas_cinema (\n")
        out.write(f"  id BIGSERIAL PRIMARY KEY,\n")
        out.write(f"  created_at TIMESTAMPTZ DEFAULT NOW(),\n")
        for h in headers:
            out.write(f"  {h} TEXT,\n")
        out.write(f"  lat_clean NUMERIC,\n")
        out.write(f"  long_clean NUMERIC\n")
        out.write(f");\n\n")

        all_rows = []
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split(';')
            row = [p.strip('" ') for p in parts]
            row = row[:len(headers)]
            while len(row) < len(headers):
                row.append('')
            row = [r.replace("'", "''") for r in row]
            all_rows.append(row)

        chunk_size = 50
        cols_str = ", ".join(headers)
        for i in range(0, len(all_rows), chunk_size):
            chunk = all_rows[i:i+chunk_size]
            out.write(f"INSERT INTO lojas_cinema ({cols_str}) VALUES\n")
            vals_lines = []
            for r in chunk:
                vals = "', '".join(r)
                vals_lines.append(f"('{vals}')")
            out.write(",\n".join(vals_lines) + ";\n\n")
            
        print(f"Generated SQL for {len(all_rows)} rows with {len(headers)} columns.")

except Exception as e:
    print(f"Error: {e}")
