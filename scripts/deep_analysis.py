#!/usr/bin/env python3
"""
Deep analysis of delpher_larashoofd_processed_data.xls
Mapping affiliations between traditional leaders and education system
in Sumatra's Westkust (colonial era)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import openpyxl
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl', 'xlrd'])
    import openpyxl

import re
from collections import Counter, defaultdict

FILE = 'delpher_larashoofd_processed_data.xls'

# Try xlrd for .xls format
try:
    import xlrd
    wb = xlrd.open_workbook(FILE)
    ws = wb.sheet_by_index(0)
    headers = [ws.cell_value(0, c) for c in range(ws.ncols)]
    rows = []
    for r in range(1, ws.nrows):
        row = {}
        for c in range(ws.ncols):
            row[headers[c]] = str(ws.cell_value(r, c)).strip()
        rows.append(row)
    print(f"Loaded {len(rows)} rows via xlrd")
    print(f"Headers: {headers}")
except Exception as e:
    print(f"xlrd failed: {e}, trying openpyxl")
    wb = openpyxl.load_workbook(FILE)
    ws = wb.active
    headers = [str(c.value).strip() for c in list(ws.rows)[0]]
    rows = []
    for row in list(ws.rows)[1:]:
        r = {}
        for i, cell in enumerate(row):
            r[headers[i]] = str(cell.value).strip() if cell.value else ''
        rows.append(r)
    print(f"Loaded {len(rows)} rows via openpyxl")
    print(f"Headers: {headers}")

print(f"\n{'='*70}")
print(f"ANALISIS MENDALAM: AFILIASI PEJABAT PRIBUMI & PENDIDIKAN")
print(f"{'='*70}")

# Combine all text columns for analysis
def get_full_text(row):
    return ' '.join(row.values()).lower()

# ═══════════════════════════════════════════════════════════
# 1. KATEGORI PEJABAT PRIBUMI
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("1. IDENTIFIKASI PEJABAT PRIBUMI")
print(f"{'─'*70}")

categories = {
    'larashoofd': ['larashoofd', 'laras hoofd', 'laras-hoofd', 'hoofd van de laras'],
    'datuk/datoe': ['datoe', 'datuk', 'datoek', 'dato'],
    'angku_kepala': ['angkoe', 'angku', 'ankou', 'angko', 'kepala'],
    'penghulu': ['penghulu', 'penghoeloe', 'panghoeloe', 'panghulu', 'panghoelo'],
    'mantri': ['mantri', 'mandoer'],
    'toekoe/tuanku': ['toekoe', 'tuanku', 'toeankoe'],
    'regen/kepala_negeri': ['regent', 'kepala negeri', 'hoofd van'],
}

cat_counts = {}
cat_rows = {}
for cat, keywords in categories.items():
    matched = []
    for i, row in enumerate(rows):
        text = get_full_text(row)
        if any(kw in text for kw in keywords):
            matched.append(i)
    cat_counts[cat] = len(matched)
    cat_rows[cat] = set(matched)
    print(f"  {cat:25s}: {len(matched):5d} entri")

# Unique pribumi officials (union)
all_pribumi = set()
for s in cat_rows.values():
    all_pribumi |= s
print(f"\n  {'TOTAL UNIK pejabat pribumi':25s}: {len(all_pribumi):5d} entri")

# ═══════════════════════════════════════════════════════════
# 2. KATEGORI PENDIDIKAN
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("2. IDENTIFIKASI ENTRI PENDIDIKAN")
print(f"{'─'*70}")

edu_categories = {
    'school/sekolah': ['school', 'scholieren', 'schoolcommissie', 'schoolbestuur'],
    'kweekschool': ['kweekschool', 'kweekeling'],
    'onderwijzer/guru': ['onderwijzer', 'onderwijzers', 'hulponderwijzer', 'onderwijzeressen'],
    'onderwijs/pendidikan': ['onderwijs', 'inlandsch onderwijs', 'schoolonderwijs'],
    'lezen_schrijven': ['lezen', 'schrijven', 'rekenen', 'leer', 'leeren'],
    'examen/ujian': ['examen', 'examin', 'onderzoek'],
    'benoemd/diangkat': ['benoemd', 'benoeming', 'aangesteld', 'werkzaamgesteld'],
}

edu_counts = {}
edu_rows = {}
for cat, keywords in edu_categories.items():
    matched = []
    for i, row in enumerate(rows):
        text = get_full_text(row)
        if any(kw in text for kw in keywords):
            matched.append(i)
    edu_counts[cat] = len(matched)
    edu_rows[cat] = set(matched)
    print(f"  {cat:25s}: {len(matched):5d} entri")

all_edu = set()
for s in edu_rows.values():
    all_edu |= s
print(f"\n  {'TOTAL UNIK entri pendidikan':25s}: {len(all_edu):5d} entri")

# ═══════════════════════════════════════════════════════════
# 3. AFILIASI: PEJABAT PRIBUMI × PENDIDIKAN
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("3. AFILIASI: PEJABAT PRIBUMI + PENDIDIKAN")
print(f"{'─'*70}")

# Cross-tabulation
print(f"\n  {'Pejabat':25s} × {'Pendidikan':25s} = Afiliasi")
print(f"  {'─'*65}")

affiliation_matrix = {}
for pcat, prows in cat_rows.items():
    affiliation_matrix[pcat] = {}
    for ecat, erows in edu_rows.items():
        overlap = prows & erows
        affiliation_matrix[pcat][ecat] = len(overlap)

# Print matrix
for pcat in categories:
    total_aff = len(cat_rows[pcat] & all_edu)
    pct = (total_aff / len(cat_rows[pcat]) * 100) if len(cat_rows[pcat]) > 0 else 0
    print(f"  {pcat:25s}: {total_aff:5d} terafiliasi pendidikan ({pct:.1f}%)")
    for ecat in edu_categories:
        v = affiliation_matrix[pcat].get(ecat, 0)
        if v > 0:
            print(f"    ├─ {ecat:23s}: {v:4d}")

# Total unique affiliation
total_affiliated = all_pribumi & all_edu
print(f"\n  ┌─────────────────────────────────────────────────┐")
print(f"  │ TOTAL: {len(total_affiliated)} pejabat pribumi terafiliasi pendidikan │")
print(f"  │ dari {len(all_pribumi)} total pejabat ({len(total_affiliated)/len(all_pribumi)*100:.1f}%)             │")
print(f"  └─────────────────────────────────────────────────┘")

# ═══════════════════════════════════════════════════════════
# 4. DETAIL PER KATEGORI AFILIASI
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("4. DETAIL AFILIASI PER KATEGORI") 
print(f"{'─'*70}")

# Larashoofd + school/onderwijs
larashoofd_edu = cat_rows['larashoofd'] & all_edu
print(f"\n  LARASHOOFD + Pendidikan: {len(larashoofd_edu)} entri")
for ecat in edu_categories:
    v = len(cat_rows['larashoofd'] & edu_rows[ecat])
    if v > 0:
        print(f"    → + {ecat}: {v}")

# Datuk + education
datuk_edu = cat_rows['datuk/datoe'] & all_edu
print(f"\n  DATUK/DATOE + Pendidikan: {len(datuk_edu)} entri")
for ecat in edu_categories:
    v = len(cat_rows['datuk/datoe'] & edu_rows[ecat])
    if v > 0:
        print(f"    → + {ecat}: {v}")

# Penghulu + education
penghulu_edu = cat_rows['penghulu'] & all_edu
print(f"\n  PENGHULU + Pendidikan: {len(penghulu_edu)} entri")
for ecat in edu_categories:
    v = len(cat_rows['penghulu'] & edu_rows[ecat])
    if v > 0:
        print(f"    → + {ecat}: {v}")

# Angku + education  
angku_edu = cat_rows['angku_kepala'] & all_edu
print(f"\n  ANGKU/KEPALA + Pendidikan: {len(angku_edu)} entri")
for ecat in edu_categories:
    v = len(cat_rows['angku_kepala'] & edu_rows[ecat])
    if v > 0:
        print(f"    → + {ecat}: {v}")

# Mantri + education
mantri_edu = cat_rows['mantri'] & all_edu
print(f"\n  MANTRI + Pendidikan: {len(mantri_edu)} entri")
for ecat in edu_categories:
    v = len(cat_rows['mantri'] & edu_rows[ecat])
    if v > 0:
        print(f"    → + {ecat}: {v}")


# ═══════════════════════════════════════════════════════════
# 5. PEJABAT YANG MENJADI GURU (onderwijzer)
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("5. PEJABAT PRIBUMI YANG TERAFILIASI SEBAGAI GURU")
print(f"{'─'*70}")

guru_rows = edu_rows.get('onderwijzer/guru', set()) | edu_rows.get('benoemd/diangkat', set())
for pcat in categories:
    overlap = cat_rows[pcat] & guru_rows
    if len(overlap) > 0:
        print(f"  {pcat:25s}: {len(overlap)} entri terafiliasi guru/pengangkatan")


# ═══════════════════════════════════════════════════════════
# 6. SCHOOLCOMMISSIE (komisi sekolah)
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("6. PEJABAT PRIBUMI DI SCHOOLCOMMISSIE")
print(f"{'─'*70}")

schoolcommissie_rows = set()
for i, row in enumerate(rows):
    text = get_full_text(row)
    if 'schoolcommissie' in text or 'schoolbestuur' in text or 'school commissie' in text:
        schoolcommissie_rows.add(i)

print(f"  Total entri schoolcommissie: {len(schoolcommissie_rows)}")
for pcat in categories:
    overlap = cat_rows[pcat] & schoolcommissie_rows
    if len(overlap) > 0:
        print(f"  {pcat:25s}: {len(overlap)} di schoolcommissie")

# ═══════════════════════════════════════════════════════════
# 7. LOKASI GEOGRAFIS
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("7. DISTRIBUSI GEOGRAFIS")
print(f"{'─'*70}")

locations = {
    'Fort de Kock': ['fort de kock', 'fortdekock', 'bukittinggi'],
    'Fort v/d Capellen': ['capellen', 'batusangkar', 'batoe sangkar'],
    'Padang': ['padang'],
    'Payakumbuh': ['payakumbuh', 'pajakoemboeh', 'paja koemboeh'],
    'Agam': ['agam', 'iv kotta', 'iv kota'],
    'Solok': ['solok'],
    'Tanah Datar': ['tanah datar'],
    'L. Kota': ['l. kota', 'lima puluh', '50 kota', 'limapuluh'],
}

for loc, kws in locations.items():
    loc_rows = set()
    for i, row in enumerate(rows):
        text = get_full_text(row)
        if any(kw in text for kw in kws):
            loc_rows.add(i)
    affiliated = loc_rows & total_affiliated
    if len(loc_rows) > 0:
        print(f"  {loc:25s}: {len(loc_rows):4d} total | {len(affiliated):4d} terafiliasi pendidikan ({len(affiliated)/len(loc_rows)*100:.0f}%)")


# ═══════════════════════════════════════════════════════════
# 8. SAMPLE ENTRIES
# ═══════════════════════════════════════════════════════════
print(f"\n{'─'*70}")
print("8. CONTOH ENTRI AFILIASI (10 pertama)")
print(f"{'─'*70}")

sample = list(total_affiliated)[:10]
for idx in sample:
    row = rows[idx]
    text = ' | '.join([f"{k}: {v[:60]}" for k,v in row.items() if v and v != 'None'])
    print(f"\n  [{idx}] {text[:200]}")


# ═══════════════════════════════════════════════════════════
# RINGKASAN FINAL
# ═══════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("RINGKASAN FINAL")
print(f"{'='*70}")
print(f"""
  Total dokumen dianalisis     : {len(rows)}
  Total entri pejabat pribumi  : {len(all_pribumi)} ({len(all_pribumi)/len(rows)*100:.1f}%)
  Total entri pendidikan       : {len(all_edu)} ({len(all_edu)/len(rows)*100:.1f}%)
  AFILIASI pribumi+pendidikan  : {len(total_affiliated)} ({len(total_affiliated)/len(all_pribumi)*100:.1f}% dari pejabat)
  
  Detail afiliasi:
    Larashoofd + pendidikan    : {len(larashoofd_edu)}
    Datuk/Datoe + pendidikan   : {len(datuk_edu)}
    Penghulu + pendidikan      : {len(penghulu_edu)}
    Angku/Kepala + pendidikan  : {len(angku_edu)}
    Mantri + pendidikan        : {len(mantri_edu)}
    
  Pejabat di Schoolcommissie  : {len(all_pribumi & schoolcommissie_rows)}
""")
