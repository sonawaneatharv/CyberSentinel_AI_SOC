import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_word_document():
    doc = docx.Document()

    # Configure Margins (0.8 inches all around)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Color Palette
    NAVY = RGBColor(26, 54, 93)       # Primary #1A365D
    CYAN = RGBColor(2, 132, 199)      # Accent #0284C7
    TEXT_COLOR = RGBColor(31, 41, 55) # Neutral Dark #1F2937
    DARK_RED = RGBColor(185, 28, 28)  # Warning/Attack #B91C1C
    GREEN = RGBColor(21, 128, 61)     # Safe/Success #15803D
    GOLD = RGBColor(180, 83, 9)       # Zero-Day #B45309

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

    # ---------------------------------------------------------------------------
    # TITLE & HEADER
    # ---------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("🛡️ CYBER SENTINEL: NEXT-GEN AI-SOC")
    r_t.bold = True
    r_t.font.size = Pt(24)
    r_t.font.color.rgb = NAVY
    r_t.font.name = 'Calibri'

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_sub.add_run("Comprehensive Faculty Viva & Project Presentation Master Guide\nWritten in Plain English for Students with Zero Prior Background in ML or Networks")
    r_s.font.size = Pt(12)
    r_s.font.color.rgb = CYAN
    r_s.font.italic = True
    r_s.font.name = 'Calibri'

    add_callout(
        "You do NOT need any prior knowledge of Machine Learning formulas, calculus, or deep network protocols to present this project. "
        "Every single concept in this document is explained using simple, intuitive real-world analogies (airports, post offices, and security guards). "
        "Follow the word-for-word 5-minute presentation script inside, and you will present with complete confidence in front of your faculty evaluators!",
        bold_prefix="🌟 INSTRUCTIONS FOR THE PRESENTER:"
    )

    # ---------------------------------------------------------------------------
    # 1. WHAT IS THIS PROJECT IN PLAIN ENGLISH?
    # ---------------------------------------------------------------------------
    add_heading_1("1. What is This Project Actually? (In Plain English)")
    add_body_p(
        "Imagine your computer, campus Wi-Fi, or company server is a giant international airport terminal. "
        "Thousands of travelers (digital data packets) are entering and exiting through the security gates every second. "
        "Over 95% of these travelers are normal, innocent passengers going to work or school (watching YouTube videos, "
        "browsing Wikipedia, sending college emails, downloading lecture PDFs)."
    )
    add_body_p(
        "However, hidden among this massive crowd are digital thieves, saboteurs, and hackers attempting to carry out cyber attacks "
        "(such as crashing the college server, scanning for open vulnerabilities, or guessing admin passwords)."
    )
    add_body_p(
        "Historically, security systems (traditional antiviruses or tools like Snort) acted like old-fashioned security guards with a "
        "printed binder of 'wanted posters' (called Signatures). If a hacker changed their disguise slightly, or used a brand-new trick, "
        "the old guard let them walk right past! Furthermore, manually inspecting every single passenger caused huge lines, slowing down the airport."
    )
    add_body_p(
        "Cyber Sentinel is an autonomous, high-speed AI Security Operations Center (AI-SOC) that acts like a futuristic airport security gate:",
        bold_prefix="Our Project (Cyber Sentinel):"
    )
    add_body_p(
        "• Stage 1 (High-Speed Gatekeeper): Uses a lightning-fast AI algorithm (LightGBM) to screen traffic in 0.0014 milliseconds. Over 95% of innocent traffic passes immediately without slowing down the network.\n"
        "• Stage 2 (Threat Specialist): If a suspicious flow is flagged, Stage 2 immediately diagnoses the exact type of attack (DoS, PortScan, BruteForce, or Botnet).\n"
        "• Stage 3 (Zero-Day Anomaly Engine): If an attacker uses a brand-new exploit that nobody has ever seen before (Zero-Day), our unsupervised AI detects the weird behavioral deviation and sounds the alarm!\n"
        "• Explainable AI (XAI): It explains to the human manager WHY it stopped the packet (e.g. 'Packet speed was 45x normal, SYN flag hammering detected').\n"
        "• Active IPS Firewall Quarantine: With a single click, it executes an OS-level Windows Firewall command (netsh advfirewall) to block the attacker's IP permanently."
    )

    # ---------------------------------------------------------------------------
    # 2. PROBLEM STATEMENT (WHY TRADITIONAL SYSTEMS FAIL)
    # ---------------------------------------------------------------------------
    add_heading_1("2. Problem Statement (Why Existing Solutions Fail)")
    add_body_p(
        "When explaining the problem statement to your faculty, emphasize these 4 major flaws in traditional systems that Cyber Sentinel solves:"
    )

    ps_points = [
        ("Problem 1: Signature Limitations", "Traditional tools (like Snort or ClamAV) rely on static rules. If an attack pattern is slightly modified or obfuscated, signatures fail completely."),
        ("Problem 2: Network Latency Bottlenecks", "In real enterprise networks, over 95% of traffic is benign. Running heavy Deep Learning (CNN/LSTM) models on every incoming packet slows down the network and drops traffic."),
        ("Problem 3: The ML 'Black Box' Dilemma", "Standard Machine Learning models output probabilities (e.g. '0.87'), but cannot explain why. Security analysts suffer from alert fatigue and distrust the system."),
        ("Problem 4: Passive Alerting vs. Active Mitigation", "Most student projects and traditional IDS are purely passive; they just write an alert into a log file while the attacker continues hacking. They lack automated active countermeasures.")
    ]

    for p_title, p_desc in ps_points:
        add_heading_3(p_title)
        add_body_p(p_desc)

    # ---------------------------------------------------------------------------
    # 3. JARGON BUSTER (DICTIONARY FOR NON-TECHIES)
    # ---------------------------------------------------------------------------
    add_heading_1("3. Jargon Buster: Big Technical Words Explained with Analogies")
    add_body_p("Use this table as your secret weapon during your viva. If an evaluator throws a technical term at you, respond with the simple concept below:")

    terms_data = [
        ("IP Address\n(e.g. 192.168.1.5)", "Home Street Address / Phone Number", "Every computer connected to the internet gets a unique address so data knows where to go. Source IP is where the packet came from; Destination IP is where it is going."),
        ("Port Number\n(e.g. 80, 443, 22)", "Room / Apartment Number", "If an IP is a giant office building, ports are the specific doors inside. Port 80 & 443 are for Web browsing, Port 22 is for remote login (SSH), and Port 53 is for DNS lookups."),
        ("Network Packet & Flow", "Letters & Envelopes in a Mailbag", "Computers don't send whole videos at once; they chop them into tiny envelopes called packets. A 'flow' is a bidirectional stream of packets belonging to the same conversation."),
        ("NIDS vs. IPS", "Barking Dog vs. Guard Dog with Teeth", "NIDS (Intrusion Detection System) only monitors and alerts (barks). IPS (Intrusion Prevention System) takes active action to lock the door and block the attacker."),
        ("Machine Learning (ML)", "Learning from Experience", "Instead of a programmer writing thousands of strict IF-ELSE rules, we showed an algorithm 35,000 past network records. The algorithm discovered the patterns automatically."),
        ("Binary Classification", "Airport Metal Detector (Yes / No)", "The model asks one simple question: 'Is this traffic Safe or Malicious?'"),
        ("Multi-Class Classification", "Crime Investigation Specialist", "Once confirmed malicious, the model diagnoses: 'Is it DoS, PortScan, BruteForce, or Botnet?'"),
        ("Zero-Day Attack", "A Brand-New Crime Never Seen Before", "A brand-new hack invented today that has no entry in any antivirus database. Traditional signature systems fail against it 100% of the time."),
        ("Isolation Forest (Unsupervised)", "The 'Weird Outfit' Detector", "Trained STRICTLY on normal benign traffic. If a packet arrives with bizarre timing or weird sizes, the algorithm isolates it and flags it as an anomaly, even without prior training labels!"),
        ("Explainable AI (XAI / SHAP)", "Opening the Black Box", "Translates mathematical model weights into human-readable explanations (e.g. 'Flagged because packet velocity is 45x normal baseline')."),
        ("MITRE ATT&CK Framework", "The Global FBI Cyber Threat Matrix", "An internationally recognized knowledge base of adversary tactics and techniques used by enterprise SOC analysts worldwide."),
        ("Firewall / Quarantine", "Digital Security Door Slam", "An operating system tool (Windows netsh advfirewall) that blocks packets from a malicious IP address at the hardware network layer.")
    ]

    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    col_widths = [Inches(1.8), Inches(2.2), Inches(2.8)]
    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(["Technical Term", "Everyday Analogy", "What It Actually Means"]):
        set_cell_background(hdr_cells[i], "1A365D")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, (t_name, t_analogy, t_desc) in enumerate(terms_data):
        row_cells = tbl.add_row().cells
        bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for i, text in enumerate([t_name, t_analogy, t_desc]):
            set_cell_background(row_cells[i], bg)
            set_cell_margins(row_cells[i], top=100, bottom=100, left=120, right=120)
            p = row_cells[i].paragraphs[0]
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

    # ---------------------------------------------------------------------------
    # 4. THE 4 ATTACKS WE DETECT
    # ---------------------------------------------------------------------------
    add_heading_1("4. The 4 Cyber Attacks We Catch (Explained Simply)")
    add_body_p("Our system is trained on the benchmark CICIDS2017 feature distribution to detect the 4 most prominent enterprise attack vectors:")

    attacks_list = [
        (
            "1. DoS (Denial of Service - SYN Flood)",
            "The 'Prank Phone Call Mob'",
            "Imagine 10,000 automated bots calling a hospital reception at the exact same second, saying 'Hello?' and hanging up. The hospital phone lines get jammed, and real patients with medical emergencies cannot get through. "
            "In our project, an attacker floods a web server on Port 80 with SYN packets, exhausting its connection buffer so legitimate users get a 'Server Unreachable' error."
        ),
        (
            "2. PortScan (Reconnaissance)",
            "The 'Midnight Burglar Checking Every Window'",
            "Before breaking into a mansion, a thief walks around testing every door handle, back window, and basement latch to find an open entry point. "
            "In network attacks, a hacker sends fast probe packets to thousands of port numbers (from Port 20 to 65,000) to find vulnerable running services."
        ),
        (
            "3. BruteForce (Credential Access)",
            "Trying Every Key on the Keychain",
            "An automated script attempts 500 password combinations every second ('admin123', 'root', 'password') against an SSH (Port 22) or web admin login until it forces its way in. "
            "Our system detects the rapid repetition of tiny authentication flows."
        ),
        (
            "4. Botnet (Command & Control - C2)",
            "The 'Sleeper Agent' Phoning the Boss",
            "A computer in the building gets secretly infected with malware. Every few minutes, it sends a quiet, periodic signal ('beacon') to the attacker's server asking for new instructions. "
            "Our system flags this by detecting abnormally low jitter in packet timing (Inter-Arrival Time)."
        )
    ]

    for a_name, a_analogy, a_desc in attacks_list:
        add_heading_3(a_name)
        add_body_p(a_desc, bold_prefix=a_analogy + ":")

    # ---------------------------------------------------------------------------
    # 5. THE 3-STAGE AI PIPELINE (TECHNICAL ARCHITECTURE)
    # ---------------------------------------------------------------------------
    add_heading_1("5. The 3-Stage AI Architecture (Why It's Academically Superior)")
    add_body_p(
        "Many student projects simply train a single Random Forest or Decision Tree. Here is the architectural reasoning why our 3-stage pipeline is enterprise-grade:"
    )

    stage_breakdown = [
        (
            "Stage 1: Binary Gatekeeper (LightGBM)",
            "Ultra-Fast High-Speed Screening",
            "In real life, 95%+ of traffic is benign. Running heavy multi-class models on every single packet slows down the entire network. Stage 1 takes only 0.0014 milliseconds per flow to filter out benign traffic, saving over 90% of processing power."
        ),
        (
            "Stage 2: Multi-Class Specialist (LightGBM / XGBoost)",
            "Deep Vector Diagnosis",
            "Only the suspicious flows flagged by Stage 1 are sent to Stage 2. This specialist model diagnoses whether the threat is DoS, PortScan, BruteForce, or Botnet with near 100% accuracy."
        ),
        (
            "Stage 3: Zero-Day Anomaly Engine (Isolation Forest)",
            "Unsupervised Outlier Detection",
            "Trained strictly on legitimate baseline traffic. If a hacker invents a brand-new zero-day attack not present in our training dataset, Stage 3 isolates it based on abnormal statistical reconstruction deviation and assigns an Anomaly Divergence Score (0% to 100%)."
        )
    ]

    for s_name, s_role, s_desc in stage_breakdown:
        add_heading_3(s_name)
        add_body_p(s_desc, bold_prefix=s_role + ":")

    add_callout(
        "Why LightGBM instead of Deep Learning (like CNNs or LSTMs)?\n"
        "Deep Learning requires massive GPU resources and introduces 5 to 50 milliseconds of latency, which causes packet drops on high-speed 1 Gbps / 10 Gbps network cards. "
        "LightGBM runs on standard CPUs in 0.0014 milliseconds with 100% recall, making it realistic for line-rate enterprise deployment!",
        bold_prefix="💡 VIVA WINNING POINT:"
    )

    # ---------------------------------------------------------------------------
    # 6. READY-TO-GO 5-MINUTE FACULTY DEMO SCRIPT
    # ---------------------------------------------------------------------------
    add_heading_1("6. Ready-to-Go 5-Minute Faculty Demonstration Walkthrough")
    add_body_p(
        "Follow this exact script during your presentation. You can literally read the spoken words directly from this page:"
    )

    demo_steps = [
        {
            "step": "Step 0: Pre-Demo Setup (Before Calling Faculty)",
            "action": "Double click 'start.bat' or open terminal and run 'python run.py'. Browser will open at http://127.0.0.1:8000. Press F11 for full screen.",
            "screen": "The Cyber Sentinel HUD loads and streams normal background flows.",
            "speech": "\"Good morning Respected Evaluators. Today I am presenting Cyber Sentinel, an Autonomous AI Security Operations Center (AI-SOC) and Hybrid Intrusion Detection and Prevention System.\""
        },
        {
            "step": "Step 1: Baseline Normal Operation (0:00 – 0:45)",
            "action": "Point to the main streaming HUD.",
            "screen": "Status badge indicates 'SYSTEM SECURE' in bright green.",
            "speech": "\"Right now, our Stage 1 LightGBM gatekeeper is analyzing live bidirectional network traffic at sub-millisecond speeds. The status badge indicates SYSTEM SECURE because all incoming flows match normal benign HTTPS and DNS browsing behavior.\""
        },
        {
            "step": "Step 2: Injecting a Known Attack (0:45 – 1:30)",
            "action": "Click the top red button: '[🔴 Inject DoS Flood]'.",
            "screen": "The HUD flashes red, an alert chime plays, and a High-Priority Incident card appears.",
            "speech": "\"When an adversary launches a DoS flood, our Stage 1 model detects the anomaly in less than 0.05 milliseconds and routes it to Stage 2, which pinpoints it as a Denial-of-Service attack targeting Port 80. The threat distribution and MITRE ATT&CK mapping (T1498) update automatically.\""
        },
        {
            "step": "Step 3: The Faculty Shocker — Zero-Day Attack (1:30 – 2:30)",
            "action": "Click the gold glowing button: '[⚡ INJECT ZERO-DAY UNKNOWN ATTACK]'.",
            "screen": "The alert card shows 'ZeroDay_Anomaly' with an anomaly divergence score over 90%.",
            "speech": "\"Most machine learning projects fail completely if an attacker invents a brand-new zero-day attack not present in their training data. But look here: our Stage 3 Unsupervised Isolation Forest Engine catches this unseen exploit purely based on behavioral divergence. This proves our system can catch brand new threats without needing prior labels!\""
        },
        {
            "step": "Step 4: Explainable AI (XAI) — Opening the Black Box (2:30 – 3:15)",
            "action": "On any alert card, click the '[🔍 Explain (XAI)]' button.",
            "screen": "Displays the top 3 statistical drivers, observed vs. baseline values, and percentage bars.",
            "speech": "\"Machine learning models are often criticized as opaque black boxes. We solved this using Explainable AI. As you can see, the AI explains to the security analyst that it flagged this packet because the packet speed was 45 times higher than normal and SYN flags were hammering the server.\""
        },
        {
            "step": "Step 5: Active Defense & Windows Firewall Quarantine (3:15 – 4:00)",
            "action": "Click '[⚡ Neutralize IP]' on the alert card or switch to Tab 3: Active IPS Mitigation.",
            "screen": "Shows the active OS-level Windows Firewall rule generated (netsh advfirewall).",
            "speech": "\"Traditional intrusion detection systems are passive—they only log an alert. Cyber Sentinel is an active Intrusion Prevention System. With one click, it generates and enforces an active OS-level Windows Firewall rule to isolate the attacker host immediately.\""
        },
        {
            "step": "Step 6: Academic Benchmarks & Viva Defense (4:00 – 5:00)",
            "action": "Click Tab 4: Model Benchmarks (Viva Defense).",
            "screen": "Empirical comparison table comparing LightGBM, XGBoost, Random Forest, and Decision Tree.",
            "speech": "\"We trained and benchmarked multiple ML architectures on the CICIDS2017 benchmark distribution. LightGBM emerged as our champion model, achieving 100% recall with a blistering 0.0014 millisecond inference latency per flow, which is fast enough for enterprise line-rate traffic.\""
        }
    ]

    for item in demo_steps:
        add_heading_2(item["step"])
        add_body_p(item["action"], bold_prefix="What you do:")
        add_body_p(item["screen"], bold_prefix="What happens on screen:")
        add_body_p(item["speech"], bold_prefix="What you say to faculty:")

    # ---------------------------------------------------------------------------
    # 7. TRICKY FACULTY QUESTIONS & WINNING VIVA DEFENSE
    # ---------------------------------------------------------------------------
    add_heading_1("7. Tricky Faculty Viva Questions & Winning Answers")
    add_body_p("If the professors try to grill you, memorize these short, authoritative answers:")

    qna_list = [
        (
            "Q1: 'Which dataset did you train on, and what features did you select?'",
            "A1: 'We modeled 20 industry-standard bidirectional NetFlow features based on the benchmark CICIDS2017 dataset distribution. Key features include Flow Duration, Flow Packets/s, Flow Bytes/s, Inter-Arrival Times (IAT), and TCP flags (SYN, ACK, RST, PSH).'"
        ),
        (
            "Q2: 'Why use a 2-stage architecture instead of a single multi-class model?'",
            "A2: 'In real networks, over 95% of traffic is normal. Running a heavy multi-class classifier on every packet causes severe latency and packet drops. Our two-stage design uses a rapid binary gatekeeper to filter out 95% of safe traffic in 0.0014 ms, saving over 90% of computational resources.'"
        ),
        (
            "Q3: 'How can you claim to detect zero-day attacks if supervised models only know past data?'",
            "A3: 'Supervised models only recognize known classes. That is why we added Stage 3: an Unsupervised Isolation Forest. It is calibrated strictly on normal benign behavior. When a zero-day exploit arrives, its packet sizes and timing deviate drastically from normal, so the Isolation Forest isolates it and flags it as an anomaly.'"
        ),
        (
            "Q4: 'Does this project work on real live physical network cards?'",
            "A4: 'Yes! We implemented a dual-mode ingestion engine. Clicking the Live Sniffer button uses Python Scapy to sniff raw live packets from our physical Wi-Fi or Ethernet interface, aggregating them into 20-feature bidirectional flow vectors in real time.'"
        ),
        (
            "Q5: 'Why did you select LightGBM over Random Forest or Deep Learning?'",
            "A5: 'Random Forest had an inference latency of 0.0054 ms, while LightGBM achieved 0.0014 ms—nearly 4 times faster! Deep learning models require high GPU power and introduce too much latency for live packet streaming. LightGBM gave us 100% recall with sub-millisecond line-rate speed on commodity CPU hardware.'"
        ),
        (
            "Q6: 'What is the practical difference between an IDS and an IPS?'",
            "A6: 'An IDS (Intrusion Detection System) only monitors and logs alerts. An IPS (Intrusion Prevention System) takes active countermeasures. Cyber Sentinel is an IPS because it dynamically creates and enforces Windows Firewall rules (netsh advfirewall) to block malicious IPs in real time.'"
        )
    ]

    for q, a in qna_list:
        add_heading_3(q)
        add_body_p(a)

    # ---------------------------------------------------------------------------
    # 8. HOW TO RUN & TROUBLESHOOTING
    # ---------------------------------------------------------------------------
    add_heading_1("8. How to Run the Project & Quick Troubleshooting")
    add_body_p("To run the project at any time, open your command terminal or PowerShell and run:")
    add_body_p(
        "cd \"d:\\Laptop local Disk D\\study\\Sem 5\\ML\\ML_project\\CyberSentinel_AI_SOC\"\n"
        "python run.py"
    )
    add_body_p(
        "• Your dashboard will open automatically at: http://127.0.0.1:8000\n"
        "• Interactive API Swagger Docs: http://127.0.0.1:8000/docs\n"
        "• To re-train models from scratch: run 'python ml/prepare_dataset.py' followed by 'python ml/train_advanced_models.py'."
    )

    # Save to both file names so the user can access either
    file1 = os.path.join(os.path.dirname(__file__), "CyberSentinel_Faculty_Presentation_Guide.docx")
    file2 = os.path.join(os.path.dirname(__file__), "CyberSentinel_Complete_Presentation_Guide.docx")
    
    doc.save(file1)
    doc.save(file2)
    print(f"[+] Successfully generated Word documents:\n 1. {file1}\n 2. {file2}")

if __name__ == "__main__":
    build_word_document()
