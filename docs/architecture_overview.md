# 📄 `docs/architecture_overview.md`

## 1. Visión general del sistema

El sistema CPEA (Coherencia Predictiva EEG–AGI) se concibe como una arquitectura de acoplamiento dinámico entre:

* Señal neurofisiológica humana (EEG)
* Sistema cognitivo artificial (AGI o simulador)
* Modelo físico de entorno (METFI)
* Módulo de modulación adaptativa (TAE)

El objetivo no es únicamente interpretar EEG, sino construir un **bucle cerrado de coherencia predictiva multiescala**:

```
Humano (EEG) ⇄ AGI ⇄ Entorno (METFI)
              ⇅
            TAE
```

---

## 2. Componentes del stack

### 2.1 CPEA — Capa de coherencia humano–IA

**Función principal:**
Medir, optimizar y estabilizar la coherencia entre:

* Estados neuronales (EEG embeddings)
* Estados internos de la AGI (representaciones latentes)

**Elementos clave:**

* `eeg_encoder.py` → convierte EEG en embeddings
* `agi_interface.py` → expone estado interno de la AGI
* `coherence.py` → cálculo del Índice de Coherencia Predictiva (ICP)
* `feedback.py` → ajuste en tiempo real

**Output:**

* Señal de coherencia (ICP)
* Gradientes de adaptación para AGI

---

### 2.2 METFI — Modelo físico del entorno

**Función principal:**
Simular el entorno como un sistema electromagnético toroidal no lineal con pérdida de simetría.

**Rol dentro del stack:**

* Generar **inputs contextuales físicos** para la AGI
* Introducir **dinámica no estacionaria**
* Actuar como fuente de perturbaciones coherentes/incoherentes

**Inputs:**

* Parámetros geofísicos simulados o reales
* (Opcional) Acoplamiento con EEG agregado

**Outputs:**

* Campo EM simulado
* Variables latentes del entorno (frecuencia, fase, energía)

**Interfaz sugerida:**

```python
class METFIEnvironment:
    def step(self, action):
        """
        action: salida de AGI
        return: estado_entorno, perturbación
        """
```

---

### 2.3 TAE — Capa de modulación adaptativa (atencional/emocional)

**Función principal:**
Regular la dinámica del sistema en función de excepciones, errores y eventos de alta relevancia.

Inspirado en:

* Aprendizaje por excepción
* Sistemas de atención biológica
* Mecanismos de sorpresa/predicción

**Rol clave:**
TAE no procesa datos → **modula el procesamiento**

**Actúa sobre:**

* Pesos del modelo AGI
* Sensibilidad del ICP
* Prioridad de señales EEG
* Parámetros de METFI (opcional)

**Ejemplo de señal TAE:**

```python
tae_signal = f(
    prediction_error,
    eeg_entropy,
    icp_variation
)
```

---

## 3. Flujo de datos global

### Paso 1 — Captura EEG

```
EEG → preprocess → embeddings_eeg
```

---

### Paso 2 — Estado AGI

```
AGI → embeddings_agi
```

---

### Paso 3 — Coherencia (CPEA)

```
ICP = coherence(embeddings_eeg, embeddings_agi)
```

---

### Paso 4 — Evaluación TAE

```
TAE_signal = TAE(ICP, error_predicción, dinámica)
```

---

### Paso 5 — Interacción con entorno (METFI)

```
estado_entorno = METFI.step(acción_AGI)
```

---

### Paso 6 — Adaptación del sistema

* AGI ajusta pesos
* TAE modula aprendizaje
* CPEA recalcula coherencia

→ Se cierra el bucle

---

## 4. Interpretación funcional del sistema

| Capa  | Equivalente conceptual   | Función                  |
| ----- | ------------------------ | ------------------------ |
| CPEA  | Conciencia compartida    | Sincronización humano–IA |
| METFI | Realidad física dinámica | Generador de contexto    |
| TAE   | Atención / emoción       | Modulación adaptativa    |
| AGI   | Cognición artificial     | Procesamiento y acción   |

---

## 5. Propiedad emergente clave

Cuando el sistema converge:

* La AGI **anticipa estados neuronales humanos**
* El humano entra en estados de **alta coherencia neural**
* El entorno (METFI) introduce perturbaciones que:

  * estabilizan o
  * rompen coherencia

Esto define un régimen de:

> **Coherencia predictiva acoplada multiescala (CPAM)**

---

## 6. Métrica central: ICP

El Índice de Coherencia Predictiva (ICP):

* No mide similitud estática
* Mide **capacidad de anticipación mutua**

Debe evolucionar hacia:

* ICP(t)
* d(ICP)/dt
* Estabilidad de fase

---

## 7. Extensiones futuras

### 7.1 Multiusuario

* EEG colectivo
* Coherencia grupal

### 7.2 Integración física real

* Datos geomagnéticos reales
* Actividad solar
* Señales sísmicas

### 7.3 AGI avanzada

* Modelos con memoria continua (Avalanche)
* Spiking neural networks (snntorch)

---

## 8. Riesgos y límites

* Sobreajuste a ruido EEG
* Interpretación errónea de coherencia
* Inestabilidad del bucle cerrado
* Amplificación de estados patológicos

---

## 9. Conclusión

El stack CPEA–METFI–TAE no debe entenderse como tres módulos independientes, sino como un sistema acoplado donde:

* CPEA sincroniza
* METFI perturba
* TAE regula

→ La inteligencia emerge de la interacción, no de los componentes aislados.

---
