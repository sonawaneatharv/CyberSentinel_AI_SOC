import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for i in range(25, 55):
    p = doc.paragraphs[i]
    print(f"P{i:03d} [{p.style.name}] (align={p.alignment}): '{p.text.strip()}'")
