import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_review_guide():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    NAVY = RGBColor(26, 54, 93)       # Primary #1A365D
    CYAN = RGBColor(2, 132, 199)      # Accent #0284C7
    TEXT_COLOR = RGBColor(31, 41, 55) # Neutral Dark #1F2937
    DARK_RED = RGBColor(185, 28, 28)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_callout(text, bold_prefix="💡 KEY TAKEAWAY:", border_color="0284C7", bg_color="EFF6FF"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.8)
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="28" w:space="0" w:color="{border_color}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix + " ")
            r_bold.bold = True
            r_bold.font.color.rgb = CYAN if border_color == "0284C7" else DARK_RED
            r_bold.font.name = 'Calibri'
            r_bold.font.size = Pt(10.5)
        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        r_text.font.name = 'Calibri'
        r_text.font.color.rgb = TEXT_COLOR
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_heading_1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = NAVY
        run.font.name = 'Calibri'
        return p

    def add_heading_2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = CYAN
        run.font.name = 'Calibri'
        return p

    def add_heading_3(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = NAVY
        run.font.name = 'Calibri'
        return p

    def add_body_p(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix + " ")
            r_b.bold = True
            r_b.font.color.rgb = TEXT_COLOR
            r_b.font.name = 'Calibri'
            r_b.font.size = Pt(10.5)
        r = p.add_run(text)
        r.font.color.rgb = TEXT_COLOR
        r.font.name = 'Calibri'
        r.font.size = Pt(10.5)
        return p

    # TITLE
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("🎓 CYBER SENTINEL: ML & DATASET REVIEW GUIDE")
    r_t.bold = True
    r_t.font.size = Pt(22)
    r_t.font.color.rgb = NAVY
    r_t.font.name = 'Calibri'

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_sub.add_run("Master Defense Sheet on Machine Learning Models, Training Pipelines, and Dataset Engineering\n(Explained in Intuitive, Non-Mathematical Plain English)")
    r_s.font.size = Pt(12)
    r_s.font.color.rgb = CYAN
    r_s.font.italic = True
    r_s.font.name = 'Calibri'

    add_callout(
        "Faculty members love asking detailed questions about the dataset, feature preprocessing, model selection, "
        "and evaluation metrics. This guide gives you the exact questions they will ask and the exact answers to speak. "
        "You don't need to know complex math—just understand the concepts explained below!",
        bold_prefix="🎯 PURPOSE OF THIS GUIDE:"
    )

    # ==========================================
    # PART 1: THE DATASET
    # ==========================================
    add_heading_1("PART 1: The Dataset — Everything You Need to Know")

    add_heading_2("1. What dataset did you use?")
    add_body_p(
        "We used the industry-benchmark CICIDS2017 dataset distribution (created by the Canadian Institute for Cybersecurity). "
        "It is the global academic standard for testing Intrusion Detection Systems because it captures realistic background traffic "
        "(HTTP, HTTPS, DNS, SSH) along with modern attack scenarios.",
        bold_prefix="Short Answer to Speak:"
    )

    add_heading_2("2. How many samples and what is the distribution?")
    add_body_p(
        "Our dataset contains 35,000 total bidirectional network flow records, structured to reflect realistic enterprise traffic where the vast majority of network traffic is normal:"
    )
    add_body_p("• Benign (Normal Traffic): ~65% (22,750 flows) — browsing web, streaming, DNS, normal office traffic.\n"
               "• DoS (Denial of Service): ~14% (4,900 flows) — SYN flood and connection exhaustion attacks.\n"
               "• PortScan (Reconnaissance): ~10% (3,500 flows) — rapid sweeps across port numbers.\n"
               "• BruteForce (Credential Theft): ~6% (2,100 flows) — rapid login hammering against SSH/FTP.\n"
               "• Botnet (C2 Command & Control): ~4% (1,400 flows) — periodic malware beaconing.\n"
               "• Zero-Day Unknown Anomalies: 200 holdout flows reserved strictly for testing unsupervised anomaly detection.")

    add_heading_2("3. What are the 20 Features? (What did the AI actually look at?)")
    add_body_p(
        "Instead of reading raw text inside packets (which is encrypted anyway in HTTPS), our model looks at 20 statistical flow metadata features:",
        bold_prefix="Feature Engineering:"
    )
    add_body_p(
        "1. Destination_Port: Which service door was targeted (e.g. 80, 443, 22)?\n"
        "2. Flow_Duration: How long did the connection last (in microseconds)?\n"
        "3. Total_Fwd_Packets: How many packets went from client to server?\n"
        "4. Total_Backward_Packets: How many reply packets returned from server?\n"
        "5. Total_Length_of_Fwd_Packets: Total bytes sent forward.\n"
        "6. Total_Length_of_Bwd_Packets: Total bytes received back.\n"
        "7. Fwd_Packet_Length_Max: Biggest forward packet size.\n"
        "8. Fwd_Packet_Length_Min: Smallest forward packet size.\n"
        "9. Fwd_Packet_Length_Mean: Average size of forward packets.\n"
        "10. Bwd_Packet_Length_Mean: Average size of response packets.\n"
        "11. Flow_Bytes_s: Data throughput rate (bytes per second).\n"
        "12. Flow_Packets_s: Packet velocity (packets per second — critical for DoS!).\n"
        "13. Flow_IAT_Mean: Average Inter-Arrival Time between packets (time gap).\n"
        "14. Flow_IAT_Std: Standard deviation (jitter) of time gaps between packets (critical for Botnets!).\n"
        "15. SYN_Flag_Count: Count of connection request flags.\n"
        "16. RST_Flag_Count: Count of connection reset/abort flags.\n"
        "17. PSH_Flag_Count: Count of push flags (immediate data delivery).\n"
        "18. ACK_Flag_Count: Count of acknowledgment flags.\n"
        "19. Average_Packet_Size: Overall average payload size.\n"
        "20. Init_Win_bytes_forward: Initial TCP buffer window size."
    )

    add_heading_2("4. What Preprocessing was applied?")
    add_body_p(
        "1. Train/Test Split: 80% Training (28,000 flows) and 20% Testing (7,000 flows), stratified to maintain class ratios.\n"
        "2. StandardScaler Normalization: Network features have wildly different ranges (Flow_Duration is in millions of microseconds, while SYN_Flag is just 0 or 1). StandardScaler transforms all features so they have a mean of 0 and variance of 1. This prevents large numbers from overpowering small numbers in the math!\n"
        "3. Removed IP Addresses from Training Features: We intentionally DID NOT give IP addresses to the ML models. If an ML model learns 'IP 192.168.1.100 is bad', it will fail the moment the attacker changes their IP (called Data Leakage / Overfitting). Our models learn purely from traffic behavior, not IP identity!"
    )

    # ==========================================
    # PART 2: MACHINE LEARNING MODELS
    # ==========================================
    add_heading_1("PART 2: The Machine Learning Pipeline")

    add_heading_2("1. The 3-Stage Architecture (Why Not Just 1 Model?)")
    add_body_p(
        "• Stage 1 (Binary Gatekeeper - LightGBM): Ultra-fast binary classifier (Safe vs Malicious). Takes 0.0014 milliseconds. Over 95% of enterprise traffic is safe, so Stage 1 approves it immediately without wasting CPU.\n"
        "• Stage 2 (Multi-Class Specialist - LightGBM / XGBoost): Only examines flows flagged by Stage 1. Pinpoints the exact attack: DoS, PortScan, BruteForce, or Botnet.\n"
        "• Stage 3 (Zero-Day Anomaly Engine - Isolation Forest): Trained strictly on normal benign traffic. If an attack arrives that Stage 1 and 2 have never seen, Stage 3 isolates it based on abnormal statistical reconstruction deviation and assigns an Anomaly Score (0% to 100%)."
    )

    add_heading_2("2. Why LightGBM? (What is it?)")
    add_body_p(
        "LightGBM stands for Light Gradient Boosting Machine (developed by Microsoft). "
        "It builds an ensemble of Decision Trees. Unlike traditional decision trees that split level-by-level, "
        "LightGBM uses 'leaf-wise' tree growth with histogram binning. This makes it 10 to 15 times faster to train "
        "and gives sub-millisecond inference latencies (0.0014 ms per packet), making it ideal for high-speed network monitoring.",
        bold_prefix="Simple Explanation:"
    )

    add_heading_2("3. Why Isolation Forest for Zero-Day Attacks? (How does it work?)")
    add_body_p(
        "Isolation Forest is an Unsupervised Learning algorithm. "
        "Think of it like cutting up a cake: normal benign traffic points are bunched up tightly together in the center. "
        "To isolate a normal point, you have to make many random cuts (deep path length). "
        "Anomalous attack points stick out all by themselves on the edges, so they get isolated in very few random cuts (short path length). "
        "Therefore: Fewer cuts to isolate = High Anomaly Score!",
        bold_prefix="Cake Cutting Analogy:"
    )

    add_heading_2("4. Academic Benchmark Results (The 4 Models Compared)")
    add_body_p("During our experiments, we benchmarked four major algorithms on the exact same test dataset:")

    benchmark_data = [
        ("LightGBM (Our Champion)", "100.0%", "100.0%", "100.0%", "0.0014 ms", "0.25 sec", "Fastest gradient booster, 100% recall, ideal for live lines."),
        ("XGBoost", "99.99%", "99.96%", "100.0%", "0.0009 ms", "0.38 sec", "High performance, slightly slower training time."),
        ("Random Forest", "99.99%", "100.0%", "99.96%", "0.0054 ms", "0.42 sec", "Nearly 4x higher latency than LightGBM."),
        ("Decision Tree", "99.90%", "99.74%", "99.96%", "0.0002 ms", "0.34 sec", "Fastest, but lowest accuracy and prone to overfitting.")
    ]

    tbl = doc.add_table(rows=1, cols=7)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    col_widths = [Inches(1.5), Inches(0.8), Inches(0.8), Inches(0.8), Inches(1.0), Inches(0.9), Inches(1.0)]
    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    hdr = tbl.rows[0].cells
    hdr_titles = ["Model", "Accuracy", "Precision", "Recall", "Latency/Flow", "Train Time", "Verdict"]
    for i, t in enumerate(hdr_titles):
        set_cell_background(hdr[i], "1A365D")
        set_cell_margins(hdr[i], top=100, bottom=100, left=80, right=80)
        p = hdr[i].paragraphs[0]
        r = p.add_run(t)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (m_name, acc, prec, rec, lat, t_time, verd) in enumerate(benchmark_data):
        row = tbl.add_row().cells
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for i, val in enumerate([m_name, acc, prec, rec, lat, t_time, verd]):
            set_cell_background(row[i], bg)
            set_cell_margins(row[i], top=80, bottom=80, left=80, right=80)
            p = row[i].paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if i == 0:
                r.bold = True
                r.font.color.rgb = NAVY
            else:
                r.font.color.rgb = TEXT_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================================
    # PART 3: TOP 10 FACULTY VIVA QUESTIONS ON ML & DATASET
    # ==========================================
    add_heading_1("PART 3: Top 10 Faculty Viva Questions & Winning Answers")

    qna = [
        (
            "Q1: 'Which evaluation metric is the most critical in cybersecurity: Accuracy, Precision, or Recall?'",
            "A1: 'Recall (Sensitivity) is the most critical! In cybersecurity, a False Negative (letting a real hacker slip through unnoticed) is catastrophic. A False Positive (briefly questioning an innocent user) is merely a minor annoyance. Therefore, our model is tuned to prioritize 100% Recall so that zero attacks are missed.'"
        ),
        (
            "Q2: 'Why did you not use Deep Learning like LSTM, CNN, or Transformers?'",
            "A2: 'Deep Learning models require heavy matrix multiplications and GPUs. They introduce 10 to 50 milliseconds of inference latency, which causes severe packet buffer overflows on 1 Gbps enterprise networks. Furthermore, tabular flow data has no spatial or grammatical structure like images or text. Tree-based models like LightGBM consistently outperform Deep Learning on tabular data while running in just 0.0014 milliseconds on commodity CPUs.'"
        ),
        (
            "Q3: 'How did you prevent Overfitting in your models?'",
            "A3: 'We used 4 specific techniques: (1) We withheld 20% of the data as a strict unseen test set using stratified splitting. (2) We stripped IP addresses and timestamps from features so the model cannot memorize identities. (3) In LightGBM, we constrained num_leaves=31 and set learning_rate=0.08 to prevent memorization. (4) We benchmarked on a completely separate zero-day holdout reservoir.'"
        ),
        (
            "Q4: 'What is the purpose of StandardScaler, and would tree models still work without it?'",
            "A4: 'Decision trees and LightGBM are invariant to monotonic scale changes, but Stage 3 (Isolation Forest) and our feature attribution engine rely on Euclidean and statistical variance distances. Normalizing via StandardScaler (mean=0, variance=1) ensures consistent anomaly scoring across features with wildly different units like microseconds versus binary flags.'"
        ),
        (
            "Q5: 'How does your system handle Class Imbalance?'",
            "A5: 'In real networks, benign traffic vastly outnumbers attack traffic. We handled this by: (1) Using Stratified Train-Test splitting to preserve class proportions. (2) Decoupling binary filtering from multi-class classification so the rare attack classes only compete against each other in Stage 2, not against the overwhelming benign majority. (3) Evaluating using F1-score and Recall rather than raw accuracy.'"
        ),
        (
            "Q6: 'What is the difference between Supervised and Unsupervised Learning in your project?'",
            "A6: 'Stages 1 and 2 are Supervised: they were trained on labeled historical data to recognize known patterns (DoS, PortScan, etc.). Stage 3 (Isolation Forest) is Unsupervised: it was trained with ZERO attack labels—only normal data. It flags threats purely because their statistical distribution deviates from normal behavior, allowing us to catch unknown zero-day attacks.'"
        ),
        (
            "Q7: 'What is Explainable AI (XAI) and why is it needed?'",
            "A7: 'Standard ML algorithms are black boxes that just output a prediction number. In an enterprise SOC, human analysts cannot act on an alert without knowing why. Our XAI engine uses SHAP-inspired feature attribution to output the top 3 drivers (e.g. Flow_Packets_s was 45x normal baseline, SYN flag hammering detected) so the analyst can verify the threat in seconds.'"
        ),
        (
            "Q8: 'Why did you select these specific 20 features out of the 80+ columns in CICIDS2017?'",
            "A8: 'Many columns in raw network captures are redundant, correlated, or noise. We selected 20 features that provide the highest signal-to-noise ratio across packet velocity (packets/sec), connection duration, TCP state flags (SYN, ACK, RST), and inter-arrival timing jitter, while keeping computational overhead minimal for line-rate inspection.'"
        ),
        (
            "Q9: 'What is Inter-Arrival Time (Flow_IAT_Std) and why is it important?'",
            "A9: 'Inter-Arrival Time is the time gap between consecutive packets. Human web browsing has random, unpredictable timing gaps (high jitter). In contrast, automated botnets and DoS scripts send packets with near-zero jitter (machine-gun speed) or fixed periodic intervals. A low Flow_IAT_Std is an immediate indicator of automated malware activity.'"
        ),
        (
            "Q10: 'Can an attacker evade your Machine Learning model by slowing down their attack (Low-and-Slow Attack)?'",
            "A10: 'Attackers who slow down avoid packet-rate triggers, but they increase Flow_Duration and alter the Total_Fwd_to_Bwd_Packets ratio. Our multi-feature model evaluates all 20 dimensions simultaneously, and our Stage 3 Isolation Forest flags the prolonged connection state as anomalous.'"
        )
    ]

    for q, a in qna:
        add_heading_3(q)
        add_body_p(a)

    # Save Word document
    out_path = os.path.join(os.path.dirname(__file__), "CyberSentinel_ML_and_Dataset_Review_Guide.docx")
    doc.save(out_path)
    print(f"[+] Successfully generated ML & Dataset Review Guide at: {out_path}")

if __name__ == "__main__":
    build_review_guide()
