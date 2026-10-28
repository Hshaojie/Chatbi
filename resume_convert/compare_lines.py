from PIL import Image
import numpy as np
import sys

def lines(path):
    im = np.array(Image.open(path).convert("L"))
    mask = im < 128
    rows = mask.sum(axis=1)
    out = []
    start = None
    for y in range(len(rows)):
        if rows[y] > 0 and start is None:
            start = y
        elif rows[y] == 0 and start is not None:
            out.append((start, y - 1))
            start = None
    if start is not None:
        out.append((start, len(rows) - 1))
    return out, mask

orig, _ = lines(r"D:\ChatBIAgent-main\resume_convert\orig144-1.png")
new, _ = lines(sys.argv[1])
print("orig lines", len(orig), "new lines", len(new))
print(f"{'#':>3} {'orig_top':>8} {'new_top':>8} {'delta':>7}")
for i in range(max(len(orig), len(new))):
    o = orig[i][0] / 2 if i < len(orig) else None
    n = new[i][0] / 2 if i < len(new) else None
    if o is not None and n is not None:
        print(f"{i:3d} {o:8.1f} {n:8.1f} {n-o:+7.1f}")
    else:
        print(f"{i:3d} {o} {n}")
