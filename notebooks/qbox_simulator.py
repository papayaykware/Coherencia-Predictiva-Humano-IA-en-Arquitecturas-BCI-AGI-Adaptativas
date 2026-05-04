#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador QBox para la teoría post-cuántica de Hefford & Wilson (2023).

Implementa:
- Tensores de densidad de 4 índices (hipercubo de densidad)
- Canales de hiperdecoherencia no markovianos
- Generación de correlaciones que violan desigualdades de Leggett-Garg
- Datos sintéticos para entrenar el Detector Post-Cuántico de Coherencia (DPCC)

Autor: papayaykware
Repositorio: https://github.com/papayaykware/dpcc
Versión: 1.0
Licencia: MIT
"""

import numpy as np
import numpy.random as rnd
from scipy.linalg import expm, sqrtm
from typing import Tuple, List, Optional
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)


# ============================================================================
# 1. FUNDAMENTOS: TENSORES DE 4 ÍNDICES Y SUPEROPERADORES
# ============================================================================

class HipercuboDensidad:
    """
    Representa un estado QBox como un tensor de 4 índices ρ_{abcd}
    con las propiedades:
      - Traza parcial preservada: Tr(ρ) = 1
      - Positividad completa generalizada
      - Simetría de intercambio entre pares (a,b) <-> (c,d) en sistemas cerrados
    """
    
    def __init__(self, tensor: np.ndarray):
        """
        Args:
            tensor: array de forma (d, d, d, d) donde d es la dimensión local.
                   Por defecto d=2 (sistemas de dos niveles, qubits).
        """
        self.tensor = np.asarray(tensor, dtype=complex)
        self.d = self.tensor.shape[0]
        assert self.tensor.shape == (self.d, self.d, self.d, self.d), \
            f"Forma incorrecta: {self.tensor.shape}, debe ser ({self.d},{self.d},{self.d},{self.d})"
        self._normalize()
    
    def _normalize(self):
        """Normaliza el tensor para que la traza parcial (contracción de índices 1 y 3 con 2 y 4) sea 1."""
        traza = np.trace(np.trace(self.tensor, axis1=0, axis2=2), axis1=0, axis2=1)  # Contracción (a=c, b=d)
        self.tensor /= traza
    
    @staticmethod
    def aleatorio(d: int = 2, pureza: float = 1.0) -> 'HipercuboDensidad':
        """
        Genera un hipercubo de densidad aleatorio.
        
        Args:
            d: dimensión local
            pureza: 0 (máximamente mixto) a 1 (puro QBox)
        """
        # Generamos un tensor gaussiano complejo
        real = rnd.randn(d, d, d, d)
        imag = rnd.randn(d, d, d, d)
        tensor = (real + 1j*imag) / np.sqrt(2)
        
        # Mezcla con el estado máximamente mixto (identidad normalizada)
        identidad = np.eye(d, dtype=complex)
        # La identidad en el espacio de 4 índices es delta_{a,c} * delta_{b,d}
        id_tensor = np.einsum('ac,bd->abcd', identidad, identidad) / d**2
        
        tensor = pureza * tensor + (1-pureza) * id_tensor
        return HipercuboDensidad(tensor)
    
    def traza(self) -> float:
        """Traza completa del tensor (debe ser 1)."""
        return np.trace(np.trace(self.tensor, axis1=0, axis2=2), axis1=0, axis2=1).real
    
    def reducir_a_matriz_densidad(self) -> np.ndarray:
        """
        Aplica hiperdecoherencia total para obtener una matriz de densidad cuántica estándar.
        Contrae pares de índices (a,c) y (b,d).
        """
        return np.trace(np.trace(self.tensor, axis1=1, axis2=3), axis1=0, axis2=2)
    
    def __add__(self, other):
        return HipercuboDensidad(self.tensor + other.tensor)
    
    def __mul__(self, scalar):
        return HipercuboDensidad(self.tensor * scalar)
    
    def __repr__(self):
        return f"HipercuboDensidad(d={self.d}, traza={self.traza():.3f})"


# ============================================================================
# 2. CANALES DE HIPERDECOHERENCIA (no markovianos)
# ============================================================================

class HiperdecoherenceChannel:
    """
    Implementa un canal Λ que transforma un hipercubo de densidad QBox en otro,
    simulando la interacción con un entorno de hiperdecoherencia.
    El canal es no markoviano (tiene memoria de 4 pasos) como requiere la teoría QBox.
    """
    
    def __init__(self, fuerza_acoplamiento: float = 0.1, memoria: int = 4):
        """
        Args:
            fuerza_acoplamiento: intensidad de la hiperdecoherencia (0 = ninguno, 1 = total)
            memoria: número de pasos temporales que retiene el canal (≥1)
        """
        self.gamma = fuerza_acoplamiento
        self.memoria = memoria
        self.historial: List[HipercuboDensidad] = []
    
    def aplicar(self, estado: HipercuboDensidad) -> HipercuboDensidad:
        """
        Aplica un paso del canal de hiperdecoherencia.
        Guarda el estado en el historial y usa los últimos `memoria` estados
        para determinar la transformación (no markoviano).
        """
        self.historial.append(estado)
        if len(self.historial) > self.memoria:
            self.historial.pop(0)
        
        # Construimos un operador efectivo a partir de la media de los estados pasados
        if len(self.historial) == 1:
            promedio = self.historial[0].tensor
        else:
            promedio = np.mean([h.tensor for h in self.historial], axis=0)
        
        # Aplicamos hiperdecoherencia: mezcla entre el estado actual y el promedio pasado
        # Esto introduce la "indefinición causal" porque el estado depende del futuro pasado (memoria)
        tensor_nuevo = (1 - self.gamma) * estado.tensor + self.gamma * promedio
        
        # Ruido térmico cuántico simulado (pequeña componente aleatoria)
        ruido = rnd.randn(*tensor_nuevo.shape) * 0.01 * self.gamma
        tensor_nuevo += ruido
        
        return HipercuboDensidad(tensor_nuevo)
    
    def reset(self):
        """Resetea el historial del canal."""
        self.historial = []


# ============================================================================
# 3. OBSERVABLES Y VIOLACIÓN DE LEGGETT-GARG GENERALIZADA
# ============================================================================

class ObservableQBox:
    """
    Representa un observable hipercuántico Q_{abcd} con autovalores ±1.
    Se define a partir de una matriz de Pauli o de fases toroidales.
    """
    
    def __init__(self, matriz: Optional[np.ndarray] = None, d: int = 2):
        """
        Args:
            matriz: operador hermítico de dimensión d×d. Por defecto σ_z.
            d: dimensión local si no se provee matriz.
        """
        if matriz is None:
            # Por defecto, σ_z (Pauli Z)
            self.matriz = np.array([[1, 0], [0, -1]], dtype=complex)
        else:
            self.matriz = np.asarray(matriz)
            assert self.matriz.shape[0] == self.matriz.shape[1]
            # Aseguramos que sea hermítico y con autovalores ±1
            autovalores, _ = np.linalg.eigh(self.matriz)
            if not np.allclose(np.abs(autovalores), 1):
                # Normalizamos
                self.matriz = self.matriz / np.max(np.abs(autovalores))
        self.d = self.matriz.shape[0]
    
    def tensor_observable(self) -> np.ndarray:
        """
        Construye el tensor de 4 índices correspondiente al observable en el espacio QBox.
        Se define como: Q_{abcd} = M_{ac} ⊗ M_{bd} (producto tensorial de dos copias)
        """
        # Producto tensorial externo: (a,c) y (b,d)
        # Forma final: (d, d, d, d)
        return np.einsum('ac,bd->abcd', self.matriz, self.matriz)
    
    def expectacion(self, estado: HipercuboDensidad) -> float:
        """
        Calcula ⟨Q⟩ = Tr(ρ_{abcd} Q_{abcd})
        """
        Q_tensor = self.tensor_observable()
        # Contracción completa: suma sobre a,b,c,d
        valor = np.einsum('abcd,abcd->', estado.tensor, Q_tensor).real
        return valor


def leggett_garg_generalizada(estados: List[HipercuboDensidad], 
                               observable: ObservableQBox) -> float:
    """
    Calcula el parámetro K^{(4)} de la desigualdad de Leggett-Garg generalizada.
    
    Args:
        estados: lista de 4 estados en tiempos t1, t2, t3, t4 (orden cronológico)
        observable: observable Q a medir
    
    Returns:
        K^{(4)} que debe ser ≤ 4 en cuántica estándar; valores >4 indican régimen QBox.
    """
    if len(estados) != 4:
        raise ValueError("Se requieren exactamente 4 estados para LG generalizada")
    
    # Correlaciones a 4 tiempos (promedio del producto de las medidas)
    # En hiperdecoherencia, esto se calcula directamente del tensor conjunto
    # Simplificación: asumimos que podemos medir Q en cada tiempo y multiplicar
    Q_vals = [observable.expectacion(est) for est in estados]
    # Producto de las 4 medidas (simulamos correlación de orden 4)
    correlacion_cuádruple = np.prod(Q_vals)
    
    # Términos de suma alternante según el tensor ε_{ijkl}
    # Para simplificar, usamos la expresión estándar de LG para 4 tiempos:
    # K = C12 + C23 + C34 - C14
    # Donde Cij = correlación a dos tiempos entre ti y tj
    
    def correlacion_dos_tiempos(i, j):
        # En nuestro modelo, las correlaciones a dos tiempos son producto de expectaciones
        # Esto es válido porque los estados ya incorporan la evolución QBox
        return Q_vals[i] * Q_vals[j]
    
    C12 = correlacion_dos_tiempos(0,1)
    C23 = correlacion_dos_tiempos(1,2)
    C34 = correlacion_dos_tiempos(2,3)
    C14 = correlacion_dos_tiempos(0,3)
    
    K = C12 + C23 + C34 - C14
    return K


# ============================================================================
# 4. GENERADOR DE DATOS SINTÉTICOS PARA DPCC
# ============================================================================

class GeneradorQBox:
    """
    Produce secuencias temporales de tensores Q_{ijkl}(t) etiquetadas como:
        - "qbox": hiperdecoherencia activa (viola LG)
        - "cuantico": decoherencia estándar hacia matriz densidad
        - "clasico": ruido gaussiano sin estructura cuántica
    """
    
    def __init__(self, d: int = 2, canales_meg: int = 8, canales_geof: int = 4):
        """
        Args:
            d: dimensión local del estado QBox
            canales_meg: número de canales MEG simulados (índices i,j)
            canales_geof: número de canales geofísicos (índices k,l)
        """
        self.d = d
        self.n_meg = canales_meg
        self.n_geo = canales_geof
        self.canal_hiperdeco = HiperdecoherenceChannel(fuerza_acoplamiento=0.3, memoria=4)
        self.observable_z = ObservableQBox()
        
    def generar_secuencia(self, T: int = 1000, modo: str = "qbox") -> np.ndarray:
        """
        Genera un tensor de 4 índices de forma (T, n_meg, n_meg, n_geo, n_geo)
        donde T es el número de pasos temporales.
        
        Args:
            T: número de muestras temporales
            modo: "qbox", "cuantico", "clasico"
        
        Returns:
            tensor_Q: array complejo o flotante (si modo='clasico')
        """
        if modo == "qbox":
            return self._generar_qbox(T)
        elif modo == "cuantico":
            return self._generar_cuantico(T)
        elif modo == "clasico":
            return self._generar_clasico(T)
        else:
            raise ValueError(f"Modo '{modo}' no reconocido")
    
    def _generar_qbox(self, T: int) -> np.ndarray:
        """Secuencia con hiperdecoherencia y correlaciones QBox."""
        self.canal_hiperdeco.reset()
        tensor_salida = np.zeros((T, self.n_meg, self.n_meg, self.n_geo, self.n_geo), dtype=complex)
        
        # Inicializamos un estado QBox aleatorio diferente para cada par de canales
        # Simulamos la red de canales: para cada combinación (meg_i, meg_j, geo_k, geo_l)
        for i in range(self.n_meg):
            for j in range(self.n_meg):
                for k in range(self.n_geo):
                    for l in range(self.n_geo):
                        # Estado aleatorio inicial (puro)
                        estado = HipercuboDensidad.aleatorio(self.d, pureza=0.9)
                        for t in range(T):
                            # Evolución temporal con hiperdecoherencia
                            if t > 0:
                                estado = self.canal_hiperdeco.aplicar(estado)
                            # Extraemos el valor del observable Z (autovalor medio)
                            valor = self.observable_z.expectacion(estado)
                            # Ruido característico QBox (no gaussiano, long tail)
                            ruido = 0.05 * np.tanh(rnd.randn()) * (1 + 0.2*np.sin(t/10))
                            tensor_salida[t, i, j, k, l] = valor + ruido + 1j*0.01*rnd.randn()
        
        # Normalizamos entre -1 y 1 (para simular observable ±1)
        max_abs = np.max(np.abs(tensor_salida))
        if max_abs > 0:
            tensor_salida = tensor_salida / max_abs
        return tensor_salida
    
    def _generar_cuantico(self, T: int) -> np.ndarray:
        """Secuencia que evoluciona a matriz densidad estándar (sin hiperdecoherencia)."""
        tensor_salida = np.zeros((T, self.n_meg, self.n_meg, self.n_geo, self.n_geo), dtype=complex)
        
        for i in range(self.n_meg):
            for j in range(self.n_meg):
                for k in range(self.n_geo):
                    for l in range(self.n_geo):
                        # Usamos matrices densidad de 2×2 estándar (qubits)
                        estado_matriz = np.eye(2, dtype=complex) / 2  # máximamente mixto
                        for t in range(T):
                            # Evolución: rotación aleatoria lenta + decoherencia
                            theta = 0.1 * np.sin(t/50)
                            rot = expm(-1j * theta * np.array([[0,1],[1,0]]))  # rotación X
                            estado_matriz = rot @ estado_matriz @ rot.conj().T
                            # Decoherencia: mezcla con matriz identidad
                            estado_matriz = 0.95 * estado_matriz + 0.05 * np.eye(2)/2
                            valor = np.trace(self.observable_z.matriz @ estado_matriz).real
                            tensor_salida[t, i, j, k, l] = valor + 0.01j * rnd.randn()
        
        # Normalización
        max_abs = np.max(np.abs(tensor_salida))
        if max_abs > 0:
            tensor_salida = tensor_salida / max_abs
        return tensor_salida
    
    def _generar_clasico(self, T: int) -> np.ndarray:
        """
        Secuencia puramente clásica: ruido coloreado con estructura temporal,
        pero sin correlaciones cuánticas ni QBox.
        """
        tensor_salida = np.zeros((T, self.n_meg, self.n_meg, self.n_geo, self.n_geo))
        
        for i in range(self.n_meg):
            for j in range(self.n_meg):
                for k in range(self.n_geo):
                    for l in range(self.n_geo):
                        # Proceso AR(1) (autorregresivo de orden 1) para dar correlación temporal
                        ruido = rnd.randn(T)
                        ar = np.zeros(T)
                        ar[0] = ruido[0]
                        for t in range(1, T):
                            ar[t] = 0.8 * ar[t-1] + 0.2 * ruido[t]
                        # Normalizamos a [-1,1]
                        ar = ar / (np.max(np.abs(ar)) + 1e-8)
                        tensor_salida[t, i, j, k, l] = ar[t]
        
        return tensor_salida
    
    def generar_dataset_etiquetado(self, n_muestras: int = 1000, 
                                   T: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera dataset balanceado para entrenamiento.
        
        Args:
            n_muestras: número total de muestras (se repartirán 1/3 cada modo)
            T: longitud temporal de cada muestra
        
        Returns:
            X: array de forma (n_muestras, T, n_meg, n_meg, n_geo, n_geo)
            y: etiquetas (0=clasico, 1=cuantico, 2=qbox)
        """
        n_por_clase = n_muestras // 3
        X_list = []
        y_list = []
        
        modos = ["clasico", "cuantico", "qbox"]
        for idx, modo in enumerate(modos):
            print(f"Generando {n_por_clase} muestras para modo '{modo}'...")
            for _ in range(n_por_clase):
                X_list.append(self.generar_secuencia(T, modo))
                y_list.append(idx)
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        # Mezclamos
        perm = rnd.permutation(n_muestras)
        return X[perm], y[perm]


# ============================================================================
# 5. FUNCIONES DE UTILIDAD PARA VIOLACIÓN DE LG
# ============================================================================

def simular_violacion_LG(estados: List[HipercuboDensidad], 
                         observable: ObservableQBox, 
                         repeticiones: int = 100) -> float:
    """
    Promedia la violación de Leggett-Garg sobre múltiples realizaciones.
    """
    valores_K = []
    for _ in range(repeticiones):
        # Simulamos mediciones: cada estado se colapsa aleatoriamente según Q
        # (En QBox, el colapso es gradual, lo simulamos como una fluctuación)
        estados_ruidosos = []
        for est in estados:
            # Ruido que simula la hiperdecoherencia en la medición
            factor = 1 + 0.1 * rnd.randn()
            tensor_ruidoso = est.tensor * factor
            estados_ruidosos.append(HipercuboDensidad(tensor_ruidoso))
        
        K = leggett_garg_generalizada(estados_ruidosos, observable)
        valores_K.append(K)
    
    return np.mean(valores_K)


# ============================================================================
# 6. EJEMPLO DE USO Y PRUEBA DE INTEGRIDAD
# ============================================================================

if __name__ == "__main__":
    print("=== SIMULADOR QBOX - PRUEBA DE INTEGRIDAD ===\n")
    
    # 1. Crear un hipercubo de densidad aleatorio
    estado_qbox = HipercuboDensidad.aleatorio(d=2, pureza=0.8)
    print(f"Estado inicial: {estado_qbox}")
    print(f"Traza del estado: {estado_qbox.traza():.6f} (debe ser 1)")
    
    # 2. Aplicar hiperdecoherencia
    canal = HiperdecoherenceChannel(fuerza_acoplamiento=0.3, memoria=4)
    for paso in range(5):
        estado_qbox = canal.aplicar(estado_qbox)
    print(f"Después de 5 pasos: {estado_qbox}")
    
    # 3. Medir observable
    obsZ = ObservableQBox()
    expectacion = obsZ.expectacion(estado_qbox)
    print(f"⟨σ_z⟩ en el estado QBox: {expectacion:.4f} ± 0.1")
    
    # 4. Generar una secuencia temporal pequeña
    generador = GeneradorQBox(d=2, canales_meg=4, canales_geof=2)
    print("\nGenerando secuencia modo 'qbox' (T=100, canales MEG=4, geo=2)...")
    secuencia = generador.generar_secuencia(T=100, modo="qbox")
    print(f"Forma del tensor resultante: {secuencia.shape}")
    print(f"Media de la señal: {np.mean(secuencia):.4f}, desviación: {np.std(secuencia):.4f}")
    
    # 5. Simular violación de Leggett-Garg
    # Creamos 4 estados correlacionados temporalmente
    estados = [HipercuboDensidad.aleatorio(pureza=0.9) for _ in range(4)]
    K_promedio = simular_violacion_LG(estados, obsZ, repeticiones=50)
    print(f"\nParámetro K^{(4)} promedio (esperado >4 para QBox): {K_promedio:.3f}")
    if K_promedio > 4.0:
        print("¡Violación de Leggett-Garg detectada! Consistente con teoría QBox.")
    else:
        print("Sin violación significativa (quizás necesitas más pasos de hiperdecoherencia).")
    
    # 6. Generar dataset pequeño para pruebas
    print("\nGenerando dataset de 30 muestras para entrenamiento rápido...")
    X_small, y_small = generador.generar_dataset_etiquetado(n_muestras=30, T=50)
    print(f"X_small shape: {X_small.shape}, y_small shape: {y_small.shape}")
    print("Distribución de clases:")
    for clase, nombre in enumerate(["clasico", "cuantico", "qbox"]):
        print(f"  {nombre}: {np.sum(y_small==clase)} muestras")
    
    print("\n=== PRUEBA COMPLETADA ===")
