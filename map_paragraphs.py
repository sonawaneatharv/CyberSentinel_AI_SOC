import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if text or 'drawing' in p._p.xml or 'oMath' in p._p.xml:
        # Check if drawing or oMath
        flags = []
        if 'drawing' in p._p.xml: flags.append('IMG')
        if 'oMath' in p._p.xml: flags.append('MATH')
        flag_str = f"[{','.join(flags)}]" if flags else ""
        print(f"P{i:03d} {flag_str} [{p.style.name}] (align={p.alignment}): {text[:75]}")
