import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('kweekschool_v3_final.html', 'r', encoding='utf-8') as f:
    c = f.read()

checks = {
    'nawawi-bg class removed': 'nawawi-bg' not in c.split('</style>')[0].split('/* NAWAWI PHOTO OVERLAY */')[1] if '/* NAWAWI PHOTO OVERLAY */' in c else True,
    'photo overlay CSS': '#nawawi .section-header::after' in c,
    'timeline scroll CSS': 'timeline-puncak-scroll' in c,
    'drag hint': 'drag-hint' in c,
    'Cultuurstelsel paragraph': 'Cultuurstelsel' in c,
    'stat 86.7%': '86,7' in c,
    'stat 421': '421' in c,
}

for k, v in checks.items():
    print(f"{'OK' if v else 'FAIL'}: {k}")
