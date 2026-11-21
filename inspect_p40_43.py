import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

with open("p40_xml.xml", "w", encoding="utf-8") as f:
    f.write(doc.paragraphs[40]._p.xml)

with open("p43_xml.xml", "w", encoding="utf-8") as f:
    f.write(doc.paragraphs[43]._p.xml)

print("Saved P40 and P43 XML.")
