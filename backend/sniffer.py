"""
Cyber Sentinel Next-Gen AI-SOC
Live Network Packet Sniffer & Flow Aggregator
Captures real live network packets from physical interfaces using Scapy,
aggregates them into 20-feature bidirectional network flow vectors in real time.
"""

import time
import threading
import collections
from typing import Optional, Dict, Any

try:
    from scapy.all import sniff, IP, TCP, UDP
    SCAPY_AVAILABLE = True
except Exception:
    SCAPY_AVAILABLE = False

class LivePacketSniffer:
    def __init__(self, max_queue_size=200):
        self.max_queue_size = max_queue_size
        self.flow_queue = collections.deque(maxlen=max_queue_size)
        self.active_flows = {}
        self.is_sniffing = False
        self.sniff_thread = None
        self.lock = threading.Lock()
        self.status_message = "Idle"
        self.packets_captured = 0

    def start(self, interface: Optional[str] = None):
        if not SCAPY_AVAILABLE:
            self.status_message = "Scapy not available. Live capture disabled."
            return False, self.status_message

        if self.is_sniffing:
            return True, "Sniffer is already active."

        self.is_sniffing = True
        self.packets_captured = 0
        self.sniff_thread = threading.Thread(target=self._sniff_worker, daemon=True)
        self.sniff_thread.start()
        self.status_message = "Sniffing live network interfaces..."
        return True, self.status_message

    def stop(self):
        self.is_sniffing = False
        self.status_message = "Sniffer stopped."
        return True, "Sniffer stopped."

    def _process_packet(self, pkt):
        if not self.is_sniffing:
            return
        if not pkt.haslayer(IP):
            return

        self.packets_captured += 1
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        proto = pkt[IP].proto
        length = len(pkt)

        sport = 0
        dport = 80
        syn = 0
        rst = 0
        psh = 0
        ack = 0
        win_size = 29200

        if pkt.haslayer(TCP):
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            flags = pkt[TCP].flags
            syn = 1 if flags & 0x02 else 0
            rst = 1 if flags & 0x04 else 0
            psh = 1 if flags & 0x08 else 0
            ack = 1 if flags & 0x10 else 0
            win_size = pkt[TCP].window or 29200
        elif pkt.haslayer(UDP):
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport

        # Flow key: sorted 5-tuple
        flow_key = tuple(sorted([(src_ip, sport), (dst_ip, dport)])) + (proto,)
        now = time.time()

        with self.lock:
            if flow_key not in self.active_flows:
                self.active_flows[flow_key] = {
                    "start_time": now,
                    "last_time": now,
                    "fwd_pkts": 1,
                    "bwd_pkts": 0,
                    "fwd_bytes": length,
                    "bwd_bytes": 0,
                    "fwd_lens": [length],
                    "bwd_lens": [],
                    "iats": [],
                    "syn": syn,
                    "rst": rst,
                    "psh": psh,
                    "ack": ack,
                    "win": win_size,
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "dport": dport
                }
            else:
                f = self.active_flows[flow_key]
                iat = (now - f["last_time"]) * 1e6
                f["iats"].append(iat)
                f["last_time"] = now

                if src_ip == f["src_ip"]:
                    f["fwd_pkts"] += 1
                    f["fwd_bytes"] += length
                    f["fwd_lens"].append(length)
                else:
                    f["bwd_pkts"] += 1
                    f["bwd_bytes"] += length
                    f["bwd_lens"].append(length)

                f["syn"] += syn
                f["rst"] += rst
                f["psh"] += psh
                f["ack"] += ack

                # If flow has accumulated enough packets or lived > 1.2s, flush to flow_queue
                duration_us = (now - f["start_time"]) * 1e6
                tot_pkts = f["fwd_pkts"] + f["bwd_pkts"]
                if tot_pkts >= 5 or duration_us >= 1.2e6:
                    sec = max(duration_us / 1e6, 0.001)
                    tot_bytes = f["fwd_bytes"] + f["bwd_bytes"]
                    flow_record = {
                        "Destination_Port": float(f["dport"]),
                        "Flow_Duration": float(duration_us),
                        "Total_Fwd_Packets": float(f["fwd_pkts"]),
                        "Total_Backward_Packets": float(f["bwd_pkts"]),
                        "Total_Length_of_Fwd_Packets": float(f["fwd_bytes"]),
                        "Total_Length_of_Bwd_Packets": float(f["bwd_bytes"]),
                        "Fwd_Packet_Length_Max": float(max(f["fwd_lens"]) if f["fwd_lens"] else 0),
                        "Fwd_Packet_Length_Min": float(min(f["fwd_lens"]) if f["fwd_lens"] else 0),
                        "Fwd_Packet_Length_Mean": float(sum(f["fwd_lens"])/len(f["fwd_lens"]) if f["fwd_lens"] else 0),
                        "Bwd_Packet_Length_Mean": float(sum(f["bwd_lens"])/len(f["bwd_lens"]) if f["bwd_lens"] else 0),
                        "Flow_Bytes_s": float(tot_bytes / sec),
                        "Flow_Packets_s": float(tot_pkts / sec),
                        "Flow_IAT_Mean": float(sum(f["iats"])/len(f["iats"]) if f["iats"] else 1000.0),
                        "Flow_IAT_Std": 250.0,
                        "SYN_Flag_Count": float(min(f["syn"], 1)),
                        "RST_Flag_Count": float(min(f["rst"], 1)),
                        "PSH_Flag_Count": float(min(f["psh"], 1)),
                        "ACK_Flag_Count": float(min(f["ack"], 1)),
                        "Average_Packet_Size": float(tot_bytes / max(tot_pkts, 1)),
                        "Init_Win_bytes_forward": float(f["win"]),
                        "Source_IP": f["src_ip"],
                        "Destination_IP": f["dst_ip"],
                        "Label": "LIVE_CAPTURED"
                    }
                    self.flow_queue.append(flow_record)
                    del self.active_flows[flow_key]

    def _sniff_worker(self):
        try:
            sniff(prn=self._process_packet, store=False, stop_filter=lambda _: not self.is_sniffing)
        except Exception as e:
            self.status_message = f"Live sniff error (admin rights may be required): {e}"
            self.is_sniffing = False

    def pop_flow(self) -> Optional[Dict[str, Any]]:
        with self.lock:
            if self.flow_queue:
                return self.flow_queue.popleft()
        return None

sniffer_service = LivePacketSniffer()
