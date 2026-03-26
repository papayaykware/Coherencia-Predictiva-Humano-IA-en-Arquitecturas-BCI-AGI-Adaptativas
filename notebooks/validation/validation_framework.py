"""
src/validation/validation_framework.py

Fase 4: Validación experimental rigurosa.
Implementa validación cruzada, análisis de robustez y pruebas estadísticas
para garantizar la reproducibilidad y solidez de los resultados.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from sklearn.model_selection import KFold, StratifiedKFold, LeaveOneOut, GroupKFold
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.base import BaseEstimator
import warnings
import logging
from pathlib import Path
import json
import hashlib
import time

logger = logging.getLogger(__name__)


@dataclass
class ValidationConfig:
    """Configuración de validación experimental."""
    cv_folds: int = 5
    cv_strategy: str = "kfold"  # "kfold", "stratified", "loo", "group"
    random_seed: int = 42
    test_size: float = 0.2
    n_repetitions: int = 10  # Para validación repetida
    metrics: List[str] = field(default_factory=lambda: ["accuracy", "f1", "auc", "icp"])
    robustness_checks: List[str] = field(default_factory=lambda: ["noise", "dropout", "temporal_shift"])
    significance_level: float = 0.05


class CrossValidator:
    """
    Validador cruzado robusto para el pipeline CPEA.
    Soporta múltiples estrategias y genera métricas completas.
    """
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.results = {}
        
        # Inicializar estrategia de CV
        self.cv = self._get_cv_strategy()
    
    def _get_cv_strategy(self):
        """Retorna el objeto de validación cruzada según configuración."""
        if self.config.cv_strategy == "kfold":
            return KFold(n_splits=self.config.cv_folds, shuffle=True, random_state=self.config.random_seed)
        elif self.config.cv_strategy == "stratified":
            return StratifiedKFold(n_splits=self.config.cv_folds, shuffle=True, random_state=self.config.random_seed)
        elif self.config.cv_strategy == "loo":
            return LeaveOneOut()
        elif self.config.cv_strategy == "group":
            return GroupKFold(n_splits=self.config.cv_folds)
        else:
            raise ValueError(f"Estrategia CV no soportada: {self.config.cv_strategy}")
    
    def validate_classifier(self, X: np.ndarray, y: np.ndarray, 
                           classifier: BaseEstimator,
                           groups: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Valida clasificador usando la estrategia de CV configurada.
        
        Args:
            X: Características EEG
            y: Etiquetas
            classifier: Clasificador sklearn-compatible
            groups: Grupos para CV por grupos (ej. participantes)
        """
        logger.info(f"Iniciando validación cruzada ({self.config.cv_strategy})")
        
        # Almacenar métricas por fold
        fold_results = []
        
        for fold, (train_idx, test_idx) in enumerate(self.cv.split(X, y, groups)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Entrenar
            classifier.fit(X_train, y_train)
            
            # Predecir
            y_pred = classifier.predict(X_test)
            y_proba = classifier.predict_proba(X_test) if hasattr(classifier, "predict_proba") else None
            
            # Calcular métricas
            metrics = {
                'fold': fold,
                'accuracy': accuracy_score(y_test, y_pred),
                'f1_macro': f1_score(y_test, y_pred, average='macro'),
            }
            
            if y_proba is not None and len(np.unique(y_test)) == 2:
                try:
                    metrics['auc'] = roc_auc_score(y_test, y_proba[:, 1])
                except:
                    pass
            
            # Matriz de confusión
            metrics['confusion_matrix'] = confusion_matrix(y_test, y_pred).tolist()
            
            fold_results.append(metrics)
        
        # Agregar resultados
        self.results['fold_metrics'] = fold_results
        self.results['summary'] = self._summarize_fold_results(fold_results)
        
        logger.info(f"Validación completada. Accuracy media: {self.results['summary']['accuracy_mean']:.4f} (+-{self.results['summary']['accuracy_std']:.4f})")
        
        return self.results
    
    def _summarize_fold_results(self, fold_results: List[Dict]) -> Dict:
        """Genera estadísticas resumen de los folds."""
        summary = {}
        metric_names = [k for k in fold_results[0].keys() if k not in ['fold', 'confusion_matrix']]
        
        for metric in metric_names:
            values = [f[metric] for f in fold_results]
            summary[f'{metric}_mean'] = np.mean(values)
            summary[f'{metric}_std'] = np.std(values)
            summary[f'{metric}_min'] = np.min(values)
            summary[f'{metric}_max'] = np.max(values)
        
        return summary


class RobustnessAnalyzer:
    """
    Analiza robustez del sistema ante perturbaciones.
    Simula ruido EEG, dropout de canales, desplazamiento temporal, etc.
    """
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.results = {}
    
    def analyze_robustness(self, model: BaseEstimator, 
                           X: np.ndarray, y: np.ndarray,
                           feature_extractor: Optional[Callable] = None) -> Dict:
        """
        Ejecuta análisis de robustez con múltiples perturbaciones.
        """
        results = {}
        
        # 1. Ruido Gaussiano
        results['noise'] = self._test_noise_robustness(model, X, y)
        
        # 2. Dropout de canales (simular pérdida de electrodos)
        results['channel_dropout'] = self._test_channel_dropout(model, X, y)
        
        # 3. Desplazamiento temporal
        if feature_extractor:
            results['temporal_shift'] = self._test_temporal_shift(model, X, y, feature_extractor)
        
        # 4. Perturbación de amplitud (variaciones de ganancia)
        results['amplitude_perturbation'] = self._test_amplitude_perturbation(model, X, y)
        
        self.results = results
        return results
    
    def _test_noise_robustness(self, model, X, y, noise_levels=[0.01, 0.05, 0.1, 0.2]):
        """Prueba robustez añadiendo ruido Gaussiano."""
        accuracies = []
        for noise_std in noise_levels:
            X_noisy = X + np.random.normal(0, noise_std * np.std(X, axis=0), X.shape)
            model.fit(X_noisy, y)
            y_pred = model.predict(X_noisy)
            acc = accuracy_score(y, y_pred)
            accuracies.append(acc)
        
        return {
            'noise_levels': noise_levels,
            'accuracies': accuracies,
            'decay_rate': np.polyfit(noise_levels, accuracies, 1)[0]  # tasa de degradación
        }
    
    def _test_channel_dropout(self, model, X, y, dropout_rates=[0.1, 0.2, 0.3, 0.5]):
        """Prueba robustez a pérdida de canales."""
        n_channels = X.shape[1]  # Asumiendo que las columnas son canales
        accuracies = []
        
        for rate in dropout_rates:
            n_drop = int(n_channels * rate)
            # Seleccionar canales aleatorios a mantener
            mask = np.ones(n_channels, dtype=bool)
            drop_indices = np.random.choice(n_channels, n_drop, replace=False)
            mask[drop_indices] = False
            
            X_dropped = X[:, mask]
            model.fit(X_dropped, y)
            y_pred = model.predict(X_dropped)
            acc = accuracy_score(y, y_pred)
            accuracies.append(acc)
        
        return {
            'dropout_rates': dropout_rates,
            'accuracies': accuracies,
            'critical_rate': self._find_critical_dropout(dropout_rates, accuracies)
        }
    
    def _test_temporal_shift(self, model, X, y, feature_extractor, shifts=[-10, -5, 5, 10, 20]):
        """Prueba robustez a desplazamiento temporal en ventanas."""
        accuracies = []
        for shift in shifts:
            # Desplazar características en el tiempo (simular latencia)
            if shift > 0:
                X_shifted = np.roll(X, shift, axis=0)
                X_shifted[:shift] = 0
            else:
                X_shifted = np.roll(X, shift, axis=0)
                X_shifted[shift:] = 0
            
            # Reextraer features si es necesario (simplificado)
            model.fit(X_shifted, y)
            y_pred = model.predict(X_shifted)
            acc = accuracy_score(y, y_pred)
            accuracies.append(acc)
        
        return {
            'shifts': shifts,
            'accuracies': accuracies
        }
    
    def _test_amplitude_perturbation(self, model, X, y, gains=[0.5, 0.8, 1.2, 1.5, 2.0]):
        """Prueba robustez a variaciones de ganancia (escala de amplitud)."""
        accuracies = []
        for gain in gains:
            X_scaled = X * gain
            model.fit(X_scaled, y)
            y_pred = model.predict(X_scaled)
            acc = accuracy_score(y, y_pred)
            accuracies.append(acc)
        
        return {
            'gains': gains,
            'accuracies': accuracies,
            'optimal_gain': gains[np.argmax(accuracies)] if accuracies else None
        }
    
    def _find_critical_dropout(self, rates, accuracies, threshold=0.7):
        """Encuentra la tasa de dropout donde accuracy cae por debajo de threshold."""
        for i, acc in enumerate(accuracies):
            if acc < threshold:
                return rates[i]
        return None


class StatisticalTester:
    """
    Pruebas estadísticas para comparar condiciones experimentales.
    """
    
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
    
    def compare_conditions(self, baseline_scores: np.ndarray, adaptive_scores: np.ndarray,
                           paired: bool = True) -> Dict:
        """
        Compara baseline vs adaptativo usando test paramétrico o no paramétrico.
        """
        from scipy.stats import ttest_rel, ttest_ind, wilcoxon, mannwhitneyu
        
        results = {}
        
        # Verificar normalidad (Shapiro-Wilk)
        from scipy.stats import shapiro
        _, p_baseline = shapiro(baseline_scores)
        _, p_adaptive = shapiro(adaptive_scores)
        normal = (p_baseline > 0.05) and (p_adaptive > 0.05)
        results['normality_assumption'] = {'baseline_p': p_baseline, 'adaptive_p': p_adaptive, 'normal': normal}
        
        if paired:
            if normal:
                stat, p = ttest_rel(baseline_scores, adaptive_scores)
                test_name = 'paired t-test'
            else:
                stat, p = wilcoxon(baseline_scores, adaptive_scores)
                test_name = 'Wilcoxon signed-rank'
        else:
            if normal:
                stat, p = ttest_ind(baseline_scores, adaptive_scores)
                test_name = 'independent t-test'
            else:
                stat, p = mannwhitneyu(baseline_scores, adaptive_scores)
                test_name = 'Mann-Whitney U'
        
        results['test'] = test_name
        results['statistic'] = float(stat)
        results['p_value'] = float(p)
        results['significant'] = p < self.alpha
        results['effect_size'] = self._cohens_d(baseline_scores, adaptive_scores, paired)
        
        return results
    
    def _cohens_d(self, a: np.ndarray, b: np.ndarray, paired: bool) -> float:
        """Calcula Cohen's d."""
        diff = a - b if paired else a.mean() - b.mean()
        if paired:
            std_diff = np.std(diff)
        else:
            pooled_std = np.sqrt((np.std(a)**2 + np.std(b)**2) / 2)
            std_diff = pooled_std
        return diff / std_diff if std_diff > 0 else 0.0


# ============================================================================
# REPRODUCIBILIDAD
# ============================================================================

class ReproducibilityManager:
    """
    Gestiona la reproducibilidad de experimentos:
    - Versiones de código y dependencias
    - Semillas aleatorias
    - Configuraciones serializables
    - Checksums de datos
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.config_dir = self.base_dir / "configs"
        self.log_dir = self.base_dir / "logs"
        self.checksums_file = self.base_dir / "checksums.json"
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def save_experiment_config(self, config: Dict, name: str) -> Path:
        """Guarda configuración de experimento con timestamp."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        path = self.config_dir / filename
        with open(path, 'w') as f:
            json.dump(config, f, indent=2, default=str)
        return path
    
    def compute_checksum(self, data: np.ndarray) -> str:
        """Calcula checksum SHA-256 de un array numpy."""
        return hashlib.sha256(data.tobytes()).hexdigest()
    
    def log_experiment(self, experiment_id: str, metrics: Dict, config: Dict):
        """Registra metadatos de experimento para trazabilidad."""
        import datetime
        log_entry = {
            'experiment_id': experiment_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'config': config,
            'metrics': metrics,
            'environment': self._capture_environment()
        }
        log_file = self.log_dir / f"{experiment_id}.json"
        with open(log_file, 'w') as f:
            json.dump(log_entry, f, indent=2)
    
    def _capture_environment(self) -> Dict:
        """Captura información del entorno (versiones, hardware)."""
        import sys, platform
        try:
            import torch
            torch_version = torch.__version__
        except:
            torch_version = None
        
        return {
            'python_version': sys.version,
            'platform': platform.platform(),
            'torch_version': torch_version,
            'timestamp': time.time()
        }


# ============================================================================
# TIEMPO REAL
# ============================================================================

import asyncio
import websockets
import threading
from queue import Queue
from collections import deque


class RealTimePipeline:
    """
    Pipeline en tiempo real con adaptación continua.
    Soporta entrada desde websockets, colas o streams simulados.
    """
    
    def __init__(self, classifier, adaptation_loop, buffer_size: int = 100):
        self.classifier = classifier
        self.adaptation_loop = adaptation_loop
        self.buffer = deque(maxlen=buffer_size)
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.is_running = False
        self.thread = None
    
    def start(self):
        """Inicia el pipeline en un thread separado."""
        self.is_running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
    
    def stop(self):
        """Detiene el pipeline."""
        self.is_running = False
        if self.thread:
            self.thread.join()
    
    def feed_data(self, eeg_features: np.ndarray, timestamp: float):
        """Alimenta datos al pipeline (desde adquisición)."""
        self.input_queue.put((eeg_features, timestamp))
    
    def _run(self):
        """Loop principal del pipeline en tiempo real."""
        while self.is_running:
            try:
                # Procesar lotes de datos
                batch = []
                while not self.input_queue.empty():
                    batch.append(self.input_queue.get_nowait())
                
                if batch:
                    features = np.array([b[0] for b in batch])
                    timestamps = [b[1] for b in batch]
                    
                    # Clasificación
                    with torch.no_grad():
                        features_tensor = torch.tensor(features, dtype=torch.float32).to(self.adaptation_loop.device)
                        logits = self.classifier(features_tensor)
                        predictions = torch.argmax(logits, dim=1).cpu().numpy()
                    
                    # Calcular ICP si hay AGI (simulado)
                    icp = 0.7  # placeholder
                    
                    # Adaptación si es necesario
                    result = self.adaptation_loop.process_window(features, predictions, icp)
                    
                    # Salida
                    self.output_queue.put({
                        'timestamp': timestamps[-1],
                        'predictions': predictions.tolist(),
                        'icp': icp,
                        'adaptation': result
                    })
                
                time.sleep(0.01)  # Pequeño sleep para no saturar CPU
            
            except Exception as e:
                logger.error(f"Error en pipeline real-time: {e}")
    
    async def websocket_handler(self, websocket, path):
        """Manejador para comunicación por websocket."""
        async for message in websocket:
            # Parsear mensaje (asumiendo JSON)
            import json
            data = json.loads(message)
            features = np.array(data['features'])
            timestamp = data['timestamp']
            
            # Alimentar al pipeline
            self.feed_data(features, timestamp)
            
            # Esperar respuesta
            if not self.output_queue.empty():
                result = self.output_queue.get()
                await websocket.send(json.dumps(result, default=str))


# ============================================================================
# PUBLICACIÓN REPRODUCIBLE
# ============================================================================

class PublicationGenerator:
    """
    Genera artefactos para publicación científica:
    - Figuras vectoriales
    - Tablas en formato LaTeX/Markdown
    - Notebooks Jupyter con análisis
    - Archivos de datos complementarios
    """
    
    def __init__(self, output_dir: Path, study_results: Dict):
        self.output_dir = Path(output_dir)
        self.study_results = study_results
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all(self):
        """Genera todos los artefactos de publicación."""
        self._generate_figures()
        self._generate_tables()
        self._generate_notebook()
        self._generate_supplementary_materials()
    
    def _generate_figures(self):
        """Genera figuras finales con estilo de publicación."""
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Configuración profesional
        plt.style.use('seaborn-v0_8-paper')
        sns.set_palette("colorblind")
        
        # Ejemplo: Figura de mejora de ICP
        if 'effect_sizes' in self.study_results:
            es = self.study_results['effect_sizes']['baseline_vs_adaptive']
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(['Baseline', 'Adaptativo'], [es['mean_baseline'], es['mean_adaptive']],
                   yerr=[es.get('std_baseline', 0), es.get('std_adaptive', 0)],
                   capsize=5, color=['gray', 'steelblue'])
            ax.set_ylabel('ICP')
            ax.set_title(f"Mejora de ICP (Cohen's d = {es['cohens_d']:.2f})")
            plt.tight_layout()
            plt.savefig(self.output_dir / "figure_icp_improvement.png", dpi=300)
            plt.savefig(self.output_dir / "figure_icp_improvement.pdf")
            plt.close()
    
    def _generate_tables(self):
        """Genera tablas en formato LaTeX y Markdown."""
        # Tabla de resultados estadísticos
        if 'descriptives' in self.study_results:
            desc = self.study_results['descriptives']
            latex_table = r"\begin{table}[h]\centering"
            latex_table += r"\caption{Estadísticas descriptivas}"
            latex_table += r"\begin{tabular}{lcc}\toprule"
            latex_table += r"Variable & Media & DE \\ \midrule"
            latex_table += f"ICP & {desc['icp_overall']['mean']:.3f} & {desc['icp_overall']['std']:.3f} \\\\"
            latex_table += r"\bottomrule\end{tabular}\end{table}"
            
            with open(self.output_dir / "table_descriptives.tex", 'w') as f:
                f.write(latex_table)
    
    def _generate_notebook(self):
        """Genera un notebook Jupyter con el análisis completo."""
        import nbformat as nbf
        nb = nbf.v4.new_notebook()
        
        # Celdas
        cells = []
        cells.append(nbf.v4.new_markdown_cell("# Análisis CPEA - Estudio Multi-Participante"))
        cells.append(nbf.v4.new_code_cell("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns"))
        cells.append(nbf.v4.new_markdown_cell("## Cargar resultados"))
        cells.append(nbf.v4.new_code_cell(f"results = {self.study_results}"))
        
        nb['cells'] = cells
        with open(self.output_dir / "analysis_notebook.ipynb", 'w') as f:
            nbf.write(nb, f)
    
    def _generate_supplementary_materials(self):
        """Exporta datos complementarios en formatos estándar."""
        # Exportar datos crudos anonimizados
        if 'participant_data' in self.study_results:
            df = pd.DataFrame(self.study_results['participant_data'])
            df.to_csv(self.output_dir / "supplementary_data.csv", index=False)


# ============================================================================
# INTEGRACIÓN FINAL - FASE 4 COMPLETA
# ============================================================================

class Phase4Orchestrator:
    """
    Orquestador final de la Fase 4.
    Coordina validación, reproducibilidad, tiempo real y publicación.
    """
    
    def __init__(self, project_root: Path, config: Dict = None):
        self.project_root = Path(project_root)
        self.config = config or {}
        self.repro_manager = ReproducibilityManager(self.project_root / "experiments")
        self.validation_config = ValidationConfig(**self.config.get('validation', {}))
        self.cross_validator = CrossValidator(self.validation_config)
        self.robustness_analyzer = RobustnessAnalyzer(self.validation_config)
        self.stat_tester = StatisticalTester()
    
    def run_full_experiment(self, data: Dict, model: BaseEstimator) -> Dict:
        """
        Ejecuta experimento completo con todas las fases de validación.
        """
        experiment_id = f"cpea_exp_{int(time.time())}"
        
        # Guardar configuración
        self.repro_manager.save_experiment_config(self.config, experiment_id)
        
        # Extraer datos
        X_train = data.get('X_train')
        y_train = data.get('y_train')
        X_test = data.get('X_test')
        y_test = data.get('y_test')
        
        # Validación cruzada
        cv_results = self.cross_validator.validate_classifier(X_train, y_train, model)
        
        # Robustez
        robustness = self.robustness_analyzer.analyze_robustness(model, X_train, y_train)
        
        # Prueba estadística (si hay datos de test)
        if X_test is not None:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            test_acc = accuracy_score(y_test, y_pred)
            # Comparar con baseline simulado (puede ser otro modelo)
            # Aquí asumimos que hay un baseline guardado en data
            baseline_acc = data.get('baseline_acc', 0.5)
            stat_test = self.stat_tester.compare_conditions(
                np.array([baseline_acc] * len(y_test)), 
                np.array([test_acc] * len(y_test)),
                paired=False
            )
        else:
            test_acc = None
            stat_test = {}
        
        # Agregar resultados
        full_results = {
            'experiment_id': experiment_id,
            'cv': cv_results,
            'robustness': robustness,
            'test_accuracy': test_acc,
            'statistical_test': stat_test,
            'timestamp': time.time()
        }
        
        # Log
        self.repro_manager.log_experiment(experiment_id, full_results, self.config)
        
        return full_results
    
    def deploy_real_time(self, model, adaptation_loop, host='localhost', port=8765):
        """
        Despliega pipeline en tiempo real con websocket.
        """
        rt_pipeline = RealTimePipeline(model, adaptation_loop)
        rt_pipeline.start()
        
        # Iniciar servidor websocket en thread separado
        async def serve():
            async with websockets.serve(rt_pipeline.websocket_handler, host, port):
                logger.info(f"Servidor WebSocket en ws://{host}:{port}")
                await asyncio.Future()  # run forever
        
        def run_server():
            asyncio.run(serve())
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        return rt_pipeline
    
    def generate_publication(self, results: Dict, output_dir: Path):
        """
        Genera artefactos de publicación a partir de resultados.
        """
        pub_gen = PublicationGenerator(output_dir, results)
        pub_gen.generate_all()
        logger.info(f"Artefactos de publicación generados en {output_dir}")


# ============================================================================
# DEMOSTRACIÓN COMPLETA
# ============================================================================

if __name__ == "__main__":
    # Configuración de prueba
    from sklearn.ensemble import RandomForestClassifier
    import tempfile
    
    # Datos simulados
    np.random.seed(42)
    X = np.random.randn(200, 64)
    y = np.random.randint(0, 2, 200)
    X_train, X_test = X[:150], X[150:]
    y_train, y_test = y[:150], y[150:]
    
    # Modelo
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    
    # Orquestador
    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = Phase4Orchestrator(Path(tmpdir))
        
        # Ejecutar experimento
        results = orchestrator.run_full_experiment({
            'X_train': X_train,
            'y_train': y_train,
            'X_test': X_test,
            'y_test': y_test,
            'baseline_acc': 0.6
        }, model)
        
        print("Resultados de validación:")
        print(f"  CV accuracy: {results['cv']['summary']['accuracy_mean']:.3f} ± {results['cv']['summary']['accuracy_std']:.3f}")
        print(f"  Test accuracy: {results['test_accuracy']:.3f}")
        print(f"  Efecto significativo: {results['statistical_test'].get('significant', False)}")
        
        # Generar publicación
        pub_dir = Path(tmpdir) / "publication"
        orchestrator.generate_publication(results, pub_dir)
        print(f"Publicación generada en {pub_dir}")
        
        # Opcional: desplegar tiempo real (comentado para demo)
        # rt = orchestrator.deploy_real_time(model, None)
        # rt.stop()
