import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for idx in [40, 43]:
    p = doc.paragraphs[idx]
    maths = p._p.xpath('.//*[local-name()="oMath"]')
    print(f"P{idx} has oMath: {len(maths)}")
    if maths:
        print("Text in oMath:", "".join(p._p.itertext()))
