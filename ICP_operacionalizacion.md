# Índice de Coherencia Predictiva (ICP): Operacionalización Práctica

## Definición Formal

El ICP se define como una combinación convexa de tres componentes que capturan diferentes aspectos de la coherencia humano-IA:

$$ICP = w_1 \cdot Acc + w_2 \cdot MI + w_3 \cdot (1 - E_{AGI})$$

Donde:
- **Acc**: Precisión de decodificación de intención motora
- **MI**: Información Mutua entre dinámica neuronal y representación interna de la AGI
- **E_{AGI}**: Error de la AGI en tarea específica
- **w_i**: Pesos normalizados (w₁ + w₂ + w₃ = 1)

## Implementación Práctica

### 1. Accuracy (Acc) - Decodificación de Intención Motora

**Definición operativa:** Capacidad del sistema para clasificar correctamente la intención del usuario a partir de EEG.

```python
# Implementación de referencia
def calcular_accuracy(y_true, y_pred):
    """
    Args:
        y_true: Etiquetas reales {0: izquierda, 1: derecha}
        y_pred: Etiquetas predichas por el clasificador EEG
    Returns:
        Acc: Precisión de clasificación [0, 1]
    """
    from sklearn.metrics import accuracy_score
    return accuracy_score(y_true, y_pred)
```

**Detalles técnicos:**
- **Ventana de análisis**: 2 segundos post-estímulo (0-2s)
- **Clases**: 2 (Motor Imagery izquierda/derecha)
- **Clasificador base**: Logistic Regression o EEGNet (para versión avanzada)
- **Validación**: Leave-one-session-out cross-validation
- **Chance level**: 50% (test binomial)

### 2. Mutual Information (MI) - Acoplamiento EEG-AGI

**Definición operativa:** Información mutua entre características EEG (en espacio de embedding) y la representación interna de la AGI.

```python
def calcular_mutual_information(eeg_features, agi_embeddings, bins=20):
    """
    Calcula MI entre features EEG y embeddings AGI.
    
    Args:
        eeg_features: Array (n_trials, n_eeg_features)
        agi_embeddings: Array (n_trials, n_agi_dim)
        bins: Número de bins para discretización
    
    Returns:
        MI: Información mutua normalizada [0, 1]
    """
    from sklearn.feature_selection import mutual_info_regression
    
    # Reducir dimensionalidad de AGI embeddings (PCA a 10 componentes)
    from sklearn.decomposition import PCA
    pca = PCA(n_components=min(10, agi_embeddings.shape[1]))
    agi_reduced = pca.fit_transform(agi_embeddings)
    
    # Calcular MI promedio entre cada feature EEG y componentes AGI
    mi_scores = []
    for i in range(agi_reduced.shape[1]):
        mi = mutual_info_regression(eeg_features, agi_reduced[:, i])
        mi_scores.append(np.mean(mi))
    
    # Normalizar por entropía máxima teórica
    max_mi = np.log2(bins)  # Para features discretizadas
    mi_normalized = np.mean(mi_scores) / max_mi
    
    return np.clip(mi_normalized, 0, 1)
```

**Detalles técnicos:**
- **Features EEG**: Potencia en bandas (mu: 8-12Hz, beta: 15-30Hz) en canales C3, Cz, C4
- **Embeddings AGI**: Última capa oculta del modelo de lenguaje (output antes de softmax)
- **Ventana temporal**: MI calculada sobre la ventana de respuesta de la AGI (0-500ms post-clasificación)

### 3. Error de AGI (E_AGI) - Precisión en Tarea Concreta

**Definición operativa:** Error de la AGI al predecir la dirección del movimiento imaginado, dada la representación EEG.

```python
def calcular_error_agi(true_direction, agi_prediction):
    """
    Calcula error de predicción de la AGI.
    
    Args:
        true_direction: Dirección real {0: izquierda, 1: derecha}
        agi_prediction: Probabilidad predicha por AGI para clase derecha [0,1]
    
    Returns:
        error: Error cuadrático medio [0, 1]
    """
    # Convertir dirección real a probabilidad (one-hot suave)
    true_prob = np.eye(2)[true_direction]
    
    # Calcular BCE (Binary Cross-Entropy)
    import torch.nn.functional as F
    import torch
    
    true_tensor = torch.tensor(true_prob)
    pred_tensor = torch.tensor([1-agi_prediction, agi_prediction])
    
    bce = F.binary_cross_entropy(pred_tensor, true_tensor)
    
    return bce.item()

# Error combinado para batch de trials
def calcular_error_agi_batch(y_true, y_pred_prob):
    """
    y_true: Array (n_trials,) con etiquetas 0/1
    y_pred_prob: Array (n_trials,) con probabilidad clase 1
    """
    from sklearn.metrics import log_loss
    return log_loss(y_true, y_pred_prob)
```

**Tarea concreta para AGI:**
- **Input**: Vector de características EEG procesado (features extraídos)
- **Output**: Probabilidad de que la intención sea "derecha" (vs "izquierda")
- **Modelo AGI**: Versión fine-tuned de TinyLLaMA o GPT-2 (para mantenerlo ligero)
- **Prompt template**:
```
"Basado en la siguiente actividad cerebral: [FEATURES_EEG],
¿el usuario está imaginando movimiento de mano izquierda o derecha?
Probabilidad de mano derecha:"
```

## Cálculo del ICP Integrado

```python
class IndiceCoherenciaPredictiva:
    def __init__(self, pesos=[0.4, 0.3, 0.3]):
        """
        Args:
            pesos: [w_acc, w_mi, w_error] con suma=1
        """
        self.w_acc, self.w_mi, self.w_error = pesos
        
    def calcular(self, y_true, y_pred_class, eeg_features, agi_embeddings, 
                 y_pred_prob_agi):
        """
        Calcula ICP completo para un bloque de trials.
        """
        # 1. Accuracy de clasificación EEG
        acc = accuracy_score(y_true, y_pred_class)
        
        # 2. Mutual Information EEG-AGI
        mi = calcular_mutual_information(eeg_features, agi_embeddings)
        
        # 3. Error de AGI
        error = calcular_error_agi_batch(y_true, y_pred_prob_agi)
        
        # 4. ICP ponderado
        icp = self.w_acc * acc + self.w_mi * mi + self.w_error * (1 - error)
        
        return {
            'icp': icp,
            'componentes': {
                'accuracy': acc,
                'mutual_info': mi,
                'agi_error': error,
                'agi_acierto': 1 - error
            },
            'pesos': {
                'w_acc': self.w_acc,
                'w_mi': self.w_mi,
                'w_error': self.w_error
            }
        }
```

## Interpretación del ICP

| Rango ICP | Interpretación | Implicación |
|-----------|----------------|-------------|
| 0.8 - 1.0 | Coherencia alta | Sistema adaptado, comunicación fluida |
| 0.6 - 0.8 | Coherencia moderada | Adaptación parcial, intervención humana necesaria |
| 0.4 - 0.6 | Coherencia baja | Desincronización, requiere reentrenamiento |
| < 0.4 | Coherencia nula | Sistema no funcional, reinicio necesario |

## Validación Estadística

Para comparar ICP entre condiciones (baseline vs adaptativo):
```python
from scipy import stats

def comparar_icp(icp_baseline, icp_adaptativo):
    """
    icp_X: arrays con ICP por sesión/sujeto
    """
    # t-test pareado (mismos sujetos)
    t_stat, p_valor = stats.ttest_rel(icp_adaptativo, icp_baseline)
    
    # Tamaño del efecto (Cohen's d)
    d = (np.mean(icp_adaptativo) - np.mean(icp_baseline)) / \
        np.std(np.concatenate([icp_adaptativo, icp_baseline]))
    
    return {
        't_statistic': t_stat,
        'p_value': p_valor,
        'cohens_d': d,
        'significativo': p_valor < 0.05
    }
```
```

## **2. Protocolo Experimental Detallado**

### **`docs/experiment_protocol.md`**

```markdown
# Protocolo Experimental: Validación de Coherencia Predictiva EEG-AGI

## 1. Resumen del Experimento

**Objetivo:** Demostrar que un pipeline adaptativo BCI-AGI mejora el Índice de Coherencia Predictiva (ICP) comparado con un pipeline baseline sin adaptación.

**Hipótesis:** El ICP en condición adaptativa será significativamente mayor (p < 0.05) que en condición baseline, con un tamaño del efecto d > 0.5.

## 2. Diseño Experimental

### 2.1 Paradigma
- **Tarea**: Motor Imagery (izquierda vs derecha)
- **Diseño**: Intra-sujeto, medidas repetidas
- **Condiciones**: 
  - **Baseline**: Clasificador fijo, AGI sin fine-tuning
  - **Adaptativa**: Clasificador actualizado online, AGI fine-tuned por bloques

### 2.2 Participantes
- **N**: 10 sujetos sanos (5 femenino, 5 masculino)
- **Edad**: 18-35 años
- **Criterios inclusión**: Diestros, sin experiencia previa en BCI
- **Criterios exclusión**: Enfermedades neurológicas, medicación psicoactiva

### 2.3 Sesiones
- **Sesiones por sujeto**: 4 (1 entrenamiento + 3 experimentales)
- **Duración por sesión**: 60 minutos
- **Total sesiones**: 40 sesiones

## 3. Adquisición de Datos

### 3.1 Hardware
- **Equipo EEG**: Muse 2016 (4 canales: TP9, AF7, AF8, TP10) o Emotiv EPOC+
- **Frecuencia muestreo**: 256 Hz
- **Impedancias**: < 5 kΩ

### 3.2 Protocolo de adquisición

```
SESIÓN TÍPICA (60 min):
├── Preparación (15 min)
│   ├── Colocación de electrodos
│   └── Verificación de señal
├── Bloque entrenamiento (15 min)
│   ├── 20 trials con feedback visual
│   └── Calibración inicial
├── Bloque experimental 1 (10 min)
│   ├── 40 trials en condición baseline
│   └── Registro continuo EEG
├── Break (2 min)
├── Bloque experimental 2 (10 min)
│   ├── 40 trials en condición adaptativa
│   └── Registro continuo EEG
└── Cierre (8 min)
    ├── Cuestionario NASA-TLX
    └── Entrevista cualitativa
```

### 3.3 Estructura del Trial

```
TRIAL INDIVIDUAL (8 segundos):
├── Fixation cross (2s): Preparación
├── Cue visual (1s): Flecha izquierda/derecha
├── Motor Imagery (4s): Imaginar movimiento
│   └── EEG procesado en ventanas deslizantes
├── Respuesta AGI (0.5s): Predicción mostrada
└── Feedback (0.5s): Acierto/Error visual
```

## 4. Pipeline de Procesamiento

### 4.1 Preprocesamiento EEG (online)

```python
config_preprocesamiento = {
    'filtro_pasa_banda': [8, 30],  # Hz
    'filtro_elimina_ruido': [48, 52],  # Hz (eliminar 50Hz)
    'rechazo_artefactos': 'ICA',
    'ventaneo': 'deslizante 1s con solapamiento 0.5s',
    'referencia': 'promedio de canales'
}
```

### 4.2 Extracción de Características

```python
config_features = {
    'bandas_frecuencia': {
        'mu': [8, 12],
        'beta_bajo': [13, 20],
        'beta_alto': [21, 30]
    },
    'método': 'FFT + Welch',
    'resolución_frecuencial': 0.5,  # Hz
    'canales_interés': ['C3', 'C4']  # equivalentes en el dispositivo
}
```

### 4.3 Clasificación EEG

```python
config_clasificador = {
    'tipo': 'EEGNet v4',
    'input_shape': (4, 256),  # canales x muestras (1s a 256Hz)
    'capas': [
        'Conv2D(8, (1,64)) + BatchNorm',
        'DepthwiseConv2D(2, (4,1))',
        'SeparableConv2D(16, (1,16))',
        'Clasificación: Dense(2, softmax)'
    ],
    'optimizador': 'Adam(lr=0.001)',
    'loss': 'categorical_crossentropy'
}
```

### 4.4 Modelo AGI

```python
config_agi = {
    'modelo_base': 'TinyLLaMA-1.1B',  # o GPT-2 small
    'fine_tuning': {
        'baseline': 'sin fine-tuning',
        'adaptativo': 'fine-tuning cada 20 trials'
    },
    'prompt_template': """
    Instrucción: Basado en la actividad cerebral, predice la dirección imaginada.
    
    Características EEG:
    - Potencia mu (8-12Hz): {mu_power_C3:.3f} µV² (C3), {mu_power_C4:.3f} µV² (C4)
    - Potencia beta (15-30Hz): {beta_power_C3:.3f} µV² (C3), {beta_power_C4:.3f} µV² (C4)
    - Asimetría C3-C4: {asymmetry:.3f}
    
    Probabilidad de mano derecha:
    """
}
```

## 5. Variables Dependientes

### 5.1 Variables Primarias
1. **ICP global** (Índice de Coherencia Predictiva)
2. **Accuracy de clasificación EEG** (por bloque)
3. **Mutual Information EEG-AGI** (por trial)

### 5.2 Variables Secundarias
1. **Tiempo de reacción del sistema** (ms)
2. **NASA-TLX** (carga de trabajo subjetiva)
3. **Tasa de adaptación** (mejora ICP/trial)

## 6. Análisis Estadístico

### 6.1 Power Analysis
```python
from statsmodels.stats.power import TTestPower

# Cálculo de N necesario
analysis = TTestPower()
n_required = analysis.solve_power(
    effect_size=0.8,  # Esperamos efecto grande
    power=0.8,
    alpha=0.05,
    alternative='two-sided'
)
print(f"Sujetos necesarios: {np.ceil(n_required)}")
# Resultado: n ≈ 15 (usamos 10 para estudio piloto)
```

### 6.2 Tests Estadísticos

```r
# Modelo lineal mixto en R (lme4)
library(lme4)
library(lmerTest)

modelo <- lmer(ICP ~ Condicion + (1|Sujeto) + (1|Sesion), 
               data = datos)
summary(modelo)

# ANOVA de medidas repetidas
anova_resultado <- aov(ICP ~ Condicion + Error(Sujeto/Condicion), 
                       data = datos)
summary(anova_resultado)
```

### 6.3 Criterios de Éxito

El experimento se considera exitoso si:
1. **Criterio principal**: ICP_adaptativo > ICP_baseline con p < 0.05
2. **Criterio secundario**: Mejora sostenida > 15% en los últimos 20 trials
3. **Criterio exploratorio**: Correlación significativa entre ICP y NASA-TLX

## 7. Materiales Suplementarios

### 7.1 Dataset
- **Fuente primaria**: PhysioNet Motor Imagery (109 sujetos)
- **Formato**: .edf (European Data Format)
- **Estructura**:
  ```
  physionet_mi/
  ├── sujeto_001/
  │   ├── sesion_1.edf  (baseline)
  │   ├── sesion_2.edf  (adaptativo)
  │   └── labels.csv
  └── ...
  ```

### 7.2 Scripts de Descarga
```python
# download_physionet.py
import wget
import os

urls = [
    "https://physionet.org/files/eegmmidb/1.0.0/S001/",
    # ... más URLs
]

for url in urls:
    wget.download(url)
```

## 8. Timeline Experimental

```
SEMANA 1-2: Preparación
├── Configurar hardware EEG
├── Implementar pipeline baseline
└── Pruebas piloto (n=2)

SEMANA 3-6: Adquisición
├── Reclutar participantes
├── Sesiones experimentales (3/sujeto)
└── Monitoreo de calidad

SEMANA 7-8: Análisis
├── Preprocesamiento batch
├── Análisis estadístico
└── Visualización de resultados

SEMANA 9-10: Escritura
├── Preprint
├── Repositorio documentado
└── Preparación de figuras
```

## 9. Reproducibilidad

Todos los análisis serán completamente reproducibles mediante:
- **Docker** con entorno fijo
- **Scripts de análisis** versionados
- **Semillas aleatorias** fijadas (seed=42)
- **Logs detallados** de cada ejecución

```bash
# Comando para reproducir análisis completo
docker run -v $(pwd)/data:/data cpea:latest \
  python run_experiment.py \
    --config configs/experiment.yaml \
    --seed 42 \
    --output /results
```
```
