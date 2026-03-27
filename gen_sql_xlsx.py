import pandas as pd
import sys

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP (1) 2.xlsx'
output_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\supabase_import_fixed_new.sql'

def clean_val(v):
    if pd.isna(v): return ''
    return str(v).replace("'", "''").strip()

def fix_coord(c):
    # Remove dots and everything not numeric/minus
    import re
    cleaned = re.sub(r'[^\d-]', '', str(c))
    if not cleaned or cleaned == '-': return 'NULL'
    # Insert dot after 2 digits (e.g., -233433997 -> -23.3433997)
    if cleaned.startswith('-'):
        if len(cleaned) > 3:
            return f"{cleaned[:3]}.{cleaned[3:]}"
    else:
        if len(cleaned) > 2:
            return f"{cleaned[:2]}.{cleaned[2:]}"
    return cleaned

try:
    df = pd.read_excel(file_path)
    all_rows = []
    
    table_columns = [
        'id_pdv', 'nome_pdv', 'razao_social', 'status', 'endereco', 'bairro', 'cidade', 'uf',
        'responsavel', 'coordenada_cnpj', 'latitude', 'longitude', 'precisao', 'rede', 'bandeira',
        'canal', 'regiao_desenho', 'cluster', 'rota', 'grupo_clientes', 'cerca_eletronica', 'mix',
        'tipo_pdv', 'nome_shopping', 'lat_clean', 'lng_clean'
    ]

    for index, row in df.iterrows():
        # Captura todos os valores da linha em uma lista limpa
        raw_line = ";".join([str(x) for x in row.values if not pd.isna(x)])
        parts = [p.strip() for p in raw_line.replace('"', '').split(';')]
        
        # Padrão básico (fallback)
        res = {col: '' for col in table_columns}
        res['lat_clean'] = 'NULL'
        res['lng_clean'] = 'NULL'

        # SMART MAPPING: Encontrar a âncora "COORDENADA"
        pos_prec = -1
        for i, p in enumerate(parts):
            if "COORDENADA" in p.upper():
                pos_prec = i
                break
        
        if pos_prec != -1:
            # Temos a âncora! Mapeamos de trás para frente a partir dela
            res['precisao'] = parts[pos_prec]
            res['longitude'] = parts[pos_prec-1] if pos_prec > 0 else ''
            res['latitude'] = parts[pos_prec-2] if pos_prec > 1 else ''
            res['responsavel'] = parts[pos_prec-3] if pos_prec > 2 else ''
            res['coordenada_cnpj'] = parts[pos_prec-4] if pos_prec > 3 else ''
            res['uf'] = parts[pos_prec-5] if pos_prec > 4 else ''
            res['cidade'] = parts[pos_prec-6] if pos_prec > 5 else ''
            
            # Tudo entre o Status (index 3) e Cidade (pos_prec-6) é Endereço/Bairro
            # Vamos tentar ser mais precisos:
            res['id_pdv'] = parts[0] if len(parts) > 0 else ''
            res['nome_pdv'] = parts[1] if len(parts) > 1 else ''
            res['razao_social'] = parts[2] if len(parts) > 2 else ''
            res['status'] = parts[3] if len(parts) > 3 else ''
            
            # O que sobrar no meio vira endereço
            endereco_parts = parts[4:pos_prec-6]
            res['endereco'] = " ".join(endereco_parts)
            
            # Mapeamento para frente da âncora
            res['rede'] = parts[pos_prec+1] if len(parts) > pos_prec+1 else ''
            res['bandeira'] = parts[pos_prec+2] if len(parts) > pos_prec+2 else ''
            res['canal'] = parts[pos_prec+3] if len(parts) > pos_prec+3 else ''
            res['regiao_desenho'] = parts[pos_prec+4] if len(parts) > pos_prec+4 else ''
            res['cluster'] = parts[pos_prec+5] if len(parts) > pos_prec+5 else ''
            res['rota'] = parts[pos_prec+6] if len(parts) > pos_prec+6 else ''
            res['grupo_clientes'] = parts[pos_prec+7] if len(parts) > pos_prec+7 else ''
            res['cerca_eletronica'] = parts[pos_prec+8] if len(parts) > pos_prec+8 else ''
            res['mix'] = parts[pos_prec+9] if len(parts) > pos_prec+9 else ''
            res['tipo_pdv'] = parts[pos_prec+10] if len(parts) > pos_prec+10 else ''
            res['nome_shopping'] = parts[pos_prec+11] if len(parts) > pos_prec+11 else ''

            # Limpeza automática para o banco
            res['lat_clean'] = fix_coord(res['latitude'])
            res['lng_clean'] = fix_coord(res['longitude'])
        
        # Escapar aspas simples para o SQL
        final_row = [str(res[col]).replace("'", "''") for col in table_columns]
        all_rows.append(final_row)

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"-- SMART SCRIPT - Corrigido para shifts e limpeza automática\n")
        out.write(f"DROP TABLE IF EXISTS lojas_cinema;\n")
        out.write(f"CREATE TABLE lojas_cinema (\n")
        out.write(f"  id BIGSERIAL PRIMARY KEY,\n")
        out.write(f"  created_at TIMESTAMPTZ DEFAULT NOW(),\n")
        for col in table_columns[:-2]: # TEXT columns
            out.write(f"  {col} TEXT,\n")
        out.write(f"  lat_clean NUMERIC,\n")
        out.write(f"  lng_clean NUMERIC\n")
        out.write(f");\n\n")

        chunk_size = 50
        cols_str = ", ".join(table_columns)
        for i in range(0, len(all_rows), chunk_size):
            chunk = all_rows[i:i+chunk_size]
            out.write(f"INSERT INTO lojas_cinema ({cols_str}) VALUES\n")
            vals_lines = []
            for r in chunk:
                # Tratar NULLs numéricos sem aspas
                lat = r[-2]
                lng = r[-1]
                v_text = "', '".join(r[:-2])
                vals_lines.append(f"('{v_text}', {lat}, {lng})")
            out.write(",\n".join(vals_lines) + ";\n\n")
            
    print(f"Generated Smart Corrected SQL for {len(all_rows)} rows.")

except Exception as e:
    print(f"Error: {e}")
