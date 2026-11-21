"""
Cyber Sentinel Next-Gen AI-SOC
Application Launcher & Web Server Runner
Features:
- Auto-detects free ports (8000, 8050, 8080)
- Auto-launches default web browser directly to the dashboard
- Serves high-performance FastAPI backend
"""

import os
import sys
import time
import socket
import webbrowser
import uvicorn

# Ensure the root of CyberSentinel_AI_SOC is in the python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def is_port_available(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False

def find_available_port(preferred_ports=[8050, 8000, 8080, 8888]):
    for p in preferred_ports:
        if is_port_available(p):
            return p
    return 8050

def main():
    host = "127.0.0.1"
    port = find_available_port()
    dashboard_url = f"http://{host}:{port}"

    print("=" * 75)
    print("🛡️  CYBER SENTINEL — NEXT-GEN AI-SOC & AUTONOMOUS THREAT DEFENSE")
    print("=" * 75)
    print(f"[*] Starting High-Performance FastAPI Backend Engine...")
    print(f"[*] Access Cyber SOC Dashboard at: {dashboard_url}")
    print(f"[*] Interactive API Docs (Swagger): {dashboard_url}/docs")
    print(f"[*] Real-Time Explainable AI (XAI) & Incident Copilot: ACTIVE")
    print("=" * 75)
    print(f"[*] Launching browser dashboard in 1.5 seconds...")

    def open_browser():
        time.sleep(1.5)
        webbrowser.open(dashboard_url)

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # Run Uvicorn server
    uvicorn.run("backend.main:app", host=host, port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()
