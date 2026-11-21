/**
 * Cyber Sentinel • Web3 Bento Grid Telemetry Engine
 * Dynamic SVG Charting, 3D Cards Stack, SHAP XAI Inspector, and Autonomous Mitigation Logic
 */

let isAudioMuted = false;
let isStreamPaused = false;
let streamSpeedMode = 'Normal';
let streamIntervalMs = 1200;
let streamTimer = null;
let currentInspectedFlow = null;

// Telemetry state for Hero 30-day/interval strip
const HERO_STRIP_COUNT = 30;
let heroStripData = Array.from({ length: HERO_STRIP_COUNT }, (_, i) => ({
  val: 20 + Math.sin(i * 0.4) * 12 + Math.random() * 8,
  anomaly: Math.random() > 0.8
}));

// SVG Chart Telemetry Queues (15 points)
const CHART_POINTS = 16;
let chartPrimaryData = [12, 14, 18, 15, 22, 28, 24, 35, 42, 38, 48, 52, 45, 62, 58, 48.5];
let chartBaselineData = [10, 11, 12, 10, 13, 12, 14, 13, 15, 14, 16, 15, 14, 15, 16, 15];

// Threat Counts
const threatDistribution = {
  DoS: 252,
  PortScan: 179,
  BruteForce: 105,
  Botnet: 69,
  ZeroDay_Anomaly: 139
};
let totalInspectedCounter = 1896;

// Traffic Filter & Continuous Flow History (Normal + Attacks)
let currentTrafficFilter = "all";
let networkFlowHistory = [
  {
    timestamp: "06:39:57 AM",
    source_ip: "192.168.1.66",
    destination_ip: "52.216.184.22",
    destination_port: 53,
    verdict: "BENIGN",
    threat_class: "BENIGN",
    is_attack: false,
    confidence: 100,
    severity: "SAFE"
  },
  {
    timestamp: "06:39:56 AM",
    source_ip: "172.16.0.24",
    destination_ip: "192.168.1.39",
    destination_port: 3389,
    verdict: "MALICIOUS",
    threat_class: "PortScan",
    is_attack: true,
    confidence: 100,
    severity: "MEDIUM"
  },
  {
    timestamp: "06:39:55 AM",
    source_ip: "192.168.1.11",
    destination_ip: "52.216.184.22",
    destination_port: 53,
    verdict: "BENIGN",
    threat_class: "BENIGN",
    is_attack: false,
    confidence: 100,
    severity: "SAFE"
  },
  {
    timestamp: "06:39:54 AM",
    source_ip: "172.16.0.7",
    destination_ip: "192.168.1.32",
    destination_port: 443,
    verdict: "MALICIOUS",
    threat_class: "PortScan",
    is_attack: true,
    confidence: 100,
    severity: "MEDIUM"
  },
  {
    timestamp: "06:39:52 AM",
    source_ip: "192.168.1.98",
    destination_ip: "142.250.190.46",
    destination_port: 80,
    verdict: "BENIGN",
    threat_class: "BENIGN",
    is_attack: false,
    confidence: 100,
    severity: "SAFE"
  },
  {
    timestamp: "06:39:51 AM",
    source_ip: "192.168.1.78",
    destination_ip: "142.250.190.46",
    destination_port: 443,
    verdict: "BENIGN",
    threat_class: "BENIGN",
    is_attack: false,
    confidence: 100,
    severity: "SAFE"
  },
  {
    timestamp: "06:39:50 AM",
    source_ip: "10.0.0.67",
    destination_ip: "192.168.1.100",
    destination_port: 80,
    verdict: "MALICIOUS",
    threat_class: "DoS",
    is_attack: true,
    confidence: 100,
    severity: "CRITICAL"
  },
  {
    timestamp: "06:39:49 AM",
    source_ip: "198.51.100.24",
    destination_ip: "192.168.1.15",
    destination_port: 22,
    verdict: "MALICIOUS",
    threat_class: "BruteForce",
    is_attack: true,
    confidence: 100,
    severity: "HIGH"
  },
  {
    timestamp: "06:39:48 AM",
    source_ip: "192.168.1.45",
    destination_ip: "104.244.42.1",
    destination_port: 443,
    verdict: "BENIGN",
    threat_class: "BENIGN",
    is_attack: false,
    confidence: 99.8,
    severity: "SAFE"
  },
  {
    timestamp: "06:39:47 AM",
    source_ip: "192.168.1.105",
    destination_ip: "13.107.42.14",
    destination_port: 443,
    verdict: "BENIGN",
    threat_class: "BENIGN",
    is_attack: false,
    confidence: 100,
    severity: "SAFE"
  },
  {
    timestamp: "06:39:46 AM",
    source_ip: "198.51.100.31",
    destination_ip: "192.168.1.5",
    destination_port: 80,
    verdict: "MALICIOUS",
    threat_class: "Botnet",
    is_attack: true,
    confidence: 98.7,
    severity: "HIGH"
  },
  {
    timestamp: "06:39:45 AM",
    source_ip: "203.0.113.88",
    destination_ip: "192.168.1.1",
    destination_port: 8080,
    verdict: "MALICIOUS",
    threat_class: "ZeroDay_Anomaly",
    is_attack: true,
    confidence: 99.2,
    severity: "CRITICAL"
  }
];

// Recent Incidents Feed Store
let incidentFeed = [
  {
    id: "ALT-DoS-01",
    type: "DoS SYN Flood",
    kind: "dos",
    ip: "198.51.100.22",
    detail: "Volumetric SYN flood on port 80",
    rate: "48,500 pkts/s",
    status: "mitigated",
    time: "now",
    flow: null
  },
  {
    id: "ALT-SCAN-02",
    type: "PortScan Recon",
    kind: "scan",
    ip: "203.0.113.88",
    detail: "Aggressive SYN sweep 1-1024",
    rate: "12,400 pkts/s",
    status: "blocked",
    time: "14s ago",
    flow: null
  },
  {
    id: "ALT-ZERO-03",
    type: "Zero-Day Anomaly",
    kind: "zero",
    ip: "192.168.1.185",
    detail: "Unseen payload entropy vector",
    rate: "94.2% div",
    status: "quarantined",
    time: "48s ago",
    flow: null
  },
  {
    id: "ALT-BOT-04",
    type: "Botnet C2 Beacon",
    kind: "bot",
    ip: "198.51.100.99",
    detail: "Periodic IRC/TLS beaconing",
    rate: "35.5% div",
    status: "neutralized",
    time: "2m ago",
    flow: null
  }
];

// -------------------------------------------------------------
// INITIALIZATION
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  try { initHeroStrip(); } catch (e) { console.error("Hero strip init error:", e); }
  try { initSVGChart(); } catch (e) { console.error("SVG chart init error:", e); }
  try { initThreatDonutChart(); } catch (e) { console.error("Donut chart init error:", e); }
  try { renderIncidentFeed(); } catch (e) { console.error("Incident feed init error:", e); }
  try { renderTrafficHistoryTable(); } catch (e) { console.error("Traffic history init error:", e); }
  try { updateFilterCounters(); } catch (e) { console.error("Filter counters init error:", e); }
  try { initDefaultDeepDive(); } catch (e) { console.error("Deep dive init error:", e); }
  try { initEpochTimer(); } catch (e) { console.error("Epoch timer init error:", e); }

  // Guarantee stream starts polling immediately
  try { startStreamTimer(); } catch (e) { console.error("Stream timer error:", e); }

  // Sync initial stats
  try { fetchSystemStats(); } catch (e) { console.error("Stats fetch error:", e); }
});

// -------------------------------------------------------------
// STREAM TIMER & SPEED CONTROLS
// -------------------------------------------------------------
function startStreamTimer() {
  if (streamTimer) clearInterval(streamTimer);
  streamTimer = setInterval(pollNextStreamFlow, streamIntervalMs);
}

function setStreamSpeed(speed, btnElem) {
  streamSpeedMode = speed;
  if (speed === 'Slow') streamIntervalMs = 2200;
  else if (speed === 'Normal') streamIntervalMs = 1200;
  else if (speed === 'Fast') streamIntervalMs = 400;

  // Update pills active state
  const parent = btnElem.parentElement;
  parent.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
  btnElem.classList.add('active');

  if (!isStreamPaused) {
    startStreamTimer();
  }
}

function toggleStreamPlayPause() {
  isStreamPaused = !isStreamPaused;
  playCyberSound('click');
  const btn = document.getElementById("btn-toggle-stream");
  const icon = document.getElementById("stream-play-icon");
  const text = document.getElementById("stream-play-text");

  if (isStreamPaused) {
    if (streamTimer) clearInterval(streamTimer);
    btn.className = "btn btn-accent";
    icon.className = "fa-solid fa-play";
    text.textContent = "Resume Stream";
    document.getElementById("nav-status-label").textContent = "STREAM PAUSED // PERIMETER FROZEN";
  } else {
    btn.className = "btn btn-primary-toggle";
    icon.className = "fa-solid fa-pause";
    text.textContent = "Pause Stream";
    document.getElementById("nav-status-label").textContent = "PERIMETER ACTIVE • TWO-STAGE LIGHTGBM";
    startStreamTimer();
  }
}

// -------------------------------------------------------------
// WEB AUDIO API SYNTHESIZER (ZERO-DEPENDENCY SCI-FI SOUND FX)
// -------------------------------------------------------------
let audioCtx = null;

function ensureAudioContext() {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (AudioContextClass) {
      audioCtx = new AudioContextClass();
    }
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}

// Automatically unlock Web Audio on first user interaction (browser autoplay policy)
['click', 'keydown', 'touchstart'].forEach(evt => {
  document.addEventListener(evt, () => {
    ensureAudioContext();
  }, { once: true });
});

function playCyberSound(type) {
  if (isAudioMuted) return;
  try {
    ensureAudioContext();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;

    if (type === 'critical' || type === 'threat_critical') {
      // Urgent intrusion alarm: dual pulsing sawteeth (820 -> 320 Hz)
      [0, 0.16].forEach(delay => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(820, now + delay);
        osc.frequency.exponentialRampToValueAtTime(320, now + delay + 0.12);
        gain.gain.setValueAtTime(0.20, now + delay);
        gain.gain.exponentialRampToValueAtTime(0.01, now + delay + 0.12);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now + delay);
        osc.stop(now + delay + 0.13);
      });
    } else if (type === 'warning' || type === 'threat_warning') {
      // Threat alert chime (medium/high): dual harmonic ping
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(587, now);
      osc.frequency.exponentialRampToValueAtTime(440, now + 0.18);
      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.19);
    } else if (type === 'zero_day') {
      // Ominous sci-fi resonance for unknown / zero-day anomalies
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(280, now);
      osc.frequency.exponentialRampToValueAtTime(90, now + 0.35);
      gain.gain.setValueAtTime(0.24, now);
      gain.gain.exponentialRampToValueAtTime(0.005, now + 0.35);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.36);
    } else if (type === 'quarantine') {
      // Firewall clamp / electric zap
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "square";
      osc.frequency.setValueAtTime(300, now);
      osc.frequency.exponentialRampToValueAtTime(60, now + 0.22);
      gain.gain.setValueAtTime(0.20, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.22);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.23);
    } else if (type === 'inject') {
      // Attack injection sci-fi uplink sweep
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(350, now);
      osc.frequency.exponentialRampToValueAtTime(1100, now + 0.14);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.14);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.15);
    } else if (type === 'click') {
      // Soft interface tap
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(800, now);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.04);
    }
  } catch (err) {
    console.debug("Audio error:", err);
  }
}

function toggleAudio() {
  isAudioMuted = !isAudioMuted;
  ensureAudioContext();
  const icon = document.getElementById("audio-icon");
  const btn = document.getElementById("btn-toggle-audio");
  const label = document.getElementById("audio-btn-label");
  if (isAudioMuted) {
    icon.className = "fa-solid fa-volume-xmark";
    icon.style.color = "var(--accent-red)";
    if (label) label.textContent = "Audio FX: OFF";
    if (btn) btn.title = "Audio Muted (Click to Unmute)";
  } else {
    icon.className = "fa-solid fa-volume-high";
    icon.style.color = "var(--accent)";
    if (label) label.textContent = "Audio FX: ON";
    if (btn) btn.title = "Audio FX Enabled (Click to Mute)";
    playCyberSound('click');
  }
}

function playAlertChime() {
  playCyberSound('critical');
}

// -------------------------------------------------------------
// LIVE STREAM POLLER (FETCHES TELEMETRY FROM FASTAPI)
// -------------------------------------------------------------
async function pollNextStreamFlow() {
  if (isStreamPaused) return;

  try {
    const response = await fetch("/api/stream/next");
    if (!response.ok) return;

    const flow = await response.json();
    totalInspectedCounter++;

    // Update Counter
    document.getElementById("hero-inspected-counter").textContent = totalInspectedCounter.toLocaleString();

    // Ingestion latency & throughput
    const kpkts = (flow.flow_packets_s / 1000).toFixed(1);
    const flowMBs = (flow.flow_bytes_s / (1024 * 1024)).toFixed(1);

    // Update Gauge
    updateGauge(parseFloat(kpkts), flowMBs);

    // Update Hero 30-interval strip
    pushHeroStrip(parseFloat(kpkts), flow.verdict === "MALICIOUS");

    // Update Dual Curve SVG Chart
    pushSVGChartData(parseFloat(kpkts), 14.5 + (Math.random() - 0.5) * 3);

    // Record into Continuous Flow History (both Benign and Attacks)
    recordFlowInHistory(flow);

    // Handle Attack / Alert
    if (flow.verdict === "MALICIOUS") {
      handleMaliciousFlow(flow, kpkts);
    }

  } catch (err) {
    console.warn("Telemetry stream error:", err);
  }
}

// -------------------------------------------------------------
// HERO 30-BAR STRIP RENDERING
// -------------------------------------------------------------
function initHeroStrip() {
  const container = document.getElementById("hero-bars-strip");
  if (!container) return;
  container.innerHTML = "";

  const maxVal = Math.max(...heroStripData.map(d => d.val), 50);

  heroStripData.forEach((item, idx) => {
    const bar = document.createElement("button");
    bar.type = "button";
    bar.className = "hero-strip-bar";
    const heightPct = Math.max(8, Math.min(100, (item.val / maxVal) * 100));
    bar.style.height = `${heightPct}%`;
    bar.style.background = item.anomaly ? "var(--accent-red)" : "var(--accent)";
    bar.style.opacity = (0.35 + (idx / HERO_STRIP_COUNT) * 0.65).toFixed(2);

    bar.addEventListener("mouseenter", () => {
      document.getElementById("hero-hover-label").textContent = 
        `Interval T-${HERO_STRIP_COUNT - idx}: ${item.val.toFixed(1)} kpkts/s ${item.anomaly ? "(ANOMALY)" : ""}`;
    });

    bar.addEventListener("mouseleave", () => {
      document.getElementById("hero-hover-label").textContent = "Packet Velocity Stream";
    });

    container.appendChild(bar);
  });
}

function pushHeroStrip(val, isAnomaly) {
  heroStripData.shift();
  heroStripData.push({ val: Math.max(val, 12), anomaly: isAnomaly });
  initHeroStrip();
}

// -------------------------------------------------------------
// PACKET VELOCITY GAUGE (SEMICIRCLE ARC & ROTATING NEEDLE)
// -------------------------------------------------------------
function updateGauge(kpkts, mbRate) {
  const arc = document.getElementById("gauge-arc-path");
  const needle = document.getElementById("gauge-needle-group");
  const valElem = document.getElementById("gauge-packets-num");
  const subElem = document.getElementById("gauge-bytes-desc");

  valElem.textContent = kpkts.toFixed(1);
  subElem.textContent = `≈ ${mbRate} MB/s throughput`;

  // Scale: 0 to 60 kpkts/s
  const t = Math.max(0, Math.min(1, kpkts / 60));
  const totalLength = 194.7; // Arc length: PI * 62
  const offset = totalLength * (1 - t);
  const angle = -90 + t * 180;

  arc.style.strokeDashoffset = offset.toFixed(1);
  arc.style.stroke = t > 0.7 ? "var(--accent-red)" : "var(--accent)";
  needle.style.transform = `rotate(${angle.toFixed(1)}deg)`;
}

// -------------------------------------------------------------
// 3D STACKED NETWORK PACKET FRAMES (PCAP BUFFER CONTROLLER)
// -------------------------------------------------------------
let cardOrder = [1, 2, 3]; // Back to front
const cardMetadata = {
  1: { ip: "198.51.100.22 ➔ PORT 80", sub: "Captured Packet Frame · Volumetric SYN Flood", score: "98.4% conf" },
  2: { ip: "203.0.113.88 ➔ PORTS 1-1024", sub: "Captured Packet Frame · SYN PortScan Sweep", score: "99.1% conf" },
  3: { ip: "192.168.1.185 ➔ PORT 8080", sub: "Unsupervised Anomaly · High-Entropy Payload", score: "94.2% conf" }
};

function bringCardToFront(cardId) {
  if (cardOrder[cardOrder.length - 1] === cardId) return;

  cardOrder = [...cardOrder.filter(id => id !== cardId), cardId];

  cardOrder.forEach((id, pos) => {
    const elem = document.getElementById(`threat-card-${id}`);
    if (!elem) return;
    const fromFront = cardOrder.length - 1 - pos;
    const topOffset = pos * 24;
    const scale = (1 - fromFront * 0.055).toFixed(3);

    elem.style.top = `${topOffset}px`;
    elem.style.zIndex = pos + 1;
    elem.style.transform = `translateX(-50%) scale(${scale})`;
    elem.style.cursor = fromFront === 0 ? "default" : "pointer";
  });

  // Update frosted panel with the active front card
  const meta = cardMetadata[cardId];
  if (meta) {
    document.getElementById("card-active-ip").textContent = meta.ip;
    document.getElementById("card-active-sub").textContent = meta.sub;
    document.getElementById("card-active-score").textContent = meta.score;
  }
}

// -------------------------------------------------------------
// DUAL CURVE SVG AREA CHART (SMOOTH CUBIC BEZIER)
// -------------------------------------------------------------
function smoothPoints(pts) {
  return pts.map(([x, y], i) => {
    if (i === 0) return `M ${x.toFixed(1)} ${y.toFixed(1)}`;
    const [px, py] = pts[i - 1];
    const mx = (px + x) / 2;
    return `C ${mx.toFixed(1)} ${py.toFixed(1)}, ${mx.toFixed(1)} ${y.toFixed(1)}, ${x.toFixed(1)} ${y.toFixed(1)}`;
  }).join(" ");
}

function initSVGChart() {
  const W = 640;
  const H = 220;
  const allVals = [...chartPrimaryData, ...chartBaselineData];
  const lo = Math.min(...allVals) * 0.8;
  const hi = Math.max(...allVals) * 1.15 || 1;

  const getY = (v) => H - 20 - ((v - lo) / (hi - lo || 1)) * (H - 45);

  const pa = chartPrimaryData.map((v, i) => [(i / (chartPrimaryData.length - 1)) * W, getY(v)]);
  const pb = chartBaselineData.map((v, i) => [(i / (chartBaselineData.length - 1)) * W, getY(v)]);

  const la = smoothPoints(pa);
  const lb = smoothPoints(pb);

  const primaryPath = document.getElementById("svg-chart-primary");
  const baselinePath = document.getElementById("svg-chart-baseline");
  const areaPath = document.getElementById("svg-chart-area");

  if (primaryPath) primaryPath.setAttribute("d", la);
  if (baselinePath) baselinePath.setAttribute("d", lb);
  if (areaPath) areaPath.setAttribute("d", `${la} L ${W} ${H} L 0 ${H} Z`);

  // Update stats
  const lastA = chartPrimaryData[chartPrimaryData.length - 1];
  const lastB = chartBaselineData[chartBaselineData.length - 1];
  document.getElementById("chart-observed-stat").textContent = `${Math.round(lastA * 1000).toLocaleString()} pkts/s`;
  document.getElementById("chart-baseline-stat").textContent = `${Math.round(lastB * 1000).toLocaleString()} pkts/s`;

  const ratio = (lastA / (lastB || 1)).toFixed(1);
  document.getElementById("chart-divergence-badge").textContent = `+${ratio}x vs Baseline`;
}

function pushSVGChartData(primaryVal, baselineVal) {
  chartPrimaryData.shift();
  chartPrimaryData.push(primaryVal);
  chartBaselineData.shift();
  chartBaselineData.push(baselineVal);
  initSVGChart();
}

function setChartRange(range, btn) {
  btn.parentElement.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function onChartPointerMove(e) {
  const box = document.getElementById("svg-chart-box");
  const rect = box.getBoundingClientRect();
  const relX = Math.max(0, Math.min(rect.width, e.clientX - rect.left));
  const pct = relX / rect.width;

  const idx = Math.min(chartPrimaryData.length - 1, Math.round(pct * (chartPrimaryData.length - 1)));
  const cursorLine = document.getElementById("chart-cursor-line");
  const dotA = document.getElementById("chart-cursor-dot-a");
  const dotB = document.getElementById("chart-cursor-dot-b");

  cursorLine.style.opacity = "1";
  cursorLine.style.left = `${pct * 100}%`;

  const W = 640;
  const H = 220;
  const allVals = [...chartPrimaryData, ...chartBaselineData];
  const lo = Math.min(...allVals) * 0.8;
  const hi = Math.max(...allVals) * 1.15 || 1;
  const getY = (v) => H - 20 - ((v - lo) / (hi - lo || 1)) * (H - 45);

  const yA = (getY(chartPrimaryData[idx]) / H) * 100;
  const yB = (getY(chartBaselineData[idx]) / H) * 100;

  dotA.style.left = `${pct * 100}%`;
  dotA.style.top = `${yA}%`;
  dotB.style.opacity = "1";
  dotB.style.left = `${pct * 100}%`;
  dotB.style.top = `${yB}%`;

  document.getElementById("chart-observed-stat").textContent = `${Math.round(chartPrimaryData[idx] * 1000).toLocaleString()} pkts/s`;
  document.getElementById("chart-baseline-stat").textContent = `${Math.round(chartBaselineData[idx] * 1000).toLocaleString()} pkts/s`;
}

function onChartPointerLeave() {
  document.getElementById("chart-cursor-line").style.opacity = "0";
  document.getElementById("chart-cursor-dot-b").style.opacity = "0";
}

// -------------------------------------------------------------
// THREAT ALLOCATION DONUT CHART (PURE SVG VECTOR ENGINE)
// -------------------------------------------------------------
function initThreatDonutChart() {
  updateThreatDonutChart();
}

function updateThreatDonutChart() {
  const sum = Object.values(threatDistribution).reduce((s, v) => s + v, 0) || 1;
  const totalElem = document.getElementById("donut-total-count");
  if (totalElem) totalElem.textContent = sum.toLocaleString();

  // SVG circle circumference for r = 70: 2 * PI * 70 = ~439.82
  const C = 439.82;
  const pDos = threatDistribution.DoS / sum;
  const pScan = threatDistribution.PortScan / sum;
  const pBf = threatDistribution.BruteForce / sum;
  const pBot = threatDistribution.Botnet / sum;
  const pZero = threatDistribution.ZeroDay_Anomaly / sum;

  const lenDos = Math.max(1, pDos * C);
  const lenScan = Math.max(1, pScan * C);
  const lenBf = Math.max(1, pBf * C);
  const lenBot = Math.max(1, pBot * C);
  const lenZero = Math.max(1, pZero * C);

  let offset = 0;

  const segDos = document.getElementById("donut-seg-dos");
  if (segDos) {
    segDos.setAttribute("stroke-dasharray", `${lenDos.toFixed(1)} ${C.toFixed(1)}`);
    segDos.setAttribute("stroke-dashoffset", `-${offset.toFixed(1)}`);
  }
  offset += lenDos;

  const segScan = document.getElementById("donut-seg-scan");
  if (segScan) {
    segScan.setAttribute("stroke-dasharray", `${lenScan.toFixed(1)} ${C.toFixed(1)}`);
    segScan.setAttribute("stroke-dashoffset", `-${offset.toFixed(1)}`);
  }
  offset += lenScan;

  const segBf = document.getElementById("donut-seg-bf");
  if (segBf) {
    segBf.setAttribute("stroke-dasharray", `${lenBf.toFixed(1)} ${C.toFixed(1)}`);
    segBf.setAttribute("stroke-dashoffset", `-${offset.toFixed(1)}`);
  }
  offset += lenBf;

  const segBot = document.getElementById("donut-seg-bot");
  if (segBot) {
    segBot.setAttribute("stroke-dasharray", `${lenBot.toFixed(1)} ${C.toFixed(1)}`);
    segBot.setAttribute("stroke-dashoffset", `-${offset.toFixed(1)}`);
  }
  offset += lenBot;

  const segZero = document.getElementById("donut-seg-zero");
  if (segZero) {
    segZero.setAttribute("stroke-dasharray", `${lenZero.toFixed(1)} ${C.toFixed(1)}`);
    segZero.setAttribute("stroke-dashoffset", `-${offset.toFixed(1)}`);
  }

  updateDonutBreakdownList(sum);
}

function updateDonutBreakdownList(sum) {
  const pDos = ((threatDistribution.DoS / sum) * 100).toFixed(1);
  const pScan = ((threatDistribution.PortScan / sum) * 100).toFixed(1);
  const pBf = ((threatDistribution.BruteForce / sum) * 100).toFixed(1);
  const pBot = ((threatDistribution.Botnet / sum) * 100).toFixed(1);
  const pZero = ((threatDistribution.ZeroDay_Anomaly / sum) * 100).toFixed(1);

  const eDos = document.getElementById("alloc-pct-dos");
  const eScan = document.getElementById("alloc-pct-scan");
  const eBf = document.getElementById("alloc-pct-bf");
  const eBot = document.getElementById("alloc-pct-bot");
  const eZero = document.getElementById("alloc-pct-zero");

  if (eDos) eDos.textContent = `${pDos}%`;
  if (eScan) eScan.textContent = `${pScan}%`;
  if (eBf) eBf.textContent = `${pBf}%`;
  if (eBot) eBot.textContent = `${pBot}%`;
  if (eZero) eZero.textContent = `${pZero}%`;
}

// -------------------------------------------------------------
// SOLID ACCENT TILE: EPOCH COUNTDOWN & QUARANTINE ACTION
// -------------------------------------------------------------
let epochTotalSeconds = 384;
let epochElapsed = 162;

function initEpochTimer() {
  setInterval(() => {
    epochElapsed = (epochElapsed + 1) % epochTotalSeconds;
    const left = epochTotalSeconds - epochElapsed;
    const m = Math.floor(left / 60);
    const s = String(left % 60).padStart(2, '0');

    document.getElementById("solid-countdown-timer").textContent = `${m}m ${s}s`;
    const pct = ((epochElapsed / epochTotalSeconds) * 100).toFixed(1);
    document.getElementById("solid-countdown-bar").style.width = `${pct}%`;
  }, 1000);
}

async function quarantineCurrentHost() {
  const ip = currentInspectedFlow ? currentInspectedFlow.source_ip : "198.51.100.22";
  const threatType = currentInspectedFlow ? currentInspectedFlow.threat_class : "DoS";

  const btn = document.getElementById("btn-block-current-host");
  btn.textContent = `Enforcing Rule on ${ip}...`;
  btn.disabled = true;

  try {
    const res = await fetch("/api/mitigation/block", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ip_address: ip, threat_type: threatType, reason: "Bento SOC Console Quarantine" })
    });

    const data = await res.json();
    btn.textContent = `Quarantined Host: ${ip}`;
    btn.style.opacity = "0.7";

    // Play electric firewall clamp sound
    playCyberSound('quarantine');

    // Refresh active quarantined rules count
    fetchSystemStats();

    setTimeout(() => {
      btn.textContent = "Enforce Firewall Quarantine";
      btn.disabled = false;
      btn.style.opacity = "1";
    }, 4000);
  } catch (err) {
    btn.textContent = "Quarantine Failed";
    btn.disabled = false;
  }
}

// -------------------------------------------------------------
// ADVERSARY ATTACK INJECTOR TRIGGER
// -------------------------------------------------------------
async function injectAttack(attackType) {
  try {
    // Play cyber injection sound
    playCyberSound('inject');

    const res = await fetch("/api/stream/inject", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ attack_type: attackType })
    });
    const result = await res.json();

    document.getElementById("nav-status-label").textContent = `PRIORITY ADVERSARY ATTACK INJECTED // ${attackType}`;
    setTimeout(() => {
      document.getElementById("nav-status-label").textContent = "PERIMETER ACTIVE • TWO-STAGE LIGHTGBM";
    }, 4000);

    // Fast-poll next flow
    setTimeout(pollNextStreamFlow, 300);
  } catch (err) {
    console.error("Injection error:", err);
  }
}

// -------------------------------------------------------------
// MALICIOUS FLOW & INCIDENTS FEED
// -------------------------------------------------------------
function handleMaliciousFlow(flow, kpkts) {
  currentInspectedFlow = flow;

  // Increment distribution
  const cName = flow.threat_class in threatDistribution ? flow.threat_class : "ZeroDay_Anomaly";
  threatDistribution[cName]++;
  updateThreatDonutChart();

  // Play specialized cyber alert sound based on threat classification
  if (cName === "ZeroDay_Anomaly") {
    playCyberSound('zero_day');
  } else if (cName === "DoS") {
    playCyberSound('critical');
  } else {
    playCyberSound('warning');
  }

  // Update front card metadata
  bringCardToFront(cName === "DoS" ? 1 : cName === "PortScan" ? 2 : 3);
  document.getElementById("card-active-ip").textContent = `${flow.source_ip} ➔ PORT ${flow.destination_port}`;
  document.getElementById("card-active-sub").textContent = `Captured Packet Frame · ${flow.threat_class}`;
  document.getElementById("card-active-score").textContent = `${flow.confidence.toFixed(1)}% conf`;

  // Prepend to Incident Feed
  const newIncident = {
    id: `ALT-${Math.floor(Math.random() * 9000 + 1000)}`,
    type: flow.threat_class,
    kind: cName === "DoS" ? "dos" : cName === "PortScan" ? "scan" : "zero",
    ip: flow.source_ip,
    detail: `Target: Port ${flow.destination_port} · ${flow.mitre?.technique_id || 'T1498'}`,
    rate: `${kpkts} kpkts/s`,
    status: "pending",
    time: "now",
    flow: flow
  };

  incidentFeed.unshift(newIncident);
  if (incidentFeed.length > 5) incidentFeed.pop();
  renderIncidentFeed();

  // Update XAI Explanation
  renderXAIExplanation(flow);
}

function renderIncidentFeed() {
  const container = document.getElementById("activity-incident-list");
  if (!container) return;
  container.innerHTML = "";

  incidentFeed.forEach(item => {
    const li = document.createElement("li");
    li.className = "activity-item";
    li.onclick = () => {
      if (item.flow) renderXAIExplanation(item.flow);
    };

    const iconClass = item.kind === "dos" ? "fa-solid fa-cloud-bolt activity-icon-dos" :
                      item.kind === "scan" ? "fa-solid fa-crosshairs activity-icon-scan" :
                      "fa-solid fa-shield-virus activity-icon-zero";

    li.innerHTML = `
      <span class="activity-icon-box ${item.kind === 'dos' ? 'activity-icon-dos' : item.kind === 'scan' ? 'activity-icon-scan' : 'activity-icon-zero'}">
        <i class="${iconClass}"></i>
      </span>
      <div class="activity-details">
        <p class="activity-title">${item.type} — ${item.ip}</p>
        <p class="activity-sub">${item.detail} · ${item.time}</p>
      </div>
      <div class="activity-amount-box">
        <p class="activity-amount-val">${item.rate}</p>
        <p class="activity-status-tag" style="color: ${item.status === 'pending' ? 'var(--accent)' : 'var(--accent2)'};">
          ${item.status === 'pending' ? '<svg width="10" height="10" viewBox="0 0 24 24" style="animation: spin 1s linear infinite;"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-opacity="0.3" stroke-width="3"/><path d="M21 12a9 9 0 0 0-9-9" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>' : ''}
          ${item.status}
        </p>
      </div>
    `;
    container.appendChild(li);
  });
}

// -------------------------------------------------------------
// REAL-TIME PACKET FLOW HISTORY & INCIDENT STREAM TABLE
// -------------------------------------------------------------
function recordFlowInHistory(flow) {
  const isAttack = flow.verdict === "MALICIOUS";
  flow.is_attack = isAttack;
  if (!flow.timestamp) {
    flow.timestamp = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
  }

  networkFlowHistory.unshift(flow);
  if (networkFlowHistory.length > 60) {
    networkFlowHistory.pop();
  }

  updateFilterCounters();
  renderTrafficHistoryTable();
}

function setTrafficFilter(filterType) {
  currentTrafficFilter = filterType;
  playCyberSound('click');

  // Update button active states
  document.querySelectorAll(".traffic-filter-btn").forEach(btn => {
    btn.classList.remove("active");
  });
  const activeBtn = document.getElementById(`btn-filter-${filterType}`);
  if (activeBtn) activeBtn.classList.add("active");

  renderTrafficHistoryTable();
}

function updateFilterCounters() {
  const total = networkFlowHistory.length;
  const attacks = networkFlowHistory.filter(f => f.is_attack).length;
  const normal = total - attacks;

  const countAll = document.getElementById("count-filter-all");
  const countAttacks = document.getElementById("count-filter-attacks");
  const countNormal = document.getElementById("count-filter-normal");
  const alertsCount = document.getElementById("alerts-count");

  if (countAll) countAll.innerText = total;
  if (countAttacks) countAttacks.innerText = attacks;
  if (countNormal) countNormal.innerText = normal;
  if (alertsCount) {
    alertsCount.innerText = `${total} Flows Inspected (${attacks} Attacks)`;
  }
}

function renderTrafficHistoryTable() {
  const tbody = document.getElementById("alerts-table-body");
  if (!tbody) return;

  const filtered = networkFlowHistory.filter(f => {
    if (currentTrafficFilter === "attacks") return f.is_attack;
    if (currentTrafficFilter === "normal") return !f.is_attack;
    return true; // "all"
  });

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr class="empty-row">
        <td colspan="7">No ${currentTrafficFilter === "attacks" ? "malicious attacks" : (currentTrafficFilter === "normal" ? "normal flows" : "network flows")} recorded in current session.</td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = "";
  filtered.slice(0, 30).forEach((flow, index) => {
    const tr = document.createElement("tr");

    if (index === 0) {
      tr.className = flow.is_attack ? "row-new-threat" : "row-new-safe";
    }

    // Row click: inspect flow in XAI
    tr.onclick = () => {
      renderXAIExplanation(flow);
      const xaiSection = document.getElementById("xai-audit-section");
      if (xaiSection) {
        xaiSection.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    };
    tr.title = "Click to inspect flow with Explainable AI (TreeSHAP)";

    const srcIp = flow.source_ip || "192.168.1.100";
    const dstIp = flow.destination_ip || "10.0.0.1";
    const dstPort = flow.destination_port || 80;
    const timeStr = flow.timestamp || new Date().toLocaleTimeString('en-US', { hour12: true });
    const confidence = flow.confidence ? `${flow.confidence}%` : "100%";

    if (flow.is_attack) {
      let sevClass = "sev-critical";
      let sevLabel = "CRITICAL";
      const tc = flow.threat_class || flow.attack_type || "Attack";

      if (flow.mitre && flow.mitre.severity) {
        sevLabel = flow.mitre.severity;
      } else if (flow.severity) {
        sevLabel = flow.severity;
      } else {
        if (tc.toLowerCase().includes("scan")) sevLabel = "MEDIUM";
        else if (tc.toLowerCase().includes("brute")) sevLabel = "HIGH";
        else sevLabel = "CRITICAL";
      }

      if (sevLabel === "MEDIUM") sevClass = "sev-medium";
      else if (sevLabel === "HIGH") sevClass = "sev-high";
      else sevClass = "sev-critical";

      tr.innerHTML = `
        <td style="color: var(--color-muted-foreground);">${timeStr}</td>
        <td><span style="color: var(--accent-red); font-weight: 700;">${srcIp}</span></td>
        <td style="color: var(--color-foreground);">${dstIp}:${dstPort}</td>
        <td><strong style="color: #f87171;">🔴 ${tc}</strong></td>
        <td><span class="badge-sev ${sevClass}">${sevLabel}</span></td>
        <td style="font-weight: 600;">${confidence}</td>
        <td><span class="action-flag">⚡ Auto-Flagged</span></td>
      `;
    } else {
      tr.innerHTML = `
        <td style="color: var(--color-muted-foreground);">${timeStr}</td>
        <td><span style="color: var(--accent-blue); font-weight: 600;">${srcIp}</span></td>
        <td style="color: var(--color-foreground);">${dstIp}:${dstPort}</td>
        <td><strong style="color: #34d399;">🟢 BENIGN (Normal)</strong></td>
        <td><span class="badge-sev sev-safe">SAFE</span></td>
        <td style="font-weight: 600;">${confidence}</td>
        <td><span class="action-pass">🛡️ Inspected & Cleared</span></td>
      `;
    }

    tbody.appendChild(tr);
  });
}

// -------------------------------------------------------------
// EXPLAINABLE AI (XAI) RENDERING (TreeSHAP ATTRIBUTION)
// -------------------------------------------------------------
function initDefaultDeepDive() {
  const defaultFlow = {
    verdict: "MALICIOUS",
    threat_class: "DoS",
    confidence: 98.4,
    anomaly_score: 94.2,
    source_ip: "198.51.100.22",
    destination_ip: "192.168.1.5",
    destination_port: 80,
    latency_ms: 0.014,
    flow_packets_s: 48500,
    mitre: {
      technique_id: "T1498",
      technique_name: "Network Denial of Service",
      tactic: "Impact",
      cvss: 7.5,
      severity: "HIGH"
    },
    xai_attributions: [
      {
        feature: "Flow_Packets_s",
        observed_value: "48,500 pkts/s",
        baseline_median: "120 pkts/s",
        importance_pct: 38.5,
        human_reason: "Extreme packet velocity (400x baseline) indicating automated volumetric SYN flood."
      },
      {
        feature: "SYN_Flag_Count",
        observed_value: "1",
        baseline_median: "0",
        importance_pct: 28.2,
        human_reason: "SYN flag active without ACK pairing signaling TCP half-open connection hammering."
      },
      {
        feature: "Flow_Duration",
        observed_value: "850 μs",
        baseline_median: "300,000 μs",
        importance_pct: 18.5,
        human_reason: "Microsecond-scale connection duration typical of automated DoS burst attack scripts."
      }
    ]
  };

  renderXAIExplanation(defaultFlow);
}

function renderXAIExplanation(flow) {
  currentInspectedFlow = flow;

  document.getElementById("xai-active-threat-badge").textContent = 
    `INSPECTING: ${flow.threat_class} (${flow.confidence.toFixed(1)}%)`;
  document.getElementById("xai-host-ip").textContent = flow.source_ip || "198.51.100.22";
  document.getElementById("xai-target-port").textContent = `Port ${flow.destination_port || 80}`;
  document.getElementById("xai-mitre-tag").textContent = flow.mitre?.technique_id ? `${flow.mitre.technique_id} (${flow.threat_class})` : "T1498 (DoS)";
  document.getElementById("xai-anomaly-score").textContent = `${flow.anomaly_score ? flow.anomaly_score.toFixed(1) : '94.2'}%`;
  document.getElementById("xai-latency-score").textContent = `${flow.latency_ms ? flow.latency_ms.toFixed(3) : '0.014'} ms`;

  const container = document.getElementById("main-xai-features-container");
  container.innerHTML = "";

  const attributions = flow.xai_attributions || [];
  attributions.forEach(item => {
    const card = document.createElement("div");
    card.className = "xai-feature-card";
    card.innerHTML = `
      <div class="xai-card-top">
        <span class="xai-feature-name">${item.feature}</span>
        <span class="xai-importance-pill">+${item.importance_pct}% SHAP</span>
      </div>
      <div class="xai-val-compare-row">
        <div>
          <div style="font-size: 10px; color: var(--color-muted-foreground);">OBSERVED</div>
          <div class="xai-observed">${item.observed_value}</div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 10px; color: var(--color-muted-foreground);">BASELINE</div>
          <div class="xai-baseline">${item.baseline_median}</div>
        </div>
      </div>
      <p class="xai-reason-text">${item.human_reason}</p>
    `;
    container.appendChild(card);
  });
}

// -------------------------------------------------------------
// FETCH SYSTEM STATS
// -------------------------------------------------------------
async function fetchSystemStats() {
  try {
    const res = await fetch("/api/stats");
    if (!res.ok) return;
    const stats = await res.json();

    if (stats.threat_distribution) {
      Object.assign(threatDistribution, stats.threat_distribution);
      updateThreatDonutChart();
    }
    if (stats.quarantined_ips_count !== undefined) {
      document.getElementById("solid-quarantined-hosts").textContent = `${stats.quarantined_ips_count} active`;
    }
    if (stats.total_inspected) {
      totalInspectedCounter = stats.total_inspected;
      document.getElementById("hero-inspected-counter").textContent = totalInspectedCounter.toLocaleString();
    }
  } catch (e) {}
}

async function toggleSnifferMode() {
  try {
    const res = await fetch("/api/sniffer/toggle", { method: "POST" });
    const data = await res.json();
    document.getElementById("sniffer-btn-text").textContent = 
      data.mode === "LIVE_SNIFFER" ? "Live Adapter: ON" : "Simulation Mode";
  } catch (e) {}
}
