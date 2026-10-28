from PIL import Image
import numpy as np

def segs(path, y0pt, y1pt, gap=6):
    im = np.array(Image.open(path).convert("L"))
    m = im[int(y0pt * 2):int(y1pt * 2)] < 128
    cols = m.any(axis=0)
    out = []
    s = None
    for x in range(len(cols)):
        if cols[x] and s is None:
            s = x
        elif not cols[x] and s is not None:
            out.append((s, x - 1))
            s = None
    if s is not None:
        out.append((s, len(cols) - 1))
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] < gap * 2:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return [(round(a / 2, 1), round(b / 2, 1)) for a, b in merged]

o = r"D:\ChatBIAgent-main\resume_convert\orig144-1.png"
n = r"D:\ChatBIAgent-main\.dsh-office-70eefc3ba13a4f58a636bfbb6c1f1200\render\page-0001.png"
for label, band in [("contact", (74, 88)), ("edu1", (115, 128)), ("entry1", (176, 192)),
                    ("entry2", (471, 485)), ("bullet1 line1", (255, 268))]:
    print(label)
    print("  orig", segs(o, *band))
    print("  new ", segs(n, *band))
