import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for i in range(30, 49):
    p = doc.paragraphs[i]
    print(f"P{i:02d}: '{p.text}'")
