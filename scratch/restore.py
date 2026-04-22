import re

with open(r"c:\Users\muhammad.ikbal\Downloads\Kweekschool\larashoofd_network.html", "r", encoding="utf-8") as f:
    content = f.read()

script_index = content.find("// ─── DATA INJECTION ───")
if script_index == -1:
    print("Could not find script anchor!")
    exit(1)

# Find where the script tag started around the DATA INJECTION anchor.
# It should be right before it.
real_script_index = content.rfind("<script>", 0, script_index)
if real_script_index == -1:
    real_script_index = script_index

javascript_part = content[real_script_index:]

# Restore exact original layout block:
original_header = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jejaring Larashoofd & Elite Lokal Minangkabau · 1873–1914</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0f0e0c;--bg2:#1a1814;--bg3:#252220;--bg4:#2f2c28;
  --ink:#f0ebe0;--ink2:#c8bfaf;--ink3:#7a6e60;--ink4:#4a4440;
  --rust:#c0542a;--rust2:#8b3a1e;--teal:#2a8c7e;--teal2:#1a5c52;
  --amber:#d4962e;--amber2:#b07828;--blue:#378ADD;--blue2:#185FA5;
  --purple:#7F77DD;--green:#639922;--gray:#888780;
  --border:rgba(240,235,224,.08);--border2:rgba(240,235,224,.15);
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:'Inter',sans-serif;font-size:13px}

/* ─ LAYOUT ─ */
.app{display:grid;grid-template-columns:320px 1fr;grid-template-rows:48px 1fr 36px;height:100vh}
.topbar{grid-column:1/-1;background:var(--bg2);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 1.25rem;gap:1rem;z-index:10}
.sidebar{background:var(--bg2);border-right:1px solid var(--border);overflow-y:auto;display:flex;flex-direction:column;position:relative}
.canvas-wrap{position:relative;overflow:hidden;background:var(--bg)}
.statusbar{grid-column:1/-1;background:var(--bg3);border-top:1px solid var(--border);display:flex;align-items:center;padding:0 1rem;gap:1.5rem;font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--ink3)}

/* ─ TOPBAR ─ */
.topbar-title{font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:var(--ink);white-space:nowrap}
.topbar-title em{font-style:italic;color:var(--amber)}
.topbar-sep{width:1px;height:24px;background:var(--border2)}
.tab-group{display:flex;gap:0;background:var(--bg3);border-radius:4px;padding:2px}
.tab{padding:4px 12px;border-radius:3px;cursor:pointer;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink3);border:none;background:none;transition:all .15s;white-space:nowrap}
.tab.active{background:var(--bg4);color:var(--amber);font-weight:500}
.topbar-right{margin-left:auto;display:flex;gap:.75rem;align-items:center}
.search-wrap{position:relative}
.search-input{background:var(--bg3);border:1px solid var(--border);border-radius:4px;padding:5px 28px 5px 10px;color:var(--ink);font-size:11px;width:180px;outline:none;font-family:'Inter',sans-serif}
.search-input::placeholder{color:var(--ink4)}
.search-input:focus{border-color:var(--border2)}
.search-icon{position:absolute;right:8px;top:50%;transform:translateY(-50%);color:var(--ink4);font-size:11px}
.icon-btn{background:var(--bg3);border:1px solid var(--border);border-radius:4px;padding:5px 10px;color:var(--ink3);cursor:pointer;font-size:11px;transition:all .15s}
.icon-btn:hover{background:var(--bg4);color:var(--ink)}

/* ─ SIDEBAR ─ */
.sidebar-section{padding:.85rem 1rem;border-bottom:1px solid var(--border)}
.sidebar-section:last-child{border-bottom:none}
.sidebar-label{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.15em;text-transform:uppercase;color:var(--ink4);margin-bottom:.6rem;display:block}
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:.5rem}
.stat-card{background:var(--bg3);border-radius:3px;padding:.6rem .75rem}
.stat-val{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:var(--amber);line-height:1;display:block}
.stat-lbl{font-size:9px;color:var(--ink3);margin-top:2px;line-height:1.4;display:block}

/* Legend */
.legend-list{display:flex;flex-direction:column;gap:.35rem}
.legend-item{display:flex;align-items:center;gap:.5rem;cursor:pointer;padding:3px 4px;border-radius:3px;transition:background .12s}
.legend-item:hover{background:var(--bg3)}
.legend-item.dim{opacity:.35}
.leg-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.leg-text{font-size:10px;color:var(--ink2)}
.leg-count{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--ink4)}

/* Controls */
.ctrl-row{display:flex;flex-direction:column;gap:.4rem}
.ctrl-label{font-size:9px;color:var(--ink3);display:flex;justify-content:space-between}
.ctrl-slider{width:100%;accent-color:var(--amber);height:3px;border-radius:2px}
.ctrl-btns{display:flex;gap:.4rem;flex-wrap:wrap}
.ctrl-btn{padding:4px 10px;background:var(--bg3);border:1px solid var(--border);border-radius:3px;color:var(--ink3);cursor:pointer;font-size:10px;transition:all .15s;white-space:nowrap}
.ctrl-btn:hover,.ctrl-btn.active{background:var(--bg4);color:var(--ink);border-color:var(--border2)}

/* Filter multi-select */
.filter-pills{display:flex;flex-wrap:wrap;gap:.3rem}
.filter-pill{padding:3px 9px;border-radius:12px;font-size:9px;cursor:pointer;border:1px solid transparent;transition:all .15s;font-family:'JetBrains Mono',monospace;letter-spacing:.05em}

/* Timeline slider */
.timeline-wrap{padding:0 .5rem}
.year-track{position:relative;height:28px;display:flex;align-items:center}
.year-marks{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:8px;color:var(--ink4);margin-top:2px}

/* Info panel */
.info-panel{flex:1;overflow-y:auto;padding:.85rem 1rem}
.info-panel.hidden{display:none}
.info-name{font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:700;color:var(--ink);margin-bottom:.25rem;line-height:1.3}
.info-type{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.75rem;padding:2px 8px;border-radius:2px;display:inline-block}
.info-row{display:flex;justify-content:space-between;padding:.3rem 0;border-bottom:1px solid var(--border);font-size:10px}
.info-row-label{color:var(--ink3)}
.info-row-val{color:var(--ink);text-align:right;max-width:160px}
.info-section-title{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink4);margin:.75rem 0 .4rem}
.neighbor-list{display:flex;flex-direction:column;gap:.2rem}
.neighbor-item{display:flex;align-items:center;gap:.5rem;padding:3px 5px;border-radius:2px;background:var(--bg3);font-size:9px;color:var(--ink2)}
.neighbor-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
.conn-badge{font-size:8px;padding:1px 5px;border-radius:2px;margin-left:auto;font-family:'JetBrains Mono',monospace}

/* Canvas tooltip */
#tooltip{position:absolute;pointer-events:none;background:rgba(15,14,12,.95);border:1px solid var(--border2);border-radius:4px;padding:.6rem .85rem;max-width:240px;opacity:0;transition:opacity .12s;z-index:100;backdrop-filter:blur(4px)}
#tooltip.show{opacity:1}
.tt-name{font-family:'Playfair Display',serif;font-size:.9rem;font-weight:700;color:var(--ink);margin-bottom:2px}
.tt-type{font-family:'JetBrains Mono',monospace;font-size:8px;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.4rem}
.tt-body{font-size:9px;color:var(--ink3);line-height:1.6}

/* Scrollbar */
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}

/* Chart mini */
.mini-chart{height:50px;display:flex;align-items:flex-end;gap:2px;padding-top:.25rem}
.mini-bar{flex:1;border-radius:1px 1px 0 0;min-height:3px;cursor:pointer;transition:opacity .15s;position:relative}
.mini-bar:hover{opacity:.8}
.mini-bar-label{position:absolute;bottom:-14px;left:50%;transform:translateX(-50%);font-family:'JetBrains Mono',monospace;font-size:7px;color:var(--ink4);white-space:nowrap}

/* View modes */
canvas{display:block;width:100%;height:100%}
</style>
</head>
<body>
<div class="app">

  <!-- TOPBAR -->
  <header class="topbar">
    <div class="topbar-title">Jejaring <em>Larashoofd</em> & Pendidikan</div>
    <div class="topbar-sep"></div>
    <div class="tab-group">
      <button class="tab active" onclick="setView('network')">Graf Jejaring</button>
      <button class="tab" onclick="setView('matrix')">Matriks Peran</button>
      <button class="tab" onclick="setView('timeline')">Temporal</button>
      <button class="tab" onclick="setView('geo')">Sebaran Lokasi</button>
    </div>
    <div class="topbar-right">
      <div class="search-wrap">
        <input class="search-input" id="search-input" placeholder="Cari tokoh, lokasi..." oninput="onSearch(this.value)">
        <span class="search-icon">⌕</span>
      </div>
      <button class="icon-btn" onclick="resetZoom()">⊹ Reset</button>
      <button class="icon-btn" onclick="toggleLabels()">⊡ Label</button>
      <button class="icon-btn" onclick="exportData()">↓ Export</button>
    </div>
  </header>

  <!-- SIDEBAR -->
  <aside class="sidebar">

    <!-- STATS -->
    <div class="sidebar-section">
      <span class="sidebar-label">Statistik Dataset · Delpher 1873–1914</span>
      <div class="stat-grid">
        <div class="stat-card"><span class="stat-val" id="stat-persons">215</span><span class="stat-lbl">Tokoh elite lokal</span></div>
        <div class="stat-card"><span class="stat-val" id="stat-locs">524</span><span class="stat-lbl">Wilayah/laras</span></div>
        <div class="stat-card"><span class="stat-val" id="stat-edu">114</span><span class="stat-lbl">Koneksi pendidikan</span></div>
        <div class="stat-card"><span class="stat-val" id="stat-edges">1356</span><span class="stat-lbl">Total relasi</span></div>
      </div>
    </div>

    <!-- TEMPORAL MINI CHART -->
    <div class="sidebar-section">
      <span class="sidebar-label">Distribusi per Dekade</span>
      <div class="mini-chart" id="mini-chart"></div>
      <div style="display:flex;justify-content:space-between;margin-top:16px;padding:0 2px">
        <span style="font-family:'JetBrains Mono',monospace;font-size:7px;color:var(--ink4)">1870s</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:7px;color:var(--ink4)">1890s</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:7px;color:var(--ink4)">1910s</span>
      </div>
    </div>

    <!-- LEGEND -->
    <div class="sidebar-section">
      <span class="sidebar-label">Legenda Node</span>
      <div class="legend-list" id="legend-list"></div>
    </div>

    <!-- FILTERS -->
    <div class="sidebar-section">
      <span class="sidebar-label">Filter Gelar Adat</span>
      <div class="filter-pills" id="adat-filters"></div>
    </div>

    <!-- ROLE FILTERS -->
    <div class="sidebar-section">
      <span class="sidebar-label">Filter Peran</span>
      <div class="filter-pills" id="role-filters"></div>
    </div>

    <!-- CONTROLS -->
    <div class="sidebar-section">
      <span class="sidebar-label">Tampilan</span>
      <div class="ctrl-row">
        <label class="ctrl-label"><span>Kekuatan tolak</span><span id="repel-val">300</span></label>
        <input class="ctrl-slider" type="range" min="100" max="800" value="300" id="repel-slider" oninput="updateRepel(this.value)">
        <label class="ctrl-label" style="margin-top:.4rem"><span>Jarak link</span><span id="link-val">60</span></label>
        <input class="ctrl-slider" type="range" min="20" max="200" value="60" id="link-slider" oninput="updateLink(this.value)">
        <div class="ctrl-btns" style="margin-top:.5rem">
          <button class="ctrl-btn" onclick="setLayout('force')">Force</button>
          <button class="ctrl-btn" onclick="setLayout('radial')">Radial</button>
          <button class="ctrl-btn" onclick="setLayout('cluster')">Cluster</button>
          <button class="ctrl-btn" onclick="toggleEdu()">Edu only</button>
        </div>
      </div>
    </div>

    <!-- INFO PANEL (shown on click) -->
    <div class="info-panel hidden" id="info-panel">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
        <span class="sidebar-label" style="margin:0">Detail Node</span>
        <button onclick="closeInfo()" style="background:none;border:none;color:var(--ink3);cursor:pointer;font-size:14px">×</button>
      </div>
      <div class="info-name" id="info-name"></div>
      <span class="info-type" id="info-type"></span>
      <div id="info-rows"></div>
      <div class="info-section-title">Koneksi Terdekat</div>
      <div class="neighbor-list" id="info-neighbors"></div>
    </div>

  </aside>

  <!-- CANVAS -->
  <div class="canvas-wrap" id="canvas-wrap">
    <canvas id="main-canvas"></canvas>
    <div id="tooltip"></div>
    <!-- View: matrix -->
    <div id="view-matrix" style="display:none;position:absolute;inset:0;overflow:auto;padding:1.5rem"></div>
    <!-- View: timeline -->
    <div id="view-timeline" style="display:none;position:absolute;inset:0;overflow:auto;padding:1.5rem"></div>
    <!-- View: geo -->
    <div id="view-geo" style="display:none;position:absolute;inset:0;overflow:auto;padding:1.5rem"></div>
  </div>

  <!-- STATUS BAR -->
  <footer class="statusbar">
    <span id="status-nodes">748 node</span>
    <span>·</span>
    <span id="status-edges">1356 relasi</span>
    <span>·</span>
    <span id="status-filter">Semua ditampilkan</span>
    <span style="margin-left:auto">Sumber: Delpher · Koninklijke Bibliotheek · 1.410 dokumen sezaman · 1859–1915</span>
  </footer>

</div>

"""

# Ensure we remove my added "toggleSidebar" code if any:
# The toggleSidebar function was injected directly into javascript_part using script_injection.
if "function toggleSidebar()" in javascript_part:
    javascript_part = javascript_part.replace("""
// UI CONTROLS
let sidebarCollapsed = false;
function toggleSidebar() {
  sidebarCollapsed = !sidebarCollapsed;
  const wrap = document.getElementById('sidebar-wrapper');
  const btn = document.getElementById('collapse-btn');
  if(sidebarCollapsed) {
    wrap.classList.add('collapsed');
    btn.textContent = '▶';
  } else {
    wrap.classList.remove('collapsed');
    btn.textContent = '◀';
  }
}
""", "")

with open(r"c:\Users\muhammad.ikbal\Downloads\Kweekschool\larashoofd_network.html", "w", encoding="utf-8") as f:
    f.write(original_header + javascript_part)

print("RESTORED COMPLETELY!")
