import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for i, p in enumerate(doc.paragraphs):
    blips = p._p.xpath('.//a:blip')
    if blips:
        rIds = [b.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed') for b in blips]
        print(f"P{i:03d} has image! rId={rIds}, text='{p.text.strip()}'")

for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith('Fig.') or p.text.strip().startswith('Figure'):
        print(f"Caption P{i:03d}: '{p.text.strip()}'")
