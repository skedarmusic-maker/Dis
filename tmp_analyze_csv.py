import csv
import json

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'

# Clean naming
def clean_name(name):
    # Map common garbage characters
    replacements = {
        'Cï¾ƒæ³¥IGO': 'codigo',
        'RAZï¾ƒã‚°': 'razao',
        'ENDEREï¾ƒï¿½O': 'endereco',
        'RESPONSï¾ƒã€ƒEL': 'responsavel',
        'PRECISï¾ƒã‚°': 'precisao',
        'REGIï¾ƒã‚°': 'regiao',
        'ELETRï¾ƒå¹´ICA': 'eletronica',
        ' ': '_',
        '.': '',
        '-': '_',
        '/': '_',
        '(': '',
        ')': '',
        'ã€ƒ': '',
        'ï¿½': 'o', # Endereço
        'ï¾ƒæ³¥': 'o', # Código
        'ï¾ƒã‚°': 'ao', # Razão, Região
        'ï¾ƒã€ƒ': 've' # Responsável?
    }
    
    # Try common cleanup if encoding was bad
    name = name.strip().upper()
    for k, v in replacements.items():
        name = name.replace(k, v)
        
    # Standard slugify
    import re
    name = re.sub(r'[^a-zA-Z0-9_]', '', name.lower())
    return name or 'column'

try:
    with open(file_path, 'r', encoding='latin1') as f:
        # Read header
        header_line = f.readline().strip()
        # Clean header line from leading/trailing quotes
        header_line = header_line.strip('"')
        headers_raw = header_line.split(';')
        headers_clean = []
        counts = {}
        for h in headers_raw:
            if not h:
                continue
            hc = clean_name(h)
            if hc in counts:
                counts[hc] += 1
                hc = f"{hc}_{counts[hc]}"
            else:
                counts[hc] = 0
            headers_clean.append(hc)
            
        print(f"Headers identified: {len(headers_clean)}")
        print(headers_clean)

        # Let's see some data rows to calibrate column count
        rows = []
        for _ in range(5):
            line = f.readline()
            if not line: break
            # Each line seems to be like "part1";"part2"
            # We should probably join them or handle the semicolons correctly
            # Actually, csv.reader should handle it if correctly configured
            rows.append(line)
        
        print("\nDEBUG Row 1 raw:")
        print(rows[0])
        
        # Try split by semicolon but handle the quotes
        import csv
        import io
        
        f.seek(0)
        # Skip header
        f.readline()
        
        reader = csv.reader(f, delimiter=';', quotechar='"')
        processed_rows = []
        for i, row in enumerate(reader):
            if i >= 5: break
            # filter out trailing empties if they exceed header count
            # processed_rows.append(row)
            print(f"Row {i} has {len(row)} columns")
            if i == 0:
                print(row)

except Exception as e:
    print(f"Error: {e}")
