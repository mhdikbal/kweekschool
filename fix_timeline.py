import sys

with open('kweekschool_v3_final.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Close the first main properly IF it wasn't closed before, wait, 
# earlier we found: 753: </main><!-- end main -->
# So <main> at the top is closed at 753.
# The network section 755-906 is outside <main>.
# We want <section id="kesimpulan"> to be inside a <main>.
# Right before <!-- KESIMPULAN --> at line 909, we should insert <main>
c = c.replace('<!-- KESIMPULAN -->\n<section id="kesimpulan"', '<main>\n<!-- KESIMPULAN -->\n<section id="kesimpulan"')

# There is a <main> at line 1195. Let's remove it so Kesimpulan and Sumber are in the same <main>.
# Line 1195: <main> right after <!-- SOURCES -->.
c = c.replace('<!-- SOURCES -->\n<main>\n<section id="sumber"', '<!-- SOURCES -->\n<section id="sumber"')

# Now fix the timeline. 
# Gradient line replacement:
old_gradient = 'background:linear-gradient(to right,var(--teal) 0%,var(--teal) 13%,var(--amber) 13%,var(--amber) 37%,var(--rust) 37%,var(--rust) 60%,var(--rust2) 60%,var(--rust2) 80%,#E24B4A 80%,#E24B4A 100%)'
new_gradient = 'background:linear-gradient(to right,var(--teal) 0%,var(--teal) 15%,var(--amber) 15%,var(--amber) 32%,var(--rust) 32%,var(--rust) 56%,var(--rust2) 56%,var(--rust2) 76%,#E24B4A 76%,#E24B4A 100%)'
c = c.replace(old_gradient, new_gradient)

# Era labels replacement:
old_labels = """        <!-- 1856-1860 Perintisan -->
        <div style="position:absolute;left:0;top:-68px;width:13%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--teal);margin-bottom:3px">Perintisan</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--teal);opacity:.7">1856–1860</div>
        </div>

        <!-- 1860-1873 Kemunduran -->
        <div style="position:absolute;left:13%;top:-68px;width:24%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--amber);margin-bottom:3px">Kemunduran</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--amber);opacity:.7">1860–1873</div>
        </div>

        <!-- 1874-1888 Kebangkitan -->
        <div style="position:absolute;left:37%;top:-68px;width:23%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--rust);margin-bottom:3px">Kebangkitan</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--rust);opacity:.7">1874–1888</div>
        </div>

        <!-- 1890-1907 Nawawi -->
        <div style="position:absolute;left:60%;top:-68px;width:20%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--rust2);margin-bottom:3px">Nawawi</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--rust2);opacity:.7">1890–1907</div>
        </div>

        <!-- 1908-1915 Pergerakan -->
        <div style="position:absolute;left:80%;top:-68px;width:20%;text-align:center">"""

new_labels = """        <!-- 1856-1860 Perintisan -->
        <div style="position:absolute;left:0;top:-68px;width:15%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--teal);margin-bottom:3px">Perintisan</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--teal);opacity:.7">1856–1860</div>
        </div>

        <!-- 1860-1873 Kemunduran -->
        <div style="position:absolute;left:15%;top:-68px;width:17%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--amber);margin-bottom:3px">Kemunduran</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--amber);opacity:.7">1860–1873</div>
        </div>

        <!-- 1874-1888 Kebangkitan -->
        <div style="position:absolute;left:32%;top:-68px;width:24%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--rust);margin-bottom:3px">Kebangkitan</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--rust);opacity:.7">1874–1888</div>
        </div>

        <!-- 1890-1907 Nawawi -->
        <div style="position:absolute;left:56%;top:-68px;width:20%;text-align:center">
          <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;color:var(--rust2);margin-bottom:3px">Nawawi</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.08em;color:var(--rust2);opacity:.7">1890–1907</div>
        </div>

        <!-- 1908-1915 Pergerakan -->
        <div style="position:absolute;left:76%;top:-68px;width:24%;text-align:center">"""
c = c.replace(old_labels, new_labels)


# Events:
old_events = """        <!-- 1858 -->
        <div style="position:absolute;left:5%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--teal);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-20px;width:60px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--teal);line-height:1.4">1858<br>Permanen</div>
        </div>

        <!-- ~1860 van Ophuysen pergi -->
        <div style="position:absolute;left:13%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--amber);margin-left:-5px;border:2px solid var(--amber2)"></div>
          <div style="position:absolute;top:16px;left:-30px;width:80px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--amber);line-height:1.4">≈1860<br>Ophuysen pergi</div>
        </div>

        <!-- 1866 audit -->
        <div style="position:absolute;left:26%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--amber);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-30px;width:80px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--amber);line-height:1.4">1866<br>49→12 lulusan</div>
        </div>

        <!-- 1873 gedung baru dibuka -->
        <div style="position:absolute;left:37%;top:4px">
          <div style="width:12px;height:12px;border-radius:50%;background:var(--rust);margin-left:-6px;border:2px solid var(--rust2)"></div>
          <div style="position:absolute;top:16px;left:-35px;width:85px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">Apr 1873<br>Gedung baru ƒ300k</div>
        </div>

        <!-- 1874 Laats+Weide pembenahan -->
        <div style="position:absolute;left:44%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-30px;width:75px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">1874<br>Pembenahan staf</div>
        </div>

        <!-- 1873 schoolcommissie larashoofd -->
        <div style="position:absolute;left:48%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">1873<br>Schoolcommissie</div>
        </div>

        <!-- 1885 gedung baru lagi -->
        <div style="position:absolute;left:56%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">1885<br>Gedung baru lagi</div>
        </div>

        <!-- ≈1890 Nawawi kweekeling lulus -->
        <div style="position:absolute;left:60%;top:4px">
          <div style="width:12px;height:12px;border-radius:50%;background:var(--rust2);margin-left:-6px;border:2px solid var(--rust)"></div>
          <div style="position:absolute;top:16px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust2);line-height:1.4">≈1890<br>Nawawi lulus</div>
        </div>

        <!-- 1899 Nawawi figur sosial -->
        <div style="position:absolute;left:68%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust2);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust2);line-height:1.4">1899<br>Nawawi: kuda balap</div>
        </div>

        <!-- 1907 Vereeniging -->
        <div style="position:absolute;left:78%;top:4px">
          <div style="width:14px;height:14px;border-radius:50%;background:var(--rust2);margin-left:-7px;border:2px solid var(--amber2)"></div>
          <div style="position:absolute;top:18px;left:-30px;width:80px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust2);line-height:1.4">1907<br>Vereeniging<br>Minangkabau</div>
        </div>

        <!-- 1908 Ibrahim / Tan Malaka masuk sekolah FdK -->
        <div style="position:absolute;left:80%;top:4px">
          <div style="width:12px;height:12px;border-radius:50%;background:#E24B4A;margin-left:-6px;border:2px solid #A32D2D"></div>
          <div style="position:absolute;top:18px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:#E24B4A;line-height:1.4">≈1908<br>Ibrahim (FdK)</div>
        </div>

        <!-- 1912 Hatta -->
        <div style="position:absolute;left:89%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:#E24B4A;margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-20px;width:60px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:#E24B4A;line-height:1.4">≈1912<br>Hatta (FdK)</div>
        </div>"""

new_events = """        <!-- 1858 -->
        <div style="position:absolute;left:4%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--teal);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-20px;width:60px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--teal);line-height:1.4">1858<br>Permanen</div>
        </div>

        <!-- ~1860 van Ophuysen pergi -->
        <div style="position:absolute;left:15%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--amber);margin-left:-5px;border:2px solid var(--amber2)"></div>
          <div style="position:absolute;top:16px;left:-30px;width:80px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--amber);line-height:1.4">≈1860<br>Ophuysen pergi</div>
        </div>

        <!-- 1866 audit -->
        <div style="position:absolute;left:23%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--amber);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-30px;width:80px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--amber);line-height:1.4">1866<br>49→12 lulusan</div>
        </div>

        <!-- 1873 gedung baru dibuka -->
        <div style="position:absolute;left:32%;top:4px">
          <div style="width:12px;height:12px;border-radius:50%;background:var(--rust);margin-left:-6px;border:2px solid var(--rust2)"></div>
          <div style="position:absolute;top:16px;left:-35px;width:85px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">Apr 1873<br>Gedung baru</div>
        </div>

        <!-- 1873 schoolcommissie larashoofd -->
        <div style="position:absolute;left:39%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-35px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">1873<br>Schoolcommissie</div>
        </div>

        <!-- 1874 Laats+Weide pembenahan -->
        <div style="position:absolute;left:46%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-30px;width:75px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">1874<br>Pembenahan staf</div>
        </div>

        <!-- 1885 gedung baru lagi -->
        <div style="position:absolute;left:54%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust);line-height:1.4">1885<br>Gedung baru lagi</div>
        </div>

        <!-- ≈1890 Nawawi kweekeling lulus -->
        <div style="position:absolute;left:60%;top:4px">
          <div style="width:12px;height:12px;border-radius:50%;background:var(--rust2);margin-left:-6px;border:2px solid var(--rust)"></div>
          <div style="position:absolute;top:16px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust2);line-height:1.4">≈1890<br>Nawawi lulus</div>
        </div>

        <!-- 1899 Nawawi figur sosial -->
        <div style="position:absolute;left:68%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--rust2);margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-35px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust2);line-height:1.4">1899<br>Nawawi: kuda balap</div>
        </div>

        <!-- 1907 Vereeniging -->
        <div style="position:absolute;left:76%;top:4px">
          <div style="width:14px;height:14px;border-radius:50%;background:var(--rust2);margin-left:-7px;border:2px solid var(--amber2)"></div>
          <div style="position:absolute;top:18px;left:-40px;width:80px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--rust2);line-height:1.4">1907<br>Vereeniging<br>Minangkabau</div>
        </div>

        <!-- 1908 Ibrahim / Tan Malaka masuk sekolah FdK -->
        <div style="position:absolute;left:84%;top:4px">
          <div style="width:12px;height:12px;border-radius:50%;background:#E24B4A;margin-left:-6px;border:2px solid #A32D2D"></div>
          <div style="position:absolute;top:18px;left:-25px;width:70px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:#E24B4A;line-height:1.4">≈1908<br>Ibrahim (FdK)</div>
        </div>

        <!-- 1912 Hatta -->
        <div style="position:absolute;left:92%;top:4px">
          <div style="width:10px;height:10px;border-radius:50%;background:#E24B4A;margin-left:-5px"></div>
          <div style="position:absolute;top:16px;left:-30px;width:60px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:8px;color:#E24B4A;line-height:1.4">≈1912<br>Hatta (FdK)</div>
        </div>"""
c = c.replace(old_events, new_events)


# If scrolling didn't work, maybe the inner wrapper min-width wasn't enough?
# Wait, timeline-puncak-scroll has `overflow-x:auto`. It should scroll smoothly.
# The user's screen was probably wider than 900px, so there was no scrollbar! We should widen the minimum timeline to 1100px so it forces a horizontal scroll on smaller monitors, or looks evenly spaced on wide monitors.

c = c.replace('.timeline-puncak-inner{min-width:900px;', '.timeline-puncak-inner{min-width:1150px;')

# Ensure old _final has the inner replaced:
with open('kweekschool_v3_final.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done')
