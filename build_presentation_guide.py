import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_guide():
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Style definitions
    # Primary Palette: Deep Navy (#1A365D), Cyan Accent (#0284C7), Dark Gray Text (#1F2937), Light Gray Fill (#F8FAFC)
    NAVY = RGBColor(26, 54, 93)
    CYAN = RGBColor(2, 132, 199)
    TEXT_COLOR = RGBColor(31, 41, 55)
    MUTED_GRAY = RGBColor(100, 116, 139)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_callout(text, bold_prefix="💡 KEY TAKEAWAY:"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.8)
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "EFF6FF")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

        # Left border cyan, remove others
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/>
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
            r_bold.font.color.rgb = CYAN
            r_bold.font.name = 'Calibri'
            r_bold.font.size = Pt(10.5)
        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        r_text.font.name = 'Calibri'
        r_text.font.color.rgb = TEXT_COLOR
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_heading_1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
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
        p.paragraph_format.space_before = Pt(12)
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
        p.paragraph_format.space_before = Pt(8)
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

    # ==========================================
    # TITLE SECTION
    # ==========================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("🛡️ CYBER SENTINEL: NEXT-GEN AI-SOC")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = NAVY
    r_title.font.name = 'Calibri'

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("Complete Beginner-Friendly Faculty Viva & Project Presentation Guide\n(Zero Pre-requisite Knowledge Required)")
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = CYAN
    r_sub.font.italic = True
    r_sub.font.name = 'Calibri'

    add_callout(
        "Don't worry if you don't know deep Machine Learning or Computer Networking formulas. "
        "This guide explains everything using simple everyday life examples (like houses, airports, and security guards). "
        "Read this document once, follow the step-by-step presentation script, and you will speak with 100% confidence in front of your professors!",
        bold_prefix="🌟 DEAR STUDENT:"
    )

    # ==========================================
    # SECTION 1: WHAT IS THIS PROJECT IN 60 SECONDS?
    # ==========================================
    add_heading_1("1. What is This Project Actually? (In 60 Seconds)")
    add_body_p(
        "Imagine your computer or your college campus network is a giant international airport. Thousands of people (data packets) "
        "are walking through the doors every second. Most of them are normal travelers going to work or school (watching YouTube, browsing Google, downloading files). "
        "However, some people in the crowd are digital thieves, hackers, and saboteurs carrying hidden weapons (viruses, cyber attacks, password stealers)."
    )
    add_body_p(
        "Historically, companies hired security guards who only had a printed list of wanted criminals (called 'Signatures' or 'Antivirus rules'). "
        "If a hacker changed their jacket or used a new trick, the guard let them right through! Furthermore, the guard was too slow to check thousands of people."
    )
    add_body_p(
        "Cyber Sentinel is an ultra-fast, intelligent AI Security System that acts like an autonomous Airport Security Checkpoint:",
        bold_prefix="Our Solution:"
    )
    add_body_p(
        "1. It scans thousands of travelers in fractions of a millisecond with a super-fast AI Metal Detector (Stage 1 Binary Gatekeeper).\n"
        "2. If an alarm rings, it immediately identifies what crime they are attempting (Stage 2 Threat Specialist).\n"
        "3. If a criminal uses a brand-new, never-before-seen trick that has no name, it still stops them because their behavior looks abnormal (Stage 3 Zero-Day Anomaly Engine).\n"
        "4. It clearly explains to the human manager WHY it stopped them in plain English (Explainable AI - XAI).\n"
        "5. With a single click, it locks the door and blocks that attacker from ever entering again (Active Windows Firewall IPS)."
    )

    # ==========================================
    # SECTION 2: JARGON BUSTER (DICTIONARY FOR NON-TECHIES)
    # ==========================================
    add_heading_1("2. Jargon Buster: Big Words Explained with Simple Real-Life Analogies")
    add_body_p("Whenever your faculty asks a question with technical jargon, use these simple concepts to answer instantly:")

    terms = [
        ("IP Address (e.g. 192.168.1.5)", "Like a Home Address / Phone Number", "Every computer connected to the internet gets a unique digital address so data knows where to go. An attacker has a 'Source IP' (where the attack comes from), and your server has a 'Destination IP'."),
        ("Port (e.g. Port 80, 443, 22)", "Like Apartment / Room Numbers inside a Building", "If an IP is a giant building, Ports are the specific doors inside. Port 80 & 443 are for Web Browsing (HTTP/HTTPS). Port 22 is for remote login (SSH). Port 53 is for address lookups (DNS)."),
        ("Network Packet / Flow", "Envelopes and Letters passing through the Post Office", "Computers don't send movies or webpages in one giant chunk; they chop them into tiny envelopes called 'packets'. A 'Flow' is a group of packets belonging to the same conversation between two computers."),
        ("NIDS vs. IPS", "Barking Dog vs. Guard Dog with Teeth", "NIDS (Intrusion Detection) is passive; it just barks (logs an alert) when a thief arrives. IPS (Intrusion Prevention) is active; it actually locks the door and tackles the intruder (blocks their IP with a firewall)."),
        ("Machine Learning (ML)", "Learning from Examples, not Strict Rules", "Instead of a programmer writing 10,000 'IF-ELSE' rules, we showed an algorithm 35,000 past network records (normal and attacks). The computer figured out the subtle math patterns all by itself!"),
        ("Binary Classification", "Yes/No Gatekeeper", "Does this packet smell like a threat? Yes or No. (Benign vs Malicious)."),
        ("Multi-Class Classification", "Specific Crime Specialist", "If it is a threat, what type is it? DoS? PortScan? BruteForce? Botnet?"),
        ("Zero-Day Attack", "A Brand-New Crime Nobody Has Seen Before", "A brand-new hacker exploit that was just invented today. Standard antivirus can't stop it because it has no record of it in its database."),
        ("Isolation Forest (Unsupervised ML)", "The 'Weird Behavior' Detector", "An algorithm trained ONLY on normal, honest behavior. If someone walks into a bank wearing a scuba diving suit and flippers, the guard stops them because it doesn't look like anything normal, even if the guard doesn't know what crime they plan to commit!"),
        ("Explainable AI (XAI / SHAP)", "Opening the 'Black Box'", "Old AI models just gave a number without explaining why. XAI shows the human: 'I stopped this flow because the packet speed was 45 times higher than normal, and the SYN flag was turned on.'"),
        ("MITRE ATT&CK", "The Global FBI Playbook of Cyber Crimes", "An internationally recognized catalog that gives standard codes (like T1498 for DoS) to categorize hacker techniques and assign severity levels.")
    ]

    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    col_widths = [Inches(1.8), Inches(2.2), Inches(2.8)]
    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    # Header Row
    hdr_cells = tbl.rows[0].cells
    hdr_titles = ["Technical Term", "Real-World Analogy", "What It Actually Means"]
    for i, title in enumerate(hdr_titles):
        set_cell_background(hdr_cells[i], "1A365D")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(255, 255, 255)

    for term, analogy, explanation in terms:
        row_cells = tbl.add_row().cells
        for i, text in enumerate([term, analogy, explanation]):
            set_cell_background(row_cells[i], "F8FAFC" if len(tbl.rows) % 2 == 0 else "FFFFFF")
            set_cell_margins(row_cells[i], top=100, bottom=100, left=120, right=120)
            p = row_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.name = 'Calibri'
            run.font.size = Pt(9.5)
            if i == 0:
                run.bold = True
                run.font.color.rgb = NAVY
            elif i == 1:
                run.font.italic = True
                run.font.color.rgb = CYAN
            else:
                run.font.color.rgb = TEXT_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================================
    # SECTION 3: THE 4 TYPES OF ATTACKS OUR SYSTEM DETECTS
    # ==========================================
    add_heading_1("3. The 4 Attacks We Catch (Explained Simply)")
    add_body_p("Our system is trained to recognize the four most common and dangerous enterprise network attacks:")

    attacks = [
        ("1. DoS (Denial of Service - SYN Flood)", "The 'Prank Phone Call Mob'", "Imagine 10,000 people calling a pizza restaurant at the exact same second, saying 'Hello?', and refusing to order. The phone lines get blocked, and real hungry customers can't call in. In our project, an attacker floods the server with fake connection requests so real users get locked out."),
        ("2. PortScan (Reconnaissance)", "The 'Midnight Burglar Checking Every Window'", "Before breaking in, a thief walks around a house shaking every doorknob and window to see which one was left unlocked. In networking, an attacker sends quick ping packets to all 65,000 ports to see which software services are open and vulnerable."),
        ("3. BruteForce (Credential Access)", "Trying Every Key on the Keychain", "An automated hacker script that tries 500 passwords a second (admin123, password, letmein) on an SSH or web login portal until it cracks the account."),
        ("4. Botnet (Command & Control)", "The 'Zombie Army' Checking in with the Boss", "A computer infected with malware quietly reaches out to the hacker's secret server every few minutes ('beaconing') waiting for commands to steal data or launch attacks.")
    ]

    for title, analogy, desc in attacks:
        add_heading_3(title)
        add_body_p(desc, bold_prefix=analogy + ":")

    # ==========================================
    # SECTION 4: THE 3-STAGE AI PIPELINE (THE BRAIN)
    # ==========================================
    add_heading_1("4. The 3-Stage AI Architecture (Why Our Design is So Smart)")
    add_body_p(
        "Many students just train one standard model (like Random Forest) and throw every packet at it. "
        "In a real company, that causes the network to crash or lag horribly! Here is why our 3-stage design is superior:"
    )

    stages = [
        ("Stage 1: Binary Gatekeeper (LightGBM)", "Super-Fast Airport Metal Detector", "Takes only 0.0014 milliseconds. Over 95% of traffic is normal innocent data, so Stage 1 approves it immediately without slowing down your computer. Only suspicious flows are sent to Stage 2."),
        ("Stage 2: Multi-Class Specialist (LightGBM/XGBoost)", "The Investigation Interrogation Room", "Only inspects the suspicious packets passed by Stage 1. It accurately diagnoses whether the attack is DoS, PortScan, BruteForce, or a Botnet."),
        ("Stage 3: Zero-Day Anomaly Engine (Isolation Forest)", "The 'Weird Behavior' Watchdog", "Trained strictly on normal traffic. If an attacker uses a brand-new custom attack that Stage 1 or 2 have never heard of, Stage 3 notices the math doesn't look like normal traffic and assigns an Anomaly Score (e.g. 94% Anomaly!).")
    ]

    for s_title, s_analogy, s_desc in stages:
        add_heading_3(s_title)
        add_body_p(s_desc, bold_prefix=s_analogy + ":")

    add_callout(
        "Why LightGBM instead of Deep Learning (like Neural Networks)?\n"
        "Deep Learning is too heavy and slow for inspecting live network cables. LightGBM runs at line-rate (0.0014 milliseconds per flow) "
        "and consumes very little CPU power while maintaining 100% recall!",
        bold_prefix="💡 VIVA GOLDEN ANSWER:"
    )

    # ==========================================
    # SECTION 5: READY-TO-GO 5-MINUTE FACULTY DEMO SCRIPT
    # ==========================================
    add_heading_1("5. Ready-to-Go 5-Minute Faculty Demonstration Walkthrough")
    add_body_p("Follow this exact step-by-step walkthrough during your lab demo or semester viva. You can read these lines word-for-word:")

    demo_steps = [
        {
            "title": "Step 0: Launching the App (Before your turn)",
            "action": "Double-click 'start.bat' or run 'python run.py'. Browser pops open to http://127.0.0.1:8000. Press F11 for full screen.",
            "what_happens": "Dashboard loads and streams normal background network traffic.",
            "script": "\"Good morning Respected Evaluators. Today I am presenting Cyber Sentinel, an Autonomous AI Security Operations Center and active Intrusion Prevention System.\""
        },
        {
            "title": "Step 1: Showing Baseline Normal Traffic (First 45 seconds)",
            "action": "Point to the main dashboard streaming green flows.",
            "what_happens": "System Status badge shows 'SYSTEM SECURE' in glowing green.",
            "script": "\"Right now, our Stage 1 LightGBM gatekeeper is analyzing live bidirectional network traffic at sub-millisecond speeds. The status badge indicates SYSTEM SECURE because all incoming flows match normal benign HTTPS and DNS browsing behavior.\""
        },
        {
            "title": "Step 2: Injecting a Known Attack (Minute 1)",
            "action": "Click the red button at the top: '[🔴 Inject DoS Flood]'.",
            "what_happens": "The HUD flashes red, an alert chime sounds, and an incident card appears under High-Priority Security Incidents.",
            "script": "\"When an adversary launches a DoS flood, our Stage 1 model detects the anomaly in less than 0.05 milliseconds and routes it to Stage 2, which pinpoints it as a Denial-of-Service attack targeting Port 80. The threat distribution updates dynamically.\""
        },
        {
            "title": "Step 3: The Faculty Shocker — Injecting a Zero-Day (Minute 2)",
            "action": "Click the gold glowing button: '[⚡ INJECT ZERO-DAY UNKNOWN ATTACK]'.",
            "what_happens": "The alert card shows 'ZeroDay_Anomaly' with an anomaly score of 90%+.",
            "script": "\"Most machine learning projects fail completely if an attacker invents a brand-new zero-day attack not present in their training data. But look here: our Stage 3 Unsupervised Isolation Forest Engine catches this unseen exploit purely based on behavioral divergence. This proves our system can catch brand new threats without needing prior labels!\""
        },
        {
            "title": "Step 4: Explainable AI (XAI) — Opening the Black Box (Minute 3)",
            "action": "On any alert card, click the '[🔍 Explain (XAI)]' button.",
            "what_happens": "The screen displays the top 3 features with percentage bars and plain-English reasons.",
            "script": "\"Machine learning models are often criticized as opaque black boxes. We solved this using Explainable AI. As you can see, the AI explains to the security analyst that it flagged this packet because the packet speed was 45 times higher than normal and SYN flags were hammering the server.\""
        },
        {
            "title": "Step 5: Active Defense & Windows Firewall Quarantine (Minute 4)",
            "action": "Click '[⚡ Neutralize IP]' on the alert card, or click Tab 3: Active IPS Mitigation.",
            "what_happens": "An active OS-level Windows Firewall command (netsh advfirewall) is generated and enforced.",
            "script": "\"Traditional intrusion detection systems are passive—they only log an alert. Cyber Sentinel is an active Intrusion Prevention System. With one click, it generates and enforces an active OS-level Windows Firewall rule to isolate the attacker host immediately.\""
        },
        {
            "title": "Step 6: Model Benchmarks & Viva Defense (Minute 5)",
            "action": "Click Tab 4: Model Benchmarks (Viva Defense).",
            "what_happens": "Shows the comparison table of LightGBM vs XGBoost vs Random Forest vs Decision Tree.",
            "script": "\"We trained and benchmarked multiple ML architectures. LightGBM emerged as our champion model, achieving 100% recall with a blistering 0.0014 millisecond inference latency per flow, which is fast enough for enterprise line-rate traffic.\""
        }
    ]

    for step in demo_steps:
        add_heading_2(step["title"])
        add_body_p(step["action"], bold_prefix="What you do:")
        add_body_p(step["what_happens"], bold_prefix="What happens on screen:")
        add_body_p(step["script"], bold_prefix="What you say to faculty:")

    # ==========================================
    # SECTION 6: TOUGH FACULTY VIVA QUESTIONS & WINNING ANSWERS
    # ==========================================
    add_heading_1("6. Tough Faculty Viva Questions & Winning Answers")
    add_body_p("If the professors try to grill you with difficult questions, memorize these short, killer answers:")

    qna = [
        (
            "Q1: 'Which dataset did you use, and how did you get the features?'",
            "A1: 'We modeled 20 industry-standard bidirectional NetFlow features based on the benchmark CICIDS2017 dataset distribution. These include flow duration, packet velocity (packets/sec), inter-arrival times, and TCP flags (SYN, ACK, RST).'"
        ),
        (
            "Q2: 'Why use a 2-stage model instead of just one multi-class model?'",
            "A2: 'In real networks, over 95% of traffic is normal. Running a heavy multi-class classifier on every packet slows down the entire network. Our two-stage design uses a rapid binary gatekeeper to filter out 95% of safe traffic in 0.0014 ms, saving over 90% of computational resources.'"
        ),
        (
            "Q3: 'How can your model detect zero-day attacks if it was never trained on them?'",
            "A3: 'Supervised models cannot detect unknown attacks, which is why we built Stage 3: an Unsupervised Isolation Forest. It was trained strictly on normal benign traffic. When a zero-day exploit arrives, its packet sizes and timing deviate drastically from normal, so the Isolation Forest isolates it and flags it as an anomaly.'"
        ),
        (
            "Q4: 'Does this work on REAL live network cards, or only on saved data?'",
            "A4: 'It works on both! We built a dual-mode ingestion engine. Clicking the Live Sniffer button uses Python Scapy to capture real live packets from our physical Wi-Fi or Ethernet card and aggregates them into 20-feature flow vectors in real time.'"
        ),
        (
            "Q5: 'Why did you choose LightGBM over Deep Learning (CNN/LSTM) or Random Forest?'",
            "A5: 'Random Forest had an inference latency of 0.0054 ms, while LightGBM achieved 0.0014 ms—nearly 4 times faster! Deep learning models require high GPU power and introduce too much latency for live packet streaming. LightGBM gave us 100% recall with sub-millisecond line-rate speed.'"
        ),
        (
            "Q6: 'What is the difference between an IDS and an IPS?'",
            "A6: 'An IDS (Intrusion Detection System) only monitors and alerts. An IPS (Intrusion Prevention System) takes active countermeasures. Cyber Sentinel is an IPS because it generates real Windows Firewall rules (netsh advfirewall) to block malicious IPs dynamically.'"
        )
    ]

    for q, a in qna:
        add_heading_3(q)
        add_body_p(a)

    # ==========================================
    # SECTION 7: STEP-BY-STEP CHECKLIST FOR PRESENTATION DAY
    # ==========================================
    add_heading_1("7. Presentation Day Checklist")
    add_body_p("Before you walk up to present, make sure you have done these 4 quick checks:")
    add_body_p("1. Laptop plugged in to charger (so Windows doesn't throttle CPU performance).\n"
               "2. Run 'python run.py' and verify the dashboard opens at http://127.0.0.1:8000.\n"
               "3. Click '[🔴 Inject DoS Flood]' and '[⚡ INJECT ZERO-DAY UNKNOWN ATTACK]' once in private to ensure alerts fire cleanly.\n"
               "4. Keep this document printed or open on your phone for a quick glance if you forget any term!")

    # Save document
    output_path = os.path.join(os.path.dirname(__file__), "CyberSentinel_Faculty_Presentation_Guide.docx")
    doc.save(output_path)
    print(f"[+] Successfully generated Word file at: {output_path}")

if __name__ == "__main__":
    create_guide()
