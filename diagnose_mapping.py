import re

file_path = r'c:\Users\Gabriel Amorim\Desktop\APPS ANTIGRAVITY\Rota Disney\public\Disney Cinemas- CONSULTOR 04 - SP base 1csv.csv'

def parse_line(raw_line):
    # Remove outer quotes and split by ;
    # The file has a weird format: "A;B";"C;D"
    # We'll split by ";" and clean up
    line = raw_line.replace('"', '').strip()
    return line.split(';')

try:
    with open(file_path, 'r', encoding='latin1') as f:
        lines = f.readlines()
        
        # Header (Row 1)
        headers = parse_line(lines[0])
        # Filter empty headers at the end
        headers = [h for h in headers if h]
        
        print(f"HEADER ({len(headers)} columns):")
        for i, h in enumerate(headers):
            print(f"  {i}: {h}")

        # Data Row (Row 2) - Example
        data = parse_line(lines[1])
        print(f"\nDATA ROW 1 ({len(data)} columns):")
        for i, d in enumerate(data):
            corr_h = headers[i] if i < len(headers) else "EXTRA"
            print(f"  {i}: {d} (mapped to {corr_h})")

        # Data Row (Row 3) - Example
        data2 = parse_line(lines[2])
        print(f"\nDATA ROW 2 ({len(data2)} columns):")
        for i, d in enumerate(data2):
            corr_h = headers[i] if i < len(headers) else "EXTRA"
            print(f"  {i}: {d} (mapped to {corr_h})")

except Exception as e:
    print(f"Error: {e}")
