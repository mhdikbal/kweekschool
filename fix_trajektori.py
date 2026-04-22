import sys

with open('kweekschool_v3_final.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Timeline Padding
c = c.replace('margin:80px 0 60px', 'margin:80px 40px 60px')

# 2. Add Trajektori CSS right before timeline CSS
css = """
/* TRAJEKTORI PHOTO OVERLAY */
#trajektori{position:relative;}
#trajektori::after{content:'';position:absolute;top:-20px;right:-20px;bottom:-20px;width:600px;background:url('murid2-kweekschool-fort-de-kock.jpg') center 20%/cover no-repeat;opacity:.4;mask-image:linear-gradient(to left,rgba(0,0,0,0.85) 0%,transparent 100%);-webkit-mask-image:linear-gradient(to left,rgba(0,0,0,0.85) 0%,transparent 100%);pointer-events:none;filter:grayscale(1) sepia(0.2) contrast(1.2);z-index:0;}
#trajektori > *{position:relative;z-index:1}

"""
c = c.replace('/* HORIZONTAL TIMELINE SCROLL */', css + '/* HORIZONTAL TIMELINE SCROLL */')

# 3. Add ID trajektori to the wrapper
c = c.replace('<!-- TRAJECTORY CARDS -->\n  <div class="fade-in">', '<!-- TRAJECTORY CARDS -->\n  <div id="trajektori" class="fade-in">')

# 4. Push 1858 from 4% to 8% to give it more room
c = c.replace('        <!-- 1858 -->\n        <div style="position:absolute;left:4%;top:4px">', '        <!-- 1858 -->\n        <div style="position:absolute;left:8%;top:4px">')

with open('kweekschool_v3_final.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Success')
