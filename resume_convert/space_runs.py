import xml.etree.ElementTree as ET

tree = ET.parse(r"D:\ChatBIAgent-main\resume_convert\source.xml")
root = tree.getroot()
fonts = {fs.get("id"): (float(fs.get("size")) / 1.5, fs.get("family")) for fs in root.iter("fontspec")}
items = []
for t in root.find("page").findall("text"):
    size, fam = fonts[t.get("font")]
    items.append({
        "top": float(t.get("top")) / 1.5,
        "left": float(t.get("left")) / 1.5,
        "width": float(t.get("width")) / 1.5,
        "size": size,
        "fam": fam,
        "text": "".join(t.itertext()),
    })
items.sort(key=lambda x: (x["top"], x["left"]))
lines = []
for it in items:
    if lines and abs(lines[-1]["top"] - it["top"]) <= 5.5:
        lines[-1]["items"].append(it)
    else:
        lines.append({"top": it["top"], "items": [it]})

for ln in lines:
    its = sorted(ln["items"], key=lambda x: x["left"])
    for i, r in enumerate(its):
        if r["text"].strip() == "":
            nxt = its[i + 1]["left"] if i + 1 < len(its) else r["left"] + r["width"]
            adv = nxt - r["left"]
            n = len(r["text"])
            print("top=%6.1f left=%6.1f size=%.1f nspace=%d advance=%5.2f per=%4.2f fam=%s next=%r" % (
                ln["top"], r["left"], r["size"], n, adv, adv / n, r["fam"][-14:],
                its[i + 1]["text"][:10] if i + 1 < len(its) else ""))
