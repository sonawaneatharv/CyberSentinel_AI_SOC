import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for idx in [32, 46, 47]:
    p = doc.paragraphs[idx]
    exts = p._p.xpath('.//*[local-name()="extent"]')
    if not exts:
        exts = p._p.xpath('.//*[local-name()="ext"]')
    print(f"P{idx}: exts={len(exts)}")
    for e in exts:
        print(f"  attribs: {e.attrib}")
