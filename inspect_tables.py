import docx

path = r'C:\Users\asus\.gemini\antigravity\brain\10ceb86f-7614-4f76-ba2f-d095afcd5396\.user_uploaded\media_1795213544881_c7378ab6.docx'
doc = docx.Document(path)

for t_idx, table in enumerate(doc.tables):
    print(f"\n=================== TABLE {t_idx} ===================")
    print(f"Rows: {len(table.rows)}, Cols: {len(table.columns)}")
    for r_idx, row in enumerate(table.rows):
        row_str = []
        for c_idx, cell in enumerate(row.cells):
            # Check font size and runs
            cell_texts = []
            for p in cell.paragraphs:
                for r in p.runs:
                    cell_texts.append(f"{r.text}(fs={r.font.size.pt if r.font.size else 'def'}, b={r.bold})")
            row_str.append(" ".join(cell_texts))
        print(f"Row {r_idx}: {' | '.join(row_str)}")
