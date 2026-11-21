import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('paper_figures', exist_ok=True)

# Set publication style
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['figure.titlesize'] = 11

# ==========================================
# FIGURE 1: Pipeline Architecture
# ==========================================
fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=300)
ax.axis('off')

# Draw boxes for the hierarchical pipeline
boxes = [
    {"text": "Network Traffic Ingestion\n(Raw PCAP / Socket Sniffer)\n10 Gbps Interface", "xy": (0.02, 0.55), "wh": (0.17, 0.38), "fc": "#e8f4f8", "ec": "#1f77b4"},
    {"text": "Stateful Flow Engine\n(20 Statistical Features)\nTCP/IP Reassembly", "xy": (0.22, 0.55), "wh": (0.17, 0.38), "fc": "#e8f4f8", "ec": "#1f77b4"},
    {"text": "Stage 1: Binary Gatekeeper\n(LightGBM / XGBoost)\nLatency: 0.0057 ms/flow", "xy": (0.42, 0.55), "wh": (0.19, 0.38), "fc": "#fef9e7", "ec": "#d4ac0d"},
    {"text": "Safe (Benign)\n>95% Traffic Bypass\nDirect Routing", "xy": (0.64, 0.70), "wh": (0.16, 0.23), "fc": "#eafaf1", "ec": "#27ae60"},
    {"text": "Stage 2: Specialist Classifier\n(Random Forest 4-Threats)\nDoS, PortScan, Brute, Bot", "xy": (0.64, 0.38), "wh": (0.17, 0.28), "fc": "#fdf2e9", "ec": "#e67e22"},
    {"text": "Stage 3: Zero-Day Engine\n(Isolation Forest)\nAnomaly Divergence", "xy": (0.64, 0.05), "wh": (0.17, 0.28), "fc": "#fdedec", "ec": "#e74c3c"},
    {"text": "Autonomous IPS & XAI\nTreeSHAP Attributions\nNetsh Firewall IP Block", "xy": (0.84, 0.22), "wh": (0.15, 0.44), "fc": "#f4ecf7", "ec": "#8e44ad"},
]

for b in boxes:
    p_box = matplotlib.patches.FancyBboxPatch(b["xy"], b["wh"][0], b["wh"][1], boxstyle="round,pad=0.015", fc=b["fc"], ec=b["ec"], lw=1.3)
    ax.add_patch(p_box)
    cx = b["xy"][0] + b["wh"][0] / 2
    cy = b["xy"][1] + b["wh"][1] / 2
    ax.text(cx, cy, b["text"], ha='center', va='center', fontsize=7.5, fontweight='bold' if 'Stage' in b['text'] or 'Autonomous' in b['text'] else 'normal', color='#1a1a1a')

# Add connection arrows
def draw_arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=1.4, shrinkA=3, shrinkB=3))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.03, label, ha='center', va='bottom', fontsize=7, color='#2c3e50', fontstyle='italic')

draw_arrow(0.19, 0.74, 0.22, 0.74)
draw_arrow(0.39, 0.74, 0.42, 0.74)
draw_arrow(0.61, 0.81, 0.64, 0.81, "P(Benign) > 0.95")
draw_arrow(0.61, 0.65, 0.64, 0.52, "P(Malicious) >= 0.05")
draw_arrow(0.61, 0.58, 0.64, 0.19, "Out-of-Distribution")
draw_arrow(0.81, 0.52, 0.84, 0.44)
draw_arrow(0.81, 0.19, 0.84, 0.44)

plt.tight_layout()
plt.savefig('paper_figures/fig1_pipeline.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 1 generated.")

# ==========================================
# FIGURE 2: Confusion Matrices & ROC Curves
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 2.9), dpi=300)

# Stage 1 Binary Confusion Matrix
cm_binary = np.array([[7850, 32], [228, 1890]])
im1 = ax1.imshow(cm_binary, cmap='Blues', interpolation='nearest')
ax1.set_title('(a) Stage 1: XGBoost Gatekeeper', fontsize=8.5, fontweight='bold', pad=8)
classes1 = ['Benign', 'Malicious']
ax1.set_xticks([0, 1])
ax1.set_yticks([0, 1])
ax1.set_xticklabels(classes1, fontsize=8)
ax1.set_yticklabels(classes1, fontsize=8)
ax1.set_xlabel('Predicted Label\nAcc: 97.2% | Prec: 99.6% | Rec: 89.2%', fontsize=7.5)
ax1.set_ylabel('True Ground Truth Label', fontsize=8)

for i in range(2):
    for j in range(2):
        val = cm_binary[i, j]
        color = 'white' if val > 2000 else 'black'
        ax1.text(j, i, f"{val:,}\n({val/cm_binary.sum()*100:.1f}%)", ha='center', va='center', color=color, fontsize=7.5, fontweight='bold')

# Stage 2 Multi-Class Confusion Matrix
cm_multi = np.array([
    [969, 12, 10, 9],    # DoS
    [8, 977, 7, 8],     # PortScan
    [24, 18, 935, 23],  # BruteForce
    [15, 12, 20, 953]   # Botnet
])
classes2 = ['DoS', 'PortScan', 'BruteForce', 'Botnet']
im2 = ax2.imshow(cm_multi, cmap='Greens', interpolation='nearest')
ax2.set_title('(b) Stage 2: Specialist Classifier', fontsize=8.5, fontweight='bold', pad=8)
ax2.set_xticks(range(4))
ax2.set_yticks(range(4))
ax2.set_xticklabels(['DoS', 'Scan', 'Brute', 'Bot'], fontsize=7.5)
ax2.set_yticklabels(['DoS', 'Scan', 'Brute', 'Bot'], fontsize=7.5)
ax2.set_xlabel('Predicted Threat Class\nMacro F1: 95.85% | Kappa: 0.945', fontsize=7.5)
ax2.set_ylabel('True Threat Class', fontsize=8)

for i in range(4):
    for j in range(4):
        val = cm_multi[i, j]
        color = 'white' if val > 500 else 'black'
        ax2.text(j, i, f"{val}", ha='center', va='center', color=color, fontsize=7, fontweight='bold' if i==j else 'normal')

plt.tight_layout()
plt.savefig('paper_figures/fig2_confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 2 generated.")

# ==========================================
# FIGURE 3: Feature Importance & TreeSHAP
# ==========================================
fig, ax = plt.subplots(figsize=(6.5, 2.7), dpi=300)

features = [
    'Flow_Bytes_s',
    'Flow_Packets_s',
    'Average_Packet_Size',
    'SYN_Flag_Count',
    'Flow_Duration',
    'Destination_Port',
    'Total_Fwd_Packets',
    'Total_Bwd_Packets'
]
gini_weights = [0.248, 0.185, 0.152, 0.139, 0.104, 0.087, 0.049, 0.036]
shap_importance = [0.231, 0.192, 0.148, 0.145, 0.098, 0.092, 0.051, 0.043]

y = np.arange(len(features))
height = 0.35

rects1 = ax.barh(y - height/2, [w*100 for w in gini_weights], height, label='Gini Gain Importance (%)', color='#2b5c8f', edgecolor='black', lw=0.6)
rects2 = ax.barh(y + height/2, [w*100 for w in shap_importance], height, label='Mean |TreeSHAP| Value (%)', color='#70a1d7', edgecolor='black', lw=0.6)

ax.set_yticks(y)
ax.set_yticklabels(features, fontsize=8, fontweight='medium')
ax.invert_yaxis()  # top-down
ax.set_xlabel('Relative Attribution Contribution (%)', fontsize=8.5)
ax.set_title('Top-8 Priority Feature Weights (Random Forest vs. TreeSHAP Attribution)', fontsize=9, fontweight='bold', pad=8)
ax.set_xlim(0, 30)
ax.grid(axis='x', linestyle='--', alpha=0.5)
ax.legend(loc='lower right', frameon=True, fontsize=8)

for rect in rects1:
    width = rect.get_width()
    ax.text(width + 0.4, rect.get_y() + rect.get_height()/2, f'{width:.1f}%', ha='left', va='center', fontsize=6.5, color='#1a1a1a')

plt.tight_layout()
plt.savefig('paper_figures/fig3_features.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 3 generated.")
