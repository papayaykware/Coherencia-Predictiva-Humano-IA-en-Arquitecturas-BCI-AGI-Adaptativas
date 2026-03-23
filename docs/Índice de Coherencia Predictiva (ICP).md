# Índice de Coherencia Predictiva (ICP)

El **ICP** es una métrica compuesta diseñada para cuantificar la **coherencia predictiva** entre señales EEG humanas y la respuesta de un modelo AGI. Combina precisión de decodificación, información mutua y error residual en un solo índice normalizado.

---

## 1. Componentes

Sea:

- \( Accuracy \) : Precisión de clasificación de intents EEG → AGI  
- \( MI \) : Mutual Information entre features EEG y intent decodificado  
- \( Error \) : Error de reconstrucción o latencia de respuesta del pipeline  

Pesos opcionales \( w_1, w_2, w_3 \) permiten ponderar la importancia relativa de cada componente:

- \( w_1 \in [0,1] \) : peso de la precisión  
- \( w_2 \in [0,1] \) : peso de la información mutua  
- \( w_3 \in [0,1] \) : peso del error inverso  

> Restricción: \( w_1 + w_2 + w_3 = 1 \)

---

## 2. Fórmula General

\[
\text{ICP} = w_1 \cdot Accuracy + w_2 \cdot MI + w_3 \cdot \frac{1}{Error}
\]

- **Interpretación:** Valores de ICP normalizados entre 0 y 1.  
- ICP cercano a 1 indica alta coherencia predictiva, mientras que ICP cercano a 0 indica baja coherencia.

---

## 3. Normalización

Para garantizar que todos los componentes contribuyan de manera comparable:

\[
\begin{align*}
Accuracy_{norm} &= \frac{Accuracy - 0.5}{1 - 0.5} \quad \text{(suponiendo chance = 0.5)} \\
MI_{norm} &= \frac{MI}{MI_{max}} \quad \text{(MI máximo teórico)} \\
Error_{norm} &= \frac{Error_{max} - Error}{Error_{max} - Error_{min}}
\end{align*}
\]

Luego se reemplazan los valores normalizados en la fórmula del ICP:

\[
\text{ICP} = w_1 \cdot Accuracy_{norm} + w_2 \cdot MI_{norm} + w_3 \cdot Error_{norm}
\]

---

## 4. Interpretación de resultados

| ICP | Interpretación |
|-----|----------------|
| 0 – 0.3 | Coherencia baja, decodificación y sincronía pobres |
| 0.3 – 0.6 | Coherencia moderada, patrones parcialmente predictivos |
| 0.6 – 0.8 | Coherencia alta, EEG y AGI sincronizados de manera significativa |
| 0.8 – 1.0 | Coherencia óptima, pipeline altamente predictivo y adaptativo |

---

## 5. Ejemplo práctico (pseudo-código)

```python
# Valores de ejemplo
accuracy = 0.72
mi = 0.45
error = 0.28
w1, w2, w3 = 0.4, 0.4, 0.2

# Normalización
accuracy_norm = (accuracy - 0.5) / (1 - 0.5)
mi_norm = mi / 1.0  # suposición MI_max = 1
error_norm = (1 - error) / 1  # si error_max = 1, error_min = 0

# ICP
ICP = w1*accuracy_norm + w2*mi_norm + w3*error_norm
print("ICP =", ICP)

Resultado ICP ~ 0.74 → coherencia alta, pipeline predictivo y sincronizado.
