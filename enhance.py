#!/usr/bin/env python3
"""
Add 6 enhancements to kweekschool_network_mapping.html:
1. Counter animation on Kesimpulan stats
2. Timeline filter by era
3. Click-to-pin tooltips on network graph
4. Academic citation copy button on timeline events
5. Visual career path infographic for Nawawi
6. Simple geographic map of Minangkabau highlands
"""
import unicodedata, sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = 'kweekschool_network_mapping.html'
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()
html = unicodedata.normalize('NFC', html)
print(f"Read {len(html)} bytes")

changes = 0
def do_replace(html, old, new, label, allow_missing=False):
    global changes
    old = unicodedata.normalize('NFC', old)
    new = unicodedata.normalize('NFC', new)
    if old not in html:
        if allow_missing:
            print(f"  ~ SKIPPED: {label}")
            return html
        print(f"  ✗ NOT FOUND: {label}")
        print(f"    {repr(old[:100])}")
        return html
    result = html.replace(old, new)
    changes += 1
    print(f"  ✓ {label}")
    return result


# ═══════════════════════════════════════════════════════════
# CSS ADDITIONS FOR ALL 6 FEATURES
# ═══════════════════════════════════════════════════════════
print("\n[1] CSS for all 6 features")

CSS_ENHANCEMENTS = """
/* COUNTER ANIMATION */
@keyframes countUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.kd-item.animated .num{animation:countUp .6s ease-out both}
.kd-item:nth-child(2).animated .num{animation-delay:.15s}
.kd-item:nth-child(3).animated .num{animation-delay:.3s}
.kd-item:nth-child(4).animated .num{animation-delay:.45s}
/* TIMELINE FILTER */
.tl-filter-bar{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:2.5rem;padding:.75rem 0}
.tl-filter-btn{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border-radius:2px;cursor:pointer;border:.5px solid var(--border);background:transparent;color:var(--ink3);transition:all .25s}
.tl-filter-btn:hover{border-color:var(--ink2);color:var(--ink2)}
.tl-filter-btn.active{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.tl-event.tl-hidden{display:none}
.tl-era.tl-hidden{display:none}
/* CITE BUTTON */
.cite-btn{position:absolute;top:.75rem;right:.75rem;width:28px;height:28px;border-radius:2px;border:.5px solid var(--border);background:var(--paper);color:var(--ink3);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:12px;transition:all .2s;opacity:0;z-index:2}
.tl-card:hover .cite-btn{opacity:1}
.cite-btn:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.cite-btn.copied{background:var(--teal);color:#fff;border-color:var(--teal)}
.cite-toast{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(20px);background:var(--ink);color:var(--paper);font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.08em;padding:.6rem 1.5rem;border-radius:3px;opacity:0;transition:all .3s;z-index:999;pointer-events:none;border:.5px solid rgba(245,240,232,.15)}
.cite-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
/* CAREER PATH */
.career-path{margin:3rem 0;padding:2rem 0;border-top:.5px solid var(--border);border-bottom:.5px solid var(--border)}
.career-path-title{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--rust2);margin-bottom:1.5rem;text-align:center}
.career-steps{display:flex;align-items:stretch;gap:0;position:relative;overflow-x:auto;padding-bottom:.5rem}
.career-step-item{flex:1;min-width:130px;text-align:center;position:relative;padding:0 .5rem}
.career-step-item::before{content:'';position:absolute;top:22px;left:0;right:0;height:2px;background:var(--border)}
.career-step-item:first-child::before{left:50%}
.career-step-item:last-child::before{right:50%}
.cs-dot{width:14px;height:14px;border-radius:50%;margin:16px auto 12px;position:relative;z-index:1;transition:transform .3s}
.career-step-item:hover .cs-dot{transform:scale(1.5)}
.cs-year{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.08em;color:var(--amber);display:block;margin-bottom:4px}
.cs-label{font-family:'Playfair Display',serif;font-size:.8rem;font-weight:700;color:var(--ink);line-height:1.3;margin-bottom:2px}
.cs-detail{font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--ink3);letter-spacing:.03em;line-height:1.4}
/* PINNED TOOLTIP */
.net-tooltip.pinned{pointer-events:auto;opacity:1}
.net-tooltip .tt-close{position:absolute;top:6px;right:8px;width:20px;height:20px;border:none;background:none;color:rgba(245,240,232,.4);font-size:14px;cursor:pointer;display:none;align-items:center;justify-content:center;border-radius:2px}
.net-tooltip .tt-close:hover{color:var(--paper);background:rgba(245,240,232,.1)}
.net-tooltip.pinned .tt-close{display:flex}
/* GEO MAP */
.geo-section{padding:3rem 0;margin:3rem 0;border-top:.5px solid var(--border)}
.geo-title{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--rust2);margin-bottom:.5rem;text-align:center}
.geo-subtitle{font-family:'Source Serif 4',serif;font-size:.9rem;color:var(--ink3);font-style:italic;text-align:center;margin-bottom:1.5rem;font-weight:300}
.geo-canvas-wrap{position:relative;background:var(--paper2);border:.5px solid var(--border);border-radius:3px;padding:1rem;overflow:hidden}
.geo-canvas-wrap canvas{display:block;width:100%}
.geo-tooltip{position:absolute;background:rgba(26,20,16,.93);border:.5px solid rgba(245,240,232,.2);border-radius:3px;padding:.6rem .9rem;pointer-events:none;z-index:10;max-width:200px;opacity:0;transition:opacity .15s}
.geo-tooltip.visible{opacity:1}
.geo-tooltip .gt-name{font-family:'Playfair Display',serif;font-size:.85rem;font-weight:700;color:var(--paper);margin-bottom:2px}
.geo-tooltip .gt-detail{font-family:'JetBrains Mono',monospace;font-size:8px;color:rgba(245,240,232,.5);letter-spacing:.03em;line-height:1.5}
"""

html = do_replace(html, '</style>', CSS_ENHANCEMENTS + '</style>', "Enhancement CSS added")


# ═══════════════════════════════════════════════════════════
# FEATURE 2: Timeline era filter buttons
# ═══════════════════════════════════════════════════════════
print("\n[2] Timeline filter buttons")

# Add filter bar after Bab I section header (Kelahiran)
FILTER_BAR_I = """<div class="tl-filter-bar" id="filter-kelahiran">
      <button class="tl-filter-btn active" onclick="filterTimeline('kelahiran','all')">Semua</button>
      <button class="tl-filter-btn" onclick="filterTimeline('kelahiran','lahir')">Pendirian</button>
    </div>
    """
html = do_replace(html,
    '<div class="timeline">\n    <div class="tl-line"></div>\n    <div class="tl-era fade-in"><div class="era-badge lahir">',
    '<div class="timeline">\n    ' + FILTER_BAR_I + '<div class="tl-line"></div>\n    <div class="tl-era fade-in"><div class="era-badge lahir">',
    "Filter bar added to Bab I",
    allow_missing=True
)

# Add filter to Kemerosotan (Bab II) 
FILTER_BAR_II = """<div class="tl-filter-bar" id="filter-merosot">
      <button class="tl-filter-btn active" onclick="filterTimeline('merosot','all')">Semua</button>
      <button class="tl-filter-btn" onclick="filterTimeline('merosot','merosot')">Kemerosotan</button>
      <button class="tl-filter-btn" onclick="filterTimeline('merosot','reformasi')">Reformasi</button>
    </div>
    """

# Find the merosot timeline start
html = do_replace(html,
    '<div class="timeline">\n    <div class="tl-line"></div>\n    <div class="tl-era fade-in"><div class="era-badge merosot">',
    '<div class="timeline">\n    ' + FILTER_BAR_II + '<div class="tl-line"></div>\n    <div class="tl-era fade-in"><div class="era-badge merosot">',
    "Filter bar added to Bab II Kemerosotan"
)

# Add filter to Akses (Bab III)
FILTER_BAR_III = """<div class="tl-filter-bar" id="filter-akses">
      <button class="tl-filter-btn active" onclick="filterTimeline('akses','all')">Semua</button>
      <button class="tl-filter-btn" onclick="filterTimeline('akses','akses')">Akses</button>
    </div>
    """
html = do_replace(html,
    '<div class="timeline fade-in">\n    <div class="tl-line"></div>\n    <div class="tl-era"><div class="era-badge akses">',
    '<div class="timeline fade-in">\n    ' + FILTER_BAR_III + '<div class="tl-line"></div>\n    <div class="tl-era"><div class="era-badge akses">',
    "Filter bar added to Bab III Akses"
)

# Add filter to Nawawi (Bab IV)
FILTER_BAR_IV = """<div class="tl-filter-bar" id="filter-nawawi">
      <button class="tl-filter-btn active" onclick="filterTimeline('nawawi','all')">Semua</button>
      <button class="tl-filter-btn" onclick="filterTimeline('nawawi','nawawi')">Karir & Jejak</button>
    </div>
    """
html = do_replace(html,
    '<div class="timeline">\n    <div class="tl-line"></div>\n    <div class="tl-era fade-in"><div class="era-badge nawawi">',
    '<div class="timeline">\n    ' + FILTER_BAR_IV + '<div class="tl-line"></div>\n    <div class="tl-era fade-in"><div class="era-badge nawawi">',
    "Filter bar added to Bab IV Nawawi"
)


# ═══════════════════════════════════════════════════════════
# FEATURE 4: Citation button on src-blocks
# ═══════════════════════════════════════════════════════════
print("\n[4] Citation copy buttons")

# Add a cite toast container before </body>
html = do_replace(html,
    '</body>',
    '<div class="cite-toast" id="cite-toast">Sitasi disalin ke clipboard</div>\n</body>',
    "Citation toast added"
)

# Make tl-card position:relative for cite button positioning (already has position:relative from overflow:hidden)
# Add cite buttons via JavaScript (see JS section below)


# ═══════════════════════════════════════════════════════════
# FEATURE 5: Visual career path infographic for Nawawi
# ═══════════════════════════════════════════════════════════
print("\n[5] Nawawi career path infographic")

CAREER_PATH_HTML = """
  <div class="career-path fade-in">
    <div class="career-path-title">Jalur Karir Nawawi Soetan Makmoer</div>
    <div class="career-steps">
      <div class="career-step-item">
        <div class="cs-year">\u22481880an</div>
        <div class="cs-dot" style="background:var(--teal)"></div>
        <div class="cs-label">Kweekeling</div>
        <div class="cs-detail">Siswa kweekschool<br>Fort de Kock</div>
      </div>
      <div class="career-step-item">
        <div class="cs-year">\u22481885</div>
        <div class="cs-dot" style="background:var(--teal2)"></div>
        <div class="cs-label">Lulus Ujian</div>
        <div class="cs-detail">Hulponderwijzer<br>Padang</div>
      </div>
      <div class="career-step-item">
        <div class="cs-year">\u22481890an</div>
        <div class="cs-dot" style="background:var(--amber)"></div>
        <div class="cs-label">Onderwijzer</div>
        <div class="cs-detail">Guru kelas 1<br>Fort de Kock</div>
      </div>
      <div class="career-step-item">
        <div class="cs-year">\u22481895</div>
        <div class="cs-dot" style="background:var(--amber2)"></div>
        <div class="cs-label">Guru Melayu</div>
        <div class="cs-detail">Kweekschool<br>Fort de Kock</div>
      </div>
      <div class="career-step-item">
        <div class="cs-year">1899</div>
        <div class="cs-dot" style="background:var(--rust2)"></div>
        <div class="cs-label">Figur Sosial</div>
        <div class="cs-detail">Pemilik kuda balap<br>Notabel kolonial</div>
      </div>
      <div class="career-step-item">
        <div class="cs-year">1906</div>
        <div class="cs-dot" style="background:var(--rust)"></div>
        <div class="cs-label">Paken Malam</div>
        <div class="cs-detail">Panitia festival<br>bersama Kontrolir</div>
      </div>
      <div class="career-step-item">
        <div class="cs-year">1907</div>
        <div class="cs-dot" style="background:var(--ink)"></div>
        <div class="cs-label">Voorzitter</div>
        <div class="cs-detail">Vereeniging<br>Minangkabau</div>
      </div>
    </div>
  </div>
"""

# Insert before closing </div> of timeline in Nawawi section (before </section> of nawawi)
html = do_replace(html,
    '  </div>\n</section>\n\n</main><!-- end main -->',
    CAREER_PATH_HTML + '  </div>\n</section>\n\n</main><!-- end main -->',
    "Nawawi career path infographic added"
)


# ═══════════════════════════════════════════════════════════
# FEATURE 6: Geographic map of Minangkabau highlands
# ═══════════════════════════════════════════════════════════
print("\n[6] Geographic map section")

GEO_MAP_HTML = """
  <div class="geo-section fade-in">
    <div class="geo-title">Peta Dataran Tinggi Minangkabau</div>
    <div class="geo-subtitle">Lokasi-lokasi kunci dalam jaringan pendidikan kolonial 1856\u20131912</div>
    <div class="geo-canvas-wrap">
      <canvas id="canvas-geo" height="400"></canvas>
      <div class="geo-tooltip" id="tt-geo"></div>
    </div>
  </div>
"""

# Insert after the career path, before closing of main section
html = do_replace(html,
    '</section>\n\n</main><!-- end main -->',
    GEO_MAP_HTML + '</section>\n\n</main><!-- end main -->',
    "Geographic map section added"
)


# ═══════════════════════════════════════════════════════════
# JAVASCRIPT: All 6 features
# ═══════════════════════════════════════════════════════════
print("\n[JS] Adding all feature scripts")

JS_ENHANCEMENTS = """

// ─── FEATURE 1: COUNTER ANIMATION ───
const counterObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if(e.isIntersecting){
      const items = e.target.querySelectorAll('.kd-item');
      items.forEach((item, i) => {
        item.classList.add('animated');
        const numEl = item.querySelector('.num');
        if(!numEl) return;
        const target = numEl.textContent.replace(/\\./g,'');
        const targetNum = parseInt(target);
        if(isNaN(targetNum)) return;
        const duration = 1500;
        const start = performance.now();
        const fmt = (n) => n.toLocaleString('id-ID');
        function tick(now){
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          numEl.textContent = fmt(Math.round(targetNum * eased));
          if(progress < 1) requestAnimationFrame(tick);
        }
        setTimeout(() => requestAnimationFrame(tick), i * 150);
      });
      counterObs.unobserve(e.target);
    }
  });
},{threshold:.3});
const statsGrid = document.querySelector('.kesimpulan-stats');
if(statsGrid) counterObs.observe(statsGrid);

// ─── FEATURE 2: TIMELINE FILTER ───
function filterTimeline(sectionId, era){
  const section = document.getElementById(sectionId);
  if(!section) return;
  // Update buttons
  const bar = section.querySelector('.tl-filter-bar') || document.getElementById('filter-'+sectionId);
  if(bar){
    bar.querySelectorAll('.tl-filter-btn').forEach(b=>b.classList.remove('active'));
    event.target.classList.add('active');
  }
  // Filter events
  const events = section.querySelectorAll('.tl-event');
  const eras = section.querySelectorAll('.tl-era');
  if(era === 'all'){
    events.forEach(ev=>{ev.classList.remove('tl-hidden');ev.style.opacity='';ev.style.transform='';});
    eras.forEach(er=>er.classList.remove('tl-hidden'));
  } else {
    events.forEach((ev,i)=>{
      const match = ev.classList.contains(era);
      if(match){
        ev.classList.remove('tl-hidden');
        ev.style.opacity='1';ev.style.transform='';
      } else {
        ev.classList.add('tl-hidden');
      }
    });
    eras.forEach(er=>{
      const badge = er.querySelector('.era-badge');
      if(badge && badge.classList.contains(era)){er.classList.remove('tl-hidden');}
      else{er.classList.add('tl-hidden');}
    });
  }
}

// ─── FEATURE 3: CLICK-TO-PIN TOOLTIPS ───
function setupPinnedTooltips(){
  document.querySelectorAll('canvas[id^="canvas-"]').forEach(canvas=>{
    canvas.addEventListener('click', function(e){
      const ttId = 'tt-' + this.id.replace('canvas-','');
      const tt = document.getElementById(ttId);
      if(!tt) return;
      if(tt.classList.contains('pinned')){
        tt.classList.remove('pinned');
        return;
      }
      if(tt.classList.contains('visible')){
        tt.classList.add('pinned');
        // Add close button if not present
        if(!tt.querySelector('.tt-close')){
          const closeBtn = document.createElement('button');
          closeBtn.className = 'tt-close';
          closeBtn.innerHTML = '\\u00d7';
          closeBtn.onclick = function(ev){
            ev.stopPropagation();
            tt.classList.remove('pinned','visible');
          };
          tt.prepend(closeBtn);
        }
      }
    });
  });
}
setupPinnedTooltips();

// ─── FEATURE 4: CITATION COPY BUTTONS ───
function setupCiteButtons(){
  document.querySelectorAll('.src-block').forEach(srcBlock=>{
    const card = srcBlock.closest('.tl-card');
    if(!card) return;
    // Get source text
    const srcText = srcBlock.textContent.replace('Sumber','').trim();
    const titleEl = card.querySelector('h3');
    const title = titleEl ? titleEl.textContent : '';
    const dateEl = card.closest('.tl-event');
    const yearEl = dateEl ? dateEl.querySelector('.tl-date .year') : null;
    const year = yearEl ? yearEl.textContent : '';
    const monthEl = dateEl ? dateEl.querySelector('.tl-date .month') : null;
    const month = monthEl ? monthEl.textContent : '';
    
    const btn = document.createElement('button');
    btn.className = 'cite-btn';
    btn.title = 'Salin sitasi';
    btn.innerHTML = '\\u201e';
    btn.onclick = function(e){
      e.stopPropagation();
      const citation = `${srcText}. Dikutip dalam: "${title}" (${month ? month+' ' : ''}${year}). Kweekschool Fort de Kock — Riset Sejarah Pendidikan Kolonial.`;
      navigator.clipboard.writeText(citation).then(()=>{
        btn.classList.add('copied');
        btn.innerHTML = '\\u2713';
        const toast = document.getElementById('cite-toast');
        toast.classList.add('show');
        setTimeout(()=>{toast.classList.remove('show');btn.classList.remove('copied');btn.innerHTML='\\u201e';},2000);
      });
    };
    card.appendChild(btn);
  });
}
setupCiteButtons();

// ─── FEATURE 6: GEOGRAPHIC MAP ───
const GEO_PLACES = [
  {id:'fdk',name:'Fort de Kock (Bukittinggi)',x:.52,y:.32,r:12,col:'#8b3a1e',detail:'Kweekschool (1856)\\nPusat pendidikan guru'},
  {id:'fvdc',name:'Fort van der Capellen (Batusangkar)',x:.58,y:.52,col:'#c0542a',r:9,detail:'Schoolcommissie pertama (1873)\\nLarashoofd Salimpawang'},
  {id:'kotogadang',name:'Koto Gadang',x:.48,y:.28,r:8,col:'#2a8c7e',detail:'Sekolah bumiputra\\nOnderwijzer Sakin'},
  {id:'payakumbuh',name:'Payakumbuh',x:.63,y:.38,r:8,col:'#2a8c7e',detail:'Sekolah bumiputra\\nOnderwijzer Salim'},
  {id:'padang',name:'Padang',x:.28,y:.72,r:10,col:'#185FA5',detail:'Ibukota karesidenan\\nUjian hulponderwijzer'},
  {id:'pdgpanjang',name:'Padang Panjang',x:.45,y:.48,r:8,col:'#d4962e',detail:'Jalur kereta api\\nWilayah pendidikan'},
  {id:'solok',name:'Solok',x:.48,y:.62,r:7,col:'#d4962e',detail:'Wilayah pendidikan\\nPadangsche Bovenlanden'},
  {id:'sawahlunto',name:'Sawahlunto',x:.58,y:.58,r:7,col:'#888780',detail:'Tambang batu bara\\nWilayah pendidikan'},
  {id:'palembajan',name:'Palembajan',x:.42,y:.42,r:7,col:'#c0542a',detail:'Schoolcommissie (1874)\\nLarashoofd VIII Kottas'},
  {id:'bondjol',name:'Bondjol',x:.38,y:.22,r:7,col:'#c0542a',detail:'Schoolcommissie\\nLarashoofd Si Nailic'},
  {id:'soepajang',name:'Soepajang',x:.52,y:.68,r:7,col:'#534AB7',detail:'Asal mantri inisiator\\nVereeniging Minangkabau'},
  {id:'boea',name:'Boea',x:.62,y:.48,r:7,col:'#c0542a',detail:'Schoolcommissie (1874)\\nLarashoofd van Lintoe'},
];
const GEO_CONNECTIONS = [
  ['fdk','fvdc'],['fdk','kotogadang'],['fdk','payakumbuh'],['fdk','padang'],
  ['fdk','pdgpanjang'],['fdk','palembajan'],['fdk','bondjol'],
  ['padang','solok'],['pdgpanjang','solok'],['solok','sawahlunto'],
  ['fvdc','boea'],['soepajang','fdk'],
];

function drawGeoMap(){
  const canvas = document.getElementById('canvas-geo');
  const tt = document.getElementById('tt-geo');
  if(!canvas) return;
  const W = canvas.offsetWidth;
  const H = parseInt(canvas.getAttribute('height'));
  canvas.width = W * devicePixelRatio;
  canvas.height = H * devicePixelRatio;
  canvas.style.width = W+'px'; canvas.style.height = H+'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(devicePixelRatio, devicePixelRatio);
  const placed = GEO_PLACES.map(p=>({...p, px:p.x*W, py:p.y*H}));

  // Background - terrain feel
  const bg = ctx.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,'#e8e0d0');bg.addColorStop(.5,'#ddd5c5');bg.addColorStop(1,'#d5cdb8');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

  // Subtle topographic lines
  ctx.strokeStyle='rgba(26,20,16,.06)';ctx.lineWidth=.5;
  for(let i=0;i<12;i++){
    ctx.beginPath();
    const cy=H*(.15+i*.065), cx=W*(.48+Math.sin(i)*.08), rx=W*(.25+i*.02), ry=H*(.06+i*.015);
    ctx.ellipse(cx,cy,rx,ry,Math.sin(i)*.2,0,Math.PI*2);
    ctx.stroke();
  }

  // Mountain range hint
  ctx.fillStyle='rgba(26,20,16,.04)';
  ctx.beginPath();
  ctx.moveTo(0,H*.6);
  ctx.quadraticCurveTo(W*.2,H*.1,W*.5,H*.15);
  ctx.quadraticCurveTo(W*.8,H*.2,W,H*.5);
  ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.fill();

  // "Danau Singkarak" hint
  ctx.fillStyle='rgba(26,92,82,.08)';
  ctx.beginPath();ctx.ellipse(W*.5,H*.55,W*.06,H*.04,-.2,0,Math.PI*2);ctx.fill();
  ctx.font='italic 8px "Source Serif 4",serif';ctx.fillStyle='rgba(26,92,82,.25)';ctx.textAlign='center';
  ctx.fillText('Danau Singkarak',W*.5,H*.55+H*.06);

  // "Danau Maninjau" hint
  ctx.fillStyle='rgba(26,92,82,.06)';
  ctx.beginPath();ctx.ellipse(W*.35,H*.32,W*.03,H*.05,.3,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='rgba(26,92,82,.2)';
  ctx.fillText('D. Maninjau',W*.35,H*.32+H*.07);

  // Coast hint
  ctx.fillStyle='rgba(26,61,110,.06)';
  ctx.beginPath();ctx.moveTo(0,H*.5);ctx.quadraticCurveTo(W*.1,H*.6,W*.15,H*.9);
  ctx.lineTo(0,H);ctx.fill();
  ctx.fillStyle='rgba(26,61,110,.15)';ctx.font='italic 9px "Source Serif 4",serif';
  ctx.fillText('Samudera Hindia',W*.08,H*.9);

  // Connections
  GEO_CONNECTIONS.forEach(([a,b])=>{
    const na=placed.find(p=>p.id===a),nb=placed.find(p=>p.id===b);
    if(!na||!nb)return;
    ctx.beginPath();ctx.moveTo(na.px,na.py);
    ctx.lineTo(nb.px,nb.py);
    ctx.strokeStyle='rgba(139,58,30,.15)';ctx.lineWidth=1;ctx.setLineDash([3,4]);ctx.stroke();ctx.setLineDash([]);
  });

  // Places
  placed.forEach(p=>{
    // Glow
    const g=ctx.createRadialGradient(p.px,p.py,0,p.px,p.py,p.r*3);
    g.addColorStop(0,p.col+'30');g.addColorStop(1,'transparent');
    ctx.fillStyle=g;ctx.beginPath();ctx.arc(p.px,p.py,p.r*3,0,Math.PI*2);ctx.fill();
    // Dot
    ctx.beginPath();ctx.arc(p.px,p.py,p.r,0,Math.PI*2);
    ctx.fillStyle=p.col+'55';ctx.fill();
    ctx.strokeStyle=p.col;ctx.lineWidth=1.5;ctx.stroke();
    // Label
    ctx.fillStyle='rgba(26,20,16,.75)';
    ctx.font='600 9px "JetBrains Mono",monospace';
    ctx.textAlign='center';
    ctx.fillText(p.name, p.px, p.py+p.r+13);
  });

  // Title overlay
  ctx.fillStyle='rgba(26,20,16,.5)';
  ctx.font='italic 10px "Source Serif 4",serif';
  ctx.textAlign='left';
  ctx.fillText('Padangsche Bovenlanden (Dataran Tinggi Padang)',12,H-12);

  // Interaction
  canvas.onmousemove=function(e){
    const rect=canvas.getBoundingClientRect();
    const mx=e.clientX-rect.left, my=e.clientY-rect.top;
    let hit=null;
    placed.forEach(p=>{if(Math.hypot(mx-p.px,my-p.py)<p.r+10)hit=p;});
    if(hit){
      canvas.style.cursor='pointer';
      tt.innerHTML='<div class="gt-name">'+hit.name+'</div><div class="gt-detail">'+hit.detail.replace(/\\\\n/g,'<br>').replace(/\\n/g,'<br>')+'</div>';
      let lft=mx+14,top=my-10;
      if(lft+200>W)lft=mx-210;
      if(top<0)top=0;
      tt.style.left=lft+'px';tt.style.top=top+'px';
      tt.classList.add('visible');
    }else{canvas.style.cursor='default';tt.classList.remove('visible');}
  };
  canvas.onmouseleave=()=>tt.classList.remove('visible');
}

// Init geo map
const geoObs = new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){drawGeoMap();geoObs.unobserve(e.target);}});
},{threshold:.1});
const geoCanvas = document.getElementById('canvas-geo');
if(geoCanvas) geoObs.observe(geoCanvas.parentElement);
window.addEventListener('resize',()=>{if(document.getElementById('canvas-geo'))drawGeoMap();});
"""

html = do_replace(html,
    '</script>',
    JS_ENHANCEMENTS + '\n</script>',
    "All 6 feature scripts added"
)


# ═══════════════════════════════════════════════════════════
# FINAL: Write output
# ═══════════════════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"Total changes: {changes}")
print(f"Output: {len(html)} bytes")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"✓ Written to {FILE}")
