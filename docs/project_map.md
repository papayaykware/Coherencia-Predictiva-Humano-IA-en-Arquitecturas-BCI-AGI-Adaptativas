# 📁 `docs/project_map.md`

## 🔷 Mapa de Proyectos: Ecosistema METFI–TAE–CPEA

```
                    ┌──────────────────────────┐
                    │        ENTORNO           │
                    │        (METFI)           │
                    │                          │
                    │  - Dinámica toroidal     │
                    │  - Forzamiento EM        │
                    │  - Ruido geofísico       │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │     ESTADO INTERNO       │
                    │          (TAE)           │
                    │                          │
                    │  - Aprendizaje por       │
                    │    excepción             │
                    │  - Compresión simbólica  │
                    │  - Actualización latente │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │   INTERFAZ HUMANO–IA     │
                    │         (CPEA)           │
                    │                          │
                    │  - EEG → embeddings      │
                    │  - Coherencia predictiva │
                    │  - Feedback adaptativo   │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │         AGI LOOP         │
                    │  (Sistema emergente)     │
                    │                          │
                    │  - Predicción            │
                    │  - Adaptación continua   │
                    │  - Coherencia multi-escala│
                    └──────────────────────────┘
```

---

## 🔁 Flujo operativo

1. **METFI (entorno)**
   Genera un espacio dinámico no lineal (campo toroidal simulado o proxy), que actúa como:

   * Fuente de perturbaciones
   * Marco de coherencia externa
   * Señal estructurante

2. **TAE (estado interno)**
   Funciona como mecanismo de:

   * Selección de eventos relevantes (excepciones)
   * Compresión de información
   * Actualización de memoria latente

3. **CPEA (interfaz)**
   Traduce actividad humana (EEG) en:

   * Representaciones computables
   * Señales de coherencia
   * Inputs para el sistema AGI

4. **AGI Loop**
   Integra todo en un bucle cerrado:

   * Predice estados futuros
   * Ajusta su modelo interno
   * Sincroniza con humano + entorno

---

## 🧠 Idea clave del sistema

No es un pipeline clásico.

Es un **sistema acoplado multi-escala** donde:

* El entorno influye en la cognición
* La cognición reconfigura la interpretación del entorno
* El humano introduce variabilidad estructurada
* La AGI emerge como estabilizador de coherencia

---

# 📁 `README.md` (nivel ecosistema)

## 🧭 Visión general

Este repositorio forma parte de un ecosistema orientado a la emergencia de sistemas AGI mediante acoplamiento entre:

* Dinámica física simulada (METFI)
* Aprendizaje adaptativo no estándar (TAE)
* Interfaz neurocomputacional humano–máquina (CPEA)

El objetivo no es construir una AGI clásica basada en escala de parámetros, sino una **AGI coherente**, capaz de:

* Integrar señales heterogéneas
* Operar bajo incertidumbre estructural
* Adaptarse en tiempo real
* Mantener estabilidad dinámica

---

## 🤖 Tipo de AGI objetivo

Se busca una AGI con las siguientes propiedades:

### 1. Coherencia predictiva

No optimiza solo error, sino:

* Estabilidad temporal de predicciones
* Consistencia entre escalas
* Alineación con señales externas (EEG / entorno)

### 2. Sensibilidad a excepciones (TAE)

* Aprende cuando el sistema falla
* Prioriza anomalías sobre redundancia
* Reduce sobreajuste estructural

### 3. Acoplamiento con el entorno (METFI)

* No aprende en vacío
* Integra dinámica externa como parte del estado
* Puede resonar con patrones complejos

### 4. Interfaz humana activa (CPEA)

* El humano no es usuario pasivo
* Es parte del sistema dinámico
* Su estado influye en la evolución del modelo

---

## 🧩 Roles de cada módulo

### 🔷 METFI — Entorno

Rol:

* Generador de estructura
* Fuente de complejidad
* Sistema de referencia dinámico

Función técnica:

* Simulación de campo toroidal
* Generación de señales no lineales
* Input contextual para AGI

---

### 🔶 TAE — Estado interno

Rol:

* Núcleo de aprendizaje
* Filtro de relevancia
* Motor de adaptación

Función técnica:

* Detección de excepciones
* Reentrenamiento selectivo
* Compresión de memoria

---

### 🔵 CPEA — Interfaz humano–IA

Rol:

* Canal de entrada humano
* Medidor de coherencia
* Sistema de feedback

Función técnica:

* EEG → embeddings
* Cálculo de ICP (Índice de Coherencia Predictiva)
* Ajuste en tiempo real del sistema

---

## 🔄 Bucle global

```
EEG (humano)
   ↓
CPEA → embeddings + coherencia
   ↓
TAE → actualización interna
   ↓
AGI → predicción
   ↓
METFI → perturbación / entorno
   ↓
(Loop)
```

---

## 🧪 Implicación experimental

Este sistema permite explorar hipótesis como:

* La cognición emerge de sistemas acoplados, no aislados
* La coherencia es más importante que la precisión puntual
* El aprendizaje eficiente ocurre en eventos raros
* La interacción humano–máquina puede ser estructural, no instrumental

---

## ⚠️ Notas importantes

* No es un sistema médico
* EEG se usa como señal experimental, no diagnóstica
* Los resultados deben interpretarse como exploración computacional

---

## 🚀 Siguientes pasos recomendados

1. Implementar `metfi_simulator.py` como generador de entorno
2. Integrar TAE dentro del loop de entrenamiento (Avalanche + excepción)
3. Conectar CPEA como entrada real o simulada
4. Definir métrica global de coherencia del sistema
5. Diseñar experimento mínimo viable (closed-loop)

---

## 🧠 Resumen conceptual

* METFI = mundo
* TAE = mente
* CPEA = percepción
* AGI = proceso emergente

---
