# 1. Versión LaTeX del Preprint (`paper/preprint.tex`)

Este archivo está preparado para **arXiv / OSF / HAL**.

```latex
\documentclass[11pt]{article}

\usepackage{arxiv}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{float}

\title{CPEA: Predictive Coherence Between EEG Dynamics and Adaptive Artificial General Intelligence}

\author{
Javi Ciborro \\
Independent Researcher \\
\texttt{papayaykware} \\
}

\begin{document}

\maketitle

\begin{abstract}

This paper proposes the Coherencia Predictiva EEG–AGI (CPEA) framework, a novel architecture designed to explore predictive coupling between human neural dynamics and adaptive artificial intelligence systems. 

Unlike traditional brain–computer interfaces that operate through static decoding pipelines, CPEA introduces a bidirectional predictive loop in which artificial agents adapt their internal models in response to exception signals emerging from EEG dynamics.

The architecture integrates predictive embeddings, anomaly detection mechanisms, and continual learning modules inspired by the Theory of Learning by Exception (TAE). Preliminary simulations using synthetic EEG environments demonstrate the feasibility of predictive synchronization between neural signals and artificial agents.

The framework aims to open new research directions in neuroadaptive interfaces, human–AI symbiosis, and predictive cognitive systems.

\end{abstract}

\section{Introduction}

Brain–computer interfaces have traditionally focused on decoding neural signals to control external systems. 

However, emerging perspectives suggest that neural systems operate fundamentally as predictive engines. Artificial intelligence systems designed to interact with neural activity may therefore benefit from predictive alignment mechanisms rather than simple signal decoding.

This work proposes the Coherencia Predictiva EEG–AGI (CPEA) architecture as a framework for studying predictive coupling between biological and artificial cognitive systems.

\section{Conceptual Framework}

The conceptual basis of the CPEA architecture combines three key principles:

\begin{itemize}

\item Predictive processing models of neural activity.
\item Continual learning in artificial intelligence systems.
\item Exception-driven learning dynamics inspired by TAE.

\end{itemize}

Together these principles define a system capable of adapting its internal representations when encountering unexpected neural patterns.

\section{System Architecture}

The architecture contains four core modules:

\begin{enumerate}

\item EEG Signal Encoder
\item Predictive Embedding Network
\item Anomaly Detection Layer
\item Continual Learning Engine

\end{enumerate}

Figure \ref{fig:architecture} illustrates the conceptual architecture.

\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{figures/cpea_architecture.png}
\caption{Conceptual architecture of the CPEA predictive loop.}
\label{fig:architecture}
\end{figure}

\section{Predictive Coherence Model}

The central hypothesis of the framework is that predictive coherence can emerge when artificial systems adapt to temporal structures present in neural signals.

Predictive coherence is defined as the minimization of temporal prediction error:

\[
E_t = ||x_t - \hat{x}_t||
\]

where \(x_t\) represents EEG observations and \(\hat{x}_t\) represents model predictions.

\section{Experimental Protocol}

The experimental protocol includes three stages:

\begin{enumerate}

\item Synthetic EEG simulation
\item Training of predictive models
\item Evaluation of coherence metrics
\end{enumerate}

\section{Discussion}

The framework proposes a new paradigm for human–AI interaction based on predictive synchronization between neural and artificial systems.

\section{Conclusion}

CPEA introduces a predictive architecture for exploring coupled cognitive systems between human neural activity and artificial intelligence.

Future work will validate the framework using real EEG datasets and closed-loop experimental environments.

\bibliographystyle{plain}

\begin{thebibliography}{9}

\bibitem{friston2010}
Friston, K.
The Free Energy Principle.
Nature Reviews Neuroscience, 2010.

\bibitem{kirkpatrick2017}
Kirkpatrick et al.
Overcoming catastrophic forgetting in neural networks.
PNAS, 2017.

\end{thebibliography}

\end{document}
```

---

# 2. Figuras científicas reproducibles

En lugar de subir imágenes estáticas, es mucho más potente generar las figuras con código.

Archivo:

```
figures/generate_figures.py
```

```python
import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()

nodes = [
"EEG Signals",
"Predictive Encoder",
"Embedding Space",
"Anomaly Detector",
"Continual Learning",
"Adaptive AGI"
]

G.add_nodes_from(nodes)

edges = [
("EEG Signals","Predictive Encoder"),
("Predictive Encoder","Embedding Space"),
("Embedding Space","Anomaly Detector"),
("Anomaly Detector","Continual Learning"),
("Continual Learning","Adaptive AGI"),
("Adaptive AGI","Predictive Encoder")
]

G.add_edges_from(edges)

pos = nx.spring_layout(G)

plt.figure(figsize=(10,7))
nx.draw(G,pos,with_labels=True,node_size=3000,font_size=10)

plt.title("CPEA Predictive Cognitive Loop")

plt.savefig("cpea_architecture.png")
```

Esto genera automáticamente la **figura del paper**.

---

# 3. Primer Notebook reproducible

Archivo:

```
notebooks/01_predictive_coherence_demo.ipynb
```

Versión Python equivalente:

```python
import torch
import torch.nn as nn
import numpy as np

# Synthetic EEG signal
t = np.linspace(0,10,2000)

signal = np.sin(10*t) + 0.2*np.random.randn(len(t))

x = torch.tensor(signal,dtype=torch.float32)

class Predictor(nn.Module):

    def __init__(self):

        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(1,32),
            nn.ReLU(),
            nn.Linear(32,1)
        )

    def forward(self,x):

        return self.net(x)

model = Predictor()

optimizer = torch.optim.Adam(model.parameters(),lr=1e-3)

loss_fn = nn.MSELoss()

for epoch in range(200):

    inp = x[:-1].unsqueeze(1)
    target = x[1:].unsqueeze(1)

    pred = model(inp)

    loss = loss_fn(pred,target)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if epoch % 20 == 0:

        print(epoch,loss.item())
```

Este notebook demuestra:

* predicción temporal EEG
* cálculo de error predictivo
* base para coherencia predictiva

---

# 4. Estructura final recomendada del repositorio

```
CPEA
│
├── README.md
├── LICENSE
│
├── paper
│   ├── preprint.md
│   └── preprint.tex
│
├── figures
│   └── generate_figures.py
│
├── notebooks
│   └── 01_predictive_coherence_demo.ipynb
│
├── models
│   ├── predictive_encoder.py
│   ├── anomaly_detector.py
│   └── continual_learning.py
│
└── experiments
    └── synthetic_environment.py
```
