"""
Cyber Sentinel Next-Gen AI-SOC
Pydantic Schemas & Data Transfer Objects
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class NetworkFlowInput(BaseModel):
    Destination_Port: float = Field(80, description="Destination port number")
    Flow_Duration: float = Field(150000, description="Flow duration in microseconds")
    Total_Fwd_Packets: float = Field(8, description="Total packets in forward direction")
    Total_Backward_Packets: float = Field(7, description="Total packets in backward direction")
    Total_Length_of_Fwd_Packets: float = Field(2400, description="Total bytes in forward direction")
    Total_Length_of_Bwd_Packets: float = Field(4500, description="Total bytes in backward direction")
    Fwd_Packet_Length_Max: float = Field(500, description="Max length of forward packet")
    Fwd_Packet_Length_Min: float = Field(40, description="Min length of forward packet")
    Fwd_Packet_Length_Mean: float = Field(300, description="Mean length of forward packet")
    Bwd_Packet_Length_Mean: float = Field(640, description="Mean length of backward packet")
    Flow_Bytes_s: float = Field(46000, description="Flow byte throughput per second")
    Flow_Packets_s: float = Field(100, description="Flow packet rate per second")
    Flow_IAT_Mean: float = Field(10500, description="Mean time between two packets")
    Flow_IAT_Std: float = Field(4200, description="Standard deviation of inter-arrival time")
    SYN_Flag_Count: float = Field(0, description="SYN flag count (0 or 1)")
    RST_Flag_Count: float = Field(0, description="RST flag count (0 or 1)")
    PSH_Flag_Count: float = Field(1, description="PSH flag count (0 or 1)")
    ACK_Flag_Count: float = Field(1, description="ACK flag count (0 or 1)")
    Average_Packet_Size: float = Field(460, description="Average packet size across flow")
    Init_Win_bytes_forward: float = Field(29200, description="Initial TCP window size forward")

class InjectRequest(BaseModel):
    attack_type: str = Field(..., description="Threat type: DoS, PortScan, BruteForce, Botnet, or ZeroDay_Anomaly")

class BlockIPRequest(BaseModel):
    ip_address: str = Field(..., description="Target attacker IPv4 address to quarantine")
    threat_type: Optional[str] = Field("Unknown", description="Threat type that triggered the block")
    reason: Optional[str] = Field("Automated IPS Rule Triggered", description="Audit reason")

class BlockIPResponse(BaseModel):
    status: str
    ip_address: str
    rule_id: str
    firewall_command: str
    message: str
    timestamp: str

class CopilotAnalysisRequest(BaseModel):
    alert_id: str
    flow_details: Optional[Dict[str, Any]] = None

class CopilotAnalysisResponse(BaseModel):
    alert_id: str
    incident_title: str
    severity: str
    executive_summary: str
    threat_actor_ttp: str
    recommended_mitigation: List[str]
    firewall_command: str
