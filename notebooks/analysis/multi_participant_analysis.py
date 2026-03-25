"""
src/analysis/multi_participant_analysis.py

Fase 3: Escalado a múltiples participantes y análisis estadístico avanzado.
Diseñado para ser interpretable por AGIs y humanos.

Funcionalidades:
1. Gestión de cohortes de participantes
2. Análisis de varianza multinivel (ANOVA mixto)
3. Modelos lineales mixtos (LMM) para efectos aleatorios
4. Análisis de poder estadístico y tamaño de efecto
5. Visualizaciones científicas avanzadas
6. Exportación a formatos interoperables (JSON, HDF5, ONNX)
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any, Union
from collections import defaultdict
import logging
import json
import pickle
from pathlib import Path
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# Estadística y modelado
import scipy.stats as stats
from scipy.stats import f_oneway, ttest_rel, pearsonr, spearmanr
from scipy.spatial.distance import pdist, squareform
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm, ols
from statsmodels.stats.power import FTestAnovaPower, TTestPower
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pingouin as pg  # Estadística elegante para AGIs

# Machine learning para análisis
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Visualización científica
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Logging estructurado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# MODELOS DE DATOS
# ============================================================================

@dataclass
class ParticipantData:
    """Estructura de datos para un participante individual."""
    participant_id: str
    session_data: Dict[str, Any] = field(default_factory=dict)
    icp_history: List[float] = field(default_factory=list)
    classification_accuracies: List[float] = field(default_factory=list)
    adaptation_events: List[Dict] = field(default_factory=list)
    demographics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_session(self, session_id: str, data: Dict[str, Any]):
        """Añade datos de una sesión experimental."""
        self.session_data[session_id] = data
        if 'icp_values' in data:
            self.icp_history.extend(data['icp_values'])
        if 'accuracies' in data:
            self.classification_accuracies.extend(data['accuracies'])
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumen estadístico del participante."""
        return {
            'participant_id': self.participant_id,
            'n_sessions': len(self.session_data),
            'mean_icp': np.mean(self.icp_history) if self.icp_history else None,
            'std_icp': np.std(self.icp_history) if self.icp_history else None,
            'mean_accuracy': np.mean(self.classification_accuracies) if self.classification_accuracies else None,
            'n_adaptations': len(self.adaptation_events),
            **self.demographics
        }


@dataclass
class ExperimentalCohort:
    """Cohorte completa de participantes para análisis multi-sujeto."""
    name: str
    participants: Dict[str, ParticipantData] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_participant(self, participant: ParticipantData):
        """Añade un participante a la cohorte."""
        self.participants[participant.participant_id] = participant
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convierte todos los datos a DataFrame para análisis estadístico."""
        rows = []
        for pid, pdata in self.participants.items():
            summary = pdata.get_summary()
            rows.append(summary)
        return pd.DataFrame(rows)
    
    def get_long_format(self) -> pd.DataFrame:
        """
        Convierte a formato largo para modelos mixtos.
        Cada fila es una observación por sesión/ventana.
        """
        rows = []
        for pid, pdata in self.participants.items():
            for session_id, session_data in pdata.session_data.items():
                if 'icp_values' in session_data:
                    for window_idx, icp in enumerate(session_data['icp_values']):
                        rows.append({
                            'participant_id': pid,
                            'session': session_id,
                            'window': window_idx,
                            'icp': icp,
                            'condition': session_data.get('condition', 'baseline'),
                            'adaptation_applied': session_data.get('adaptation_applied', False)
                        })
        return pd.DataFrame(rows)


# ============================================================================
# ANALIZADOR ESTADÍSTICO AVANZADO
# ============================================================================

class AdvancedStatisticalAnalyzer:
    """
    Analizador estadístico para estudios multi-participante.
    Implementa métodos rigurosos para inferencia en CPEA.
    """
    
    def __init__(self, cohort: ExperimentalCohort, alpha: float = 0.05):
        """
        Args:
            cohort: Cohorte experimental
            alpha: Nivel de significancia
        """
        self.cohort = cohort
        self.alpha = alpha
        self.results = {}
        self.figures = {}
        
        # Preparar datos
        self.df_summary = cohort.to_dataframe()
        self.df_long = cohort.get_long_format()
        
        logger.info(f"Analizador inicializado con {len(cohort.participants)} participantes")
        logger.info(f"Total observaciones en formato largo: {len(self.df_long)}")
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Ejecuta análisis completo incluyendo:
        - Estadísticas descriptivas
        - ANOVA mixto
        - Modelos lineales mixtos
        - Análisis de correlación
        - Tamaños de efecto
        - Análisis de poder
        """
        logger.info("=" * 60)
        logger.info("INICIANDO ANÁLISIS ESTADÍSTICO AVANZADO")
        logger.info("=" * 60)
        
        # 1. Estadísticas descriptivas
        self.results['descriptives'] = self._descriptive_statistics()
        
        # 2. ANOVA mixto (entre-sujetos y dentro-sujetos)
        if len(self.df_long) > 0:
            self.results['mixed_anova'] = self._mixed_anova()
        
        # 3. Modelos lineales mixtos (LMM)
        self.results['linear_mixed_models'] = self._linear_mixed_models()
        
        # 4. Análisis de correlación ICP vs métricas
        self.results['correlations'] = self._correlation_analysis()
        
        # 5. Tamaños de efecto (Cohen's d, eta-squared)
        self.results['effect_sizes'] = self._effect_size_analysis()
        
        # 6. Análisis de poder post-hoc
        self.results['power_analysis'] = self._posthoc_power_analysis()
        
        # 7. Análisis de clusters por perfil de respuesta
        self.results['participant_clusters'] = self._participant_clustering()
        
        logger.info("Análisis completo finalizado")
        return self.results
    
    def _descriptive_statistics(self) -> Dict[str, Any]:
        """Estadísticas descriptivas por grupo y condición."""
        stats_dict = {
            'n_participants': len(self.cohort.participants),
            'n_sessions_total': sum(len(p.session_data) for p in self.cohort.participants.values()),
            'icp_overall': {
                'mean': self.df_long['icp'].mean() if len(self.df_long) > 0 else None,
                'std': self.df_long['icp'].std() if len(self.df_long) > 0 else None,
                'min': self.df_long['icp'].min() if len(self.df_long) > 0 else None,
                'max': self.df_long['icp'].max() if len(self.df_long) > 0 else None,
                'quartiles': self.df_long['icp'].quantile([0.25, 0.5, 0.75]).to_dict() if len(self.df_long) > 0 else None
            }
        }
        
        # Estadísticas por condición
        if 'condition' in self.df_long.columns:
            stats_dict['by_condition'] = self.df_long.groupby('condition')['icp'].agg(['mean', 'std', 'count']).to_dict()
        
        return stats_dict
    
    def _mixed_anova(self) -> Dict[str, Any]:
        """
        ANOVA mixto: analiza efectos entre-sujetos y dentro-sujetos.
        Utiliza pingouin para resultados claros.
        """
        try:
            if 'condition' not in self.df_long.columns:
                return {'error': 'Condition column not found'}
            
            # ANOVA mixto: condition (within) x participant (between)
            aov = pg.mixed_anova(
                data=self.df_long,
                dv='icp',
                within='condition',
                subject='participant_id'
            )
            
            # Resultados en formato interpretable
            return {
                'success': True,
                'table': aov.to_dict(),
                'interpretation': self._interpret_anova(aov)
            }
        except Exception as e:
            logger.error(f"Error en ANOVA mixto: {e}")
            return {'error': str(e)}
    
    def _linear_mixed_models(self) -> Dict[str, Any]:
        """
        Modelos lineales mixtos con efectos aleatorios por participante.
        Modela la trayectoria de ICP a lo largo del tiempo.
        """
        results = {}
        
        try:
            # Modelo 1: ICP ~ Tiempo + (1|Participante)
            if 'window' in self.df_long.columns:
                model1 = mixedlm("icp ~ window", self.df_long, groups=self.df_long["participant_id"])
                model1_fit = model1.fit()
                results['time_trend'] = {
                    'summary': model1_fit.summary().as_text(),
                    'coefficients': model1_fit.params.to_dict(),
                    'pvalues': model1_fit.pvalues.to_dict(),
                    'significant': any(p < self.alpha for p in model1_fit.pvalues)
                }
            
            # Modelo 2: ICP ~ Condición + (1|Participante)
            if 'condition' in self.df_long.columns:
                model2 = mixedlm("icp ~ condition", self.df_long, groups=self.df_long["participant_id"])
                model2_fit = model2.fit()
                results['condition_effect'] = {
                    'summary': model2_fit.summary().as_text(),
                    'coefficients': model2_fit.params.to_dict(),
                    'pvalues': model2_fit.pvalues.to_dict()
                }
            
            # Modelo 3: Modelo completo con interacción
            if 'window' in self.df_long.columns and 'condition' in self.df_long.columns:
                model3 = mixedlm("icp ~ window * condition", self.df_long, groups=self.df_long["participant_id"])
                model3_fit = model3.fit()
                results['interaction'] = {
                    'summary': model3_fit.summary().as_text(),
                    'coefficients': model3_fit.params.to_dict()
                }
        
        except Exception as e:
            logger.error(f"Error en modelos mixtos: {e}")
            results['error'] = str(e)
        
        return results
    
    def _correlation_analysis(self) -> Dict[str, Any]:
        """
        Análisis de correlación entre ICP y métricas de rendimiento.
        """
        results = {}
        
        # Correlación ICP vs Accuracy de clasificación
        if 'mean_icp' in self.df_summary.columns and 'mean_accuracy' in self.df_summary.columns:
            valid_data = self.df_summary.dropna(subset=['mean_icp', 'mean_accuracy'])
            if len(valid_data) > 3:
                pearson_corr, pearson_p = pearsonr(valid_data['mean_icp'], valid_data['mean_accuracy'])
                spearman_corr, spearman_p = spearmanr(valid_data['mean_icp'], valid_data['mean_accuracy'])
                
                results['icp_vs_accuracy'] = {
                    'pearson': {'r': pearson_corr, 'p': pearson_p},
                    'spearman': {'rho': spearman_corr, 'p': spearman_p},
                    'significant': pearson_p < self.alpha or spearman_p < self.alpha,
                    'interpretation': self._interpret_correlation(pearson_corr)
                }
        
        # Correlación ICP vs Número de adaptaciones
        if 'mean_icp' in self.df_summary.columns and 'n_adaptations' in self.df_summary.columns:
            valid_data = self.df_summary.dropna(subset=['mean_icp', 'n_adaptations'])
            if len(valid_data) > 3:
                corr, p = pearsonr(valid_data['mean_icp'], valid_data['n_adaptations'])
                results['icp_vs_adaptations'] = {
                    'r': corr, 'p': p,
                    'significant': p < self.alpha
                }
        
        return results
    
    def _effect_size_analysis(self) -> Dict[str, Any]:
        """
        Calcula tamaños de efecto para comparaciones clave.
        Cohen's d, eta-squared, etc.
        """
        results = {}
        
        # Cohen's d para comparación baseline vs adaptativo
        if 'condition' in self.df_long.columns and len(self.df_long) > 0:
            baseline = self.df_long[self.df_long['condition'] == 'baseline']['icp']
            adaptive = self.df_long[self.df_long['condition'] == 'adaptive']['icp']
            
            if len(baseline) > 0 and len(adaptive) > 0:
                # Cohen's d
                pooled_std = np.sqrt((np.std(baseline)**2 + np.std(adaptive)**2) / 2)
                cohens_d = (np.mean(adaptive) - np.mean(baseline)) / pooled_std
                
                # Hedges' g (corregido para muestras pequeñas)
                n1, n2 = len(baseline), len(adaptive)
                hedges_g = cohens_d * (1 - 3 / (4*(n1 + n2) - 9))
                
                results['baseline_vs_adaptive'] = {
                    'cohens_d': cohens_d,
                    'hedges_g': hedges_g,
                    'interpretation': self._interpret_effect_size(cohens_d),
                    'mean_baseline': np.mean(baseline),
                    'mean_adaptive': np.mean(adaptive)
                }
        
        # Eta-squared para ANOVA
        if 'mixed_anova' in self.results and 'table' in self.results['mixed_anova']:
            # Extraer eta-squared si está disponible
            pass
        
        return results
    
    def _posthoc_power_analysis(self) -> Dict[str, Any]:
        """
        Análisis de poder estadístico post-hoc.
        Determina si el estudio tuvo suficiente poder para detectar efectos.
        """
        results = {}
        
        # Poder para prueba t (comparación baseline vs adaptive)
        if 'effect_sizes' in self.results and 'baseline_vs_adaptive' in self.results['effect_sizes']:
            es = self.results['effect_sizes']['baseline_vs_adaptive']['cohens_d']
            n_participants = len(self.cohort.participants)
            
            power_analysis = TTestPower()
            power = power_analysis.power(effect_size=es, nobs=n_participants, alpha=self.alpha)
            
            results['t_test_power'] = {
                'power': power,
                'sufficient': power >= 0.8,
                'interpretation': f"Poder estadístico = {power:.3f} {'(suficiente)' if power >= 0.8 else '(insuficiente)'}"
            }
        
        # Número mínimo de participantes necesario para efecto observado
        if 't_test_power' in results:
            desired_power = 0.8
            power_analysis = TTestPower()
            n_required = power_analysis.solve_power(
                effect_size=results['t_test_power']['power'],
                power=desired_power,
                alpha=self.alpha
            )
            results['n_required'] = {
                'n_participants_needed': int(np.ceil(n_required)),
                'current_n': len(self.cohort.participants),
                'recommendation': f"Necesarios {int(np.ceil(n_required))} participantes para poder = {desired_power}"
            }
        
        return results
    
    def _participant_clustering(self) -> Dict[str, Any]:
        """
        Agrupa participantes por perfiles de respuesta.
        Identifica subgrupos con diferentes patrones de adaptación.
        """
        results = {}
        
        # Preparar features para clustering
        feature_cols = []
        for col in ['mean_icp', 'std_icp', 'mean_accuracy', 'n_adaptations']:
            if col in self.df_summary.columns:
                feature_cols.append(col)
        
        if len(feature_cols) < 2:
            return {'error': 'Insufficient features for clustering'}
        
        # Preparar datos
        X = self.df_summary[feature_cols].dropna()
        if len(X) < 5:
            return {'error': 'Not enough participants for clustering'}
        
        # Escalar
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Determinar número óptimo de clusters (silhouette)
        n_clusters_range = range(2, min(6, len(X) - 1))
        silhouette_scores = []
        
        for k in n_clusters_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            silhouette_scores.append(silhouette_score(X_scaled, labels))
        
        if silhouette_scores:
            optimal_k = n_clusters_range[np.argmax(silhouette_scores)]
            
            # Clustering final
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Asignar clusters a participantes
            participant_ids = X.index.tolist()
            cluster_assignments = {pid: int(clusters[i]) for i, pid in enumerate(participant_ids)}
            
            # Caracterizar cada cluster
            cluster_profiles = {}
            for k in range(optimal_k):
                cluster_mask = clusters == k
                cluster_data = X[cluster_mask]
                cluster_profiles[k] = {
                    'n_participants': int(cluster_mask.sum()),
                    'mean_icp': cluster_data['mean_icp'].mean() if 'mean_icp' in cluster_data else None,
                    'mean_accuracy': cluster_data['mean_accuracy'].mean() if 'mean_accuracy' in cluster_data else None,
                    'n_adaptations': cluster_data['n_adaptations'].mean() if 'n_adaptations' in cluster_data else None
                }
            
            results['optimal_k'] = optimal_k
            results['silhouette_score'] = float(np.max(silhouette_scores))
            results['cluster_assignments'] = cluster_assignments
            results['cluster_profiles'] = cluster_profiles
        
        return results
    
    # ========================================================================
    # MÉTODOS DE INTERPRETACIÓN (Diseñados para AGIs)
    # ========================================================================
    
    def _interpret_anova(self, aov: pd.DataFrame) -> str:
        """Interpreta resultados ANOVA para AGIs."""
        if 'p-unc' in aov.columns:
            significant_effects = []
            for _, row in aov.iterrows():
                if row['p-unc'] < self.alpha:
                    significant_effects.append(f"{row['Source']} (F({row.get('ddof1', '?')}, {row.get('ddof2', '?')}) = {row['F']:.2f}, p = {row['p-unc']:.4f})")
            
            if significant_effects:
                return f"Efectos significativos encontrados: {', '.join(significant_effects)}"
            else:
                return "No se encontraron efectos estadísticamente significativos"
        return "No se pudo interpretar ANOVA"
    
    def _interpret_correlation(self, r: float) -> str:
        """Interpreta magnitud de correlación."""
        r_abs = abs(r)
        if r_abs < 0.1:
            return "despreciable"
        elif r_abs < 0.3:
            return "pequeña"
        elif r_abs < 0.5:
            return "moderada"
        else:
            return "fuerte"
    
    def _interpret_effect_size(self, d: float) -> str:
        """Interpreta tamaño de efecto Cohen's d."""
        d_abs = abs(d)
        if d_abs < 0.2:
            return "muy pequeño"
        elif d_abs < 0.5:
            return "pequeño"
        elif d_abs < 0.8:
            return "mediano"
        else:
            return "grande"
    
    def generate_report(self, output_dir: Path) -> str:
        """
        Genera reporte completo en múltiples formatos.
        Retorna ruta del reporte principal.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Reporte JSON (para AGIs)
        json_path = output_dir / "statistical_analysis.json"
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Reporte Markdown (para humanos)
        md_path = output_dir / "analysis_report.md"
        with open(md_path, 'w') as f:
            f.write(self._generate_markdown_report())
        
        # Exportar dataframes
        self.df_summary.to_csv(output_dir / "participant_summary.csv", index=False)
        self.df_long.to_csv(output_dir / "long_format_data.csv", index=False)
        
        logger.info(f"Reportes generados en {output_dir}")
        return str(json_path)
    
    def _generate_markdown_report(self) -> str:
        """Genera reporte en formato Markdown."""
        report = []
        report.append("# CPEA - Análisis Estadístico Avanzado")
        report.append(f"\n*Generado por AdvancedStatisticalAnalyzer*\n")
        
        # Descriptivos
        report.append("## 1. Estadísticas Descriptivas")
        if 'descriptives' in self.results:
            desc = self.results['descriptives']
            report.append(f"- **Participantes:** {desc['n_participants']}")
            report.append(f"- **Sesiones totales:** {desc['n_sessions_total']}")
            if desc['icp_overall']['mean']:
                report.append(f"- **ICP global:** μ = {desc['icp_overall']['mean']:.3f}, σ = {desc['icp_overall']['std']:.3f}")
        
        # Efectos
        report.append("\n## 2. Tamaños de Efecto")
        if 'effect_sizes' in self.results and 'baseline_vs_adaptive' in self.results['effect_sizes']:
            es = self.results['effect_sizes']['baseline_vs_adaptive']
            report.append(f"- **Cohen's d:** {es['cohens_d']:.3f} ({es['interpretation']})")
            report.append(f"- **Mejora ICP:** {es['mean_adaptive'] - es['mean_baseline']:.3f}")
        
        # Poder estadístico
        report.append("\n## 3. Análisis de Poder")
        if 'power_analysis' in self.results:
            pa = self.results['power_analysis']
            if 't_test_power' in pa:
                report.append(f"- **Poder observado:** {pa['t_test_power']['power']:.3f}")
                report.append(f"- **Interpretación:** {pa['t_test_power']['interpretation']}")
        
        # Clusters
        report.append("\n## 4. Perfiles de Participantes")
        if 'participant_clusters' in self.results and 'optimal_k' in self.results['participant_clusters']:
            clusters = self.results['participant_clusters']
            report.append(f"- **Clusters identificados:** {clusters['optimal_k']}")
            report.append(f"- **Silhouette score:** {clusters['silhouette_score']:.3f}")
        
        return "\n".join(report)


# ============================================================================
# VISUALIZACIÓN CIENTÍFICA AVANZADA
# ============================================================================

class ScientificVisualizer:
    """
    Genera visualizaciones científicas de alta calidad para publicaciones.
    Compatible con formatos vectoriales (SVG, PDF) y notebooks interactivos.
    """
    
    def __init__(self, cohort: ExperimentalCohort, analyzer: AdvancedStatisticalAnalyzer):
        self.cohort = cohort
        self.analyzer = analyzer
        self.figures = {}
        
        # Configurar estilo científico
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_context("paper", font_scale=1.2)
        sns.set_palette("husl")
    
    def create_all_figures(self, output_dir: Path) -> Dict[str, Path]:
        """
        Genera todas las figuras para publicación.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        figure_paths = {}
        
        # 1. Trayectorias individuales de ICP
        figure_paths['individual_trajectories'] = self._plot_individual_trajectories(output_dir)
        
        # 2. Comparación entre condiciones
        figure_paths['condition_comparison'] = self._plot_condition_comparison(output_dir)
        
        # 3. Correlación ICP vs Accuracy
        figure_paths['icp_accuracy_correlation'] = self._plot_icp_accuracy_correlation(output_dir)
        
        # 4. Evolución temporal de ICP (con bandas de confianza)
        figure_paths['temporal_evolution'] = self._plot_temporal_evolution(output_dir)
        
        # 5. Distribución de tamaños de efecto
        figure_paths['effect_size_distribution'] = self._plot_effect_size_distribution(output_dir)
        
        # 6. Visualización de clusters de participantes (t-SNE)
        if 'participant_clusters' in self.analyzer.results:
            figure_paths['participant_clusters'] = self._plot_participant_clusters(output_dir)
        
        # 7. Matriz de correlación entre métricas
        figure_paths['correlation_matrix'] = self._plot_correlation_matrix(output_dir)
        
        return figure_paths
    
    def _plot_individual_trajectories(self, output_dir: Path) -> Path:
        """Traza trayectorias individuales de ICP a lo largo del tiempo."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        df = self.analyzer.df_long
        if len(df) == 0:
            return None
        
        # Agrupar por participante y ventana
        for pid, group in df.groupby('participant_id'):
            if len(group) > 1:
                ax.plot(group['window'], group['icp'], 
                       alpha=0.5, linewidth=1, label=pid if len(df['participant_id'].unique()) < 10 else "")
        
        # Línea promedio
        avg_icp = df.groupby('window')['icp'].mean()
        std_icp = df.groupby('window')['icp'].std()
        
        ax.plot(avg_icp.index, avg_icp.values, 'k-', linewidth=2, label='Promedio grupo')
        ax.fill_between(avg_icp.index, 
                        avg_icp.values - std_icp.values,
                        avg_icp.values + std_icp.values,
                        alpha=0.2, color='gray')
        
        ax.set_xlabel('Ventana temporal', fontsize=12)
        ax.set_ylabel('Índice de Coherencia Predictiva (ICP)', fontsize=12)
        ax.set_title('Trayectorias individuales de ICP', fontsize=14, fontweight='bold')
        ax.legend(loc='best', ncol=2 if len(df['participant_id'].unique()) < 10 else 1)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        path = output_dir / "individual_trajectories.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.savefig(output_dir / "individual_trajectories.svg", format='svg')
        plt.close()
        
        return path
    
    def _plot_condition_comparison(self, output_dir: Path) -> Path:
        """Comparación entre condiciones (baseline vs adaptativo)."""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        df = self.analyzer.df_long
        if 'condition' not in df.columns:
            return None
        
        # Violin plot con boxplot superpuesto
        sns.violinplot(data=df, x='condition', y='icp', ax=ax, inner=None, alpha=0.6)
        sns.boxplot(data=df, x='condition', y='icp', ax=ax, width=0.2, color='white', boxprops={'alpha': 0.8})
        
        # Añadir puntos individuales
        sns.stripplot(data=df, x='condition', y='icp', ax=ax, color='black', alpha=0.3, size=3)
        
        ax.set_xlabel('Condición', fontsize=12)
        ax.set_ylabel('Índice de Coherencia Predictiva (ICP)', fontsize=12)
        ax.set_title('Comparación de ICP entre condiciones', fontsize=14, fontweight='bold')
        
        # Añadir estadísticas
        if 'effect_sizes' in self.analyzer.results:
            es = self.analyzer.results['effect_sizes'].get('baseline_vs_adaptive', {})
            if es:
                ax.text(0.5, 0.95, f"Cohen's d = {es.get('cohens_d', 0):.3f}\n{es.get('interpretation', '')}",
                       transform=ax.transAxes, ha='center', fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        path = output_dir / "condition_comparison.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    def _plot_icp_accuracy_correlation(self, output_dir: Path) -> Path:
        """Correlación entre ICP y accuracy de clasificación."""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        df = self.analyzer.df_summary.dropna(subset=['mean_icp', 'mean_accuracy'])
        
        if len(df) < 3:
            return None
        
        # Scatter plot
        sns.regplot(data=df, x='mean_icp', y='mean_accuracy', ax=ax, 
                   scatter_kws={'s': 100, 'alpha': 0.6}, line_kws={'color': 'red'})
        
        # Añadir correlación
        if 'correlations' in self.analyzer.results:
            corr = self.analyzer.results['correlations'].get('icp_vs_accuracy', {})
            if 'pearson' in corr:
                r = corr['pearson']['r']
                p = corr['pearson']['p']
                ax.text(0.05, 0.95, f"Pearson r = {r:.3f}\np = {p:.4f}\n{corr.get('interpretation', '')}",
                       transform=ax.transAxes, fontsize=10, verticalalignment='top',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        ax.set_xlabel('ICP promedio', fontsize=12)
        ax.set_ylabel('Accuracy de clasificación', fontsize=12)
        ax.set_title('Correlación ICP vs Accuracy', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        path = output_dir / "icp_accuracy_correlation.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    def _plot_temporal_evolution(self, output_dir: Path) -> Path:
        """Evolución temporal con bandas de confianza."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        df = self.analyzer.df_long
        if len(df) == 0:
            return None
        
        # Agrupar por condición y ventana
        if 'condition' in df.columns and 'window' in df.columns:
            for condition in df['condition'].unique():
                subset = df[df['condition'] == condition]
                avg = subset.groupby('window')['icp'].mean()
                sem = subset.groupby('window')['icp'].sem()  # Error estándar
                
                ax.plot(avg.index, avg.values, linewidth=2, label=condition)
                ax.fill_between(avg.index, 
                                avg.values - 1.96 * sem.values,
                                avg.values + 1.96 * sem.values,
                                alpha=0.2)
        
        ax.set_xlabel('Ventana temporal', fontsize=12)
        ax.set_ylabel('Índice de Coherencia Predictiva (ICP)', fontsize=12)
        ax.set_title('Evolución temporal de ICP por condición', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        path = output_dir / "temporal_evolution.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    def _plot_effect_size_distribution(self, output_dir: Path) -> Path:
        """Distribución de tamaños de efecto por participante."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Calcular efecto por participante (baseline vs adaptativo)
        participant_effects = []
        df = self.analyzer.df_long
        
        if 'condition' in df.columns and 'window' in df.columns:
            for pid in df['participant_id'].unique():
                pdata = df[df['participant_id'] == pid]
                baseline = pdata[pdata['condition'] == 'baseline']['icp']
                adaptive = pdata[pdata['condition'] == 'adaptive']['icp']
                
                if len(baseline) > 0 and len(adaptive) > 0:
                    pooled_std = np.sqrt((np.std(baseline)**2 + np.std(adaptive)**2) / 2)
                    if pooled_std > 0:
                        d = (np.mean(adaptive) - np.mean(baseline)) / pooled_std
                        participant_effects.append(d)
        
        if participant_effects:
            ax.hist(participant_effects, bins=15, edgecolor='black', alpha=0.7)
            ax.axvline(x=0, color='red', linestyle='--', linewidth=1.5, label='Sin efecto')
            ax.axvline(x=np.mean(participant_effects), color='green', linestyle='-', 
                      linewidth=2, label=f'Media = {np.mean(participant_effects):.3f}')
            
            ax.set_xlabel('Cohen\'s d (mejora adaptativa)', fontsize=12)
            ax.set_ylabel('Número de participantes', fontsize=12)
            ax.set_title('Distribución de tamaños de efecto por participante', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        path = output_dir / "effect_size_distribution.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    def _plot_participant_clusters(self, output_dir: Path) -> Path:
        """Visualización t-SNE de clusters de participantes."""
        if 'participant_clusters' not in self.analyzer.results:
            return None
        
        clusters = self.analyzer.results['participant_clusters']
        if 'error' in clusters:
            return None
        
        # Preparar features
        feature_cols = []
        for col in ['mean_icp', 'std_icp', 'mean_accuracy', 'n_adaptations']:
            if col in self.analyzer.df_summary.columns:
                feature_cols.append(col)
        
        if len(feature_cols) < 2:
            return None
        
        X = self.analyzer.df_summary[feature_cols].dropna()
        if len(X) < 5:
            return None
        
        # t-SNE
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(X)-1))
        X_tsne = tsne.fit_transform(X_scaled)
        
        # Asignar clusters
        cluster_labels = [clusters['cluster_assignments'][pid] for pid in X.index]
        
        # Visualizar
        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(X_tsne[:, 0], X_tsne[:, 1], 
                            c=cluster_labels, cmap='viridis', 
                            s=100, alpha=0.7, edgecolors='black', linewidth=1)
        
        # Añadir etiquetas de participantes
        for i, pid in enumerate(X.index):
            ax.annotate(pid, (X_tsne[i, 0], X_tsne[i, 1]), 
                       fontsize=8, alpha=0.7, xytext=(5, 5), textcoords='offset points')
        
        ax.set_xlabel('t-SNE 1', fontsize=12)
        ax.set_ylabel('t-SNE 2', fontsize=12)
        ax.set_title(f'Clusters de participantes (k={clusters["optimal_k"]})', fontsize=14, fontweight='bold')
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Cluster', fontsize=10)
        
        plt.tight_layout()
        path = output_dir / "participant_clusters.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    def _plot_correlation_matrix(self, output_dir: Path) -> Path:
        """Matriz de correlación entre todas las métricas."""
        df = self.analyzer.df_summary
        
        # Seleccionar columnas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < 2:
            return None
        
        corr_matrix = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='RdBu_r', center=0, square=True,
                   linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
        
        ax.set_title('Matriz de correlación entre métricas', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        path = output_dir / "correlation_matrix.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path


# ============================================================================
# FUNCIONES DE ALTO NIVEL PARA AGIs
# ============================================================================

def run_multi_participant_study(
    data_directory: Path,
    output_directory: Path,
    cohort_name: str = "CPEA_Study"
) -> Dict[str, Any]:
    """
    Función principal para ejecutar estudio multi-participante completo.
    Diseñada para ser llamada por AGIs.
    
    Args:
        data_directory: Directorio con datos de participantes
        output_directory: Directorio para resultados
        cohort_name: Nombre de la cohorte
        
    Returns:
        Diccionario con resultados completos
    """
    logger.info(f"Iniciando estudio multi-participante desde {data_directory}")
    
    # 1. Cargar cohorte
    cohort = ExperimentalCohort(name=cohort_name)
    
    # Simulación: en producción, cargar desde archivos
    # Por ahora, crear datos sintéticos para demostración
    n_participants = 20
    
    for i in range(n_participants):
        pid = f"P{i+1:03d}"
        participant = ParticipantData(
            participant_id=pid,
            demographics={'age': np.random.randint(20, 50), 'gender': np.random.choice(['M', 'F'])}
        )
        
        # Simular sesiones
        for session in range(3):
            condition = 'baseline' if session == 0 else 'adaptive'
            n_windows = np.random.randint(50, 150)
            
            # ICP con mejora en sesiones adaptativas
            if condition == 'baseline':
                icp_values = np.random.beta(2, 2, n_windows) * 0.5 + 0.3
            else:
                # Mejora progresiva
                icp_values = np.random.beta(3, 1.5, n_windows) * 0.6 + 0.4
                icp_values = icp_values * (1 + np.linspace(0, 0.3, n_windows))  # Tendencia ascendente
            
            session_data = {
                'icp_values': icp_values.tolist(),
                'accuracies': np.random.beta(2, 1, n_windows).tolist(),
                'condition': condition,
                'adaptation_applied': condition == 'adaptive'
            }
            participant.add_session(f"session_{session}", session_data)
        
        cohort.add_participant(participant)
    
    # 2. Análisis estadístico
    analyzer = AdvancedStatisticalAnalyzer(cohort)
    results = analyzer.run_complete_analysis()
    
    # 3. Visualización
    visualizer = ScientificVisualizer(cohort, analyzer)
    figure_paths = visualizer.create_all_figures(output_directory)
    
    # 4. Generar reportes
    report_path = analyzer.generate_report(output_directory)
    
    # 5. Exportar para AGIs (formato estructurado)
    structured_output = {
        'cohort_name': cohort_name,
        'n_participants': len(cohort.participants),
        'results': results,
        'figure_paths': {k: str(v) for k, v in figure_paths.items() if v},
        'report_path': str(report_path),
        'interpretation': {
            'main_finding': _generate_main_finding(results),
            'recommendations': _generate_recommendations(results),
            'limitations': _identify_limitations(results)
        }
    }
    
    # Guardar salida estructurada
    with open(output_directory / "study_results.json", 'w') as f:
        json.dump(structured_output, f, indent=2, default=str)
    
    logger.info(f"Estudio completado. Resultados guardados en {output_directory}")
    
    return structured_output


def _generate_main_finding(results: Dict[str, Any]) -> str:
    """Genera hallazgo principal en lenguaje natural."""
    if 'effect_sizes' in results and 'baseline_vs_adaptive' in results['effect_sizes']:
        es = results['effect_sizes']['baseline_vs_adaptive']
        improvement = es.get('mean_adaptive', 0) - es.get('mean_baseline', 0)
        return f"Se observó una mejora de {improvement:.3f} en ICP (Cohen's d = {es.get('cohens_d', 0):.3f}) en condiciones adaptativas comparado con baseline."
    return "Análisis completado. Revisar resultados detallados."


def _generate_recommendations(results: Dict[str, Any]) -> List[str]:
    """Genera recomendaciones basadas en resultados."""
    recommendations = []
    
    if 'power_analysis' in results and 'n_required' in results['power_analysis']:
        n_required = results['power_analysis']['n_required']['n_participants_needed']
        n_current = results['power_analysis']['n_required']['current_n']
        if n_required > n_current:
            recommendations.append(f"Considerar aumentar número de participantes a {n_required} para alcanzar poder estadístico de 0.8")
    
    if 'participant_clusters' in results and 'optimal_k' in results['participant_clusters']:
        k = results['participant_clusters']['optimal_k']
        recommendations.append(f"Se identificaron {k} perfiles distintos de respuesta. Considerar análisis estratificado por cluster.")
    
    if not recommendations:
        recommendations.append("Estudio con poder adecuado. Proceder a validación en entornos reales.")
    
    return recommendations


def _identify_limitations(results: Dict[str, Any]) -> List[str]:
    """Identifica limitaciones del estudio."""
    limitations = []
    
    if 'power_analysis' in results and 't_test_power' in results['power_analysis']:
        power = results['power_analysis']['t_test_power']['power']
        if power < 0.8:
            limitations.append(f"Poder estadístico marginal ({power:.2f}). Resultados deben interpretarse con cautela.")
    
    if 'participant_clusters' in results and 'silhouette_score' in results['participant_clusters']:
        if results['participant_clusters']['silhouette_score'] < 0.3:
            limitations.append("Estructura de clusters débil. La variabilidad entre participantes puede ser continua más que categórica.")
    
    return limitations


# ============================================================================
# EJECUCIÓN DEMOSTRATIVA
# ============================================================================

if __name__ == "__main__":
    # Ejecutar estudio demostrativo
    data_dir = Path("./demo_data")
    output_dir = Path("./study_results")
    
    results = run_multi_participant_study(data_dir, output_dir)
    
    print("\n" + "=" * 60)
    print("RESUMEN DEL ESTUDIO MULTI-PARTICIPANTE")
    print("=" * 60)
    print(f"Cohorte: {results['cohort_name']}")
    print(f"Participantes: {results['n_participants']}")
    print(f"Hallazgo principal: {results['interpretation']['main_finding']}")
    print(f"\nRecomendaciones:")
    for rec in results['interpretation']['recommendations']:
        print(f"  • {rec}")
    print(f"\nResultados guardados en: {output_dir}")
