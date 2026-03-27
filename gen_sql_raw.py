import sys
import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'
output_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\supabase_import_raw.sql'

try:
    with open(file_path, 'r', encoding='latin1') as f, open(output_path, 'w', encoding='utf-8') as out:
        # We'll just read everything and split by semicolon.
        # We'll create columns col0, col1, etc.
        max_cols = 35 # Observed max seems around 30
        
        out.write(f"CREATE TABLE IF NOT EXISTS lojas_cinema_raw (\n")
        out.write(f"  id BIGSERIAL PRIMARY KEY,\n")
        out.write(f"  created_at TIMESTAMPTZ DEFAULT NOW(),\n")
        for i in range(max_cols):
            out.write(f"  col{i} TEXT,\n")
        out.write(f"  source_line INTEGER\n")
        out.write(f");\n\n")

        # Skip header
        header = f.readline()
        
        all_rows = []
        line_num = 2
        for line in f:
            line = line.strip()
            if not line: continue
            # Format: "A;B";"C;D"
            # Rule: split by ; and remove "
            parts = line.replace('"', '').split(';')
            row = [p.strip() for p in parts]
            
            # Pad/trim
            row = row[:max_cols]
            while len(row) < max_cols:
                row.append('')
            
            # Escape single quotes
            row = [r.replace("'", "''") for r in row]
            row.append(str(line_num))
            all_rows.append(row)
            line_num += 1

        chunk_size = 50
        cols_str = ", ".join([f"col{i}" for i in range(max_cols)]) + ", source_line"
        for i in range(0, len(all_rows), chunk_size):
            chunk = all_rows[i:i+chunk_size]
            out.write(f"INSERT INTO lojas_cinema_raw ({cols_str}) VALUES\n")
            vals_lines = []
            for r in chunk:
                vals = "', '".join(r)
                vals_lines.append(f"('{vals}')")
            out.write(",\n".join(vals_lines) + ";\n\n")
            
        print(f"Generated Raw SQL for {len(all_rows)} rows.")

except Exception as e:
    print(f"Error: {e}")
