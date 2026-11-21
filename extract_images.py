import docx
import os

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

out_dir = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\extracted_template_images'
os.makedirs(out_dir, exist_ok=True)

for rel_id, rel in doc.part.rels.items():
    if "image" in rel.target_ref:
        img_part = rel.target_part
        filename = os.path.basename(rel.target_ref)
        out_path = os.path.join(out_dir, filename)
        with open(out_path, "wb") as f:
            f.write(img_part.blob)
        print(f"Saved {rel_id}: {filename} ({len(img_part.blob)} bytes)")
