# 🛡️ Cyber Sentinel Next-Gen AI-SOC & Autonomous Threat Defense

An end-to-end, enterprise-grade **Autonomous AI Security Operations Center (AI-SOC)** and **Hybrid Intrusion Detection & Prevention System (NIDS/IPS)** featuring **Two-Stage Machine Learning**, **Unsupervised Zero-Day Anomaly Detection**, **Explainable AI (XAI)**, **MITRE ATT&CK Enterprise Mapping**, **Live Network Packet Sniffing**, and **Active OS Firewall Quarantine**.

---

## 🌟 Key Upgrades & Architectural Capabilities

1. **Two-Stage Supervised Pipeline**:
   - **Stage 1 (Binary Gatekeeper)**: Ultra-fast **LightGBM** binary classifier filtering Benign vs Threat in sub-millisecond latency ($<0.002\text{ ms}$).
   - **Stage 2 (Multi-Class Threat Specialist)**: Specializes in pinpointing specific attack vectors: **DoS**, **PortScan**, **BruteForce**, and **Botnet**.

2. **Stage 3 Unsupervised Zero-Day Anomaly Engine**:
   - An **Isolation Forest Anomaly Detector** calibrated strictly on Benign traffic.
   - Detects brand new, never-before-seen zero-day polymorphic attacks and protocol tunneling without needing prior labels.

3. **Explainable AI (XAI & SHAP Feature Attributions)**:
   - Eliminates the ML "black box" criticism.
   - Every detected threat outputs the top 3 statistical drivers (e.g. `Flow_Packets_s`, `SYN_Flag_Count`, `Average_Packet_Size`) with human-readable reasoning and percentage divergence bars.

4. **Active IPS & Autonomous OS Firewall Quarantine**:
   - Upgrades passive detection into active defense.
   - Generates executable Windows Firewall rules (`netsh advfirewall firewall add rule...`) to instantly quarantine malicious source IPs with a single click.

5. **MITRE ATT&CK Enterprise Matrix Alignment**:
   - Automatically maps all threat classifications to official MITRE tactics and techniques:
     - **DoS** $\rightarrow$ `T1498: Network Denial of Service` (Tactics: Impact, CVSS: 7.5)
     - **PortScan** $\rightarrow$ `T1046: Network Service Discovery` (Tactics: Reconnaissance, CVSS: 5.3)
     - **BruteForce** $\rightarrow$ `T1110: Brute Force` (Tactics: Credential Access, CVSS: 8.1)
     - **Botnet** $\rightarrow$ `T1071: Application Layer Protocol` (Tactics: Command & Control, CVSS: 8.8)
     - **Zero-Day** $\rightarrow$ `T1203: Exploitation for Client Execution` (Tactics: Initial Access, CVSS: 9.4)

6. **Dual Ingestion Engine**:
   - **Mode 1: High-Speed Simulation Stream** (Reliable holdout test reservoir for seamless live presentations).
   - **Mode 2: Real Physical Network Sniffer** (Uses `scapy` to capture real live Wi-Fi/Ethernet packets and aggregate them into bidirectional 5-tuple flow vectors).

7. **Embedded AI Security Analyst Copilot**:
   - Autonomous incident investigation copilot that drafts executive incident briefs, evaluates blast radius, and provides containment playbooks.

---

## 🏗️ System Architecture

```
                       [ Incoming Telemetry Ingestion ]
                       ┌───────────────┴──────────────┐
                       ▼                              ▼
             [ Test Reservoir Stream ]     [ Real Scapy Live Sniffer ]
                       └───────────────┬──────────────┘
                                       │
                                       ▼
                       [ StandardScaler Normalization ]
                         (20 NetFlow/CICIDS Features)
                                       │
                                       ▼
    ┌──────────────────────────────────┴──────────────────────────────────┐
    ▼                                                                     ▼
[ Stage 1: Binary Gatekeeper ]                           [ Stage 3: Zero-Day Anomaly Engine ]
    (LightGBM: 0.0014 ms latency)                             (Unsupervised Isolation Forest)
    │                                                                     │
    ├──► SAFE (Benign Traffic Passed)                                    ▼
    │                                                    [ Anomaly Divergence Score (0-100%) ]
    ▼ If Attack Detected                                                  │
[ Stage 2: Multi-Class Specialist ]                                       │
    (DoS / PortScan / BruteForce / Botnet)                                │
    │                                                                     │
    └──────────────────────────────────┬──────────────────────────────────┘
                                       │
                                       ▼
                    [ Explainable AI (XAI) Engine ]
              (SHAP Feature Attributions & Root-Cause Reasons)
                                       │
                                       ▼
                    [ MITRE ATT&CK Matrix TTP Mapper ]
                                       │
                                       ▼
                 [ Active IPS Mitigation & AI Copilot ]
           (Windows Firewall 'netsh' Rule + Incident Briefing)
                                       │
                                       ▼
                     [ Cyber SOC HUD Web Dashboard ]
```

---

## 🚀 Quick Start Guide

### 1. Launch the Application
Run the launcher:
```bash
python run.py
```
*(Or double-click `start.bat`)*

Your browser will automatically open to:
* **SOC Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. (Optional) Re-train the Pipeline
To re-run dataset processing and train the advanced models:
```bash
python ml/prepare_dataset.py
python ml/train_advanced_models.py
```

---

## 🎓 Faculty Presentation Guide
For your semester viva or project demonstration, check the step-by-step presentation script:
👉 **[FACULTY_DEMO_CHEATSHEET.md](file:///d:/Laptop%20local%20Disk%20D/study/Sem%205/ML/ML_project/CyberSentinel_AI_SOC/FACULTY_DEMO_CHEATSHEET.md)**
