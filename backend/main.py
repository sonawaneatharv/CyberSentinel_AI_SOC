"""
Cyber Sentinel Next-Gen AI-SOC
FastAPI Backend Server & High-Performance Security Operations Center REST API
"""

import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.engine import engine
from backend.sniffer import sniffer_service
from backend.schemas import (
    NetworkFlowInput,
    InjectRequest,
    BlockIPRequest,
    BlockIPResponse,
    CopilotAnalysisRequest,
    CopilotAnalysisResponse
)

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
MODELS_DIR = os.path.join(BASE_DIR, "..", "ml", "models")

app = FastAPI(
    title="Cyber Sentinel Next-Gen AI-SOC",
    description="Intelligent Autonomous Security Operations Center with Explainable AI (XAI), Zero-Day Anomaly Detection, MITRE ATT&CK Mapping, and Active IPS Mitigation.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# REST API ENDPOINTS
# -------------------------------------------------------------

@app.get("/api/stream/next")
def get_next_telemetry_flow():
    """
    Returns the next telemetry flow with Stage 1 Binary classification,
    Stage 2 Attack classification, Stage 3 Zero-Day anomaly score,
    and Explainable AI (XAI) feature attributions.
    """
    return engine.get_next_flow()

@app.post("/api/stream/inject")
def inject_threat_flow(req: InjectRequest):
    """
    Injects a targeted cyber attack (DoS, PortScan, BruteForce, Botnet, or ZeroDay_Anomaly)
    into the priority simulation queue.
    """
    success, msg = engine.inject_attack(req.attack_type)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg, "attack_type": req.attack_type}

@app.post("/api/mitigation/block", response_model=BlockIPResponse)
def quarantine_attacker_ip(req: BlockIPRequest):
    """
    Active IPS Mitigation: Generates an OS-level firewall rule to quarantine an attacker IP.
    """
    record = engine.block_ip(req.ip_address, threat_type=req.threat_type or "Unknown", reason=req.reason or "Manual Admin Quarantine")
    return BlockIPResponse(
        status="ENFORCED",
        ip_address=record["ip_address"],
        rule_id=record["rule_id"],
        firewall_command=record["firewall_command"],
        message=f"Host {req.ip_address} successfully quarantined via active firewall rule.",
        timestamp=record["timestamp"]
    )

@app.post("/api/mitigation/unblock")
def release_attacker_ip(req: BlockIPRequest):
    """
    Releases an IP address from active quarantine.
    """
    success, msg = engine.unblock_ip(req.ip_address)
    if not success:
        raise HTTPException(status_code=404, detail=msg)
    return {"status": "success", "message": msg, "ip_address": req.ip_address}

@app.get("/api/mitigation/rules")
def get_active_quarantine_rules():
    """
    Returns the list of active firewall quarantine rules.
    """
    return engine.get_quarantine_rules()

@app.post("/api/sniffer/toggle")
def toggle_live_sniffer():
    """
    Toggles between Test Reservoir Simulation Mode and Real Live Network Sniffer Mode.
    """
    if engine.ingestion_mode == "SIMULATION":
        started, msg = sniffer_service.start()
        if started:
            engine.set_ingestion_mode("LIVE_SNIFFER")
            return {"status": "success", "mode": "LIVE_SNIFFER", "message": msg}
        else:
            return {"status": "warning", "mode": "SIMULATION", "message": f"Could not bind raw socket: {msg}. Retaining simulation stream."}
    else:
        sniffer_service.stop()
        engine.set_ingestion_mode("SIMULATION")
        return {"status": "success", "mode": "SIMULATION", "message": "Switched to Authentic Reservoir Simulation Mode."}

@app.get("/api/stats")
def get_realtime_system_stats():
    """
    Returns rolling system stats, benign/threat ratios, and threat distribution.
    """
    return engine.get_system_stats()

@app.get("/api/alerts")
def get_security_alerts(limit: int = 15):
    """
    Returns recent security intrusion alerts with XAI feature breakdowns.
    """
    return engine.get_recent_alerts(limit=limit)

@app.get("/api/benchmarks")
def get_academic_benchmarks():
    """
    Returns model benchmark comparisons (LightGBM vs XGBoost vs Random Forest vs Decision Tree),
    Stage 2 multi-class confusion matrix, and feature importance rankings for academic defense.
    """
    metrics_path = os.path.join(MODELS_DIR, "metrics_summary.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Benchmarks not found.")

@app.post("/api/copilot/briefing", response_model=CopilotAnalysisResponse)
def generate_ai_copilot_briefing(req: CopilotAnalysisRequest):
    """
    AI Security Copilot: Synthesizes a human-readable threat investigation report
    with technical blast radius, MITRE alignment, and remediation instructions.
    """
    flow = req.flow_details or {}
    threat = flow.get("threat_type", "Unknown Intrusion")
    src_ip = flow.get("source_ip", "198.51.100.22")
    dst_port = flow.get("destination_port", 80)
    mitre_id = flow.get("mitre_id", "T1498")
    severity = flow.get("severity", "HIGH")
    anomaly = flow.get("anomaly_score", 85.0)

    title = f"AI Incident Report: Critical {threat} Campaign from {src_ip}"
    summary = (
        f"Autonomous Threat Engine flagged suspicious activity from external host {src_ip} "
        f"targeting internal service on port {dst_port}. The flow exhibited an anomaly divergence "
        f"score of {anomaly}% with high statistical deviation in packet timing and TCP flags."
    )
    ttp = (
        f"Mapped to MITRE ATT&CK {mitre_id} ({threat}). Adversary behavior exhibits automated "
        f"scripting and connection saturation intended to degrade availability or discover service vulnerabilities."
    )
    mitigation = [
        f"Enforce immediate OS firewall block on remote IP: {src_ip}",
        f"Audit incoming SYN queues on port {dst_port} and enable SYN Cookie protection",
        "Capture pcap sample for sandbox dynamic behavioral analysis",
        "Notify upstream gateway router to scrub traffic originating from subnet"
    ]
    fw_cmd = f'netsh advfirewall firewall add rule name="CS_BLOCK_{src_ip.replace(".", "_")}" dir=in action=block remoteip={src_ip}'

    return CopilotAnalysisResponse(
        alert_id=req.alert_id,
        incident_title=title,
        severity=severity,
        executive_summary=summary,
        threat_actor_ttp=ttp,
        recommended_mitigation=mitigation,
        firewall_command=fw_cmd
    )

# -------------------------------------------------------------
# FRONTEND STATIC SERVING
# -------------------------------------------------------------

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_dashboard():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Cyber Sentinel Next-Gen AI-SOC is running. Frontend UI not found."}
