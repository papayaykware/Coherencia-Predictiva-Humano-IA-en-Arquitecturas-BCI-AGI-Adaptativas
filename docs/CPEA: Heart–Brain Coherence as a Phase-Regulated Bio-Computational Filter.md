# 🧠❤️ CPEA: Heart–Brain Coherence as a Phase-Regulated Bio-Computational Filter

![Status](https://img.shields.io/badge/status-active-success)
![Field](https://img.shields.io/badge/field-AGI%20%7C%20Neurodynamics-blue)
![Framework](https://img.shields.io/badge/framework-CPEA--TAE--METFI-purple)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![DOI](https://img.shields.io/badge/DOI-10.3389%2Ffnins.2019.00508-blue)

---

> ⚡ **Core Thesis**  
> The heart operates as a primary toroidal oscillator regulating phase coherence across bio-computational systems. HRV becomes a global stability variable for predictive cognition.

---

# 📑 Table of Contents

- [📌 Abstract](#-abstract)
- [🔑 Keywords](#-keywords)
- [🧭 Conceptual Overview](#-conceptual-overview)
- [❤️ Heart as Primary Oscillator](#-heart-as-primary-oscillator)
- [📈 HRV as Coherence State Variable](#-hrv-as-coherence-state-variable)
- [🧠 Gut–Brain Interface (Biological Modem)](#-gutbrain-interface-biological-modem)
- [🔄 Phase Synchronization Model](#-phase-synchronization-model)
- [⚙️ Phase Training in AGI (CPEA Extension)](#️-phase-training-in-agi-cpea-extension)
- [🧪 Experimental Tracking Programs](#-experimental-tracking-programs)
- [📊 Implementation (PyTorch Sketch)](#-implementation-pytorch-sketch)
- [🧩 Discussion](#-discussion)
- [✅ Conclusions](#-conclusions)
- [📌 Key Takeaways](#-key-takeaways)
- [📚 References (Expandable)](#-references-expandable)

---

# 📌 Abstract

This work extends the EEG–AGI Predictive Coherence framework (CPEA) by incorporating Heart Rate Variability (HRV) as a central state variable in coupled bio-computational systems. The heart is proposed as the primary toroidal oscillator governing systemic phase alignment, while the enteric nervous system acts as a preprocessing interface. A novel **phase training paradigm** is introduced, enabling AGI architectures to stabilize predictions under uncertainty by anchoring inference to cardiac coherence.

---

# 🔑 Keywords

`CPEA` · `HRV` · `Phase Synchronization` · `Heart-Brain Coupling` · `TAE` · `METFI` · `AGI` · `Bioelectricity`

---

# 🧭 Conceptual Overview

> 💡 **Insight**  
> Cognition is not only computation — it is synchronization.

The system can be modeled as a hierarchy of coupled oscillators:

- Heart → base frequency anchor  
- Gut → signal transduction layer  
- Brain → predictive computation layer  

---

# ❤️ Heart as Primary Oscillator

> 🔬 **Observation**  
> The القلب generates the strongest electromagnetic field in the human body.

**Properties:**
- High amplitude field
- Temporal stability
- Global physiological coupling

```mermaid
graph TD
    Heart --> Brain
    Heart --> Gut
    Gut --> Brain
    Brain --> Heart
````

---

# 📈 HRV as Coherence State Variable

> ⚙️ **Definition**
> HRV encodes the system’s position within its dynamic attractor landscape.

| HRV Pattern            | System State     |
| ---------------------- | ---------------- |
| Coherent sinusoidal    | Stable attractor |
| Irregular / fragmented | Chaotic regime   |

---

# 🧠 Gut–Brain Interface (Biological Modem)

> 📡 **Analogy**
> The enteric system functions as a biological modem.

**Functions:**

* Signal compression
* Multimodal integration
* Low-latency transmission

---

# 🔄 Phase Synchronization Model

> 🧮 **Key Shift**
> From state-based learning → phase-based learning

System representation:

```
x(t) = Σ Ai sin(ωi t + φi)
```

Where coherence depends on **phase alignment (φ)** rather than amplitude alone.

---

# ⚙️ Phase Training in AGI (CPEA Extension)

> 🚀 **Core Innovation**

Traditional AI:

* Learns patterns

CPEA Phase Training:

* Learns **synchronization relationships**

---

## 🔁 Updated Loop

1. EEG input
2. HRV modulation
3. Phase alignment
4. Prediction
5. Exception correction (TAE)

---

> ⚠️ **Callout**
> Phase instability = origin of hallucination in AI systems.

---

# 🧪 Experimental Tracking Programs

## 🧪 Experiment 1: HRV–EEG Coupling

* Simultaneous acquisition
* Phase-locking value (PLV)
* Cognitive performance correlation

---

## 🧪 Experiment 2: Vagal Modulation

* Controlled stimulation
* HRV coherence tracking
* EEG response shifts

---

## 🧪 Experiment 3: AI Integration

* Input: EEG + HRV
* Output: predictive accuracy under noise

---

# 📊 Implementation (PyTorch Sketch)

```python
class CPEA_Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.eeg_layer = nn.Linear(128, 64)
        self.hrv_layer = nn.Linear(1, 64)
        self.output = nn.Linear(64, 10)

    def forward(self, eeg, hrv):
        eeg_feat = self.eeg_layer(eeg)
        hrv_feat = torch.tanh(self.hrv_layer(hrv))
        fused = eeg_feat * hrv_feat  # phase modulation
        return self.output(fused)
```

---

> 📎 **Notebook**
> 👉 [https://github.com/papayaykware/METFI/tree/main/CPEA-demo](https://github.com/papayaykware/METFI/tree/main/CPEA-demo)

---

# 🧩 Discussion

> 🧠 **Shift in Paradigm**

* From computation → coordination
* From prediction → coherence
* From data → dynamics

---

# ✅ Conclusions

The heart is not a peripheral system. It is a **global coherence regulator**.

Integrating HRV into AGI architectures:

* stabilizes inference
* reduces hallucination
* enables adaptive synchronization

---

# 📌 Key Takeaways

* ❤️ Heart = primary oscillator
* 📈 HRV = coherence metric
* 🧠 Brain = predictive engine
* 🔄 TAE = phase error correction
* ⚙️ AGI = synchronization system

---

# 📚 References (Expandable)

<details>
<summary>🧾 McCraty et al. — Cardiac Coherence</summary>

* DOI: [https://doi.org/10.3389/fnins.2019.00508](https://doi.org/10.3389/fnins.2019.00508)
* Summary: Demonstrates heart-brain synchronization and its cognitive effects.

</details>

<details>
<summary>🧾 Karl Friston — Active Inference</summary>

* DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
* Summary: Free energy principle applied to biological systems.

</details>

<details>
<summary>🧾 György Buzsáki — Neural Oscillations</summary>

* DOI: [https://doi.org/10.1093/brain/awh408](https://doi.org/10.1093/brain/awh408)
* Summary: Brain rhythms and synchronization principles.

</details>

<details>
<summary>🧾 Stephen Porges — Polyvagal Theory</summary>

* DOI: [https://doi.org/10.1016/S0306-9877(96)90007-1](https://doi.org/10.1016/S0306-9877%2896%2990007-1)
* Summary: Autonomic regulation and emotional processing.

</details>

<details>
<summary>🧾 Walter Freeman — Nonlinear Brain Dynamics</summary>

* DOI: [https://doi.org/10.1016/S0165-0173(00)00066-5](https://doi.org/10.1016/S0165-0173%2800%2900066-5)
* Summary: Chaotic dynamics in neural systems.

</details>

---

# 📎 Appendix

> 🧬 **Framework Integration**

* METFI → environmental field coupling
* TAE → exception-driven learning
* CPEA → coherence architecture

---

# 🧭 Navigation Index

* [Top](#-cpea-heartbrain-coherence-as-a-phase-regulated-bio-computational-filter)
* [Abstract](#-abstract)
* [Experiments](#-experimental-tracking-programs)
* [Implementation](#-implementation-pytorch-sketch)
* [References](#-references-expandable)

---

> ✨ *Designed for direct deployment in GitHub repositories and scientific preprint workflows.*

```

---
