import pandas as pd
import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\BASE END.xlsx'
output_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\supabase_import_consultores.sql'

def fix_coord(c):
    if pd.isna(c): return 'NULL'
    cleaned = re.sub(r'[^\d-]', '', str(c))
    if not cleaned or cleaned == '-': return 'NULL'
    
    # Se for um número gigante negativo (ex: -23641848193651500)
    # Queremos transformá-lo em algo com 2 dígitos antes do ponto (para Brasil)
    # Lat Brasil: -3 a -33 | Lng Brasil: -34 a -73
    
    val = cleaned
    if val.startswith('-'):
        # Ex: -23641848 -> -23.641848
        if len(val) > 3:
            return f"{val[:3]}.{val[3:]}"
    else:
        if len(val) > 2:
            return f"{val[:2]}.{val[2:]}"
    return val

try:
    df = pd.read_excel(file_path)
    # Filtra linhas onde o nome seja nulo
    df = df[df['NAME'].notna()]
    
    rows = []
    for index, row in df.iterrows():
        name = str(row['NAME']).replace("'", "''")
        address = str(row.get('ENDEREÇO RESIDENCIAL', '')).replace("'", "''")
        lat_raw = str(row.get('LATITUDE', ''))
        lng_raw = str(row.get('LONGITUDE', ''))
        
        lat_clean = fix_coord(lat_raw)
        lng_clean = fix_coord(lng_raw)
        
        rows.append(f"('{name}', '{address}', {lat_clean}, {lng_clean})")

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("-- Importação de Consultores\n")
        out.write("DROP TABLE IF EXISTS consultores;\n")
        out.write("CREATE TABLE consultores (\n")
        out.write("  id BIGSERIAL PRIMARY KEY,\n")
        out.write("  nome TEXT,\n")
        out.write("  endereco TEXT,\n")
        out.write("  latitude NUMERIC,\n")
        out.write("  longitude NUMERIC,\n")
        out.write("  created_at TIMESTAMPTZ DEFAULT NOW()\n")
        out.write(");\n\n")
        
        if rows:
            out.write("INSERT INTO consultores (nome, endereco, latitude, longitude) VALUES\n")
            out.write(",\n".join(rows) + ";\n")
            
    print(f"Generated SQL for {len(rows)} consultants.")

except Exception as e:
    print(f"Error: {e}")
