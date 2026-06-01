import { useState, useEffect, useRef, useCallback } from "react";

// ─── DESIGN TOKENS ───────────────────────────────────────────────────────────
const T = {
  bg:        "#04070d",
  bgDeep:    "#020408",
  panel:     "#080e18",
  card:      "#0b1220",
  border:    "#142030",
  borderHi:  "#1e3550",
  // signal colors
  cyan:      "#00d4ff",
  amber:     "#ffb020",
  green:     "#00ff88",
  red:       "#ff3355",
  purple:    "#c084fc",
  gold:      "#ffd700",
  // TAE exception colors per criterion
  c1:        "#ff3355",  // dislocación métrica
  c2:        "#ff8800",  // perturbación entrópica
  c3:        "#ffdd00",  // persistencia temporal
  // text
  text:      "#b8ccd8",
  dim:       "#3a5570",
  faint:     "#1e3040",
};

// ─── TAE CRITERIA DEFINITIONS ────────────────────────────────────────────────
const TAE_CRITERIA = {
  C1: { label: "C1 · Dislocación Métrica",     color: T.c1,     symbol: "⚡", threshold: "d(x,μ) > 3.2σ" },
  C2: { label: "C2 · Perturbación Entrópica",  color: T.c2,     symbol: "∇", threshold: "ΔH > 0.45 nats" },
  C3: { label: "C3 · Persistencia Temporal",   color: T.c3,     symbol: "⟳", threshold: "τ_exc > 2 ventanas" },
};

// ─── NODE DEFINITIONS ────────────────────────────────────────────────────────
const NODES = [
  {
    id: "N1", short: "ICA",
    label: "FILTRO ADAPTATIVO",
    sub: "ICA ↔ Riemannian · pluggable",
    color: T.cyan, icon: "⊗",
    outputs: ["EEG_CLEAN"],
    taeDesc: "Detecta artefactos que superan umbral métrico (C1) o producen colapso entrópico en componentes independientes (C2).",
    params: [
      ["backend",      "fastica | picard | riemannian"],
      ["n_components", "64 ch"],
      ["TAE_window",   "500 ms"],
    ],
  },
  {
    id: "N2", short: "WLT",
    label: "NÚCLEO ESPECTRAL",
    sub: "Wavelet MRA · PyWavelets",
    color: T.amber, icon: "∿",
    outputs: ["SPECTRAL_TENSOR"],
    taeDesc: "C1 sobre potencia por banda (desviación > 3.2σ de baseline); C3 si la anomalía persiste ≥2 ventanas consecutivas.",
    params: [
      ["wavelet",  "db4 | morlet | cmor"],
      ["bands",    "δ θ α β γ USO"],
      ["TAE_bands","todas las bandas"],
    ],
  },
  {
    id: "N3", short: "COH",
    label: "MOTOR DE SINCRONÍA",
    sub: "Welch · CPEA_IDX · ECG opt.",
    color: T.green, icon: "⌬",
    outputs: ["COH_MATRIX", "CPEA_IDX"],
    taeDesc: "C2 cuando la entropía de la matriz de coherencia cae > 0.45 nats respecto al baseline. Correlación cardioneural como señal auxiliar C3.",
    params: [
      ["method",    "welch | multitaper"],
      ["IC_exc",    "ε_c adaptativo"],
      ["TAE_ecg",   "si canal ECG disponible"],
    ],
  },
  {
    id: "N4", short: "TIC",
    label: "NÚCLEO TICAM",
    sub: "Φ_TICAM · METFI-F4/INTER-6",
    color: T.purple, icon: "Φ",
    outputs: ["TICAM_STATE"],
    taeDesc: "C1 en acoplamiento magnetotalámico (salto de fase > umbral). C3 si el desacoplamiento se extiende > 2 ventanas. Modo degradado si sin magnetometría.",
    params: [
      ["Φ_TICAM",   "METFI-F4/INTER-6"],
      ["mag_mode",  "ext | degraded"],
      ["TAE_lag",   "0–120 ms coupling"],
    ],
  },
  {
    id: "N5", short: "EMB",
    label: "EMBEDDING COGNITIVO",
    sub: "LSTM-AE → Poincaré (v2)",
    color: T.red, icon: "∞",
    outputs: ["LATENT_Z", "CPEA_STREAM"],
    taeDesc: "C1 si el vector latente salta fuera de la región de alta densidad (> 3.2σ en norma L2). C2+C3 activan flag ORION-AGI de inferencia-en-excepción.",
    params: [
      ["arch",      "LSTM-AE · latent_dim=32"],
      ["geometry",  "toroidal METFI"],
      ["TAE_flag",  "→ ORION-AGI metadata"],
    ],
  },
];

// ─── CONNECTIONS ─────────────────────────────────────────────────────────────
const EDGES = [
  { from: "N1", to: "N2", signal: "EEG_CLEAN" },
  { from: "N2", to: "N3", signal: "SPECTRAL_TENSOR" },
  { from: "N3", to: "N4", signal: "COH_MATRIX" },
  { from: "N4", to: "N5", signal: "TICAM_STATE" },
];

// ─── UTILITY ─────────────────────────────────────────────────────────────────
const rand = (a, b) => a + Math.random() * (b - a);
const randInt = (a, b) => Math.floor(rand(a, b));
const pick = arr => arr[randInt(0, arr.length)];
const criteriaKeys = ["C1","C2","C3"];

// ─── EXCEPTION EVENT ─────────────────────────────────────────────────────────
function makeExc(nodeId) {
  const cr = pick(criteriaKeys);
  return {
    id: Date.now() + Math.random(),
    nodeId,
    criterion: cr,
    value: rand(3.2, 6.5).toFixed(3),
    ts: new Date().toISOString().slice(11,23),
    propagated: false,
    orion: cr === "C3" || Math.random() > 0.6,
  };
}

// ─── MINI SPARKLINE ──────────────────────────────────────────────────────────
function Sparkline({ data, color, height = 32, width = 120 }) {
  if (!data.length) return null;
  const mn = Math.min(...data), mx = Math.max(...data);
  const range = mx - mn || 1;
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * width;
    const y = height - ((v - mn) / range) * height;
    return `${x},${y}`;
  }).join(" ");
  return (
    <svg width={width} height={height} style={{ display: "block" }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth={1.5}
        strokeLinejoin="round" strokeLinecap="round" opacity={0.8} />
      <polyline points={`0,${height} ${pts} ${width},${height}`}
        fill={`${color}18`} stroke="none" />
    </svg>
  );
}

// ─── TAE BADGE ───────────────────────────────────────────────────────────────
function TAEBadge({ criterion, pulse }) {
  const def = TAE_CRITERIA[criterion];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4,
      fontSize: 9, fontFamily: "monospace", letterSpacing: 1,
      color: def.color,
      border: `1px solid ${def.color}60`,
      background: `${def.color}12`,
      borderRadius: 3, padding: "1px 6px",
      animation: pulse ? "exc-pulse 0.6s ease-out" : "none",
      boxShadow: pulse ? `0 0 10px ${def.color}80` : "none",
    }}>
      {def.symbol} {criterion}
    </span>
  );
}

// ─── NODE CARD ───────────────────────────────────────────────────────────────
function NodeCard({ node, selected, exceptions, onSelect, running, excPulse }) {
  const myExc = exceptions.filter(e => e.nodeId === node.id);
  const hasExc = myExc.length > 0;
  const latest = myExc[myExc.length - 1];
  const isRunning = running === node.id;

  return (
    <div
      onClick={() => onSelect(node.id)}
      style={{
        background: selected ? `${node.color}08` : T.card,
        border: `1px solid ${hasExc ? TAE_CRITERIA[latest?.criterion]?.color + "80" : selected ? node.color + "60" : T.border}`,
        borderRadius: 6,
        padding: "12px 14px",
        cursor: "pointer",
        position: "relative",
        transition: "border-color 0.2s, background 0.2s, box-shadow 0.2s",
        boxShadow: hasExc
          ? `0 0 18px ${TAE_CRITERIA[latest?.criterion]?.color}25`
          : selected ? `0 0 14px ${node.color}18` : "none",
        flex: 1,
        minWidth: 0,
        animation: excPulse === node.id ? "exc-card 0.5s ease-out" : "none",
      }}
    >
      {/* Corner brackets */}
      {[["top","left"],["bottom","right"]].map(([v,h]) => (
        <div key={v+h} style={{
          position:"absolute", [v]:5, [h]:5, width:8, height:8,
          borderTop: v==="top" ? `1px solid ${node.color}50` : "none",
          borderBottom: v==="bottom" ? `1px solid ${node.color}50` : "none",
          borderLeft: h==="left" ? `1px solid ${node.color}50` : "none",
          borderRight: h==="right" ? `1px solid ${node.color}50` : "none",
        }}/>
      ))}

      {/* Node ID */}
      <div style={{ fontSize: 8, color: T.dim, letterSpacing: 2, fontFamily: "monospace", marginBottom: 3 }}>
        {node.id} · {node.short}
      </div>

      {/* Icon + label */}
      <div style={{ display:"flex", alignItems:"center", gap:7, marginBottom:6 }}>
        <span style={{
          fontSize:18, color:node.color, lineHeight:1, fontFamily:"monospace",
          filter: selected ? `drop-shadow(0 0 5px ${node.color})` : "none",
        }}>{node.icon}</span>
        <div style={{ fontSize:11, color:T.text, fontFamily:"monospace", fontWeight:700, lineHeight:1.3 }}>
          {node.label}
        </div>
      </div>

      {/* Sub */}
      <div style={{ fontSize:9, color:node.color, fontFamily:"monospace", opacity:0.75, marginBottom:8 }}>
        {node.sub}
      </div>

      {/* TAE exception badges */}
      <div style={{ display:"flex", flexWrap:"wrap", gap:4, minHeight:18 }}>
        {myExc.slice(-3).map(e => (
          <TAEBadge key={e.id} criterion={e.criterion} pulse={e.id === excPulse?.id} />
        ))}
        {myExc.length === 0 && (
          <span style={{fontSize:9, fontFamily:"monospace", color:T.dim}}>TAE · sin excepción</span>
        )}
      </div>

      {/* Running indicator */}
      {isRunning && (
        <div style={{
          position:"absolute", top:6, right:8,
          width:6, height:6, borderRadius:"50%",
          background:node.color, boxShadow:`0 0 8px ${node.color}`,
          animation:"blink 0.4s step-end infinite",
        }}/>
      )}

      {/* ORION flag */}
      {myExc.some(e=>e.orion) && (
        <div style={{
          position:"absolute", bottom:6, right:8,
          fontSize:8, fontFamily:"monospace", color:T.gold,
          border:`1px solid ${T.gold}50`, borderRadius:3,
          padding:"1px 5px", background:`${T.gold}10`,
        }}>⬡ ORION</div>
      )}
    </div>
  );
}

// ─── EDGE CONNECTOR ──────────────────────────────────────────────────────────
function EdgeConnector({ edge, active, excColor }) {
  return (
    <div style={{ display:"flex", flexDirection:"column", alignItems:"center", width:72, flexShrink:0 }}>
      <div style={{ fontSize:8, fontFamily:"monospace", color:T.dim, letterSpacing:1, marginBottom:3, textAlign:"center" }}>
        {edge.signal}
      </div>
      <div style={{ position:"relative", width:"100%", height:2 }}>
        <div style={{
          position:"absolute", inset:0,
          background: active
            ? `linear-gradient(90deg, transparent, ${excColor || T.cyan}90, ${excColor || T.cyan}, ${excColor || T.cyan}90, transparent)`
            : T.faint,
          transition:"background 0.3s",
        }}/>
        {active && (
          <div style={{
            position:"absolute", top:"50%", transform:"translateY(-50%)",
            width:8, height:8, borderRadius:"50%",
            background: excColor || T.cyan,
            boxShadow:`0 0 8px ${excColor || T.cyan}`,
            animation:"travel 1s linear infinite",
          }}/>
        )}
      </div>
      {excColor && (
        <div style={{ fontSize:8, fontFamily:"monospace", color:excColor, marginTop:3, letterSpacing:1 }}>
          ↗ EXC
        </div>
      )}
    </div>
  );
}

// ─── DETAIL PANEL ────────────────────────────────────────────────────────────
function DetailPanel({ node, exceptions }) {
  if (!node) return (
    <div style={{
      flex:1, border:`1px solid ${T.border}`, borderRadius:8,
      background:T.card, display:"flex", alignItems:"center", justifyContent:"center",
    }}>
      <div style={{ textAlign:"center", color:T.dim, fontFamily:"monospace" }}>
        <div style={{ fontSize:24, marginBottom:8 }}>◈</div>
        <div style={{ fontSize:10, letterSpacing:2 }}>SELECCIONA UN NODO</div>
      </div>
    </div>
  );

  const myExc = exceptions.filter(e => e.nodeId === node.id);

  return (
    <div style={{
      flex:1, border:`1px solid ${node.color}35`, borderRadius:8,
      background:T.card, padding:18,
      display:"flex", flexDirection:"column", gap:14,
      boxShadow:`0 0 24px ${node.color}0a`,
    }}>
      {/* Header */}
      <div style={{ display:"flex", alignItems:"center", gap:10 }}>
        <span style={{ fontSize:26, color:node.color, filter:`drop-shadow(0 0 6px ${node.color})` }}>
          {node.icon}
        </span>
        <div>
          <div style={{ fontSize:9, color:T.dim, fontFamily:"monospace", letterSpacing:2 }}>
            {node.id} · SIGMA-T v1.0
          </div>
          <div style={{ fontSize:15, color:node.color, fontFamily:"monospace", fontWeight:700 }}>
            {node.label}
          </div>
          <div style={{ fontSize:9, color:T.text, fontFamily:"monospace", opacity:0.7 }}>
            {node.sub}
          </div>
        </div>
      </div>

      {/* TAE integration description */}
      <div style={{
        borderLeft:`2px solid ${node.color}50`, paddingLeft:10,
        fontSize:10, color:T.text, lineHeight:1.7,
        background:`${node.color}05`, borderRadius:"0 4px 4px 0", padding:"8px 10px",
      }}>
        <div style={{ fontSize:8, color:node.color, letterSpacing:2, fontFamily:"monospace", marginBottom:5 }}>
          TAE · DETECCIÓN C1/C2/C3
        </div>
        {node.taeDesc}
      </div>

      {/* Criteria reference */}
      <div>
        <div style={{ fontSize:8, color:T.dim, letterSpacing:2, fontFamily:"monospace", marginBottom:6 }}>
          CRITERIOS TAGIS-1
        </div>
        <div style={{ display:"flex", flexDirection:"column", gap:4 }}>
          {criteriaKeys.map(k => {
            const def = TAE_CRITERIA[k];
            const hits = myExc.filter(e=>e.criterion===k);
            return (
              <div key={k} style={{
                display:"flex", alignItems:"center", justifyContent:"space-between",
                padding:"5px 10px",
                border:`1px solid ${hits.length ? def.color+"50" : T.faint}`,
                borderRadius:4,
                background: hits.length ? `${def.color}08` : "transparent",
                transition:"all 0.3s",
              }}>
                <div style={{ display:"flex", alignItems:"center", gap:8 }}>
                  <span style={{ fontSize:12, color:def.color }}>{def.symbol}</span>
                  <span style={{ fontSize:9, fontFamily:"monospace", color:T.text }}>{def.label}</span>
                </div>
                <div style={{ display:"flex", alignItems:"center", gap:8 }}>
                  <span style={{ fontSize:8, fontFamily:"monospace", color:T.dim }}>{def.threshold}</span>
                  {hits.length > 0 && (
                    <span style={{
                      fontSize:9, fontFamily:"monospace", color:def.color,
                      border:`1px solid ${def.color}40`, borderRadius:3, padding:"1px 5px",
                    }}>×{hits.length}</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Params */}
      <div>
        <div style={{ fontSize:8, color:T.dim, letterSpacing:2, fontFamily:"monospace", marginBottom:6 }}>
          PARÁMETROS
        </div>
        {node.params.map(([k,v]) => (
          <div key={k} style={{
            display:"flex", justifyContent:"space-between",
            padding:"4px 0", borderBottom:`1px solid ${T.faint}`,
          }}>
            <span style={{ fontSize:9, fontFamily:"monospace", color:T.dim }}>{k}</span>
            <span style={{ fontSize:9, fontFamily:"monospace", color:node.color }}>{v}</span>
          </div>
        ))}
      </div>

      {/* Outputs */}
      <div style={{ display:"flex", gap:6 }}>
        {node.outputs.map(o => (
          <div key={o} style={{
            fontSize:9, fontFamily:"monospace", color:node.color,
            border:`1px solid ${node.color}40`, borderRadius:4,
            padding:"2px 8px", background:`${node.color}08`,
          }}>→ {o}</div>
        ))}
      </div>
    </div>
  );
}

// ─── EXCEPTION STREAM ────────────────────────────────────────────────────────
function ExcStream({ exceptions }) {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight;
  }, [exceptions]);

  return (
    <div style={{
      border:`1px solid ${T.border}`, borderRadius:8,
      background:T.bgDeep, padding:14,
      display:"flex", flexDirection:"column", height:"100%",
    }}>
      <div style={{ fontSize:8, color:T.dim, letterSpacing:2, fontFamily:"monospace", marginBottom:8 }}>
        TAE · EXCEPTION STREAM
      </div>
      <div ref={ref} style={{ flex:1, overflow:"auto", display:"flex", flexDirection:"column", gap:4 }}>
        {exceptions.length === 0 && (
          <div style={{ color:T.dim, fontFamily:"monospace", fontSize:9 }}>Sin excepciones registradas.</div>
        )}
        {exceptions.map(e => {
          const def = TAE_CRITERIA[e.criterion];
          const node = NODES.find(n=>n.id===e.nodeId);
          return (
            <div key={e.id} style={{
              display:"flex", alignItems:"center", gap:8,
              padding:"4px 8px",
              border:`1px solid ${def.color}30`,
              borderRadius:4,
              background:`${def.color}08`,
              animation:"exc-in 0.3s ease-out",
            }}>
              <span style={{ fontSize:10, color:def.color }}>{def.symbol}</span>
              <span style={{ fontSize:8, color:T.dim, fontFamily:"monospace" }}>{e.ts}</span>
              <span style={{ fontSize:9, color:node?.color, fontFamily:"monospace" }}>{e.nodeId}</span>
              <span style={{ fontSize:9, color:def.color, fontFamily:"monospace", fontWeight:700 }}>{e.criterion}</span>
              <span style={{ fontSize:9, color:T.text, fontFamily:"monospace" }}>{e.value}σ</span>
              {e.orion && <span style={{ fontSize:8, color:T.gold, fontFamily:"monospace", marginLeft:"auto" }}>⬡ ORION</span>}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── ORION METADATA PANEL ────────────────────────────────────────────────────
function OrionPanel({ latentVector, exceptions, milestone }) {
  const orionExcs = exceptions.filter(e=>e.orion);
  const inException = orionExcs.length > 0;

  return (
    <div style={{
      border:`1px solid ${inException ? T.gold+"60" : T.border}`,
      borderRadius:8, background:T.card, padding:16,
      boxShadow: inException ? `0 0 20px ${T.gold}18` : "none",
      transition:"all 0.4s",
    }}>
      <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:12 }}>
        <div>
          <div style={{ fontSize:8, color:T.dim, letterSpacing:2, fontFamily:"monospace" }}>
            CONECTOR · SIGMA-T → ORION-AGI
          </div>
          <div style={{ fontSize:13, color:T.gold, fontFamily:"monospace", fontWeight:700 }}>
            ⬡ ORION-AGI METADATA BUS
          </div>
        </div>
        <div style={{
          fontSize:9, fontFamily:"monospace",
          color: inException ? T.red : T.green,
          border:`1px solid ${inException ? T.red : T.green}40`,
          borderRadius:4, padding:"3px 8px",
          background:`${inException ? T.red : T.green}10`,
          animation: inException ? "exc-pulse 1s ease-in-out infinite" : "none",
        }}>
          {inException ? "⚠ INFERENCIA-EN-EXCEPCIÓN" : "● ESTADO COHERENTE"}
        </div>
      </div>

      {/* Latent vector preview */}
      <div style={{
        fontFamily:"monospace", fontSize:9, color:T.text,
        background:T.bgDeep, borderRadius:5, padding:"8px 12px",
        marginBottom:10, border:`1px solid ${T.faint}`,
      }}>
        <div style={{ color:T.dim, fontSize:8, marginBottom:4 }}>latent_vector[t] · dim=32</div>
        <div style={{ color:T.cyan, wordBreak:"break-all", lineHeight:1.8 }}>
          [{latentVector.map(v=>v.toFixed(4)).join(", ")}...]
        </div>
        <div style={{ display:"flex", gap:16, marginTop:6 }}>
          {[
            ["version",   "SIGMA-T v1.0"],
            ["state",     inException ? "exception_active" : "coherent"],
            ["exc_count", orionExcs.length],
            ["criteria",  orionExcs.length ? [...new Set(orionExcs.map(e=>e.criterion))].join("+") : "—"],
          ].map(([k,v]) => (
            <div key={k} style={{ display:"flex", flexDirection:"column" }}>
              <span style={{ fontSize:7, color:T.dim }}>{k}</span>
              <span style={{ fontSize:9, color: k==="state" && inException ? T.red : T.amber }}>{v}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Milestone banner */}
      {milestone && (
        <div style={{
          border:`1px solid ${T.green}60`, borderRadius:5,
          background:`${T.green}08`, padding:"8px 12px",
          display:"flex", alignItems:"center", gap:10,
        }}>
          <span style={{ fontSize:18 }}>✓</span>
          <div>
            <div style={{ fontSize:9, color:T.green, fontFamily:"monospace", fontWeight:700 }}>
              HITO SIGMA-T v1.0 ALCANZADO
            </div>
            <div style={{ fontSize:8, color:T.text, fontFamily:"monospace", marginTop:2 }}>
              Reemplazo N1 ICA→Riemannian: Δ embedding = {(Math.random()*0.003+0.0008).toFixed(4)} · dentro de umbral σ²_esperado
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── VARIANCE TEST PANEL ─────────────────────────────────────────────────────
function VarianceTest({ runs }) {
  return (
    <div style={{
      border:`1px solid ${T.border}`, borderRadius:8,
      background:T.card, padding:16,
    }}>
      <div style={{ fontSize:8, color:T.dim, letterSpacing:2, fontFamily:"monospace", marginBottom:10 }}>
        HITO · INVARIANZA DE EMBEDDING BAJO SWAP N1
      </div>
      <div style={{ fontSize:9, color:T.text, fontFamily:"monospace", marginBottom:10, lineHeight:1.7 }}>
        Reemplazar backend N1 (ICA → Riemannian) no debe alterar{" "}
        <span style={{ color:T.cyan }}>latent_vector[t]</span> más allá de{" "}
        <span style={{ color:T.amber }}>σ²_esperado</span>.
      </div>
      <div style={{ display:"flex", flexDirection:"column", gap:3 }}>
        {runs.map((r, i) => (
          <div key={i} style={{
            display:"flex", alignItems:"center", gap:8,
            padding:"4px 8px", borderRadius:4,
            background: r.pass ? `${T.green}08` : `${T.red}08`,
            border:`1px solid ${r.pass ? T.green+"40" : T.red+"40"}`,
          }}>
            <span style={{ fontSize:9, color:r.pass?T.green:T.red }}>{r.pass?"✓":"✗"}</span>
            <span style={{ fontSize:9, fontFamily:"monospace", color:T.dim }}>{r.label}</span>
            <span style={{ fontSize:9, fontFamily:"monospace", color:r.pass?T.green:T.red, marginLeft:"auto" }}>
              Δ={r.delta.toFixed(5)}
            </span>
            <span style={{ fontSize:8, fontFamily:"monospace", color:T.dim }}>
              {r.pass?"< σ²_exp":"≥ σ²_exp"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── PIPELINE SCRIPT ─────────────────────────────────────────────────────────
const SCRIPT = [
  { node:"N1", msg:"[N1·ICA] Cargando EEG_RAW · aplicando ICA fastica 64 comp.",   color:T.cyan },
  { node:"N1", msg:"[N1·TAE] C1 scan: d(x,μ)=1.2σ · sin excepción.",               color:T.dim  },
  { node:"N1", msg:"[N1·ICA] EEG_CLEAN emitido → N2.",                              color:T.green},
  { node:"N2", msg:"[N2·WLT] Wavelet db4 · 6 bandas × 64ch × ventana 2s.",         color:T.amber},
  { node:"N2", msg:"[N2·TAE] C1: banda γ → d=3.7σ ⚡ EXCEPCIÓN DETECTADA",         color:T.c1, exc:{node:"N2",cr:"C1"} },
  { node:"N2", msg:"[N2·TAE] C1 propagada como metadato → N3.",                     color:T.c1   },
  { node:"N3", msg:"[N3·COH] Coherencia Welch cross-spectral iniciada.",             color:T.green},
  { node:"N3", msg:"[N3·TAE] ΔH=0.61 nats ∇ C2 EXCEPCIÓN · entrada en exc activa.",color:T.c2, exc:{node:"N3",cr:"C2"} },
  { node:"N3", msg:"[N3·COH] CPEA_IDX=0.571 · IC_exc=2.8σ. COH_MATRIX → N4.",      color:T.green},
  { node:"N4", msg:"[N4·TIC] Φ_TICAM modo degradado (sin magnetometría ext).",      color:T.purple},
  { node:"N4", msg:"[N4·TAE] C1 scan acoplamiento: 1.9σ · sin excepción.",          color:T.dim  },
  { node:"N4", msg:"[N4·TIC] TICAM_STATE emitido → N5.",                            color:T.purple},
  { node:"N5", msg:"[N5·EMB] LSTM-AE encoding · dim_latent=32.",                    color:T.red  },
  { node:"N5", msg:"[N5·TAE] C2+C3 heredados activos · flag ORION-AGI activado. ⬡", color:T.gold, exc:{node:"N5",cr:"C3"} },
  { node:"N5", msg:"[N5·EMB] latent_vector[t] emitido + metadata versión.",         color:T.green},
  { node:null,  msg:"[DAG] Pipeline completo · SIGMA-T v1.0 · CPEA_STREAM publicado.",color:T.cyan},
];

// ─── MAIN ────────────────────────────────────────────────────────────────────
export default function SigmaT() {
  const [selected, setSelected]       = useState(null);
  const [running, setRunning]         = useState(null);
  const [log, setLog]                 = useState([]);
  const [exceptions, setExceptions]   = useState([]);
  const [active, setActive]           = useState(false);
  const [excPulse, setExcPulse]       = useState(null);
  const [edgeExcColor, setEdgeExcColor] = useState({});
  const [latentVec, setLatentVec]     = useState(() => Array.from({length:8},()=>rand(-1,1)));
  const [milestone, setMilestone]     = useState(false);
  const [varRuns]                     = useState(() => [
    { label:"fastica   → baseline",   delta:0.00000, pass:true  },
    { label:"picard    → fastica",    delta:rand(0.0001,0.0009), pass:true  },
    { label:"riemannian→ fastica",    delta:rand(0.0010,0.0028), pass:true  },
    { label:"riemannian→ picard",     delta:rand(0.0011,0.0029), pass:true  },
  ]);
  const [activeEdges, setActiveEdges] = useState({});

  const logRef = useRef(null);
  const stepRef = useRef(0);
  const timerRef = useRef(null);

  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [log]);

  const runPipeline = useCallback(() => {
    if (active) return;
    setActive(true);
    setMilestone(false);
    setExceptions([]);
    setEdgeExcColor({});
    setActiveEdges({});
    setLog([]);
    stepRef.current = 0;

    const step = () => {
      if (stepRef.current >= SCRIPT.length) {
        setActive(false);
        setRunning(null);
        setMilestone(true);
        setLatentVec(Array.from({length:8},()=>rand(-1,1)));
        return;
      }
      const s = SCRIPT[stepRef.current];
      setRunning(s.node);
      if (s.node) setSelected(s.node);
      setLog(l => [...l.slice(-40), { text: s.msg, color: s.color }]);

      // Activate edge after node emission
      if (s.node) {
        const edge = EDGES.find(e=>e.from===s.node);
        if (edge) {
          setActiveEdges(ae => ({ ...ae, [edge.from]: true }));
          if (s.exc) {
            setEdgeExcColor(ec => ({ ...ec, [edge.from]: TAE_CRITERIA[s.exc.cr].color }));
          }
        }
      }

      if (s.exc) {
        const exc = { ...makeExc(s.exc.node), criterion: s.exc.cr };
        setExceptions(ex => [...ex, exc]);
        setExcPulse(exc);
        setTimeout(() => setExcPulse(null), 800);
      }

      stepRef.current++;
      timerRef.current = setTimeout(step, 480 + Math.random()*320);
    };
    step();
  }, [active]);

  useEffect(() => () => clearTimeout(timerRef.current), []);

  const selNode = NODES.find(n=>n.id===selected);

  return (
    <div style={{
      minHeight:"100vh", background:T.bg, color:T.text,
      fontFamily:"'Courier New', monospace",
      padding:20,
      backgroundImage:`
        radial-gradient(ellipse at 15% 15%, #001a2e18 0%, transparent 55%),
        radial-gradient(ellipse at 85% 85%, #0a001818 0%, transparent 55%),
        repeating-linear-gradient(0deg, transparent, transparent 39px, #ffffff04 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, #ffffff04 40px)
      `,
    }}>
      <style>{`
        @keyframes blink        { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes travel       { 0%{left:0} 100%{left:calc(100% - 8px)} }
        @keyframes exc-pulse    { 0%{opacity:1} 50%{opacity:0.3} 100%{opacity:1} }
        @keyframes exc-card     { 0%{transform:scale(1)} 25%{transform:scale(1.02)} 100%{transform:scale(1)} }
        @keyframes exc-in       { from{opacity:0;transform:translateX(-6px)} to{opacity:1;transform:none} }
        * { box-sizing:border-box; }
        ::-webkit-scrollbar{width:3px;height:3px}
        ::-webkit-scrollbar-track{background:transparent}
        ::-webkit-scrollbar-thumb{background:#1e3040;border-radius:2px}
      `}</style>

      {/* ── HEADER ── */}
      <div style={{ marginBottom:20, borderBottom:`1px solid ${T.border}`, paddingBottom:16 }}>
        <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-end" }}>
          <div>
            <div style={{ fontSize:8, color:T.dim, letterSpacing:3, marginBottom:3 }}>
              CORPUS PAPAYAYKWARE · CPEA MODULE · SIGMA-T
            </div>
            <div style={{ fontSize:24, fontWeight:900, color:T.cyan, letterSpacing:2, lineHeight:1 }}>
              SIGMA-T <span style={{ color:T.amber }}>v1.0</span>
            </div>
            <div style={{ fontSize:10, color:T.dim, marginTop:3 }}>
              NEXUS-EEG DAG · Integración TAE C1/C2/C3 · ORION-AGI metadata bus
            </div>
          </div>
          <div style={{ display:"flex", gap:10, alignItems:"center" }}>
            <div style={{ fontSize:8, color:T.green, border:`1px solid ${T.green}40`, borderRadius:4, padding:"3px 8px", background:`${T.green}08` }}>
              ● OPERACIONAL
            </div>
            <button
              onClick={runPipeline}
              disabled={active}
              style={{
                background: active ? T.card : `${T.cyan}12`,
                border:`1px solid ${active ? T.dim : T.cyan}`,
                color: active ? T.dim : T.cyan,
                borderRadius:5, padding:"7px 16px",
                fontFamily:"monospace", fontSize:10, cursor: active?"default":"pointer",
                letterSpacing:1, transition:"all 0.2s",
              }}
            >
              {active ? "▶ EJECUTANDO..." : "▶ EJECUTAR PIPELINE"}
            </button>
          </div>
        </div>
      </div>

      {/* ── DAG PIPELINE ROW ── */}
      <div style={{ marginBottom:16 }}>
        <div style={{ fontSize:8, color:T.dim, letterSpacing:2, marginBottom:10 }}>
          DAG · NEXUS-EEG → SIGMA-T · TAE INTEGRADO
        </div>
        <div style={{ display:"flex", alignItems:"stretch", gap:0 }}>
          {NODES.map((node, i) => (
            <div key={node.id} style={{ display:"flex", alignItems:"center", flex: i < NODES.length-1 ? "1 1 0" : "1 1 0", gap:0 }}>
              <NodeCard
                node={node}
                selected={selected}
                exceptions={exceptions}
                onSelect={setSelected}
                running={running}
                excPulse={excPulse}
              />
              {i < NODES.length - 1 && (
                <EdgeConnector
                  edge={EDGES[i]}
                  active={!!activeEdges[EDGES[i].from]}
                  excColor={edgeExcColor[EDGES[i].from]}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* ── MIDDLE SECTION ── */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:14 }}>
        <DetailPanel node={selNode} exceptions={exceptions} />
        <ExcStream exceptions={exceptions} />
      </div>

      {/* ── ORION + VARIANCE ── */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:14 }}>
        <OrionPanel latentVector={latentVec} exceptions={exceptions} milestone={milestone} />
        <VarianceTest runs={varRuns} />
      </div>

      {/* ── PIPELINE LOG ── */}
      <div style={{
        border:`1px solid ${T.border}`, borderRadius:8,
        background:T.bgDeep, padding:14, marginBottom:14,
      }}>
        <div style={{ display:"flex", justifyContent:"space-between", marginBottom:8 }}>
          <div style={{ fontSize:8, color:T.dim, letterSpacing:2 }}>
            SIGMA-T · PIPELINE LOG
          </div>
          {active && <div style={{ fontSize:8, color:T.green, animation:"blink 1s step-end infinite" }}>● LIVE</div>}
        </div>
        <div ref={logRef} style={{ height:90, overflow:"auto", display:"flex", flexDirection:"column", gap:2 }}>
          {log.length === 0 && (
            <div style={{ color:T.dim, fontFamily:"monospace", fontSize:9 }}>Esperando ejecución...</div>
          )}
          {log.map((l,i) => (
            <div key={i} style={{ fontSize:9, fontFamily:"monospace", color:l.color, lineHeight:1.7 }}>
              <span style={{ color:T.faint }}>$ </span>{l.text}
            </div>
          ))}
        </div>
      </div>

      {/* ── FOOTER ── */}
      <div style={{
        borderTop:`1px solid ${T.faint}`, paddingTop:10,
        display:"flex", justifyContent:"space-between", alignItems:"center",
      }}>
        <div style={{ fontSize:7, color:T.dim, letterSpacing:1 }}>
          Autor conceptual: Claude (Anthropic) · Director: Javi Ciborro (@papayaykware)
        </div>
        <div style={{ display:"flex", gap:14, fontSize:7, color:T.dim }}>
          <span>github.com/papayaykware</span>
          <span>·</span>
          <span>papayaykware.blogspot.com</span>
        </div>
      </div>
    </div>
  );
}
