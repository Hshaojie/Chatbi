import re, zlib, sys

data = open(r"D:\ChatBIAgent-main\resume_convert\source.pdf", "rb").read()

# decompress all FlateDecode streams and look for text operators
for m in re.finditer(rb"stream\r?\n", data):
    start = m.end()
    end = data.find(b"endstream", start)
    raw = data[start:end]
    try:
        dec = zlib.decompress(raw)
    except Exception:
        continue
    if b"Tf" in dec and (b"Tj" in dec or b"TJ" in dec):
        text = dec.decode("latin-1")
        # report Tf operators and Tm matrices
        print("--- stream len", len(text))
        tf = re.findall(r"/([A-Za-z0-9+\-]+)\s+([\d.]+)\s+Tf", text)
        print("Tf:", tf[:20])
        tm = re.findall(r"([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+Tm", text)
        print("Tm sample:", tm[:10])
        break
