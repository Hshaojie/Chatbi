import xml.etree.ElementTree as ET
from collections import defaultdict

tree = ET.parse(r"D:\ChatBIAgent-main\resume_convert\source.xml")
root = tree.getroot()
fonts = {}
for fs in root.iter("fontspec"):
    fonts[fs.get("id")] = (float(fs.get("size")), fs.get("family"), fs.get("color"))

page = root.find("page")
items = []
for t in page.findall("text"):
    top = float(t.get("top"))
    left = float(t.get("left"))
    font = t.get("font")
    size, family, color = fonts[font]
    bold = t.find("b") is not None
    text = "".join(t.itertext())
    items.append({"top": top, "left": left, "size": size, "family": family,
                  "bold": bold, "text": text, "width": float(t.get("width"))})

items.sort(key=lambda x: (x["top"], x["left"]))
lines = []
for it in items:
    for ln in lines:
        if abs(ln["top"] - it["top"]) <= 7:
            ln["runs"].append(it)
            break
    else:
        lines.append({"top": it["top"], "runs": [it]})
lines.sort(key=lambda l: l["top"])

out = []
for i, ln in enumerate(lines):
    runs = sorted(ln["runs"], key=lambda r: r["left"])
    parts = []
    for r in runs:
        tag = "B" if r["bold"] else "r"
        parts.append(f"<{tag}{r['size']/1.5:.1f}@{r['left']/1.5:.1f}>{r['text']}")
    out.append(f"{i:02d} top={ln['top']/1.5:7.2f} | " + "".join(parts))

with open(r"D:\ChatBIAgent-main\resume_convert\runs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("lines:", len(lines))
