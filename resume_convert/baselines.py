import re, zlib

data = open(r"D:\ChatBIAgent-main\resume_convert\source.pdf", "rb").read()
stream = None
for m in re.finditer(rb"stream\r?\n", data):
    start = m.end()
    end = data.find(b"endstream", start)
    try:
        dec = zlib.decompress(data[start:end])
    except Exception:
        continue
    if b"BT" in dec and b"Tf" in dec:
        stream = dec.decode("latin-1")
        break

# tokenize text objects and find Tm y baselines with font size
ys = []
cur_size = None
for tm in re.finditer(r"/(F\d+)\s+([\d.]+)\s+Tf|([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+Tm", stream):
    if tm.group(1):
        cur_size = float(tm.group(2))
    else:
        y = float(tm.group(7))
        ys.append((round(y, 2), cur_size))

ys_sorted = sorted(set(y for y, _ in ys), reverse=True)
print("num distinct baselines:", len(ys_sorted))
diffs = [round(ys_sorted[i] - ys_sorted[i+1], 2) for i in range(len(ys_sorted)-1)]
print("diffs:", diffs)
