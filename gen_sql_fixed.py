import sys
import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'
output_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\supabase_import_fixed.sql'

def clean_coord(val):
    if not val: return ''
    # Remove all dots and add one after the first 2 or 3 digits
    # Or just keep it as text for now as requested? 
    # Let's keep it as text but clean the extra dots.
    # Actually, the user might want it as numeric later.
    return val.replace('"', '').strip()

try:
    with open(file_path, 'r', encoding='latin1') as f, open(output_path, 'w', encoding='utf-8') as out:
        # Define clean columns for the table
        columns = [
            'id_pdv', 'nome_pdv', 'razao_social', 'status', 'endereco', 'bairro', 'cidade', 'uf',
            'responsavel', 'coordenada_cnpj', 'latitude', 'longitude', 'precisao', 'rede', 'bandeira',
            'canal', 'regiao_desenho', 'cluster', 'rota', 'grupo_clientes', 'cerca_eletronica', 'mix',
            'tipo_pdv', 'nome_shopping'
        ]

        out.write(f"-- SCRIPT CORRIGIDO - Rota Disney\n")
        out.write(f"DROP TABLE IF EXISTS lojas_cinema;\n")
        out.write(f"CREATE TABLE lojas_cinema (\n")
        out.write(f"  id BIGSERIAL PRIMARY KEY,\n")
        out.write(f"  created_at TIMESTAMPTZ DEFAULT NOW(),\n")
        for col in columns:
            out.write(f"  {col} TEXT,\n")
        # Support for numeric lat/lng
        out.write(f"  lat_clean NUMERIC,\n")
        out.write(f"  lng_clean NUMERIC\n")
        out.write(f");\n\n")

        # Skip header
        f.readline()
        
        all_rows = []
        for line in f:
            line = line.strip()
            if not line: continue
            # Split and clean
            # Note: "A;B";"C;D" -> remove " then split by ;
            parts = line.replace('"', '').split(';')
            row_raw = [p.strip() for p in parts]
            
            # Mapping Logic (Handified)
            # data_index -> table_column
            # 0: id_pdv
            # 1: nome_pdv
            # 2: razao_social
            # 3: status
            # 4 & 5: endereco (Street + Number)
            # 6: bairro
            # 7: cidade
            # 8: uf
            # 9: responsavel
            # 10: coordenada_cnpj
            # 12: latitude
            # 13: longitude
            # 14: precisao
            # 15: rede
            # 16: bandeira
            # 17: canal
            # 18: regiao_desenho
            # 19: cluster
            # 20: rota
            # 21: grupo_clientes
            # 22: cerca_eletronica
            # 23: mix
            # 24: tipo_pdv
            # 25: nome_shopping
            
            def get(idx):
                return row_raw[idx].replace("'", "''") if idx < len(row_raw) else ''

            mapped = [
                get(0), # id_pdv
                get(1), # nome_pdv
                get(2), # razao_social
                get(3), # status
                get(4) + (" " + get(5) if get(5) else ""), # endereco
                get(6), # bairro
                get(7), # cidade
                get(8), # uf
                get(9), # responsavel
                get(10), # coordenada_cnpj (CNPJ Shifted)
                get(12), # latitude (Shifted into Rede in prev version)
                get(13), # longitude (Shifted into Bandeira in prev version)
                get(14), # precisao
                get(15), # rede
                get(16), # bandeira
                get(17), # canal
                get(18), # regiao_desenho
                get(19), # cluster
                get(20), # rota
                get(21), # grupo_clientes
                get(22), # cerca_eletronica
                get(23), # mix
                get(24), # tipo_pdv
                get(25)  # nome_shopping
            ]
            
            all_rows.append(mapped)

        chunk_size = 50
        cols_str = ", ".join(columns)
        for i in range(0, len(all_rows), chunk_size):
            chunk = all_rows[i:i+chunk_size]
            out.write(f"INSERT INTO lojas_cinema ({cols_str}) VALUES\n")
            vals_lines = []
            for r in chunk:
                vals = "', '".join(r)
                vals_lines.append(f"('{vals}')")
            out.write(",\n".join(vals_lines) + ";\n\n")
            
        print(f"Generated Corrected SQL for {len(all_rows)} rows.")

except Exception as e:
    print(f"Error: {e}")
