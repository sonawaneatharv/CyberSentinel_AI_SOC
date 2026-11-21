import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for i, p in enumerate(doc.paragraphs):
    if 'drawing' in p._p.xml:
        print(f"P{i:03d} has drawing! Text: '{p.text.strip()}'")
    if p.text.strip().startswith('Fig.') or p.text.strip().startswith('Figure'):
        print(f"P{i:03d} figure caption: '{p.text.strip()}'")
