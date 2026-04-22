import os
import shutil

images = [
    "Bagindo_Dahlan_Abdullah.jpg",
    "Engku-Nawawi--IST_ratio-16x9.jpg",
    "Kweekschoollogo.png",
    "NL-HaNA_4.MIKO_1372.1-groot.jpg",
    "Tan_Malaka.png",
    "babv.jpg",
    "hatta.jpg",
    "murid2-kweekschool-fort-de-kock-1888-nawawi-kramer-1908-p-26.webp",
    "tokoh_pergerakan_collage.png"
]

if not os.path.exists("img"):
    os.makedirs("img")

html_files = ["index.html", "kweekschool_v3_final.html", "larashoofd_network.html", "kweekschool_network_mapping.html"]

for html_file in html_files:
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        for img in images:
            content = content.replace(f"'{img}'", f"'img/{img}'")
            content = content.replace(f'"{img}"', f'"img/{img}"')
            content = content.replace(f"url({img})", f"url(img/{img})")
            content = content.replace(f"url('{img}')", f"url('img/{img}')")
            content = content.replace(f'url("{img}")', f'url("img/{img}")')
        
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {html_file}")

for img in images:
    if os.path.exists(img):
        shutil.move(img, os.path.join("img", img))
        print(f"Moved {img} to img/")

print("Done!")
