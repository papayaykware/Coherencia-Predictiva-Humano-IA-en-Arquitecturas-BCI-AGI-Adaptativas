# Fase 5: Validación Colectiva con Agentes Reales

**Versión:** 1.0  
**Fecha:** 2026-03-27  
**Estado:** Planificación  
**Duración estimada:** 16 semanas (Semanas 41–56)

---

## 📌 Tabla de Contenidos

1. [Objetivos de la Fase](#1-objetivos-de-la-fase)
2. [Estructura de la Fase](#2-estructura-de-la-fase)
3. [Subfase 5.1: Estudio Piloto con 10 Agentes](#3-subfase-51-estudio-piloto-con-10-agentes)
4. [Subfase 5.2: Validación de Métricas ICC vs ICP](#4-subfase-52-validación-de-métricas-icc-vs-icp)
5. [Subfase 5.3: Optimización de Red P2P para Sincronización](#5-subfase-53-optimización-de-red-p2p-para-sincronización)
6. [Subfase 5.4: Publicación de Resultados con n=10](#6-subfase-54-publicación-de-resultados-con-n10)
7. [Métricas y Criterios de Éxito](#7-métricas-y-criterios-de-éxito)
8. [Infraestructura y Recursos](#8-infraestructura-y-recursos)
9. [Consideraciones Éticas](#9-consideraciones-éticas)
10. [Entregables y Cronograma](#10-entregables-y-cronograma)

---

## 1. Objetivos de la Fase

### 1.1 Objetivo General
Validar el sistema CPEA-X en un entorno con **múltiples agentes humanos reales** (n=10) interactuando simultáneamente, demostrando la emergencia de coherencia colectiva cuantificable mediante el **Índice de Conciencia Colectiva (ICC)** y la mejora de la sincronización grupal a través de la red P2P.

### 1.2 Objetivos Específicos
- **O1:** Implementar y ejecutar un estudio piloto con 10 participantes utilizando el pipeline CPEA completo (EEG real, AGI local, métricas en tiempo real).
- **O2:** Evaluar la relación entre el ICP individual y el ICC grupal, verificando que el ICC captura propiedades emergentes no reducibles a promedios.
- **O3:** Optimizar la comunicación entre nodos (red P2P) para lograr latencias < 500 ms y sincronización estable.
- **O4:** Generar un preprint con los resultados de la validación colectiva, incluyendo análisis estadísticos y visualizaciones de la dinámica grupal.

---

## 2. Estructura de la Fase

| Subfase | Descripción | Duración | Dependencias |
|---------|-------------|----------|--------------|
| **5.1** | Estudio piloto con 10 agentes simultáneos | 4 semanas | Fase 4 completa |
| **5.2** | Validación de métricas ICC vs ICP individual | 3 semanas | Resultados 5.1 |
| **5.3** | Optimización de red P2P para sincronización | 4 semanas | Infraestructura de red |
| **5.4** | Publicación de resultados con n=10 | 5 semanas | Resultados 5.2, 5.3 |

---

## 3. Subfase 5.1: Estudio Piloto con 10 Agentes

### 3.1 Objetivo
Ejecutar la primera prueba con **10 participantes humanos** usando el pipeline CPEA-X en una configuración de laboratorio controlada, validando la viabilidad técnica y la capacidad de sincronización grupal.

### 3.2 Diseño Experimental

#### Participantes
- **N = 10** voluntarios sanos (reclutamiento abierto, priorizando diversidad)
- Criterios de inclusión: ≥18 años, sin trastornos neurológicos conocidos, experiencia básica con interfaces computacionales.
- Compensación: incentivo económico o participación en investigación.

#### Paradigma
- **Tarea grupal sincronizada**: Imaginación motora binaria (izquierda/derecha) con una consigna común (ej., "todos imaginen mover la mano izquierda al ver un círculo rojo, derecha al ver un círculo azul").
- **Estructura de sesión**:
  1. **Calibración individual** (10 min): cada participante ajusta su clasificador.
  2. **Entrenamiento grupal** (15 min): práctica con feedback visual grupal (estado de sincronización mostrado en pantalla compartida).
  3. **Bloques experimentales** (3 bloques de 10 min): cada bloque consta de 50 ensayos con retroalimentación del ICP y del ICC en tiempo real.
  4. **Encuesta post-sesión**: cuestionario de experiencia subjetiva (escala Likert).

#### Hardware y Software
- **EEG**: Muse 2 (4 canales) o Emotiv EPOC X, uno por participante.
- **Computadoras**: 10 laptops/PCs con capacidad de ejecutar pipeline local (CPU 4 cores, 8GB RAM mínimo).
- **AGI local**: Ollama + LLaMA 3 8B en cada nodo (o servidor compartido si latencia lo permite).
- **Red**: LAN cableada o WiFi de alta calidad con switch central.
- **Servidor central** (opcional): para agregar métricas y visualización grupal.
- **Software**: Pipeline CPEA-X extendido con soporte para múltiples agentes (módulo `collective`).

### 3.3 Variables Registradas

Por cada ensayo y participante:
- ICP individual
- Fase de oscilación cognitiva (θᵢ)
- Intent predicho y real
- Latencia de procesamiento
- Características EEG (bandas alpha, beta)
- Datos geomagnéticos (timestamp correlacionado)

Variables agregadas:
- Parámetro de orden grupal (r)
- ICC (Índice de Conciencia Colectiva)
- Entropía de fases
- Matriz de coherencia entre pares

### 3.4 Logística
- **Espacio**: Sala amplia con 10 estaciones separadas visualmente pero conectadas en red.
- **Personal**: 2 investigadores supervisores, 1 técnico de soporte.
- **Sesiones**: 3 sesiones por participante (días diferentes) para evaluar consistencia.
- **Duración total por sesión**: ~90 min (incluyendo preparación).

---

## 4. Subfase 5.2: Validación de Métricas ICC vs ICP Individual

### 4.1 Objetivo
Analizar la relación entre el ICP individual y el ICC grupal, demostrando que el ICC captura propiedades emergentes (sinergia) más allá del promedio de los ICPs.

### 4.2 Hipótesis
- **H1:** El ICC es significativamente mayor que el promedio de los ICP individuales en condiciones de alta sincronización.
- **H2:** Existe una correlación positiva entre el ICC y la coherencia de fase (r), pero no con el promedio de ICP en ausencia de sincronía.
- **H3:** La dinámica del ICC presenta transiciones de fase similares a las observadas en simulación (Fase 4.3).

### 4.3 Análisis Estadístico

#### Variables
- Variable dependiente: ICC (t)
- Variables independientes: ICP promedio, r (coherencia de fase), desviación estándar de ICP entre agentes.

#### Pruebas
- **Comparación ICC vs. promedio ICP**: t-test pareado por bloques.
- **Correlación ICC con r**: correlación de Pearson a lo largo del tiempo.
- **ANOVA de medidas repetidas**: efecto del tiempo (bloque) sobre ICC, controlando por ICP promedio.
- **Modelo de regresión lineal múltiple**: ICC ~ ICP_promedio + r + ICP_sd.

#### Visualizaciones
- Gráficas de evolución temporal de ICC vs. ICP_promedio.
- Mapas de calor de matriz de coherencia entre pares.
- Diagramas de dispersión ICC vs. r.

### 4.4 Resultados Esperados
- Confirmación de que el ICC es un mejor predictor de la calidad de la interacción colectiva que el ICP promedio.
- Identificación de umbrales críticos de r (≈0.6) a partir de los cuales el ICC se dispara.
- Validación de la métrica ICC como análogo experimental de la simulación.

---

## 5. Subfase 5.3: Optimización de Red P2P para Sincronización

### 5.1 Objetivo
Diseñar e implementar una arquitectura de red distribuida (P2P) que permita a los agentes compartir sus métricas (fase, ICP) y calcular el campo colectivo de forma descentralizada, minimizando latencia y maximizando tolerancia a fallos.

### 5.2 Arquitectura Propuesta

#### Opción A: Servidor Centralizado
- Un servidor que recibe datos de todos los nodos, calcula r, ψ, ICC y los retransmite.
- Ventajas: simple, consistente.
- Desventajas: punto único de fallo, latencia proporcional al número de nodos.

#### Opción B: P2P con Gossip Protocol
- Cada nodo se comunica con un subconjunto de vecinos (topología de grafo aleatorio o toroidal).
- El campo colectivo se calcula localmente mediante promedio ponderado de vecinos.
- Ventajas: robustez, escalabilidad, baja latencia.
- Desventajas: mayor complejidad, necesidad de consenso eventual.

#### Decisión para Fase 5: **Híbrido**
- **Servidor de coordinación** para sincronización inicial y agregación de métricas globales (logging).
- **P2P para difusión de fase** usando UDP multicast en la LAN local.
- **Algoritmo de consenso simplificado**: cada nodo actualiza su fase basándose en la media de las fases recibidas de todos los nodos en los últimos 500 ms.

### 5.3 Implementación

#### Módulo `src/collective/p2p_network.py`
- Descubrimiento de nodos mediante mDNS (Zeroconf).
- Intercambio de mensajes UDP con formato JSON: `{agent_id, phase, icp, timestamp}`.
- Búfer circular de últimos mensajes para suavizar fluctuaciones.
- Cálculo local de parámetro de orden r y ψ usando la lista de vecinos.

#### Optimizaciones
- **Compresión de datos**: enviar solo fase (float) e ICP (float).
- **Frecuencia de envío**: 10 Hz (cada 100 ms) para balancear carga y latencia.
- **Sincronización de relojes**: NTP local para garantizar timestamps coherentes.

### 5.4 Métricas de Rendimiento
- **Latencia de propagación**: tiempo desde que un nodo envía su fase hasta que es promediada en otro nodo.
- **Desviación de fase local vs. global**: diferencia entre fase calculada localmente y la del servidor central (si existe).
- **Tasa de pérdida de paquetes** en condiciones de red saturada.

### 5.5 Pruebas
- Simulación con 10 nodos virtuales en una sola máquina.
- Prueba en LAN con 10 computadoras reales.
- Medición de latencia bajo carga creciente.

---

## 6. Subfase 5.4: Publicación de Resultados con n=10

### 6.1 Objetivo
Redactar un preprint detallado que presente la metodología, resultados y conclusiones del estudio con 10 participantes, listo para envío a arXiv y posteriormente a una revista de acceso abierto (ej., *Frontiers in Human Neuroscience*, *Scientific Reports*).

### 6.2 Estructura del Preprint

1. **Título**: *Emergencia de Conciencia Colectiva en Sistemas BCI-AGI Adaptativos: Estudio con 10 Participantes*
2. **Autores**: Equipo CPEA (con contribuciones documentadas)
3. **Resumen**: Contexto, métodos, resultados principales, implicaciones.
4. **Introducción**: Breve revisión de CPEA, hipótesis de inteligencia colectiva, necesidad de validación empírica.
5. **Métodos**:
   - Participantes y reclutamiento
   - Hardware y configuración
   - Pipeline CPEA-X (con referencias a módulos)
   - Paradigma experimental
   - Métricas: ICP, ICC, r, entropía
   - Análisis estadístico
6. **Resultados**:
   - Viabilidad técnica (latencia, tasa de éxito)
   - ICP individual vs. ICC grupal (tablas, gráficas)
   - Correlación ICC con coherencia de fase
   - Efecto del tiempo (aprendizaje colectivo)
   - Análisis cualitativo de encuestas
7. **Discusión**:
   - Interpretación de los hallazgos
   - Comparación con simulaciones (Fase 4.3)
   - Limitaciones (tamaño de muestra, tipo de EEG, etc.)
8. **Conclusión y trabajo futuro**
9. **Agradecimientos**
10. **Referencias**
11. **Apéndice**: Datos anonimizados disponibles en repositorio

### 6.3 Datos Abiertos
- Todos los datos anonimizados se publicarán en la carpeta `data/collective_study/` del repositorio.
- Notebooks de análisis reproducibles (`notebooks/07_collective_analysis.ipynb`).
- Código fuente del pipeline extendido para múltiples agentes.

### 6.4 Revisión por Pares Abierta
- Se invitará a la comunidad a revisar el preprint mediante comentarios en GitHub Issues antes del envío formal.

---

## 7. Métricas y Criterios de Éxito

### 7.1 Criterios de Éxito Técnico
| Métrica | Objetivo | Mínimo Aceptable |
|---------|----------|------------------|
| Latencia máxima entre nodos | < 500 ms | < 1000 ms |
| Tasa de pérdida de paquetes | < 1% | < 5% |
| Sincronización estable (r > 0.6) durante ≥ 50% del tiempo | Sí | ≥ 30% del tiempo |
| Tasa de finalización de sesiones sin fallos | 100% | ≥ 90% |

### 7.2 Criterios de Éxito Científico
- **H1 confirmada**: ICC > ICP_promedio con p < 0.05 en al menos 2 de 3 bloques.
- **H2 confirmada**: Correlación ICC-r > 0.6 en condiciones de alta coherencia.
- **H3 confirmada**: Identificación de transición de fase con K efectivo ~1.2 (derivado de datos reales).
- **Encuestas**: Puntuación media de "conexión grupal" > 4/5 en la escala Likert.

### 7.3 Criterios de Éxito de Publicación
- Preprint enviado a arXiv antes de finalizar la fase.
- Al menos 2 revisiones externas (comentarios) recibidas.
- Notebooks de análisis documentados y ejecutables por terceros.

---

## 8. Infraestructura y Recursos

### 8.1 Hardware Requerido
| Elemento | Cantidad | Especificación |
|----------|----------|----------------|
| Dispositivos EEG | 10 | Muse 2 o Emotiv EPOC X |
| Computadoras | 10 | CPU 4 cores, 8GB RAM, WiFi/LAN |
| Switch de red | 1 | Gigabit, 16 puertos |
| Servidor central (opcional) | 1 | CPU 8 cores, 16GB RAM, SSD |
| Cables, auriculares, etc. | según necesidad | - |

### 8.2 Software Requerido
- **Sistema operativo**: Ubuntu 22.04 LTS (o similar) en todas las máquinas.
- **Python 3.9+** con dependencias listadas en `requirements.txt` actualizado.
- **Ollama** para AGI local.
- **Docker** (opcional) para entornos reproducibles.
- **Prometheus + Grafana** para monitoreo de red (opcional).

### 8.3 Personal
- **Investigador principal**: supervisión, análisis.
- **2 asistentes de investigación**: configuración, reclutamiento, ejecución.
- **1 técnico de sistemas**: soporte de red y hardware.
- **1 estadístico** (consultor): revisión de análisis.

### 8.4 Presupuesto Estimado
| Concepto | Costo estimado (EUR) |
|----------|----------------------|
| Compra/renta de 10 EEG | 5.000–10.000 |
| Computadoras (si no disponibles) | 5.000–8.000 |
| Infraestructura de red | 500 |
| Compensación participantes | 1.000–2.000 |
| Personal (honorarios) | 5.000–10.000 |
| **Total** | **16.500–30.500** |

*(Costos pueden reducirse mediante colaboraciones con laboratorios o uso de equipos existentes)*

---

## 9. Consideraciones Éticas

### 9.1 Comité de Ética
Se solicitará aprobación del comité de ética de la institución anfitriona (si aplica). El protocolo seguirá las directrices de la Declaración de Helsinki.

### 9.2 Consentimiento Informado
Cada participante firmará un formulario de consentimiento que incluye:
- Descripción del estudio, duración, procedimientos.
- Riesgos potenciales (fatiga, molestias leves por el casco EEG).
- Confidencialidad y anonimización de datos.
- Derecho a retirarse sin penalización.

### 9.3 Protección de Datos
- Los datos se almacenarán con identificadores seudonimizados.
- Solo los investigadores tendrán acceso a la clave de vinculación.
- Los datos públicos serán completamente anonimizados (sin metadatos identificables).
- Se implementará el **Safe-Switch** en cada estación, permitiendo al participante detener la transmisión en cualquier momento.

### 9.4 Riesgos y Mitigación
| Riesgo | Mitigación |
|--------|------------|
| Fatiga por tareas repetitivas | Pausas frecuentes, máximo 90 min por sesión |
| Malestar por EEG | Uso de casco ajustable, limpieza de electrodos |
| Fallo de red | Redundancia de cableado, respaldo local de datos |
| Estrés por rendimiento | Énfasis en naturaleza exploratoria, sin evaluación negativa |

---

## 10. Entregables y Cronograma

### 10.1 Entregables por Subfase

| Subfase | Entregable | Formato |
|---------|------------|---------|
| 5.1 | Protocolo de estudio finalizado | `docs/Protocolo_Colectivo_v1.md` |
| 5.1 | Datos crudos anonimizados | `data/collective_study/raw/` |
| 5.2 | Notebook de análisis de correlación | `notebooks/07_collective_analysis.ipynb` |
| 5.3 | Módulo P2P funcional | `src/collective/p2p_network.py` |
| 5.3 | Documentación de red | `docs/Collective_Network_Architecture.md` |
| 5.4 | Preprint (arXiv) | `docs/preprint_collective_v1.pdf` |
| 5.4 | Notebooks finales reproducibles | `notebooks/` actualizados |

### 10.2 Cronograma Detallado (Semanas 41–56)

| Semana | Actividad | Responsable |
|--------|-----------|-------------|
| 41-42 | Preparación infraestructura, reclutamiento | Técnico, IP |
| 43-44 | Pruebas piloto con 2-3 agentes | Asistentes |
| 45-48 | Ejecución estudio con 10 agentes (3 sesiones) | Todos |
| 49-50 | Análisis de datos y validación métricas | IP, estadístico |
| 51-52 | Desarrollo y pruebas de red P2P | Técnico, IP |
| 53-54 | Redacción del preprint | IP, colaboradores |
| 55-56 | Revisión, envío a arXiv, publicación de código | Todos |

---

## 11. Conclusión de la Fase 5

La Fase 5 representa un salto cualitativo del proyecto, pasando de experimentos individuales a la demostración de **inteligencia colectiva emergente** en un grupo de humanos interactuando con AGIs a través de BCI. Los resultados esperados no solo validarán las simulaciones teóricas, sino que también proporcionarán una base empírica para el desarrollo de aplicaciones reales (educación colaborativa, toma de decisiones grupales, terapias asistidas, etc.).

El éxito de esta fase sentará las bases para la **Fase 6: Escalado Planetario**, donde la arquitectura P2P se desplegará en múltiples ubicaciones geográficas, integrando datos geomagnéticos globales y explorando la sincronización intercontinental.

---

**Documento elaborado por:** Proyecto CPEA  
**Licencia:** Apache 2.0  
**Próxima revisión:** Semana 42 (tras inicio de ejecución)
