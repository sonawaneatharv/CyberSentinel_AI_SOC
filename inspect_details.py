import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

print("Headers & Footers:")
for s_idx, s in enumerate(doc.sections):
    h = s.header
    f = s.footer
    print(f"  Section {s_idx} Header text: {[p.text for p in h.paragraphs if p.text.strip()]}")
    print(f"  Section {s_idx} Footer text: {[p.text for p in f.paragraphs if p.text.strip()]}")

print("\nParagraph formatting details for key elements:")
for p_idx in [0, 3, 9, 10, 11, 12, 13, 19, 23, 25, 27, 43, 67, 89, 101, 103, 104]:
    if p_idx < len(doc.paragraphs):
        p = doc.paragraphs[p_idx]
        pf = p.paragraph_format
        print(f"P{p_idx:03d} style={p.style.name} align={p.alignment} space_before={pf.space_before} space_after={pf.space_after} line_spacing={pf.line_spacing} text={p.text[:40]}")
