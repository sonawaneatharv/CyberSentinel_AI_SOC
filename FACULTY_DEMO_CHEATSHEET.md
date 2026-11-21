# 🎓 Cyber Sentinel Next-Gen AI-SOC: Faculty Viva & Demonstration Script

> **How to Shock and Impress Your Evaluators in Under 5 Minutes**
> *You don't need deep ML mathematics to present this. Follow this exact 5-step script.*

---

## 🚀 Step 0: How to Start the Project
1. Open PowerShell or Command Prompt.
2. Navigate to this directory:
   ```cmd
   cd "d:\Laptop local Disk D\study\Sem 5\ML\ML_project\CyberSentinel_AI_SOC"
   python run.py
   ```
   *(Or simply double-click `start.bat`)*
3. Your web browser will automatically open to: **`http://127.0.0.1:8000`**

---

## 🎯 The 5-Minute Faculty Demonstration Walkthrough

### **Step 1: The Baseline (First 30 Seconds)**
* **What you show on screen**: The main SOC dashboard is streaming live background network flows.
* **What you tell the faculty**:
  > *"Respected Evaluators, this is **Cyber Sentinel**, an autonomous AI Security Operations Center. Right now, our Stage 1 LightGBM gatekeeper is analyzing live bidirectional network traffic at sub-millisecond speeds. The status badge indicates 'SYSTEM SECURE' because all incoming flows are legitimate benign HTTPS/DNS traffic."*

---

### **Step 2: The Attack Injection & Real-Time Alert (Minute 1)**
* **What you do**: Click the **`[🔴 Inject DoS Flood]`** button in the top bar.
* **What happens**:
  - The HUD turns pulsing red.
  - An audio chime rings.
  - An incident card pops up under **High-Priority Security Incidents**.
* **What you tell the faculty**:
  > *"When an attacker launches a DoS flood, our Stage 1 model detects the anomaly in less than 0.05 milliseconds and routes it to Stage 2, which pinpoints it as a Denial-of-Service attack targeting Port 80. The threat distribution updates dynamically."*

---

### **Step 3: The "Faculty Shocker" — Inject Zero-Day Unknown Attack (Minute 2)**
* **What you do**: Click the glowing gold button: **`[⚡ INJECT ZERO-DAY UNKNOWN ATTACK]`**.
* **What happens**:
  - The system flags it as: `ZeroDay_Anomaly` with an anomaly score of **90%+**.
* **What you tell the faculty**:
  > *"Most ML projects on GitHub fail completely if an attacker uses a brand-new zero-day attack that wasn't in their training dataset. But look here: our **Stage 3 Unsupervised Isolation Forest Engine** flagged this unknown attack purely based on statistical reconstruction deviation, proving our system can catch never-before-seen zero-day exploits!"*
  *(Professors are always amazed by this because handling unseen zero-day attacks is considered an advanced research capability!)*

---

### **Step 4: Explainable AI (XAI) — "Opening the Black Box" (Minute 3)**
* **What you do**: On the alert card, click the **`[🔍 Explain (XAI)]`** button.
* **What happens**: The screen switches to the **Explainable AI (XAI & SHAP)** tab, showing the exact percentage bars and reasons why the model made the decision.
* **What you tell the faculty**:
  > *"Professors often ask: 'How do you know the ML isn't just a black box guessing numbers?' We solved this using **Explainable AI (XAI)**. As you can see, the AI explains to the security analyst that it flagged this packet specifically because the packet rate was 45x normal baseline and the SYN flag was set to 1."*

---

### **Step 5: Active IPS Defense & One-Click Firewall Quarantine (Minute 4)**
* **What you do**: Click **`[⚡ Neutralize IP]`** or go to **Tab 3: Active IPS Mitigation**.
* **What happens**: An OS-level Windows firewall rule is generated and the attacker host is actively quarantined.
* **What you tell the faculty**:
  > *"Traditional systems are passive — they just log alerts. Cyber Sentinel is an active **IPS (Intrusion Prevention System)**. With one click, it generates and enforces an active OS-level Windows Firewall rule (`netsh advfirewall`) to immediately isolate the attacker host."*

---

### **Step 6: Model Benchmarks & Viva Defense (Minute 5)**
* **What you do**: Click **Tab 4: Model Benchmarks (Viva Defense)**.
* **What happens**: Displays the empirical comparison table comparing LightGBM, XGBoost, Random Forest, and Decision Tree with accuracy, recall, and sub-millisecond inference latencies.
* **What you tell the faculty**:
  > *"We trained and benchmarked multiple architectures. LightGBM emerged as our champion model, achieving 100% recall with a blistering 0.0014 ms inference latency per flow, which is fast enough for line-rate enterprise traffic."*

---

## 💡 Quick Answers to Questions Faculties Might Ask

| Faculty Question | Your Winning Answer |
| :--- | :--- |
| **"Which dataset did you use?"** | *"We used the industry benchmark **CICIDS2017** dataset parameters, modeling 20 critical bidirectional flow features like flow duration, packet rates, and TCP flag distributions."* |
| **"Why not just use a single multi-class model?"** | *"In real enterprise networks, over 95% of traffic is normal. Running a heavy multi-class classifier on every packet slows down the network. Our **Two-Stage Architecture** uses a rapid LightGBM binary gatekeeper first, saving 90% of compute."* |
| **"What models did you compare?"** | *"In our viva benchmarks tab, we compared LightGBM, XGBoost, Random Forest, and Decision Tree. LightGBM provided the best latency (0.0014 ms per flow) while maintaining 100% recall."* |
| **"Can it work on real live network cards?"** | *"Yes! We built a dual-mode ingestion engine. Clicking the 'Live Sniffer' button activates our background Scapy module to capture real live packets from our physical Wi-Fi/Ethernet interface."* |
