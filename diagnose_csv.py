import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'
output_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\supabase_import_fixed.sql'

# ---------------------------------------------------------------
# O arquivo tem aspas duplas que agrupam colunas. Cada linha tem:
# "col1;col2;...;col10";"col11;col12;...;colN";
# A ";" entre os grupos de aspas é o delimitador REAL da linha.
# Precisamos: tirar as aspas externas e unir tudo em um único split.
# ---------------------------------------------------------------

# Nomes corretos das colunas (baseado no order original do header)
COLUMNS = [
    'codigo_pdv',      #  0
    'nome_pdv',        #  1
    'razao_social',    #  2
    'status',          #  3
    'endereco',        #  4
    'bairro',          #  5
    'cidade',          #  6
    'uf',              #  7
    'cep',             #  8
    'responsavel',     #  9
    'lat',             # 10  <- na planilha chamada COORDENADA (valor 1)
    'lng',             # 11  <- segundo valor de coordenada (estava vazio ou era precisão)
    'lat2',            # 12  <- -XX.XXX.XXX (latitude com ponto como milhar)
    'lng2',            # 13  <- longitude
    'precisao',        # 14
    'rede',            # 15
    'bandeira',        # 16
    'canal',           # 17
    'regiao',          # 18
    'cluster',         # 19
    'rota',            # 20
    'grupo_clientes',  # 21
    'cerca_eletronica',# 22
    'mix',             # 23
    'tipo_pdv',        # 24
    'nome_shopping',   # 25
]

def parse_line(raw_line):
    """Strip outer quotes and split by semicolon, then re-stitch segments."""
    # The line looks like: "A;B;C";"D;E;F"; or "A;B;C";"D;E;F"
    # We need to remove the wrapping quotes and join all semicolons together
    raw_line = raw_line.strip()
    # Remove CRLF
    raw_line = raw_line.rstrip('\r\n')
    
    # Strategy: remove all " characters, then split by ;
    # This works because the quotes are just wrappers, not escaping internal ;
    clean = raw_line.replace('"', '')
    parts = clean.split(';')
    return parts

def read_all():
    results = []
    with open(file_path, 'r', encoding='latin1') as f:
        lines = f.readlines()

    # Header
    header_raw = lines[0]
    raw_parts = parse_line(header_raw)
    # Filter empty
    headers_in_file = [p.strip() for p in raw_parts if p.strip()]

    print(f"Headers detected ({len(headers_in_file)}):")
    for i, h in enumerate(headers_in_file):
        print(f"  [{i:02d}] {h}")

    # Rows
    for line_num, line in enumerate(lines[1:], start=2):
        parts = parse_line(line)
        # Trim trailing empties
        while parts and not parts[-1].strip():
            parts.pop()
        if not any(p.strip() for p in parts):
            continue
        results.append((line_num, parts))

    return headers_in_file, results

def generate_sql(headers_in_file, data_rows):
    # We'll use the detected header positions to map to clean names
    # But we need to discover the real column count first
    max_cols = max(len(r) for _, r in data_rows)
    print(f"\nMax columns in data: {max_cols}")
    print(f"Header columns: {len(headers_in_file)}")
    
    # Show first few rows full content with index
    print("\n--- First row column-by-column ---")
    _, sample = data_rows[0]
    for i, v in enumerate(sample):
        header = headers_in_file[i] if i < len(headers_in_file) else f"extra_{i}"
        print(f"  [{i:02d}] {header!r:35s} = {v!r}")

    # Show 2nd row too
    print("\n--- Second row column-by-column ---")
    _, sample2 = data_rows[1]
    for i, v in enumerate(sample2):
        header = headers_in_file[i] if i < len(headers_in_file) else f"extra_{i}"
        print(f"  [{i:02d}] {header!r:35s} = {v!r}")

    return None

headers_in_file, data_rows = read_all()
generate_sql(headers_in_file, data_rows)
