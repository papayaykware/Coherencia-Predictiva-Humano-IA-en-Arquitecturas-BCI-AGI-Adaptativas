import { useState, useEffect, useRef, useCallback } from "react";

// ─── PALETTE & CONSTANTS ────────────────────────────────────────────────────
const C = {
  bg: "#070a0f",
  bgPanel: "#0c1118",
  bgCard: "#101820",
  border: "#1a2535",
  borderActive: "#00c8ff",
  cyan: "#00c8ff",
  amber: "#ffb830",
  green: "#00ff9d",
  red: "#ff4560",
  purple: "#a855f7",
  muted: "#3a4a5e",
  text: "#c8d8e8",
  textDim: "#5a7a9a",
};

// ─── NODE DEFINITIONS ────────────────────────────────────────────────────────
const NODES = [
  {
    id: "N1",
    label: "FILTRO ADAPTATIVO",
    sublabel: "ICA / Riemannian Source Sep.",
    color: C.cyan,
    icon: "⊗",
    desc: "Independent Component Analysis sobre señal EEG cruda. Arquitectura intercambiable: backend ICA (MNE-Python) sustituible por separación de fuentes geométrica Riemanniana (Pymanopt) sin alterar interfaces downstream.",
    inputs: ["EEG_RAW"],
    outputs: ["EEG_CLEAN"],
    params: [
      { k: "n_components", v: "64", unit: "ch" },
      { k: "method", v: "fastica | picard | riemannian", unit: "" },
      { k: "reject_threshold", v: "4.0", unit: "σ" },
      { k: "backend", v: "pluggable", unit: "" },
    ],
    status: "ready",
    badge: "INTERCAMBIABLE",
    badgeColor: C.green,
  },
  {
    id: "N2",
    label: "NÚCLEO ESPECTRAL",
    sublabel: "Wavelet Multiresolución",
    color: C.amber,
    icon: "∿",
    desc: "Análisis wavelet multiresolución (PyWavelets). Descomposición en bandas δ / θ / α / β / γ / USO. Salida: tensor P[banda × electrodo × ventana] normalizado por baseline.",
    inputs: ["EEG_CLEAN"],
    outputs: ["SPECTRAL_TENSOR"],
    params: [
      { k: "wavelet", v: "db4 | cmor | morlet", unit: "" },
      { k: "bands", v: "δ θ α β γ USO", unit: "" },
      { k: "window", v: "2.0", unit: "s" },
      { k: "overlap", v: "0.5", unit: "%" },
    ],
    status: "ready",
    badge: "TENSOR 3D",
    badgeColor: C.amber,
  },
  {
    id: "N3",
    label: "MOTOR DE SINCRONÍA",
    sublabel: "Coherencia + CPEA Index",
    color: C.green,
    icon: "⌬",
    desc: "Coherencia espectral Welch inter-hemisférica y cortico-cortical. Correlación cardioneural si canal ECG disponible. Alimenta directamente el índice CPEA y el operador IC_exc.",
    inputs: ["SPECTRAL_TENSOR", "ECG_OPT"],
    outputs: ["COH_MATRIX", "CPEA_IDX"],
    params: [
      { k: "method", v: "welch | multitaper", unit: "" },
      { k: "n_fft", v: "512", unit: "pts" },
      { k: "ecg_channel", v: "opcional", unit: "" },
      { k: "interhemi_pairs", v: "auto", unit: "" },
    ],
    status: "ready",
    badge: "→ CPEA",
    badgeColor: C.cyan,
  },
  {
    id: "N4",
    label: "NÚCLEO TICAM",
    sublabel: "Operador Φ_TICAM",
    color: C.purple,
    icon: "Φ",
    desc: "Acoplamiento magnetotalámico. Integra Φ_TICAM (METFI-F4/INTER-6). Con magnetometría ambiental: correlación corticotalámica ↔ campo geomagnético. Sin datos: modo degradado, señal interna únicamente.",
    inputs: ["COH_MATRIX", "MAG_OPT"],
    outputs: ["TICAM_STATE"],
    params: [
      { k: "Φ_TICAM", v: "METFI-F4/INTER-6", unit: "" },
      { k: "mag_source", v: "ext | degraded", unit: "" },
      { k: "thalamic_roi", v: "pulvinar | MD", unit: "" },
      { k: "coupling_lag", v: "0–120", unit: "ms" },
    ],
    status: "degraded",
    badge: "MODO DEGRADADO",
    badgeColor: C.purple,
  },
  {
    id: "N5",
    label: "EMBEDDING COGNITIVO",
    sublabel: "LSTM-AE → Poincaré",
    color: C.red,
    icon: "∞",
    desc: "Transformación de estados neurodinámicos a espacio latente. v1: autoencoder LSTM sobre EEG baseline. Implementaciones futuras: Poincaré embeddings (geometría hiperbólica), coherente con topología toroidal METFI.",
    inputs: ["TICAM_STATE", "SPECTRAL_TENSOR"],
    outputs: ["LATENT_Z", "CPEA_STREAM"],
    params: [
      { k: "arch_v1", v: "LSTM-AE", unit: "" },
      { k: "arch_v2", v: "Poincaré embed.", unit: "futuro" },
      { k: "latent_dim", v: "32", unit: "d" },
      { k: "geometry", v: "toroidal METFI", unit: "" },
    ],
    status: "ready",
    badge: "→ .cpea_stream",
    badgeColor: C.red,
  },
];

// ─── ANIMATED SIGNAL LINE ────────────────────────────────────────────────────
function SignalLine({ active, color }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 0, width: "100%", position: "relative", height: 24 }}>
      <div style={{
        position: "absolute", left: 0, right: 0, top: "50%",
        height: 1,
        background: active
          ? `linear-gradient(90deg, transparent, ${color}80, ${color}, ${color}80, transparent)`
          : `${C.border}`,
        transform: "translateY(-50%)",
        transition: "background 0.4s",
      }} />
      {active && (
        <div style={{
          position: "absolute", top: "50%", left: 0,
          transform: "translateY(-50%)",
          width: 8, height: 8,
          borderRadius: "50%",
          background: color,
          boxShadow: `0 0 8px ${color}`,
          animation: "pulse-dot 1.4s ease-in-out infinite",
        }} />
      )}
      <div style={{
        position: "absolute", right: -4, top: "50%", transform: "translateY(-50%)",
        color: active ? color : C.muted,
        fontSize: 12,
        transition: "color 0.3s",
      }}>▶</div>
    </div>
  );
}

// ─── DATA FLOW CONNECTOR ─────────────────────────────────────────────────────
function Connector({ from, to, active }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "2px 0", gap: 2 }}>
      <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 1 }}>
        {from}
      </div>
      <SignalLine active={active} color={NODES.find(n => n.outputs?.includes(from))?.color || C.cyan} />
      <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 1 }}>
        {to}
      </div>
    </div>
  );
}

// ─── NODE CARD ───────────────────────────────────────────────────────────────
function NodeCard({ node, active, onClick, running }) {
  const isActive = active === node.id;
  const isRunning = running === node.id;

  return (
    <div
      onClick={() => onClick(node.id)}
      style={{
        background: isActive ? `${node.color}0a` : C.bgCard,
        border: `1px solid ${isActive ? node.color : C.border}`,
        borderRadius: 8,
        padding: "16px 18px",
        cursor: "pointer",
        transition: "all 0.25s ease",
        position: "relative",
        boxShadow: isActive ? `0 0 20px ${node.color}25, inset 0 0 20px ${node.color}05` : "none",
        minWidth: 220,
        flex: 1,
      }}
    >
      {/* Header row */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{
            fontSize: 22,
            color: node.color,
            fontFamily: "monospace",
            lineHeight: 1,
            filter: isActive ? `drop-shadow(0 0 6px ${node.color})` : "none",
            transition: "filter 0.3s",
          }}>{node.icon}</span>
          <div>
            <div style={{ fontSize: 10, color: C.textDim, fontFamily: "monospace", letterSpacing: 2 }}>
              {node.id}
            </div>
            <div style={{ fontSize: 13, color: C.text, fontFamily: "monospace", fontWeight: 700, lineHeight: 1.2 }}>
              {node.label}
            </div>
          </div>
        </div>
        <span style={{
          fontSize: 8,
          fontFamily: "monospace",
          letterSpacing: 1,
          color: node.badgeColor,
          border: `1px solid ${node.badgeColor}60`,
          borderRadius: 3,
          padding: "2px 5px",
          background: `${node.badgeColor}12`,
        }}>{node.badge}</span>
      </div>

      {/* Sublabel */}
      <div style={{ fontSize: 10, color: node.color, fontFamily: "monospace", marginBottom: 10, opacity: 0.85 }}>
        {node.sublabel}
      </div>

      {/* Status indicator */}
      <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
        <div style={{
          width: 6, height: 6, borderRadius: "50%",
          background: node.status === "ready" ? C.green : C.purple,
          boxShadow: `0 0 6px ${node.status === "ready" ? C.green : C.purple}`,
          animation: isRunning ? "blink 0.5s step-end infinite" : "none",
        }} />
        <span style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 1 }}>
          {isRunning ? "EJECUTANDO..." : node.status.toUpperCase()}
        </span>
      </div>

      {/* Corner decoration */}
      <div style={{
        position: "absolute", top: 6, left: 6,
        width: 8, height: 8,
        borderTop: `1px solid ${node.color}60`,
        borderLeft: `1px solid ${node.color}60`,
      }} />
      <div style={{
        position: "absolute", bottom: 6, right: 6,
        width: 8, height: 8,
        borderBottom: `1px solid ${node.color}60`,
        borderRight: `1px solid ${node.color}60`,
      }} />
    </div>
  );
}

// ─── DETAIL PANEL ────────────────────────────────────────────────────────────
function DetailPanel({ node }) {
  if (!node) return (
    <div style={{
      flex: 1, border: `1px solid ${C.border}`, borderRadius: 8,
      background: C.bgCard, padding: 24,
      display: "flex", alignItems: "center", justifyContent: "center",
    }}>
      <div style={{ textAlign: "center", color: C.muted, fontFamily: "monospace" }}>
        <div style={{ fontSize: 28, marginBottom: 12 }}>◈</div>
        <div style={{ fontSize: 11, letterSpacing: 2 }}>SELECCIONA UN NODO</div>
        <div style={{ fontSize: 10, marginTop: 4, opacity: 0.6 }}>para inspeccionar parámetros</div>
      </div>
    </div>
  );

  return (
    <div style={{
      flex: 1, border: `1px solid ${node.color}40`,
      borderRadius: 8, background: C.bgCard, padding: 20,
      boxShadow: `0 0 30px ${node.color}10`,
      display: "flex", flexDirection: "column", gap: 16,
    }}>
      {/* Title */}
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
          <span style={{ fontSize: 28, color: node.color, filter: `drop-shadow(0 0 8px ${node.color})` }}>
            {node.icon}
          </span>
          <div>
            <div style={{ fontSize: 9, color: C.textDim, fontFamily: "monospace", letterSpacing: 2 }}>{node.id} · CORPUS PAPAYAYKWARE</div>
            <div style={{ fontSize: 16, color: node.color, fontFamily: "monospace", fontWeight: 700 }}>{node.label}</div>
          </div>
        </div>
        <div style={{ fontSize: 11, color: C.text, lineHeight: 1.7, borderLeft: `2px solid ${node.color}40`, paddingLeft: 12 }}>
          {node.desc}
        </div>
      </div>

      {/* IO */}
      <div style={{ display: "flex", gap: 12 }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 2, marginBottom: 6 }}>INPUTS</div>
          {node.inputs.map(i => (
            <div key={i} style={{
              fontSize: 10, fontFamily: "monospace", color: C.text,
              background: `${C.border}40`, borderRadius: 4, padding: "3px 7px",
              marginBottom: 3, border: `1px solid ${C.border}`,
            }}>← {i}</div>
          ))}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 2, marginBottom: 6 }}>OUTPUTS</div>
          {node.outputs.map(o => (
            <div key={o} style={{
              fontSize: 10, fontFamily: "monospace", color: node.color,
              background: `${node.color}10`, borderRadius: 4, padding: "3px 7px",
              marginBottom: 3, border: `1px solid ${node.color}40`,
            }}>→ {o}</div>
          ))}
        </div>
      </div>

      {/* Params table */}
      <div>
        <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 2, marginBottom: 8 }}>PARÁMETROS</div>
        <div style={{ border: `1px solid ${C.border}`, borderRadius: 6, overflow: "hidden" }}>
          {node.params.map((p, i) => (
            <div key={p.k} style={{
              display: "flex", justifyContent: "space-between", alignItems: "center",
              padding: "7px 12px",
              background: i % 2 === 0 ? "transparent" : `${C.border}20`,
              borderBottom: i < node.params.length - 1 ? `1px solid ${C.border}` : "none",
            }}>
              <span style={{ fontSize: 10, fontFamily: "monospace", color: C.textDim }}>{p.k}</span>
              <span style={{ fontSize: 10, fontFamily: "monospace", color: node.color }}>
                {p.v} <span style={{ color: C.muted }}>{p.unit}</span>
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── LIVE MONITOR ────────────────────────────────────────────────────────────
function LiveMonitor({ running, log }) {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight;
  }, [log]);

  return (
    <div style={{
      border: `1px solid ${C.border}`, borderRadius: 8,
      background: "#050810", padding: 16,
      fontFamily: "monospace", fontSize: 10,
      height: 120, overflow: "hidden",
      position: "relative",
    }}>
      <div style={{ fontSize: 9, color: C.textDim, letterSpacing: 2, marginBottom: 8 }}>
        NEXUS-EEG · PIPELINE LOG
        {running && <span style={{ color: C.green, marginLeft: 10, animation: "blink 1s step-end infinite" }}>● LIVE</span>}
      </div>
      <div ref={ref} style={{ height: 80, overflow: "auto" }}>
        {log.map((l, i) => (
          <div key={i} style={{ color: l.color || C.textDim, lineHeight: 1.8 }}>
            <span style={{ color: C.muted }}>{">"} </span>{l.text}
          </div>
        ))}
        {!log.length && (
          <div style={{ color: C.muted }}>Esperando ejecución del pipeline...</div>
        )}
      </div>
    </div>
  );
}

// ─── BAND TENSOR VIZ ─────────────────────────────────────────────────────────
const BANDS = ["δ", "θ", "α", "β", "γ", "USO"];
const BAND_COLORS = [C.purple, C.cyan, C.green, C.amber, C.red, "#ff6ef7"];

function BandTensor({ active }) {
  const [vals, setVals] = useState(BANDS.map(() => Math.random()));

  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => {
      setVals(BANDS.map(() => 0.1 + Math.random() * 0.9));
    }, 800);
    return () => clearInterval(id);
  }, [active]);

  return (
    <div style={{
      border: `1px solid ${C.border}`, borderRadius: 8,
      background: C.bgCard, padding: 16,
    }}>
      <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 2, marginBottom: 12 }}>
        TENSOR ESPECTRAL · P[banda × electrodo × ventana]
      </div>
      <div style={{ display: "flex", gap: 8, alignItems: "flex-end", height: 60 }}>
        {BANDS.map((b, i) => (
          <div key={b} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
            <div style={{
              width: "100%", background: BAND_COLORS[i],
              height: `${vals[i] * 52}px`,
              borderRadius: "3px 3px 0 0",
              transition: "height 0.7s ease",
              boxShadow: active ? `0 0 8px ${BAND_COLORS[i]}60` : "none",
              minHeight: 3,
            }} />
            <span style={{ fontSize: 9, fontFamily: "monospace", color: BAND_COLORS[i] }}>{b}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── COHERENCE MATRIX ────────────────────────────────────────────────────────
const REGIONS = ["F3", "F4", "C3", "C4", "P3", "P4"];
function CoherenceMatrix({ active }) {
  const [mat, setMat] = useState(() =>
    REGIONS.map(() => REGIONS.map(() => Math.random()))
  );
  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => {
      setMat(REGIONS.map(() => REGIONS.map(() => Math.random())));
    }, 1200);
    return () => clearInterval(id);
  }, [active]);

  return (
    <div style={{
      border: `1px solid ${C.border}`, borderRadius: 8,
      background: C.bgCard, padding: 16,
    }}>
      <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 2, marginBottom: 10 }}>
        MATRIZ COHERENCIA INTER-HEMISFÉRICA
      </div>
      <div style={{ display: "grid", gridTemplateColumns: `20px repeat(${REGIONS.length}, 1fr)`, gap: 2, fontSize: 8, fontFamily: "monospace" }}>
        <div />
        {REGIONS.map(r => <div key={r} style={{ color: C.textDim, textAlign: "center" }}>{r}</div>)}
        {REGIONS.map((r, i) => (
          <>
            <div key={r + "label"} style={{ color: C.textDim, display: "flex", alignItems: "center" }}>{r}</div>
            {mat[i].map((v, j) => (
              <div key={j} style={{
                height: 18, borderRadius: 2,
                background: i === j
                  ? `${C.muted}40`
                  : `rgba(${i < 3 && j >= 3 || i >= 3 && j < 3 ? "0,200,255" : "255,184,48"},${v * 0.85})`,
                transition: "background 0.8s ease",
              }} />
            ))}
          </>
        ))}
      </div>
      <div style={{ display: "flex", gap: 12, marginTop: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
          <div style={{ width: 10, height: 10, background: C.cyan, borderRadius: 2 }} />
          <span style={{ fontSize: 8, fontFamily: "monospace", color: C.textDim }}>inter-hemisférica</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
          <div style={{ width: 10, height: 10, background: C.amber, borderRadius: 2 }} />
          <span style={{ fontSize: 8, fontFamily: "monospace", color: C.textDim }}>intra-hemisférica</span>
        </div>
      </div>
    </div>
  );
}

// ─── CPEA INDEX GAUGE ────────────────────────────────────────────────────────
function CPEAGauge({ active }) {
  const [val, setVal] = useState(0.42);
  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => {
      setVal(v => Math.max(0, Math.min(1, v + (Math.random() - 0.48) * 0.08)));
    }, 900);
    return () => clearInterval(id);
  }, [active]);

  const color = val > 0.7 ? C.green : val > 0.4 ? C.amber : C.red;
  const angle = val * 180 - 90;

  return (
    <div style={{
      border: `1px solid ${C.border}`, borderRadius: 8,
      background: C.bgCard, padding: 16,
      display: "flex", flexDirection: "column", alignItems: "center",
    }}>
      <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim, letterSpacing: 2, marginBottom: 10 }}>
        ÍNDICE CPEA · IC_exc
      </div>
      <svg width={120} height={65} viewBox="0 0 120 65">
        <path d="M10 60 A50 50 0 0 1 110 60" fill="none" stroke={C.border} strokeWidth={6} strokeLinecap="round" />
        <path
          d={`M10 60 A50 50 0 0 1 ${60 + 50 * Math.cos((angle - 90) * Math.PI / 180)} ${60 + 50 * Math.sin((angle - 90) * Math.PI / 180)}`}
          fill="none" stroke={color} strokeWidth={6} strokeLinecap="round"
          style={{ transition: "d 0.8s ease, stroke 0.8s ease" }}
        />
        <line
          x1={60} y1={60}
          x2={60 + 38 * Math.cos(angle * Math.PI / 180)}
          y2={60 + 38 * Math.sin(angle * Math.PI / 180)}
          stroke={color} strokeWidth={2} strokeLinecap="round"
          style={{ transition: "all 0.8s ease" }}
        />
        <circle cx={60} cy={60} r={4} fill={color} />
      </svg>
      <div style={{
        fontSize: 24, fontFamily: "monospace", fontWeight: 900,
        color, transition: "color 0.8s ease",
        filter: active ? `drop-shadow(0 0 8px ${color})` : "none",
      }}>
        {val.toFixed(3)}
      </div>
      <div style={{ fontSize: 9, fontFamily: "monospace", color: C.textDim }}>
        {val > 0.7 ? "COHERENCIA ALTA" : val > 0.4 ? "COHERENCIA MEDIA" : "COHERENCIA BAJA"}
      </div>
    </div>
  );
}

// ─── PIPELINE RUNNER ─────────────────────────────────────────────────────────
const PIPELINE_STEPS = [
  { node: "N1", msg: "Cargando señal EEG cruda... aplicando ICA (fastica, 64 comp.)", color: C.cyan },
  { node: "N1", msg: "Artefactos oculares y musculares eliminados. EEG_CLEAN emitido.", color: C.green },
  { node: "N2", msg: "Descomposición wavelet (db4) en 6 bandas × 64 electrodos × ventana 2s", color: C.amber },
  { node: "N2", msg: "SPECTRAL_TENSOR [6 × 64 × T] generado y normalizado.", color: C.green },
  { node: "N3", msg: "Coherencia Welch cross-spectral... calculando pares inter-hemisféricos.", color: C.green },
  { node: "N3", msg: "COH_MATRIX emitida. CPEA_IDX = 0.618. IC_exc threshold: 2.3σ", color: C.green },
  { node: "N4", msg: "Φ_TICAM: modo degradado (sin magnetometría externa).", color: C.purple },
  { node: "N4", msg: "Acoplamiento corticotalámico interno calculado. TICAM_STATE emitido.", color: C.purple },
  { node: "N5", msg: "LSTM-AE: encoding en espacio latente (dim=32)...", color: C.red },
  { node: "N5", msg: "Embedding convergido. LATENT_Z + CPEA_STREAM → .cpea_stream publicado.", color: C.green },
  { node: null, msg: "Pipeline DAG completo. Listo para siguiente ventana temporal.", color: C.cyan },
];

// ─── MAIN APP ────────────────────────────────────────────────────────────────
export default function NexusDag() {
  const [activeNode, setActiveNode] = useState(null);
  const [runningNode, setRunningNode] = useState(null);
  const [log, setLog] = useState([]);
  const [pipelineActive, setPipelineActive] = useState(false);
  const [vizActive, setVizActive] = useState(false);
  const stepRef = useRef(0);
  const timerRef = useRef(null);

  const runPipeline = useCallback(() => {
    if (pipelineActive) return;
    setPipelineActive(true);
    setVizActive(true);
    setLog([]);
    stepRef.current = 0;

    const step = () => {
      if (stepRef.current >= PIPELINE_STEPS.length) {
        setPipelineActive(false);
        setRunningNode(null);
        return;
      }
      const s = PIPELINE_STEPS[stepRef.current];
      setRunningNode(s.node);
      if (s.node) setActiveNode(s.node);
      setLog(l => [...l, { text: `[${s.node || "DAG"}] ${s.msg}`, color: s.color }]);
      stepRef.current++;
      timerRef.current = setTimeout(step, 600 + Math.random() * 400);
    };
    step();
  }, [pipelineActive]);

  useEffect(() => () => clearTimeout(timerRef.current), []);

  const selectedNode = NODES.find(n => n.id === activeNode);

  // Connection pairs: [output_key, input_display, between_node_ids]
  const CONNECTIONS = [
    { label: "EEG_CLEAN", from: "N1", to: "N2" },
    { label: "SPECTRAL_TENSOR", from: "N2", to: "N3" },
    { label: "COH_MATRIX", from: "N3", to: "N4" },
    { label: "TICAM_STATE", from: "N4", to: "N5" },
  ];

  const isConnActive = (conn) => {
    const idx = PIPELINE_STEPS.findIndex(s => s.node === conn.to);
    const curIdx = PIPELINE_STEPS.findIndex(s => s.node === runningNode);
    return pipelineActive && curIdx >= idx - 2;
  };

  return (
    <div style={{
      minHeight: "100vh", background: C.bg, color: C.text,
      fontFamily: "monospace", padding: 24,
      backgroundImage: `radial-gradient(ellipse at 20% 20%, #001a2e20 0%, transparent 60%), radial-gradient(ellipse at 80% 80%, #0a001a18 0%, transparent 60%)`,
    }}>
      <style>{`
        @keyframes pulse-dot { 0%,100%{opacity:1;transform:translateY(-50%) scale(1)} 50%{opacity:0.4;transform:translateY(-50%) scale(0.6)} }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 4px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: #1a2535; border-radius: 2px; }
      `}</style>

      {/* Header */}
      <div style={{ marginBottom: 28, borderBottom: `1px solid ${C.border}`, paddingBottom: 18 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <div style={{ fontSize: 9, color: C.textDim, letterSpacing: 3, marginBottom: 4 }}>
              CORPUS PAPAYAYKWARE · CPEA MODULE
            </div>
            <div style={{ fontSize: 22, fontWeight: 900, color: C.cyan, letterSpacing: 1 }}>
              NEXUS-EEG v2.0
            </div>
            <div style={{ fontSize: 11, color: C.textDim, marginTop: 2 }}>
              DAG Pipeline · 5 nodos · ICA → Wavelet → Coherencia → Φ_TICAM → Embedding
            </div>
          </div>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <div style={{
              fontSize: 9, fontFamily: "monospace", color: C.green,
              border: `1px solid ${C.green}40`, borderRadius: 4, padding: "4px 10px",
              background: `${C.green}10`,
            }}>● OPERACIONAL</div>
            <button
              onClick={runPipeline}
              disabled={pipelineActive}
              style={{
                background: pipelineActive ? C.bgCard : `${C.cyan}15`,
                border: `1px solid ${pipelineActive ? C.muted : C.cyan}`,
                color: pipelineActive ? C.muted : C.cyan,
                borderRadius: 6, padding: "8px 18px",
                fontFamily: "monospace", fontSize: 11, cursor: pipelineActive ? "default" : "pointer",
                letterSpacing: 1, transition: "all 0.2s",
              }}
            >
              {pipelineActive ? "▶ EJECUTANDO..." : "▶ EJECUTAR PIPELINE"}
            </button>
          </div>
        </div>
      </div>

      {/* DAG Pipeline — horizontal */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ fontSize: 9, color: C.textDim, letterSpacing: 2, marginBottom: 12 }}>DAG · FLUJO DE DATOS</div>
        <div style={{ display: "flex", alignItems: "stretch", gap: 0 }}>
          {NODES.map((node, i) => (
            <>
              <NodeCard
                key={node.id}
                node={node}
                active={activeNode}
                onClick={setActiveNode}
                running={runningNode}
              />
              {i < NODES.length - 1 && (
                <div key={`conn-${i}`} style={{ display: "flex", alignItems: "center", padding: "0 8px", minWidth: 80 }}>
                  <div style={{ width: "100%" }}>
                    <Connector
                      from={CONNECTIONS[i].label}
                      to=""
                      active={isConnActive(CONNECTIONS[i])}
                    />
                  </div>
                </div>
              )}
            </>
          ))}
        </div>
      </div>

      {/* Detail + Live section */}
      <div style={{ display: "flex", gap: 16, marginBottom: 16 }}>
        <DetailPanel node={selectedNode} />
        <div style={{ display: "flex", flexDirection: "column", gap: 16, minWidth: 280 }}>
          <CPEAGauge active={vizActive} />
        </div>
      </div>

      {/* Visualizations row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <BandTensor active={vizActive} />
        <CoherenceMatrix active={vizActive} />
      </div>

      {/* Log */}
      <LiveMonitor running={pipelineActive} log={log} />

      {/* Footer */}
      <div style={{
        marginTop: 20, borderTop: `1px solid ${C.border}`, paddingTop: 12,
        display: "flex", justifyContent: "space-between", alignItems: "center",
      }}>
        <div style={{ fontSize: 8, color: C.muted, letterSpacing: 1 }}>
          Autor conceptual: Claude (Anthropic) · Director: Javi Ciborro (@papayaykware)
        </div>
        <div style={{ display: "flex", gap: 16, fontSize: 8, color: C.muted }}>
          <span>github.com/papayaykware</span>
          <span>·</span>
          <span>papayaykware.blogspot.com</span>
        </div>
      </div>
    </div>
  );
}
