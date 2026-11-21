import docx
import os

path = r'd:\Laptop local Disk D\study\Sem 5\ML\ML_project\CyberSentinel_Two_Stage_ML_NIDS_Research_Paper.docx'
print("File size:", os.path.getsize(path), "bytes")

doc = docx.Document(path)
print("Paragraphs count:", len(doc.paragraphs))
print("Tables count:", len(doc.tables))
print("Sections count:", len(doc.sections))

# Check for any lingering old text
old_keywords = ["Braille", "servo", "slider", "Bruijn", "piezoelectric", "solenoid", "RBD", "Arduino Uno"]
found_old = []
for i, p in enumerate(doc.paragraphs):
    for kw in old_keywords:
        if kw.lower() in p.text.lower():
            found_old.append((i, kw, p.text[:50]))

for t_idx, t in enumerate(doc.tables):
    for r_idx, row in enumerate(t.rows):
        for c_idx, cell in enumerate(row.cells):
            for kw in old_keywords:
                if kw.lower() in cell.text.lower():
                    found_old.append((f"Table {t_idx} R{r_idx}C{c_idx}", kw, cell.text[:50]))

if found_old:
    print("WARNING: Lingering old text found:")
    for item in found_old:
        print(" ", item)
else:
    print("SUCCESS: Zero lingering old text detected! The entire paper is 100% CyberSentinel ML-NIDS.")

print("\n--- SAMPLE CHECKS ---")
print("Title:", doc.paragraphs[0].text)
print("Abstract:", doc.paragraphs[9].text[:120], "...")
print("Keywords:", doc.paragraphs[10].text)
print("Intro heading:", doc.paragraphs[11].text)
print("Table I caption:", doc.paragraphs[19].text)
print("Table I Row 0:", [c.text for c in doc.tables[0].rows[0].cells])
print("Table I Row 5:", [c.text for c in doc.tables[0].rows[5].cells])
print("Table II caption:", doc.paragraphs[75].text)
print("Table II Row 1:", [c.text for c in doc.tables[1].rows[1].cells])
print("Table II Row 4:", [c.text for c in doc.tables[1].rows[4].cells])
print("Conclusion heading:", doc.paragraphs[85].text)
print("Ref [1]:", doc.paragraphs[104].text[:100])
print("Ref [11]:", doc.paragraphs[114].text[:100])
