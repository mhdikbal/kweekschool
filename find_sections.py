import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('kweekschool_network_mapping.html','r',encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    s = l.strip()
    if 'id="nawawi"' in s or 'id="akses"' in s or ('divider' in s and 'section' not in s and 'css' not in s.lower()):
        print(f'{i+1}: {s}')
