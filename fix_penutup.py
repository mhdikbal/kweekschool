import sys

with open('kweekschool_v3_final.html', 'r', encoding='utf-8') as f:
    c = f.read()

# CSS for Penutup Overlay
css = """
/* PENUTUP OVERLAY */
#penutup-box{position:relative;overflow:hidden;z-index:1;}
#penutup-box::after{content:'';position:absolute;top:0;right:0;bottom:0;width:350px;background:url('tokoh_pergerakan_collage.png') center center/cover no-repeat;opacity:.4;mask-image:linear-gradient(to left,rgba(0,0,0,1) 0%,rgba(0,0,0,.8) 40%,transparent 100%);-webkit-mask-image:linear-gradient(to left,rgba(0,0,0,1) 0%,rgba(0,0,0,.8) 40%,transparent 100%);pointer-events:none;filter:grayscale(100%) sepia(.2) contrast(1.1);z-index:0;}
#penutup-box > *{position:relative;z-index:1}
"""

c = c.replace('/* TRAJEKTORI PHOTO OVERLAY */', css + '\n/* TRAJEKTORI PHOTO OVERLAY */')

# Add id to the penutup box
c = c.replace('<!-- PENUTUP -->\n  <div class="fade-in" style="margin-top:3rem;', '<!-- PENUTUP -->\n  <div id="penutup-box" class="fade-in" style="margin-top:3rem;')

with open('kweekschool_v3_final.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Penutup overlay added!')
