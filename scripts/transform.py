#!/usr/bin/env python3
"""
Apply 9 improvements to kweekschool_network_mapping.html:
1. Swap Bab II (Akses) <-> Bab III (Kemerosotan) for chronological order
2. Replace melacak-kweekschool.docx annotations with proper sources
3. Fix Koto Gadang (Tapanuli) -> Koto Gadang (Agam)
4. Remove "Kebakaran besar Fort van der Capellen" from title
5. Replace "Si Nawawi" with "Nawawi Soetan Makmoer"
6. Add Nawawi background image CSS
7. Add G.H. Horensma + Ibrahim/Tan Malaka to network graph
8. Add Kesimpulan section before Sumber
9. Write Kesimpulan content "Merunduk bukan Tunduk"
"""
import unicodedata
import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = 'kweekschool_network_mapping.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Normalize Unicode to NFC so combining characters match precomposed forms
html = unicodedata.normalize('NFC', html)
print(f"Read {len(html)} bytes")

changes = 0

def do_replace(html, old, new, label, allow_missing=False):
    global changes
    old = unicodedata.normalize('NFC', old)
    new = unicodedata.normalize('NFC', new)
    if old not in html:
        if allow_missing:
            print(f"  ~ SKIPPED (not found): {label}")
            return html
        print(f"  ✗ NOT FOUND: {label}")
        print(f"    Looking for: {repr(old[:120])}")
        return html
    count = html.count(old)
    result = html.replace(old, new)
    changes += 1
    print(f"  ✓ {label} ({count} occurrence{'s' if count>1 else ''})")
    return result


# ═══════════════════════════════════════════════════════════
# POINT 6: CSS for Nawawi background image
# POINTS 8-9: CSS for Kesimpulan section
# ═══════════════════════════════════════════════════════════
print("\n── CSS Additions ──")
CSS_ADD = """/* NAWAWI BG */
#nawawi .section-header{position:relative;overflow:hidden}
#nawawi .section-header::after{content:'';position:absolute;top:0;right:0;bottom:0;width:280px;background:url('Engku-Nawawi--IST_ratio-16x9.jpg') center top/cover no-repeat;opacity:.18;mask-image:linear-gradient(to left,rgba(0,0,0,.7),transparent 80%);-webkit-mask-image:linear-gradient(to left,rgba(0,0,0,.7),transparent 80%);pointer-events:none;border-radius:3px}
/* KESIMPULAN */
.kesimpulan-section{background:var(--ink);color:var(--paper);padding:5rem 2rem;position:relative;overflow:hidden}
.kesimpulan-section::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 50% 50%,rgba(176,120,40,.12) 0%,transparent 70%)}
.kesimpulan-inner{max-width:1100px;margin:0 auto;position:relative;z-index:1}
.kesimpulan-header{text-align:center;margin-bottom:3.5rem}
.kesimpulan-eyebrow{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--rust2);margin-bottom:1rem;display:block}
.kesimpulan-quote{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3.2rem);font-weight:700;color:var(--paper);line-height:1.2;margin-bottom:.75rem}
.kesimpulan-quote em{font-style:italic;color:var(--amber2)}
.kesimpulan-sub{font-size:1.05rem;color:rgba(245,240,232,.5);font-style:italic;font-weight:300;max-width:640px;margin:0 auto}
.kesimpulan-body{display:grid;grid-template-columns:3fr 2fr;gap:3rem;margin-bottom:3rem}
.kesimpulan-text{font-size:.92rem;color:rgba(245,240,232,.72);line-height:1.9;font-weight:300}
.kesimpulan-text p+p{margin-top:1.2rem}
.kesimpulan-text strong{color:rgba(245,240,232,.9);font-weight:600}
.kesimpulan-stats{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-content:start}
.kd-item{border-left:2px solid rgba(245,240,232,.15);padding-left:1rem;padding-top:.25rem;padding-bottom:.25rem}
.kd-item .num{font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:var(--amber2);display:block;line-height:1}
.kd-item .desc{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.05em;text-transform:uppercase;color:rgba(245,240,232,.4);display:block;margin-top:4px;line-height:1.5}
.pepatah-box{margin:2.5rem 0;padding:2rem;border:1px solid rgba(245,240,232,.12);border-radius:3px;text-align:center;background:rgba(255,255,255,.03);max-width:700px;margin-left:auto;margin-right:auto}
.pepatah-text{font-family:'Playfair Display',serif;font-size:1.4rem;font-style:italic;color:var(--amber2);margin-bottom:.5rem;line-height:1.4}
.pepatah-meaning{font-size:.88rem;color:rgba(245,240,232,.5);font-weight:300;line-height:1.7}
.kesimpulan-coda{text-align:center;font-size:.95rem;color:rgba(245,240,232,.6);font-style:italic;max-width:700px;margin:0 auto;line-height:1.8;font-weight:300}
@media(max-width:768px){.kesimpulan-body{grid-template-columns:1fr}}
"""
html = do_replace(html, '</style>', CSS_ADD + '</style>', "CSS added")


# ═══════════════════════════════════════════════════════════
# POINT 1: Update nav links (swap order + add Kesimpulan)
# ═══════════════════════════════════════════════════════════
print("\n── Nav Update ──")
html = do_replace(html,
    '<li><a href="#kelahiran">I. Kelahiran</a></li>\n    <li><a href="#akses">II. Akses Pendidikan</a></li>\n    <li><a href="#merosot">III. Kemerosotan</a></li>\n    <li><a href="#nawawi">IV. Nawawi</a></li>\n    <li><a href="#network">V. Network Mapping</a></li>\n    <li><a href="#sumber">VI. Sumber</a></li>',
    '<li><a href="#kelahiran">I. Kelahiran</a></li>\n    <li><a href="#merosot">II. Kemerosotan</a></li>\n    <li><a href="#akses">III. Akses Pendidikan</a></li>\n    <li><a href="#nawawi">IV. Nawawi</a></li>\n    <li><a href="#network">V. Network</a></li>\n    <li><a href="#kesimpulan">VI. Kesimpulan</a></li>\n    <li><a href="#sumber">VII. Sumber</a></li>',
    "Nav links reordered + Kesimpulan added"
)


# ═══════════════════════════════════════════════════════════
# POINT 1: Swap Bab II (Akses) and Bab III (Kemerosotan)
# ═══════════════════════════════════════════════════════════
print("\n── Section Swap ──")
marker2 = '<!-- BAB II -->'
marker3 = '<!-- BAB III -->'

pos_m2 = html.index(marker2)
end_akses = html.index('</section>', pos_m2) + len('</section>')
akses_block = html[pos_m2:end_akses]

pos_m3 = html.index(marker3)
end_merosot = html.index('</section>', pos_m3) + len('</section>')
merosot_block = html[pos_m3:end_merosot]

# Capture everything between (divider + whitespace)
between = html[end_akses:pos_m3]

# Relabel bab numbers
akses_new = akses_block.replace(marker2, '<!-- BAB III -->').replace(
    'Bab II \u00b7 1870an\u20131885', 'Bab III \u00b7 1870an\u20131885')
merosot_new = merosot_block.replace(marker3, '<!-- BAB II -->').replace(
    'Bab III \u00b7 \u22481858\u20131874', 'Bab II \u00b7 \u22481858\u20131874')

# Swap: Kemerosotan first, then between (divider), then Akses
html = html[:pos_m2] + merosot_new + between + akses_new + html[end_merosot:]
changes += 1
print("  ✓ Sections swapped: Kemerosotan (Bab II) → Akses Pendidikan (Bab III)")


# ═══════════════════════════════════════════════════════════
# POINT 4: Remove "Kebakaran besar Fort van der Capellen"
# ═══════════════════════════════════════════════════════════
print("\n── Title Fix ──")
html = do_replace(html,
    'Kebakaran besar Fort van der Capellen \u2014 gedung kweekschool baru selesai dan ditempati',
    'Gedung kweekschool baru selesai dan ditempati',
    "Kebakaran title removed"
)


# ═══════════════════════════════════════════════════════════
# POINT 2: Replace docx annotations with actual sources
# ═══════════════════════════════════════════════════════════
print("\n── Source Annotations ──")
html = do_replace(html,
    '<span>Sumber</span>Docx: "Tijdelijk werkzaamgesteld" \u2014 teks asli Belanda dalam melacak-kweekschool.docx',
    '<span>Sumber</span>Bataviaasch Handelsblad, 25 Sep 1883 \u2014 "Tijdelijk werkzaamgesteld aan de kweekschool"',
    "Source 1: docx → Bataviaasch Handelsblad"
)
html = do_replace(html,
    '<span>Sumber</span>Docx: Directeur van Onderwijs, Eeredienst en Nijverheid \u2014 benoemingen',
    '<span>Sumber</span>Bataviaasch Handelsblad, 8 Agustus 1878 \u2014 "Benoemd: Tot onderwijzer der 1e klasse"',
    "Source 2: docx → Bataviaasch Handelsblad"
)
html = do_replace(html,
    '<span>Sumber</span>Docx: "Si Nawawi galar Soeltan Ma\u00e4moer, thans tijdelijk werkzaam gesteld aan die kweekschool"',
    '<span>Sumber</span>Java-bode, 3 Feb 1887 \u2014 "Inlandsch Onderwijs: Benoemd tot hulponderwijzer van den 1en rang"',
    "Source 3: docx → Java-bode"
)


# ═══════════════════════════════════════════════════════════
# POINT 3: Fix Koto Gadang (Tapanuli) → Koto Gadang (Agam)
# ═══════════════════════════════════════════════════════════
print("\n── Koto Gadang Fix ──")
html = do_replace(html,
    'Koto Gadang (Tapanuli)',
    'Koto Gadang (Agam)',
    "Koto Gadang: Tapanuli → Agam"
)


# ═══════════════════════════════════════════════════════════
# POINT 5: Replace Si Nawawi → Nawawi Soetan Makmoer
# ═══════════════════════════════════════════════════════════
print("\n── Nawawi Name Update ──")

# 1. Section header (unique HTML pattern)
html = do_replace(html,
    '<em>Si Nawawi</em><br>galar Soetan Ma\u00e4mour',
    '<em>Nawawi</em><br>Soetan Makmoer',
    "Heading: Si Nawawi → Nawawi Soetan Makmoer"
)

# 2. Body text with galar (catches h3 title + strong text)
html = do_replace(html,
    'Si Nawawi galar Soetan Ma\u00e4mour',
    'Nawawi Soetan Makmoer',
    "Body text: Si Nawawi galar → Nawawi Soetan Makmoer"
)

# 3. Timeline title "Si Nawawi: kweekeling..."
html = do_replace(html,
    'Si Nawawi: kweekeling',
    'Nawawi Soetan Makmoer: kweekeling',
    "Timeline title: Si Nawawi → Nawawi Soetan Makmoer"
)

# 4. Section description "Nawawi adalah produk..."
html = do_replace(html,
    'Nawawi adalah produk sekaligus melampaui',
    'Nawawi Soetan Makmoer adalah produk sekaligus melampaui',
    "Section desc: add full name"
)

# 5. JS network node label
html = do_replace(html,
    "label:'Goeroe Nawawi\\n(Soetan Ma\u00e4mour)'",
    "label:'Nawawi\\nSoetan Makmoer'",
    "JS node label: Goeroe Nawawi → Nawawi Soetan Makmoer"
)

# 6. Nawawi mentioned as "Dokumen menyebut Nawawi" → add full name
html = do_replace(html,
    'Dokumen menyebut Nawawi sebagai',
    'Dokumen menyebut Nawawi Soetan Makmoer sebagai',
    "Body: add full name in doc reference",
    allow_missing=True
)


# ═══════════════════════════════════════════════════════════
# POINT 7: Add G.H. Horensma + Ibrahim/Tan Malaka to network
# ═══════════════════════════════════════════════════════════
print("\n── Network Graph Additions ──")

# Add Ibrahim/Tan Malaka to PRIBUMI_NODES
ibrahim_node = """\n  {id:'ibrahim',x:.18,y:.22,r:17,col:'#2a8c7e',label:'Ibrahim\\n(Tan Malaka)',role:'Kweekeling FdK \\u2192 Tokoh Pergerakan',body:'Kweekeling di kweekschool Fort de Kock (\\u00b11908\\u20131912). Murid G.H. Horensma. Kelak bergelar Tan Malaka \\u2014 salah satu pemikir dan tokoh pergerakan kemerdekaan Indonesia terpenting abad ke-20.',career:['\\u00b11908\\u20131912: Kweekeling di kweekschool Fort de Kock','Murid G.H. Horensma','Kelak dikenal sebagai Tan Malaka','Pemikir \\u0026 tokoh pergerakan nasional']},"""

# Find PRIBUMI_NODES closing: search for ];  after const PRIBUMI_NODES
pribumi_start = html.index('const PRIBUMI_NODES')
pribumi_close = html.index('\n];', pribumi_start)
html = html[:pribumi_close] + ibrahim_node + html[pribumi_close:]
changes += 1
print("  ✓ Ibrahim/Tan Malaka added to PRIBUMI_NODES")

# Add Ibrahim edge to PRIBUMI edges
html = do_replace(html,
    "['hamzah','nawawi','peer'],\n    ];",
    "['hamzah','nawawi','peer'],\n      ['fdk','ibrahim','trained'],\n    ];",
    "Ibrahim edge added to PRIBUMI edges"
)

# Add G.H. Horensma to BELANDA_NODES
horensma_node = """\n  {id:'horensma',x:.55,y:.68,r:15,col:'#d4962e',label:'G.H. Horensma',role:'Hulponderwijzer \\u2192 Onderwijzer FdK',body:'Diangkat hulponderwijzer di Fort de Kock (Nov 1908, Javasche Courant). Tercatat sebagai onderwijzer di wilayah Padangsche Bovenlanden. Guru dari Ibrahim yang kelak bergelar Tan Malaka \\u2014 tokoh pergerakan kemerdekaan Indonesia.',career:['Nov 1908: Diangkat hulponderwijzer, Fort de Kock','Onderwijzer di wilayah Padangsche Bovenlanden','Guru dari Ibrahim (Tan Malaka) di kweekschool FdK']},"""

belanda_start = html.index('const BELANDA_NODES')
belanda_close = html.index('\n];', belanda_start)
html = html[:belanda_close] + horensma_node + html[belanda_close:]
changes += 1
print("  ✓ G.H. Horensma added to BELANDA_NODES")

# Add Horensma edge to BELANDA edges
html = do_replace(html,
    "['barthelemy','westenenk','collab'],\n    ];",
    "['barthelemy','westenenk','collab'],\n      ['horensma','inst_fdk','taught'],\n    ];",
    "Horensma edge added to BELANDA edges"
)


# ═══════════════════════════════════════════════════════════
# POINTS 8-9: Add Kesimpulan section before Sumber
# ═══════════════════════════════════════════════════════════
print("\n── Kesimpulan Section ──")

KESIMPULAN_HTML = """
<!-- KESIMPULAN -->
<section id="kesimpulan" class="kesimpulan-section">
  <div class="kesimpulan-inner">
    <div class="kesimpulan-header fade-in">
      <span class="kesimpulan-eyebrow">Bab VI \u00b7 Kesimpulan</span>
      <h2 class="kesimpulan-quote"><em>Merunduk</em> bukan Tunduk</h2>
      <p class="kesimpulan-sub">Sebuah upaya adaptasi dan menyesuaikan diri \u2014 strategi masyarakat Minangkabau dalam memanfaatkan kebijakan pendidikan kolonial</p>
    </div>

    <div class="kesimpulan-body fade-in">
      <div class="kesimpulan-text">
        <p>Belanda memberikan akses pendidikan kepada <strong>larashoofd</strong>, angku kepala, dan datuk-datuk \u2014 para penguasa lokal yang menjadi tiang penyangga birokrasi kolonial di Dataran Tinggi Minangkabau. Data dari <strong>1.410 dokumen sezaman</strong> menunjukkan bahwa hubungan antara larashoofd dan institusi pendidikan bukan kebetulan: <strong>490 entri</strong> secara langsung menghubungkan larashoofd dengan sistem persekolahan.</p>

        <p>Di antara <strong>409 penyebutan datoe/datuk</strong> dalam arsip, banyak yang kemudian diangkat menjadi guru \u2014 <strong>322 entri</strong> menyebut onderwijzer atau guru bumiputra. Datuk dan penguasa lokal yang mendapat akses pendidikan tidak sekadar menjalankan fungsi birokrasi; mereka membaca peluang di balik sistem yang mengikat mereka.</p>

        <p>Yang terjadi kemudian adalah apa yang disebut <strong>pisau bermata dua</strong> bagi Belanda. Pendidikan yang dirancang untuk memproduksi birokrat patuh justru melahirkan generasi pemikir dan tokoh pergerakan \u2014 dari <strong>Nawawi Soetan Makmoer</strong> yang mendirikan Vereeniging Minangkabau, hingga <strong>Ibrahim (Tan Malaka)</strong> yang kelak menjadi salah satu pemikir revolusioner terpenting Indonesia. Mereka semua adalah produk kweekschool Fort de Kock.</p>
      </div>

      <div class="kesimpulan-stats">
        <div class="kd-item"><span class="num">1.410</span><span class="desc">Dokumen sezaman dianalisis dari arsip Delpher</span></div>
        <div class="kd-item"><span class="num">490</span><span class="desc">Entri menghubungkan larashoofd dengan sistem sekolah</span></div>
        <div class="kd-item"><span class="num">409</span><span class="desc">Penyebutan datoe / datuk dalam arsip pendidikan</span></div>
        <div class="kd-item"><span class="num">322</span><span class="desc">Entri menyebut onderwijzer atau guru bumiputra</span></div>
      </div>
    </div>

    <div class="pepatah-box fade-in">
      <div class="pepatah-text">\u201cIyokan nan di urang, laluan nan di awak\u201d</div>
      <div class="pepatah-meaning">Iya-kan yang dikatakan orang, tapi jalani apa yang kita kehendaki \u2014 prinsip adaptasi masyarakat Minangkabau yang menjadi senjata dalam menavigasi politik pendidikan kolonial</div>
    </div>

    <p class="kesimpulan-coda fade-in">Mereka merunduk dalam sistem \u2014 bukan untuk tunduk, tetapi untuk memanfaatkannya. Anak kemenakan mereka mendapatkan akses pendidikan yang sama, dan dari generasi itulah lahir tokoh-tokoh pergerakan yang mengubah jalannya sejarah bangsa.</p>

    <div class="src-block fade-in" style="margin-top:2rem;background:rgba(255,255,255,.04);border-color:rgba(245,240,232,.1);color:rgba(245,240,232,.4)"><span style="color:var(--rust2)">Data</span>Analisis 1.410 entri dari delpher_larashoofd_processed_data.xls \u00b7 Koninklijke Bibliotheek \u00b7 Den Haag</div>
  </div>
</section>
"""

html = do_replace(html,
    '<!-- SOURCES -->',
    KESIMPULAN_HTML + '\n<!-- SOURCES -->',
    "Kesimpulan section inserted before Sumber"
)


# ═══════════════════════════════════════════════════════════
# Update Sumber section eyebrow
# ═══════════════════════════════════════════════════════════
print("\n── Sumber Section Update ──")
html = do_replace(html,
    '<span class="eyebrow">Aparatus Kritis</span>',
    '<span class="eyebrow">VII \u00b7 Aparatus Kritis</span>',
    "Sumber eyebrow: added VII"
)


# ═══════════════════════════════════════════════════════════
# Update "Benoemingen" source card: remove docx, add Horensma
# ═══════════════════════════════════════════════════════════
html = do_replace(html,
    'Nawawi: onderwijzer, hulponderwijzer, guru Melayu<br>Si Hamzah: Probolinggo<br>Sakin, Rinding, Salim: kweekelingen lulusan FdK<br>\u2192 Docx melacak-kweekschool.docx',
    'Nawawi Soetan Makmoer: onderwijzer, guru Melayu<br>G.H. Horensma: hulponderwijzer FdK (1908)<br>Si Hamzah: Probolinggo \u00b7 Sakin, Rinding, Salim: FdK<br>\u2192 Bataviaasch Handelsblad \u00b7 Java-bode \u00b7 Javasche Courant',
    "Benoemingen card: docx → proper sources + Horensma"
)


# ═══════════════════════════════════════════════════════════
# FINAL: Write output
# ═══════════════════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"Total changes applied: {changes}")
print(f"Output length: {len(html)} bytes")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Written to {FILE}")
