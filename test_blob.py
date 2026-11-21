import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for rId in ['rId9', 'rId10', 'rId11']:
    part = doc.part.related_parts[rId]
    print(f"{rId}: part={part}, content_type={part.content_type}, blob_len={len(part._blob)}")
    # test assigning
    old_len = len(part._blob)
    part._blob = part._blob
    print(f"Assign successful! old_len={old_len}")
