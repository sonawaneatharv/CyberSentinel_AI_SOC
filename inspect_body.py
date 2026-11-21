import docx
from docx.oxml import OxmlElement

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

body = doc._body._element
print("Total child elements in body:", len(body))

elements = []
for child in body:
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        p = docx.text.paragraph.Paragraph(child, doc)
        t = p.text.strip()
        if t:
            elements.append(('p', p.style.name, t[:50]))
    elif tag == 'tbl':
        tbl = docx.table.Table(child, doc)
        elements.append(('tbl', len(tbl.rows), len(tbl.columns)))
    elif tag == 'sectPr':
        elements.append(('sectPr',))

print(f"Parsed {len(elements)} items. First 25 items:")
for idx, item in enumerate(elements[:25]):
    print(f"  {idx:2d}: {item}")

print("...")
for idx, item in enumerate(elements[50:], start=50):
    print(f"  {idx:2d}: {item}")
