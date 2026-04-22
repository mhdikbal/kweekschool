import re

with open(r"c:\Users\muhammad.ikbal\Downloads\Kweekschool\larashoofd_network.html", "r", encoding="utf-8") as f:
    text = f.read()

# Bug 1: resize fallback
text = text.replace(
    "W = canvas.width = wrap.offsetWidth;",
    "W = canvas.width = wrap.offsetWidth || window.innerWidth;"
)
text = text.replace(
    "H = canvas.height = wrap.offsetHeight;",
    "H = canvas.height = wrap.offsetHeight || window.innerHeight;"
)

# Bug 1: defer init()
text = text.replace(
    "window.addEventListener('load', init);",
    "window.addEventListener('load', () => requestAnimationFrame(() => requestAnimationFrame(init)));"
)

# Bug 2: border color
text = re.sub(
    r"--border:\s*rgba?\([^)]+\);\s*--border2:\s*rgba?\([^)]+\);",
    "--border: rgba(60, 50, 40, 0.12); --border2: rgba(60, 50, 40, 0.22);",
    text
)

# Bug 3: edge opacity adjustment for light bg
text = text.replace("'#2a8c7e44'", "'rgba(42, 140, 126, 0.6)'")
text = text.replace("'#c8bfaf33'", "'rgba(122, 110, 96, 0.4)'")
text = text.replace("'#c8bfaf'", "'#7a6e60'")

# Let's adjust the alpha hex generation base just in case
text = text.replace("Math.floor(a*255).toString(16).padStart(2,'0')", "Math.floor(a*200 + 55).toString(16).padStart(2,'0')")

# Bug 4: node fill opacity
text = text.replace(
    "ctx.fillStyle = n.color + (n.type==='location'?'55':'bb');",
    "ctx.fillStyle = n.color + (n.type==='location'?'77':'dd');"
)

with open(r"c:\Users\muhammad.ikbal\Downloads\Kweekschool\larashoofd_network.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Applied 4 bugfixes!")
