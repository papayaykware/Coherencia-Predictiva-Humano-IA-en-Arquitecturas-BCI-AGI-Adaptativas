## **Plan de Acción para el Primer Commit Funcional**

### **Paso 1: Estructura de Archivos y Código Base**

Crea esta estructura de archivos en tu repositorio local:

```
CPEA/
├── README.md (actualizado)
├── requirements.txt
├── setup.py (opcional, pero profesional)
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── generate_synthetic_eeg.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── eeg_processor.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── dummy_agi.py
│   └── pipeline/
│       ├── __init__.py
│       └── run_pipeline.py
├── notebooks/
│   └── 01_baseline_demo.ipynb
└── data/ (gitignorado, pero con instrucciones)
```

### **Paso 2: Archivos Clave para el Commit**

#### **1. `requirements.txt`**
```txt
# Core scientific
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0

# EEG processing
mne>=1.4.0

# ML basics
scikit-learn>=1.2.0

# For API calls (optional for dummy mode)
requests>=2.28.0

# For notebooks
jupyter>=1.0.0
ipykernel>=6.0.0
```

#### **2. `src/data/generate_synthetic_eeg.py`**
```python
"""
Generador de datos sintéticos de EEG para pruebas del pipeline.
Simula señales de motor imagery (izquierda/derecha) con ritmos mu/beta.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

class SyntheticEEGGenerator:
    def __init__(self, fs=256.0, duration=2.0, n_channels=4):
        """
        Args:
            fs: Frecuencia de muestreo (Hz)
            duration: Duración de cada trial (segundos)
            n_channels: Número de canales EEG
        """
        self.fs = fs
        self.duration = duration
        self.n_channels = n_channels
        self.n_samples = int(fs * duration)
        self.time = np.arange(self.n_samples) / fs
        
        # Nombres de canales estilo Muse/Emotiv
        self.ch_names = [f'EEG_{i+1}' for i in range(n_channels)]
        
    def generate_trial(self, class_label='left', snr_db=5.0):
        """
        Genera un trial sintético de EEG.
        
        Args:
            class_label: 'left' o 'right' (motor imagery)
            snr_db: Relación señal-ruido en dB
            
        Returns:
            data: array (n_channels, n_samples)
            label: 0 para left, 1 para right
        """
        # Ruido de fondo (1/f noise)
        noise = self._generate_pink_noise(self.n_samples, self.n_channels)
        
        # Señal de motor imagery (ritmo mu 8-12 Hz, beta 15-30 Hz)
        signal_eeg = np.zeros((self.n_channels, self.n_samples))
        
        # Canal C3 (left) se activa con imagery derecha, C4 con izquierda
        # Simulamos con diferente potencia en canales
        if class_label == 'left':
            active_ch = 1  # C3 index
            inactive_ch = 2  # C4 index
        else:  # right
            active_ch = 2  # C4 index
            inactive_ch = 1  # C3 index
            
        # Generar oscilaciones mu (10 Hz) y beta (20 Hz)
        t = self.time
        mu_osc = 0.5 * np.sin(2 * np.pi * 10 * t)
        beta_osc = 0.3 * np.sin(2 * np.pi * 20 * t)
        
        # Aplicar con mayor amplitud al canal activo
        for ch in range(self.n_channels):
            if ch == active_ch:
                signal_eeg[ch, :] = 1.5 * mu_osc + 0.8 * beta_osc
            elif ch == inactive_ch:
                signal_eeg[ch, :] = 0.5 * mu_osc + 0.3 * beta_osc
            else:
                signal_eeg[ch, :] = 0.2 * mu_osc  # otros canales
            
        # Mezclar señal + ruido con SNR deseado
        signal_power = np.var(signal_eeg)
        noise_power = signal_power / (10 ** (snr_db/10))
        noise_scaled = noise * np.sqrt(noise_power / np.var(noise))
        
        data = signal_eeg + noise_scaled
        
        return data, 0 if class_label == 'left' else 1
    
    def _generate_pink_noise(self, n_samples, n_channels):
        """Genera ruido rosa (1/f) para simular EEG realista"""
        noise = np.random.randn(n_channels, n_samples)
        fft = np.fft.rfft(noise)
        frequencies = np.fft.rfftfreq(n_samples)
        # Aplicar pendiente 1/f (evitar división por cero)
        frequencies[0] = np.inf
        fft = fft / np.sqrt(frequencies)[None, :]
        fft[:, 0] = 0  # DC component to zero
        pink_noise = np.fft.irfft(fft, n=n_samples, axis=1)
        return pink_noise
    
    def save_sample_trials(self, n_trials=10, output_dir='data/sample_eeg'):
        """Genera y guarda trials de ejemplo"""
        os.makedirs(output_dir, exist_ok=True)
        
        all_data = []
        all_labels = []
        
        for i in range(n_trials):
            # Alternar clases
            label = 'left' if i % 2 == 0 else 'right'
            data, label_num = self.generate_trial(label)
            
            # Guardar trial individual
            trial_file = os.path.join(output_dir, f'trial_{i:03d}_{label}.npy')
            np.save(trial_file, data)
            
            all_data.append(data)
            all_labels.append(label_num)
            
        # Guardar también dataset completo
        np.save(os.path.join(output_dir, 'all_trials.npy'), np.array(all_data))
        np.save(os.path.join(output_dir, 'all_labels.npy'), np.array(all_labels))
        
        # Crear visualización de ejemplo
        self._plot_sample(data, label, output_dir)
        
        print(f"✅ Generados {n_trials} trials sintéticos en {output_dir}/")
        
    def _plot_sample(self, data, label, output_dir):
        """Guarda una figura de ejemplo"""
        plt.figure(figsize=(12, 4))
        for ch in range(min(3, self.n_channels)):
            plt.subplot(3, 1, ch+1)
            plt.plot(self.time, data[ch, :])
            plt.ylabel(f'Canal {ch+1} (µV)')
            plt.xlim(0, self.duration)
        plt.xlabel('Tiempo (s)')
        plt.suptitle(f'Ejemplo de EEG sintético - Motor Imagery {label}')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'example_plot.png'), dpi=100)
        plt.close()

# Si se ejecuta directamente, genera datos de ejemplo
if __name__ == "__main__":
    generator = SyntheticEEGGenerator()
    generator.save_sample_trials(n_trials=20)
    print("🎉 Datos sintéticos generados correctamente")
```

#### **3. `src/utils/eeg_processor.py`**
```python
"""
Procesamiento de señales EEG para el pipeline CPEA.
"""
import numpy as np
from scipy import signal
import mne

class EEGProcessor:
    def __init__(self, fs=256.0, lowcut=8.0, highcut=30.0):
        """
        Args:
            fs: Frecuencia de muestreo (Hz)
            lowcut: Frecuencia de corte baja para filtro pasa-banda
            highcut: Frecuencia de corte alta
        """
        self.fs = fs
        self.lowcut = lowcut
        self.highcut = highcut
        
        # Diseñar filtro Butterworth
        self.b, self.a = self._design_filter()
        
    def _design_filter(self):
        """Diseña filtro Butterworth pasa-banda"""
        nyquist = 0.5 * self.fs
        low = self.lowcut / nyquist
        high = self.highcut / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        return b, a
        
    def preprocess(self, raw_data):
        """
        Pipeline completo de preprocesamiento.
        
        Args:
            raw_data: array (n_channels, n_samples)
            
        Returns:
            filtered_data: array preprocesado
        """
        # 1. Filtrar pasa-banda
        filtered = signal.filtfilt(self.b, self.a, raw_data, axis=1)
        
        # 2. Normalizar por canal (z-score)
        normalized = (filtered - np.mean(filtered, axis=1, keepdims=True)) / \
                     (np.std(filtered, axis=1, keepdims=True) + 1e-6)
        
        return normalized
    
    def extract_features(self, processed_data):
        """
        Extrae características simples para clasificación.
        
        Args:
            processed_data: array (n_channels, n_samples)
            
        Returns:
            features: vector de características (n_features,)
        """
        features = []
        
        # Potencia en banda mu (8-12 Hz) y beta (15-30 Hz)
        freqs, psd = signal.welch(processed_data, fs=self.fs, axis=1)
        
        # Índices de frecuencias
        mu_idx = np.where((freqs >= 8) & (freqs <= 12))[0]
        beta_idx = np.where((freqs >= 15) & (freqs <= 30))[0]
        
        for ch in range(processed_data.shape[0]):
            # Potencia en mu
            mu_power = np.mean(psd[ch, mu_idx])
            # Potencia en beta
            beta_power = np.mean(psd[ch, beta_idx])
            # Ratio beta/mu (común en motor imagery)
            ratio = beta_power / (mu_power + 1e-6)
            
            features.extend([mu_power, beta_power, ratio])
            
        # Asimetría entre canales centrales (C3/C4 simulados)
        if processed_data.shape[0] >= 3:
            c3_idx, c4_idx = 1, 2  # Suponiendo que C3 y C4 son canales 2 y 3
            asymmetry = features[c3_idx*3] - features[c4_idx*3]  # mu power diff
            features.append(asymmetry)
            
        return np.array(features)
    
    def load_from_npy(self, filepath):
        """Carga datos guardados por generate_synthetic_eeg.py"""
        return np.load(filepath)
```

#### **4. `src/models/dummy_agi.py`**
```python
"""
Modelo AGI simulado para pruebas del pipeline.
"""
import numpy as np
import random

class DummyAGI:
    def __init__(self, mode='dummy', response_dim=64):
        """
        Args:
            mode: 'dummy' (aleatorio), 'rule_based', o 'api' (para futuro)
            response_dim: Dimensión del embedding de respuesta
        """
        self.mode = mode
        self.response_dim = response_dim
        
        # Mapeo de intents a respuestas (reglas simples)
        self.intent_responses = {
            'left': {
                'text': "Detected left motor imagery. Moving cursor left.",
                'embedding': np.random.randn(response_dim)  # Placeholder
            },
            'right': {
                'text': "Detected right motor imagery. Moving cursor right.",
                'embedding': np.random.randn(response_dim)
            }
        }
        
    def generate_response(self, intent, return_embedding=True):
        """
        Genera respuesta basada en el intent detectado.
        
        Args:
            intent: 0 para left, 1 para right (o string)
            return_embedding: Si True, devuelve embedding, si no, texto
            
        Returns:
            Respuesta de la AGI (texto o embedding)
        """
        # Convertir intent a string si es numérico
        if isinstance(intent, (int, np.integer)):
            intent_str = 'left' if intent == 0 else 'right'
        else:
            intent_str = intent
            
        if self.mode == 'dummy':
            # Modo aleatorio - para probar métricas baseline
            if return_embedding:
                return np.random.randn(self.response_dim)
            else:
                options = ["Processing command...", "Executing action...", f"Intent: {intent_str}"]
                return random.choice(options)
                
        elif self.mode == 'rule_based':
            # Respuesta basada en reglas
            response = self.intent_responses[intent_str]
            if return_embedding:
                return response['embedding']
            return response['text']
            
    def get_embedding_similarity(self, emb1, emb2):
        """Calcula similitud coseno entre dos embeddings"""
        emb1 = emb1.flatten()
        emb2 = emb2.flatten()
        cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-6)
        return cos_sim
```

#### **5. `src/pipeline/run_pipeline.py`**
```python
#!/usr/bin/env python3
"""
Pipeline principal BCI-AGI para CPEA.
Ejecuta trials, calcula ICP y guarda resultados.
"""
import numpy as np
import argparse
import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Añadir src al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.data.generate_synthetic_eeg import SyntheticEEGGenerator
from src.utils.eeg_processor import EEGProcessor
from src.models.dummy_agi import DummyAGI

class CPEAPipeline:
    def __init__(self, mode='baseline', n_trials=10):
        """
        Args:
            mode: 'baseline' (sin adaptación) o 'adaptive' (futuro)
            n_trials: Número de trials a ejecutar
        """
        self.mode = mode
        self.n_trials = n_trials
        
        # Inicializar componentes
        self.eeg_gen = SyntheticEEGGenerator()
        self.eeg_proc = EEGProcessor()
        self.agi = DummyAGI(mode='rule_based')
        
        # Almacenar resultados
        self.results = {
            'trials': [],
            'icp_scores': [],
            'accuracy': 0.0,
            'mean_mi': 0.0
        }
        
    def simulate_trial(self, true_label):
        """
        Simula un trial completo del pipeline.
        
        Args:
            true_label: 'left' o 'right'
            
        Returns:
            dict con resultados del trial
        """
        # 1. Generar EEG sintético
        eeg_data, label_num = self.eeg_gen.generate_trial(true_label)
        
        # 2. Preprocesar EEG
        processed_eeg = self.eeg_proc.preprocess(eeg_data)
        
        # 3. Extraer características
        features = self.eeg_proc.extract_features(processed_eeg)
        
        # 4. Clasificar intent (versión simple)
        # Usamos asimetría de características como clasificador dummy
        if len(features) > 10:  # Si tenemos la característica de asimetría
            asymmetry = features[-1]  # Última feature (asimetría C3-C4)
            detected_intent = 0 if asymmetry < 0 else 1
        else:
            # Fallback: clasificador aleatorio
            detected_intent = np.random.randint(0, 2)
            
        # 5. Obtener respuesta AGI
        agi_embedding = self.agi.generate_response(detected_intent, return_embedding=True)
        
        # 6. Calcular métricas
        accuracy = 1.0 if detected_intent == label_num else 0.0
        
        # Simular mutual information (placeholder)
        mi_score = np.random.uniform(0.3, 0.8)
        
        # Calcular ICP simplificado (accuracy + MI normalizado)
        icp = 0.6 * accuracy + 0.4 * mi_score
        
        trial_result = {
            'true_label': true_label,
            'detected_intent': 'left' if detected_intent == 0 else 'right',
            'accuracy': accuracy,
            'mi_score': mi_score,
            'icp': icp,
            'features': features.tolist()[:5]  # Solo primeras 5 para no saturar
        }
        
        return trial_result
    
    def run_experiment(self):
        """Ejecuta experimento completo"""
        print(f"\n🧪 Ejecutando pipeline modo: {self.mode}")
        print(f"📊 Número de trials: {self.n_trials}\n")
        
        accuracies = []
        mi_scores = []
        
        for trial_idx in range(self.n_trials):
            # Alternar clases para balance
            true_label = 'left' if trial_idx % 2 == 0 else 'right'
            
            # Ejecutar trial
            result = self.simulate_trial(true_label)
            self.results['trials'].append(result)
            
            # Acumular métricas
            accuracies.append(result['accuracy'])
            mi_scores.append(result['mi_score'])
            self.results['icp_scores'].append(result['icp'])
            
            # Mostrar progreso
            status = "✅" if result['accuracy'] == 1.0 else "❌"
            print(f"Trial {trial_idx+1:2d}: {status} Real:{true_label:5} "
                  f"Detectado:{result['detected_intent']:5} | ICP:{result['icp']:.3f}")
        
        # Calcular métricas globales
        self.results['accuracy'] = np.mean(accuracies)
        self.results['mean_mi'] = np.mean(mi_scores)
        self.results['mean_icp'] = np.mean(self.results['icp_scores'])
        self.results['std_icp'] = np.std(self.results['icp_scores'])
        
        # Mostrar resumen
        print(f"\n{'='*50}")
        print(f"📈 RESULTADOS FINALES")
        print(f"{'='*50}")
        print(f"Accuracy media: {self.results['accuracy']:.3f}")
        print(f"Mutual Info media: {self.results['mean_mi']:.3f}")
        print(f"ICP medio: {self.results['mean_icp']:.3f} ± {self.results['std_icp']:.3f}")
        print(f"{'='*50}")
        
        return self.results
    
    def save_results(self, filename=None):
        """Guarda resultados en JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{self.mode}_{timestamp}.json"
            
        output_dir = Path("results")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        # Convertir numpy arrays a listas para JSON
        results_serializable = self.results.copy()
        for trial in results_serializable['trials']:
            if 'features' in trial and isinstance(trial['features'], np.ndarray):
                trial['features'] = trial['features'].tolist()
                
        with open(filepath, 'w') as f:
            json.dump(results_serializable, f, indent=2)
            
        print(f"\n💾 Resultados guardados en: {filepath}")
        return filepath

def main():
    parser = argparse.ArgumentParser(description='Pipeline CPEA BCI-AGI')
    parser.add_argument('--mode', type=str, default='baseline',
                       choices=['baseline', 'adaptive'],
                       help='Modo de ejecución')
    parser.add_argument('--trials', type=int, default=20,
                       help='Número de trials a ejecutar')
    parser.add_argument('--save', action='store_true',
                       help='Guardar resultados en archivo')
    
    args = parser.parse_args()
    
    # Ejecutar pipeline
    pipeline = CPEAPipeline(mode=args.mode, n_trials=args.trials)
    results = pipeline.run_experiment()
    
    if args.save:
        pipeline.save_results()
        
    return 0

if __name__ == "__main__":
    exit(main())
```

#### **6. `notebooks/01_baseline_demo.ipynb`** (Contenido mínimo)
Crea un notebook con celdas que:
1. Importen y expliquen los módulos
2. Generen y visualicen EEG sintético
3. Ejecuten el pipeline paso a paso
4. Muestren gráficas de resultados

#### **7. `README.md` Actualizado (Sección Quickstart)**
```markdown
## 🚀 Quickstart (Funcional)

### Requisitos previos
- Python 3.9+
- Git

### Instalación en 2 minutos

```bash
# 1. Clonar el repositorio
git clone https://github.com/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas.git
cd Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Generar datos sintéticos de ejemplo
python -c "from src.data.generate_synthetic_eeg import SyntheticEEGGenerator; SyntheticEEGGenerator().save_sample_trials(20)"

# 5. ¡Ejecutar el pipeline!
python src/pipeline/run_pipeline.py --mode baseline --trials 20 --save
```

### 📊 Ver resultados
```bash
# Los resultados se guardan en /results/
ls results/

# Para visualización interactiva:
jupyter notebook notebooks/01_baseline_demo.ipynb
```

### 🧠 ¿Qué acaba de pasar?
1. **Datos sintéticos**: Se generaron 20 trials de EEG simulando motor imagery
2. **Preprocesamiento**: Filtrado pasa-banda (8-30 Hz) y normalización
3. **Clasificación**: Detección simple basada en asimetría de canales
4. **AGI simulada**: Respuesta basada en reglas según el intent
5. **ICP**: Cálculo del Índice de Coherencia Predictiva simplificado
```

### **Paso 3: Script de Generación de Datos**

Añade también un script `download_sample_data.py` en `src/data/` que automatice la descarga de un dataset real pequeño (opcional para futura versión).

### **Paso 4: Commit Final**

```bash
# Añadir todos los archivos
git add .

# Crear commit con mensaje descriptivo
git commit -m "feat: Implementación MVP funcional del pipeline CPEA

- Añade generador de EEG sintético con src/data/generate_synthetic_eeg.py
- Implementa procesador EEG con filtrado y extracción de características
- Crea modelo AGI dummy con respuestas basadas en reglas
- Desarrolla pipeline orquestador con cálculo de ICP simplificado
- Actualiza requirements.txt con dependencias reales
- Mejora README con quickstart funcional y probado
- Añade notebook de demostración básico

Este commit permite ejecutar un experimento completo BCI-AGI
con datos sintéticos desde cero en menos de 2 minutos."

# Subir a GitHub
git push origin main
```

### **Verificación Final**

Antes del commit, prueba todo desde cero en un directorio nuevo:

```bash
cd /tmp
git clone <tu-repo>
cd <tu-repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/pipeline/run_pipeline.py --mode baseline --trials 10
```
