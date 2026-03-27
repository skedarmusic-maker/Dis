import sys
import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'
output_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\supabase_import.sql'

def clean_name(name):
    # Map common garbage characters
    name = str(name).strip().upper()
    # Manual cleanup for common Latin1 characters
    replacements = {
        'CÍDIGO': 'codigo',
        'RAZÃO': 'razao',
        'ENDEREÇO': 'endereco',
        'RESPONSÁVEL': 'responsavel',
        'PRECISÃO': 'precisao',
        'REGIÃO': 'regiao',
        'ELETRÔNICA': 'eletronica'
    }
    for k, v in replacements.items():
        name = name.replace(k, v)
    # Remove any non-alphanumeric except underscore
    name = re.sub(r'[^a-zA-Z0-9_]', '', name.lower())
    return name or 'column'

try:
    with open(file_path, 'r', encoding='latin1') as f, open(output_path, 'w', encoding='utf-8') as out:
        # Read header
        header_raw = f.readline().strip()
        # Clean header
        raw_headers = header_raw.split(';')
        headers = []
        counts = {}
        
        # Explicitly map known headers to avoid garbage
        known_headers = [
            'codigo_pdv', 'nome_pdv', 'razao_social', 'status', 'endereco', 'bairro', 'cidade', 'uf', 'cep', 
            'responsavel', 'coordenada_1', 'coordenada_2', 'lat', 'long', 'precisao_no_sistema',
            'rede', 'bandeira', 'canal', 'regiao', 'cluster', 'rota', 'grupo_de_clientes', 'cerca_eletronica', 'mix', 'tipo_de_pdv', 'nome_do_shopping'
        ]
        
        # Actually use identified headers but sanitized
        headers = []
        for x in raw_headers:
            x = x.strip('" ')
            if not x: continue
            h = clean_name(x)
            headers.append(h)
            
        print(f"Sanitized headers: {headers}")

        out.write(f"-- SQL script to import CSV data into Supabase\n")
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
            # Split and cleanup
            # The format is tricky: "A;B";"C;D"
            # We'll just split by ; and clean quotes
            parts = line.split(';')
            row = [p.strip('" ') for p in parts]
            
            # Pad/trim
            row = row[:len(headers)]
            while len(row) < len(headers):
                row.append('')
            
            # Escape single quotes
            row = [r.replace("'", "''") for r in row]
            all_rows.append(row)

        # Batch inserts
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
            
        print(f"Generated SQL for {len(all_rows)} rows.")

except Exception as e:
    print(f"Error: {e}")
