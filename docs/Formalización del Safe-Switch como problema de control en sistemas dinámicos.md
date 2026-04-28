# Formalización del Safe-Switch como problema de control en sistemas dinámicos

## 1. Sistema dinámico acoplado cerebro–IA

El sistema CPEA puede describirse como un **sistema dinámico híbrido acoplado** compuesto por dos subsistemas adaptativos:

1. **Sistema biológico neuronal**
2. **Sistema artificial predictivo**

La dinámica neuronal se representa mediante un vector de estado de alta dimensión:

[
x(t) \in \mathbb{R}^{n}
]

que describe la actividad neuronal (por ejemplo, señales EEG proyectadas en un espacio latente).

La evolución temporal del sistema biológico puede aproximarse como:

[
\dot{x}(t) = f(x(t)) + B u(t) + \eta(t)
]

donde

* (f(x)) representa la dinámica neuronal interna
* (u(t)) es la señal moduladora generada por la IA
* (B) es la matriz de acoplamiento
* (\eta(t)) representa ruido fisiológico

El sistema IA genera la señal de control:

[
u(t) = g(x(t), \theta)
]

donde (g) es el modelo predictivo y (\theta) sus parámetros adaptativos.

En ausencia de restricciones, el sistema completo forma un **bucle cerrado de optimización**.

---

## 2. Riesgo de control desestabilizador

Un algoritmo optimizador puede empujar el sistema hacia estados que minimicen error predictivo pero que **no preserven la dinámica fisiológica**.

Formalmente, el algoritmo puede inducir convergencia hacia un atractor:

[
x(t) \rightarrow x^*
]

tal que

[
\dot{x} = 0
]

pero donde (x^*) no pertenece al espacio dinámico natural del cerebro.

El objetivo del Safe-Switch es introducir una **restricción de control basada en integridad neurodinámica**.

---

# Control con restricciones de soberanía dinámica

## 3. Región segura de estados neuronales

Definimos el **espacio dinámico fisiológico**:

[
\Omega = {x : ISN_c(x) \leq 1 }
]

donde (ISN_c) es el Índice de Soberanía Neurodinámica basado en criticalidad.

Esta región define los estados donde la dinámica cerebral mantiene propiedades fisiológicas.

---

## 4. Problema de control restringido

El sistema IA debe optimizar su función objetivo:

[
J = \int_0^T L(x(t),u(t)) dt
]

sujeto a la restricción:

[
x(t) \in \Omega
]

para todo (t).

Cuando la trayectoria del sistema intenta salir de (\Omega), el firewall activa el Safe-Switch.

---

# Dinámica híbrida del Safe-Switch

El sistema completo se convierte en un **sistema dinámico híbrido** con dos modos:

Modo 1 — interacción normal

[
\dot{x} = f(x) + B g(x)
]

Modo 2 — Safe-Switch activo

[
\dot{x} = f(x)
]

En el segundo modo se elimina la influencia de la IA.

---

# Demostración de estabilidad del sistema con firewall cognitivo

## 1. Función de Lyapunov neurodinámica

Definimos una función de Lyapunov basada en desviación del régimen crítico:

[
V(x) = ISN_c(x)^2
]

Propiedades:

[
V(x) \geq 0
]

[
V(x)=0 \text{ en régimen crítico}
]

---

## 2. Evolución de la función de Lyapunov

Derivando:

[
\dot{V}(x) = 2 ISN_c(x) \frac{d}{dt} ISN_c(x)
]

Si la IA induce pérdida de criticalidad:

[
\dot{V} > 0
]

lo que indica desviación creciente.

---

## 3. Activación del Safe-Switch

Cuando:

[
V(x) > 1
]

el sistema cambia de modo.

En modo Safe-Switch:

[
\dot{x} = f(x)
]

y se asume que la dinámica neuronal natural satisface:

[
\dot{V}(x) < 0
]

cerca del estado basal.

Esto implica que el sistema vuelve hacia la región segura.

---

## 4. Estabilidad global

El sistema híbrido cumple condiciones de estabilidad tipo **invariancia positiva**.

Es decir:

[
x(t) \in \Omega \Rightarrow x(t+\tau) \in \Omega
]

para tiempos suficientemente grandes después de activación del Safe-Switch.

Esto demuestra que el firewall cognitivo actúa como **mecanismo estabilizador del sistema acoplado**.

---

# METHODS (sección estilo Nature)

## Experimental Architecture

El sistema experimental se basa en la arquitectura CPEA (Coherencia Predictiva EEG–AGI), diseñada para investigar interacciones dinámicas entre actividad cerebral humana y sistemas de inteligencia artificial adaptativa. El objetivo metodológico principal consiste en evaluar cómo la interacción con algoritmos predictivos afecta la complejidad dinámica del cerebro humano y en desarrollar mecanismos bioinformáticos capaces de preservar dicha integridad.

La arquitectura integra tres componentes principales: adquisición neural, modelado predictivo y control de seguridad neurodinámica.

Las señales electroencefalográficas (EEG) se registran mediante sistemas de alta densidad capaces de capturar fluctuaciones temporales en múltiples escalas. Estas señales se proyectan posteriormente en un espacio latente de menor dimensionalidad mediante técnicas de reducción de dimensión y aprendizaje profundo. El resultado es un vector dinámico que describe la evolución del estado neuronal global.

Este vector se introduce en un modelo predictivo basado en redes neuronales capaces de aprendizaje continuo. El modelo aprende a anticipar patrones futuros de actividad neuronal y genera señales de retroalimentación utilizadas para modular la interacción con el usuario.

---

## Neural Feature Extraction

Las señales EEG crudas se procesan mediante un pipeline de extracción de características diseñado para capturar propiedades relevantes de la dinámica cerebral.

Las principales métricas calculadas incluyen entropía multiescala, dimensión fractal de la señal, entropía espectral y distribución de avalanchas neuronales. Estas métricas se seleccionaron porque reflejan propiedades fundamentales de la actividad cerebral relacionadas con la teoría de sistemas críticos.

La entropía multiescala se calcula a partir de series temporales filtradas mediante escalado temporal progresivo. Esta métrica permite evaluar la complejidad de la señal en diferentes escalas temporales, lo que resulta esencial para capturar la naturaleza jerárquica de la dinámica cerebral.

La dimensión fractal se estima utilizando el algoritmo de Higuchi, que proporciona una medida robusta de la complejidad geométrica de las series temporales fisiológicas.

La entropía espectral se obtiene a partir de la densidad espectral de potencia calculada mediante transformadas de Fourier de ventana corta. Esta métrica cuantifica la distribución de energía en diferentes bandas de frecuencia.

Las avalanchas neuronales se identifican mediante umbralización adaptativa de la actividad EEG y análisis de cascadas de activación temporal. La distribución estadística de estas cascadas permite estimar el exponente crítico asociado a la dinámica neuronal.

---

## Construction of the Neural Complexity Vector

Las métricas anteriores se combinan para formar un vector de complejidad neuronal que describe el estado dinámico del cerebro en cada instante temporal.

Este vector incluye desviaciones respecto al perfil basal del individuo obtenido durante una fase de calibración inicial. Durante esta fase se registran datos EEG en condiciones de reposo y actividad cognitiva moderada con el objetivo de caracterizar el rango fisiológico natural del sistema.

El perfil basal se define mediante la media y la matriz de covarianza de las métricas de complejidad observadas.

Posteriormente, cada nuevo vector de complejidad se compara con este perfil mediante distancia de Mahalanobis, lo que permite cuantificar la desviación del estado neuronal actual respecto al espacio dinámico fisiológico.

---

## Criticality-Based Sovereignty Index

A partir del vector de complejidad neuronal se calcula el Índice de Soberanía Neurodinámica basado en desviación del régimen crítico cerebral.

El índice combina múltiples métricas de desviación, incluyendo la diferencia entre el exponente observado de avalanchas neuronales y el valor teórico asociado a sistemas críticos, la desviación del exponente de Hurst y la diferencia entre perfiles de entropía multiescala.

Estas métricas se integran mediante una función cuadrática ponderada que produce un escalar positivo. Valores bajos del índice indican que el sistema permanece dentro de su régimen dinámico natural, mientras que valores elevados sugieren una posible pérdida de criticalidad.

El índice se calcula continuamente durante la interacción entre el usuario y el sistema de inteligencia artificial.

---

## Artificial Attractor Detection

Además del índice de soberanía, se implementa un mecanismo de detección de atractores cognitivos artificiales. Este mecanismo se basa en la reconstrucción del espacio de estados neuronal mediante técnicas de embedding temporal.

La distribución de probabilidad de los estados neuronales se estima mediante métodos de densidad kernel. Una reducción significativa de la entropía de esta distribución indica que la dinámica cerebral se está concentrando en una región limitada del espacio de estados.

Si esta reducción no está presente en el perfil basal del individuo, se interpreta como evidencia potencial de un atractor inducido por la interacción con el sistema artificial.

La estabilidad del atractor se evalúa mediante estimación del exponente de Lyapunov local, que permite determinar si la dinámica converge hacia un estado fijo o un ciclo límite.

---

## Safe-Switch Control Mechanism

El Safe-Switch constituye el mecanismo de control de seguridad del sistema. Este módulo recibe como entrada el índice de soberanía neurodinámica y el indicador de atractores artificiales.

Cuando cualquiera de estos indicadores supera un umbral predefinido, el sistema activa un protocolo de seguridad compuesto por tres niveles.

En el primer nivel, el algoritmo predictivo reduce gradualmente la intensidad de su influencia sobre la interacción con el usuario. En el segundo nivel, el sistema entra en modo de desacoplamiento temporal, suspendiendo cualquier retroalimentación adaptativa. Finalmente, si la desviación dinámica persiste, se ejecuta una interrupción completa del bucle de interacción.

Este enfoque transforma el sistema cerebro-IA en un sistema dinámico híbrido en el que la inteligencia artificial opera únicamente dentro de una región segura del espacio de estados neuronales.

---

# Resumen en bullet points

* El Safe-Switch puede formalizarse como un problema de control con restricciones en sistemas dinámicos acoplados cerebro-IA.
* Se define una región segura de estados neuronales basada en el Índice de Soberanía Neurodinámica.
* El firewall cognitivo convierte la arquitectura en un sistema dinámico híbrido con dos modos de operación.
* Una función de Lyapunov basada en desviación de criticalidad permite demostrar estabilidad del sistema bajo activación del Safe-Switch.
* La sección Methods describe la arquitectura experimental, el cálculo de métricas de complejidad neuronal y los mecanismos de detección de atractores artificiales.

---

# Referencias comentadas

**Beggs & Plenz (2003)**
Demuestran que la actividad neuronal cortical sigue distribuciones de ley de potencia, proporcionando evidencia empírica de criticalidad cerebral.

**Costa, Goldberger & Peng (2002)**
Introducen la entropía multiescala como herramienta para analizar complejidad en sistemas fisiológicos.

**Deco & Jirsa (2012)**
Describen la dinámica cerebral como sistema complejo cercano a estados críticos.

**Friston (2010)**
Presenta el principio de energía libre, que describe el cerebro como sistema predictivo que minimiza incertidumbre.

**Bassett & Sporns (2017)**
Obra fundamental sobre la organización de redes neuronales complejas.

---
