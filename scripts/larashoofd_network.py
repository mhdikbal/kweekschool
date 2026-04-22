#!/usr/bin/env python3
"""
Analisis Jejaring Larashoofd & Elite Lokal Minangkabau
Dataset: Delpher Larashoofd 1859-1915 (1.410 entri)

Metode:
- Network extraction dari teks koran kolonial Belanda
- Named entity recognition berbasis regex untuk gelar adat (galar)
- Graph analysis dengan NetworkX
- Visualisasi dengan Matplotlib dan Gephi-compatible export
"""

import pandas as pd
import numpy as np
import re
import ast
import json
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings('ignore')

# ─── DEPENDENCIES ───
try:
    import networkx as nx
    print("✓ NetworkX tersedia")
except ImportError:
    print("✗ pip install networkx")

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    print("✓ Matplotlib tersedia")
except ImportError:
    print("✗ pip install matplotlib")

print()

# ─── 1. LOAD DATA ───
print("=" * 60)
print("1. LOADING DATA")
print("=" * 60)

df = pd.read_excel("delpher_larashoofd_processed_data.xls", engine="xlrd")
print(f"Dataset: {df.shape[0]} baris × {df.shape[1]} kolom")
print(f"Rentang tahun: {df['date'].astype(str).str[:4].astype(int, errors='ignore').agg(['min','max']).tolist()}")

def parse_list_col(val):
    if pd.isna(val) or val == '[]': return []
    try: return ast.literal_eval(str(val))
    except: return []

df['orgs_list'] = df['organizations'].apply(parse_list_col)
df['year'] = df['date'].astype(str).str[:4].apply(lambda x: int(x) if x.isdigit() else 0)

# ─── 2. ENTITY EXTRACTION ───
print()
print("=" * 60)
print("2. EKSTRAKSI ENTITAS")
print("=" * 60)

# Patterns
p_galar = re.compile(
    r'(?:Si|Sic)\s+(\w+)\s+galar\s+'
    r'((?:Datoe|Toeankoe|Soetan|Radja|Bagindo|Chatib|Malin|Imam|Angku|Marah)\s+[\w\s]{3,30}?)' 
    r'(?:,|;|\s{2}|\.| larashoofd| panghoeloe| distrik| koeria)', re.I
)
p_role_loc = re.compile(
    r'(larashoofd|panghoeloe(?:\s*kapala)?|koeriahoofd|distriktshoofd)'
    r'\s+(?:van|der?)\s+([\w\s\'\-]{3,35}?)(?:[,;.]|$|\s{2})', re.I
)
edu_patterns = {
    'schoolcommissie': re.compile(r'schoolcommissie|schoolkommissie', re.I),
    'kweekschool': re.compile(r'kweekschool', re.I),
    'onderwijzer': re.compile(r'onderwijzer', re.I),
    'inlandsche_school': re.compile(r'inlandsche school', re.I),
}

# Extract records
records = []
for _, row in df.iterrows():
    ft = str(row['full_text'])
    year = row['year']
    edu = {k: bool(v.search(ft)) for k, v in edu_patterns.items()}
    
    persons = [(m.group(1), m.group(2), m.start()) for m in p_galar.finditer(ft)]
    roles = [(m.group(1).lower(), m.group(2).strip(), m.start()) for m in p_role_loc.finditer(ft)]
    
    for first, galar, ppos in persons:
        adat = next((t for t in ['Datoe','Toeankoe','Soetan','Bagindo','Radja','Chatib','Malin','Angku'] 
                     if t.lower() in galar.lower()), 'unknown')
        full_name = f"{first} galar {galar}"
        
        # Find role if nearby
        nearby_roles = [(r, l) for r, l, rpos in roles if abs(rpos - ppos) < 400]
        role = nearby_roles[0][0] if nearby_roles else 'unknown'
        location = nearby_roles[0][1] if nearby_roles else 'unknown'
        
        records.append({
            'name': full_name[:60],
            'first_name': first,
            'adat_title': adat,
            'role': role,
            'location': location[:40],
            'year': year,
            'decade': (year // 10) * 10,
            'edu_schoolcommissie': edu['schoolcommissie'],
            'edu_kweekschool': edu['kweekschool'],
            'edu_onderwijzer': edu['onderwijzer'],
            'edu_inlandsche_school': edu['inlandsche_school'],
            'has_edu': any(edu.values()),
        })

records_df = pd.DataFrame(records)
print(f"Total rekaman: {len(records_df)}")
print(f"Tokoh unik: {records_df['name'].nunique()}")
print(f"Lokasi unik: {records_df['location'].nunique()}")
print(f"\nDistribusi gelar adat:")
print(records_df['adat_title'].value_counts().to_string())
print(f"\nDistribusi peran:")
print(records_df['role'].value_counts().head(8).to_string())
print(f"\nTerhubung ke pendidikan: {records_df['has_edu'].sum()} dari {len(records_df)} ({records_df['has_edu'].mean()*100:.1f}%)")
print(f"Dengan schoolcommissie: {records_df['edu_schoolcommissie'].sum()}")
print(f"Dengan kweekschool: {records_df['edu_kweekschool'].sum()}")

# ─── 3. BUILD GRAPH ───
print()
print("=" * 60)
print("3. MEMBANGUN GRAF JEJARING")
print("=" * 60)

G = nx.DiGraph()

# Add institution nodes
institutions = {
    'KweekschoolFdK': {'type':'institution','label':'Kweekschool Fort de Kock','color':'#8b3a1e'},
    'Schoolcommissie': {'type':'institution','label':'Schoolcommissie','color':'#1a5c52'},
    'Larashoofd_role': {'type':'role','label':'Larashoofd','color':'#c0542a'},
    'Panghoeloe_role': {'type':'role','label':'Panghoeloe','color':'#d4962e'},
    'Koeriahoofd_role': {'type':'role','label':'Koeriahoofd','color':'#888780'},
    'Vereeniging': {'type':'institution','label':'Vereeniging Minangkabau','color':'#534AB7'},
}
for nid, attrs in institutions.items():
    G.add_node(nid, **attrs)

# Add person + location nodes and edges
for _, r in records_df.iterrows():
    pid = re.sub(r'[^a-z0-9]','_', r['name'].lower()[:30])
    
    if not G.has_node(pid):
        G.add_node(pid, type='person', label=r['name'][:50], 
                   adat_title=r['adat_title'], year_first=r['year'])
    
    # Person → Role
    role_map = {'larashoofd':'Larashoofd_role','panghoeloe':'Panghoeloe_role',
                'koeriahoofd':'Koeriahoofd_role','panghoeloe kapala':'Panghoeloe_role'}
    if r['role'] in role_map:
        G.add_edge(pid, role_map[r['role']], edge_type='has_role', year=r['year'])
    
    # Person → Location
    if r['location'] != 'unknown' and len(r['location']) > 2:
        lid = 'loc_' + re.sub(r'[^a-z0-9]','_', r['location'].lower()[:20])
        if not G.has_node(lid):
            G.add_node(lid, type='location', label=r['location'][:35])
        G.add_edge(pid, lid, edge_type='governs', year=r['year'])
    
    # Person → Education institutions
    if r['edu_kweekschool']: G.add_edge(pid, 'KweekschoolFdK', edge_type='edu_link', year=r['year'])
    if r['edu_schoolcommissie']: G.add_edge(pid, 'Schoolcommissie', edge_type='edu_link', year=r['year'])

print(f"Graf: {G.number_of_nodes()} node, {G.number_of_edges()} edge")
print(f"Komponen terhubung (undirected): {nx.number_connected_components(G.to_undirected())}")

# Degree analysis
in_deg = dict(G.in_degree())
out_deg = dict(G.out_degree())

print(f"\nTop 10 node berdasarkan in-degree:")
for nid, d in sorted(in_deg.items(), key=lambda x:-x[1])[:10]:
    print(f"  {G.nodes[nid].get('label',nid)[:45]} → in={d}")

print(f"\nTop 10 person berdasarkan out-degree (paling banyak koneksi):")
person_nodes = [(nid, d) for nid, d in out_deg.items() if G.nodes[nid].get('type')=='person']
for nid, d in sorted(person_nodes, key=lambda x:-x[1])[:10]:
    n = G.nodes[nid]
    print(f"  {n.get('label',nid)[:45]} ({n.get('adat_title','?')}): {d} koneksi")

# ─── 4. NETWORK METRICS ───
print()
print("=" * 60)
print("4. METRIK JEJARING")
print("=" * 60)

G_undir = G.to_undirected()
# Only on largest connected component for metrics
largest_cc = max(nx.connected_components(G_undir), key=len)
G_lcc = G_undir.subgraph(largest_cc)

print(f"Komponen terbesar: {len(largest_cc)} node")
print(f"Density: {nx.density(G_lcc):.4f}")

# Betweenness centrality on LCC
print("\nMenghitung betweenness centrality...")
bc = nx.betweenness_centrality(G_lcc, normalized=True, k=min(100, len(G_lcc)))
top_bc = sorted(bc.items(), key=lambda x:-x[1])[:10]
print("Top 10 betweenness centrality:")
for nid, c in top_bc:
    print(f"  {G.nodes.get(nid,{}).get('label',nid)[:45]}: {c:.4f}")

# ─── 5. TEMPORAL ANALYSIS ───
print()
print("=" * 60)
print("5. ANALISIS TEMPORAL (per dekade)")
print("=" * 60)

print(f"{'Dekade':<10} {'Tokoh':>8} {'Edu (%)':>10} {'Sekolahcommissie':>18} {'Kweekschool':>13}")
print("-" * 62)
for decade in sorted(records_df['decade'].unique()):
    if decade < 1870 or decade > 1914: continue
    sub = records_df[records_df['decade']==decade]
    persons = sub['name'].nunique()
    edu_pct = sub['has_edu'].mean()*100
    sc = sub['edu_schoolcommissie'].sum()
    kw = sub['edu_kweekschool'].sum()
    print(f"  {decade}s{'':<6} {persons:>6}   {edu_pct:>8.1f}%   {sc:>14}   {kw:>11}")

# ─── 6. GEPHI EXPORT ───
print()
print("=" * 60)
print("6. EXPORT")
print("=" * 60)

# Export CSV for Gephi
nodes_out = []
for nid, attrs in G.nodes(data=True):
    nodes_out.append({
        'Id': nid, 'Label': attrs.get('label', nid)[:50],
        'Type': attrs.get('type','unknown'),
        'Adat_Title': attrs.get('adat_title',''),
        'Year_First': attrs.get('year_first',0),
    })
pd.DataFrame(nodes_out).to_csv('network_nodes.csv', index=False, encoding='utf-8')

edges_out = []
for src, tgt, attrs in G.edges(data=True):
    edges_out.append({'Source':src, 'Target':tgt, 
                      'Type':attrs.get('edge_type',''), 'Year':attrs.get('year',0)})
pd.DataFrame(edges_out).to_csv('network_edges.csv', index=False, encoding='utf-8')
pd.DataFrame(records).to_csv('larashoofd_records.csv', index=False, encoding='utf-8')

print("✓ network_nodes.csv — node list (Gephi compatible)")
print("✓ network_edges.csv — edge list (Gephi compatible)")
print("✓ larashoofd_records.csv — all extracted records")
print()
print("Jalankan dengan: python larashoofd_network.py")
print("Untuk visualisasi lanjutan, import CSV ke Gephi atau Cytoscape.")

# ─── 7. QUICK MATPLOTLIB PLOT ───
try:
    print()
    print("=" * 60)
    print("7. VISUALISASI RINGKAS")
    print("=" * 60)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor('#1a1410')
    for ax in axes: ax.set_facecolor('#1a1410')
    
    # Plot 1: Adat title distribution
    adat_counts = records_df['adat_title'].value_counts()
    colors_adat = ['#c0542a','#1a5c52','#7F77DD','#185FA5','#d4962e','#5F5E5A','#639922','#888780']
    axes[0].bar(range(len(adat_counts)), adat_counts.values, color=colors_adat[:len(adat_counts)])
    axes[0].set_xticks(range(len(adat_counts)))
    axes[0].set_xticklabels(adat_counts.index, rotation=45, ha='right', color='#ede6d8', fontsize=9)
    axes[0].set_title('Distribusi Gelar Adat', color='#ede6d8', fontsize=11, pad=10)
    axes[0].tick_params(colors='#ede6d8')
    axes[0].spines[:].set_color('#3d3228')
    for label in axes[0].get_yticklabels(): label.set_color('#7a6a5a')
    
    # Plot 2: Temporal trend
    decade_stats = records_df.groupby('decade').agg(
        total=('name','count'), edu_connected=('has_edu','sum')).reset_index()
    decade_stats = decade_stats[(decade_stats['decade'] >= 1870) & (decade_stats['decade'] <= 1914)]
    x = range(len(decade_stats))
    axes[1].bar([i+0.2 for i in x], decade_stats['total'], width=0.4, color='#c0542a', alpha=0.8, label='Total')
    axes[1].bar([i-0.2 for i in x], decade_stats['edu_connected'], width=0.4, color='#1a5c52', alpha=0.8, label='+ Edu')
    axes[1].set_xticks(list(x))
    axes[1].set_xticklabels([f"{int(d)}s" for d in decade_stats['decade']], color='#ede6d8', fontsize=9)
    axes[1].set_title('Tokoh per Dekade & Koneksi Edu', color='#ede6d8', fontsize=11, pad=10)
    axes[1].legend(facecolor='#3d3228', labelcolor='#ede6d8', fontsize=8)
    axes[1].tick_params(colors='#ede6d8'); axes[1].spines[:].set_color('#3d3228')
    for label in axes[1].get_yticklabels(): label.set_color('#7a6a5a')
    
    # Plot 3: Network subgraph (edu-connected persons only)
    edu_persons = [nid for nid, attrs in G.nodes(data=True) 
                   if attrs.get('type')=='person' and G.has_edge(nid, 'Schoolcommissie')]
    edu_subgraph_nodes = set(edu_persons) | {'Schoolcommissie','KweekschoolFdK','Larashoofd_role'}
    SG = G.subgraph(edu_subgraph_nodes).to_undirected()
    
    if len(SG.nodes) > 2:
        pos = nx.spring_layout(SG, seed=42, k=1.5)
        node_colors = []
        for nid in SG.nodes():
            t = G.nodes[nid].get('type','')
            if t == 'institution': node_colors.append('#8b3a1e')
            elif t == 'role': node_colors.append('#d4962e')
            else: node_colors.append(G.nodes[nid].get('color','#c0542a'))
        nx.draw(SG, pos, ax=axes[2], node_color=node_colors, 
                node_size=80, edge_color='#3d3228', width=0.5, 
                with_labels=False, arrows=False)
        axes[2].set_title('Subgraf: Tokoh–Komisie Sekolah', color='#ede6d8', fontsize=11, pad=10)
    
    plt.tight_layout(pad=2)
    plt.savefig('larashoofd_network_analysis.png', dpi=150, bbox_inches='tight',
                facecolor='#1a1410', edgecolor='none')
    print("✓ larashoofd_network_analysis.png")
    plt.close()
    
except Exception as e:
    print(f"Matplotlib plot skipped: {e}")

print()
print("=" * 60)
print("SELESAI — Jejaring larashoofd & elite lokal Minangkabau")
print(f"  {records_df['name'].nunique()} tokoh | {records_df['location'].nunique()} lokasi")
print(f"  {records_df['has_edu'].sum()} koneksi ke sistem pendidikan")
print("=" * 60)
