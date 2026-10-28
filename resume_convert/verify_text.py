import re
import docx
import difflib

pdf = open(r"D:\ChatBIAgent-main\resume_convert\source_layout.txt", encoding="utf-8").read()
d = docx.Document(r"D:\ChatBIAgent-main\resume_convert\黄绍杰_简历_agent开发.docx")
doc = "\n".join(p.text for p in d.paragraphs)


def norm(s):
    return re.sub(r"\s+", "", s)


a, b = norm(pdf), norm(doc)
print("pdf chars", len(a), "doc chars", len(b))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
with open(r"D:\ChatBIAgent-main\resume_convert\content_diff.txt", "w", encoding="utf-8") as f:
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        f.write("%s\n  PDF: %r\n  DOC: %r\n" % (tag, a[i1:i2], b[j1:j2]))
print("diff written")
