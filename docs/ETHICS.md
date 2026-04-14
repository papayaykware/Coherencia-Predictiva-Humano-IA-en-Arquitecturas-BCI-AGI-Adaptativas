# 📄 `ETHICS.md` — CPEA (BCI–AGI Predictive Coherence System)

## 1. Propósito del documento

Este documento define los principios, límites operativos y salvaguardas del sistema **CPEA (Coherencia Predictiva EEG–AGI)**, un framework experimental orientado a:

* Procesamiento de señales EEG.
* Modelado de coherencia predictiva.
* Integración con sistemas de aprendizaje adaptativo tipo AGI.

El sistema es **experimental, no clínico y no certificado**.

---

## 2. Naturaleza del sistema

CPEA debe entenderse como:

* Un sistema de **investigación computacional**.
* Un entorno de simulación de acoplamiento:

  * Señal neuronal (EEG)
  * Modelo predictivo (AGI)
* Un framework de exploración de dinámicas de coherencia.

**No es:**

* Un dispositivo médico.
* Un sistema de diagnóstico.
* Un sistema de intervención terapéutica.

---

## 3. Límites de uso

### 3.1 Uso permitido

* Investigación académica.
* Prototipado de interfaces BCI.
* Simulación de modelos cognitivos.
* Exploración de aprendizaje continuo.

### 3.2 Uso restringido

Queda explícitamente prohibido:

* Uso en diagnóstico de condiciones neurológicas.
* Toma de decisiones clínicas.
* Sustitución de profesionales sanitarios.
* Uso en contextos críticos (militar, sanitario, seguridad) sin validación formal.

---

## 4. Riesgos asociados

### 4.1 Interpretación errónea de EEG

El EEG es una señal:

* Altamente ruidosa.
* No estacionaria.
* Dependiente del contexto (fatiga, entorno, artefactos).

**Riesgo clave:**

> Inferir estados cognitivos o emocionales de forma determinista a partir de patrones ambiguos.

Esto puede inducir:

* Falsos positivos (detección inexistente).
* Falsos negativos (no detección).
* Sobreinterpretación semántica de señales estadísticas.

---

### 4.2 Adaptación no controlada del sistema

El uso de:

* Aprendizaje continuo (continual learning)
* Modelos adaptativos online
* Feedback cerrado EEG → AGI → EEG

puede generar:

* Deriva de modelo (*model drift*).
* Sobreajuste a patrones individuales no representativos.
* Amplificación de ruido como señal válida.

---

### 4.3 Acoplamiento cognitivo no deseado

En sistemas BCI adaptativos:

* El usuario puede modificar su señal inconscientemente.
* El sistema puede reforzar patrones subóptimos.

Esto introduce un bucle:

```
EEG → modelo → feedback → EEG
```

**Riesgo emergente:**

* Estabilización de estados no deseados.
* Sesgos cognitivos inducidos por el sistema.

---

### 4.4 Riesgos de privacidad

El EEG puede contener:

* Patrones biométricos únicos.
* Información potencial sobre estados cognitivos.

Riesgos:

* Reidentificación.
* Uso indebido de datos neuronales.
* Inferencias no autorizadas.

---

## 5. Principios de uso responsable

### 5.1 Supervisión humana obligatoria

Cualquier uso del sistema debe incluir:

* Supervisión por un operador humano cualificado.
* Capacidad de interrupción inmediata del sistema.

---

### 5.2 Transparencia del modelo

El sistema debe:

* Registrar decisiones del modelo.
* Permitir trazabilidad (logs, embeddings, outputs).
* Evitar cajas negras opacas en contextos sensibles.

---

### 5.3 Minimización de daño

Se prioriza:

* Seguridad sobre rendimiento.
* Robustez sobre complejidad.
* Interpretabilidad sobre optimización extrema.

---

### 5.4 Consentimiento informado

En caso de uso con sujetos humanos:

* Debe existir consentimiento explícito.
* Debe explicarse:

  * Naturaleza experimental.
  * Riesgos potenciales.
  * Limitaciones del sistema.

---

### 5.5 No autonomía crítica

El sistema **no debe operar de forma autónoma** en:

* Entornos clínicos.
* Sistemas de decisión crítica.
* Contextos donde errores impliquen daño físico o psicológico.

---

## 6. Requisitos técnicos de seguridad

### 6.1 Control de adaptación

Implementar:

* Límites en la actualización de pesos.
* Regularización (EWC, replay buffers).
* Detección de deriva.

---

### 6.2 Validación continua

* Evaluación periódica del modelo.
* Separación clara entre:

  * Entrenamiento
  * Validación
  * Uso

---

### 6.3 Gestión de datos

* Anonimización de datos EEG.
* Almacenamiento seguro.
* Control de acceso.

---

### 6.4 Modo seguro (*safe mode*)

El sistema debe poder:

* Desactivar adaptación online.
* Operar en modo solo inferencia.
* Reiniciar a estado base.

---

## 7. Prohibición de uso clínico

Este sistema:

* **No está aprobado por ningún comité ético clínico.**
* **No cumple normativa médica (ej. MDR, FDA).**

Por tanto:

> Queda prohibido su uso en diagnóstico, tratamiento o prevención de enfermedades sin aprobación ética y regulatoria explícita.

---

## 8. Marco ético extendido (CPEA–TAE–METFI)

Desde una perspectiva de sistemas complejos:

* El CPEA no solo procesa datos → **co-evoluciona con el usuario**.
* Esto implica responsabilidad sobre:

  * Dinámica cognitiva inducida.
  * Estructuras de aprendizaje emergentes.

Principio clave:

> “Todo sistema adaptativo que interactúa con la cognición humana modifica, en algún grado, el espacio de estados del propio sujeto.”

Por tanto:

* La ética no es externa al sistema.
* Es una **restricción dinámica del espacio de aprendizaje**.

---

## 9. Descargo de responsabilidad

Este software se proporciona “tal cual”, sin garantías de:

* Exactitud.
* Fiabilidad.
* Aplicabilidad en contextos reales.

Los autores no se responsabilizan de:

* Uso indebido.
* Interpretaciones erróneas.
* Consecuencias derivadas de su implementación.

---

## 10. Recomendación final

Si este sistema evoluciona hacia:

* Uso con humanos reales
* Integración hardware BCI
* Aplicaciones cognitivas avanzadas

Se recomienda:

* Evaluación por comité ético independiente.
* Auditoría técnica externa.
* Publicación transparente de resultados.

---
