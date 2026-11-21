import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

print(f"Total sections: {len(doc.sections)}")
for i, s in enumerate(doc.sections):
    print(f"Section {i}: start_type={s.start_type}, cols={s._sectPr.xpath('./w:cols/@w:num')}")

print("\n--- STYLES AND PARAGRAPHS ---")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        runs_info = []
        for r in p.runs[:3]:
            fn = r.font.name
            fs = r.font.size.pt if r.font.size else "def"
            b = r.bold
            it = r.italic
            runs_info.append(f"{fn}/{fs}/b={b}/i={it}")
        print(f"P{i:03d} [{p.style.name}] (align={p.alignment}) runs={runs_info} text: {p.text[:65]}")

print("\n--- TABLES ---")
for i, t in enumerate(doc.tables):
    print(f"Table {i}: rows={len(t.rows)}, cols={len(t.columns)}, style={t.style.name}")
    for r_idx, r in enumerate(t.rows[:3]):
        row_text = [c.text.strip().replace('\n', ' ') for c in r.cells]
        print(f"  Row {r_idx}: {row_text}")
