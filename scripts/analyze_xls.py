import sys
sys.stdout.reconfigure(encoding='utf-8')
import xlrd

wb = xlrd.open_workbook('delpher_larashoofd_processed_data.xls')
ws = wb.sheet_by_index(0)
print(f'Total rows: {ws.nrows}')

datuk_count = 0
guru_count = 0
school_count = 0
larashoofd_school = 0

for r in range(1, ws.nrows):
    ft = ws.cell_value(r, 14) if ws.ncols > 14 else ''
    title = ws.cell_value(r, 2)
    combined = (ft + ' ' + title).lower()
    
    if 'datoe' in combined or 'datuk' in combined or 'datoek' in combined:
        datuk_count += 1
    if 'onderwijzer' in combined or 'guru' in combined:
        guru_count += 1
    if 'school' in combined:
        school_count += 1
    if 'larashoofd' in combined and 'school' in combined:
        larashoofd_school += 1

print(f'Datoe/Datuk/Datoek mentions: {datuk_count}')
print(f'Onderwijzer/Guru mentions: {guru_count}')
print(f'School mentions: {school_count}')
print(f'Larashoofd + School co-mentions: {larashoofd_school}')

# Sample some records that show datuk-who-became-teacher pattern
print('\n--- SAMPLES: Datuk/Larashoofd connected to education ---')
count = 0
for r in range(1, ws.nrows):
    ft = ws.cell_value(r, 14) if ws.ncols > 14 else ''
    title = ws.cell_value(r, 2)
    combined = (ft + ' ' + title).lower()
    
    if ('datoe' in combined or 'larashoofd' in combined) and ('school' in combined or 'onderwijzer' in combined):
        if count < 10:
            print(f'[Row {r}] Title: {title[:120]}')
            print(f'  Full text snippet: {ft[:200]}')
            print()
            count += 1
