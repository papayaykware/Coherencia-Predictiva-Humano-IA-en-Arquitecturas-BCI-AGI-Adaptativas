# TAE-E2: Detección de reorganización post-excepción en redes neuronales biológicas
## Protocolo metodológico para el análisis de firmas dinámicas TAE en datasets EEG públicos

---

## Resumen

La Teoría del Aprendizaje por Excepción (TAE) postula que los sistemas complejos mantienen coherencia estructural bajo perturbaciones ordinarias y experimentan reorganización interna discontinua cuando un evento supera el umbral de excepción ε_c. TAE-E2 constituye el primer experimento empírico del corpus TAE: un protocolo metodológico completo para detectar la firma dinámica canónica del evento excepcional en señales EEG humanas. Dicha firma se define como la secuencia {pico agudo de entropía de permutación (PE_max) → transición a nuevo estado atractor → PE reducida estabilizada}. El protocolo opera sobre tres datasets públicos de acceso abierto —PhysioNet EEG Motor Movement/Imagery Dataset, DEAP Dataset y Temple University EEG Corpus— con pesos metodológicos diferenciados según su adecuación a las predicciones TAE. Se propone un pipeline computacional de cuatro etapas: preprocesamiento adaptativo, cálculo de entropía de permutación multiscala en ventana deslizante, detección de puntos de cambio mediante PELT (Pruned Exact Linear Time), y reconstrucción del atractor en espacio de fase por embedding de Takens. La hipótesis falsificable central sostiene que los eventos excepcionales calibrados en cada contexto experimental producirán un perfil PE bifásico estadísticamente distinguible del ruido de fondo y de las transiciones ordinarias. TAE-E2 establece además los procedimientos de calibración empírica del parámetro ε_c y define los criterios de éxito, fallo y revisión teórica del marco TAE.

**Palabras clave:** Teoría del Aprendizaje por Excepción, entropía de permutación, detección de puntos de cambio, reconstrucción de atractor, EEG, reorganización neural, sistemas dinámicos, PELT

---

## 1. Contexto teórico y posición en el corpus TAE

### 1.1 Predicciones empíricas de TAE relevantes para TAE-E2

La TAE define el evento excepcional como aquel cuya magnitud supera el umbral de excepción ε_c del sistema en el estado atractor corriente. Formalmente, dado el parámetro de orden Ψ(t) —definido en TAE-F1 como funcional de complejidad dinámica con dominio de instanciación neural— el evento E es excepcional si y solo si:

> **‖δE‖ > ε_c(Ψ_t)**

donde δE es la distancia euclidiana en el espacio de estados entre la perturbación inducida y el centroide del atractor vigente, y ε_c es una función del estado interno del sistema, no una constante universal.

De esta definición se derivan tres predicciones empíricamente verificables en señales EEG:

**Predicción P1 (pico de PE):** En la ventana temporal inmediatamente posterior al cruce del umbral excepcional, la entropía de permutación local alcanza un máximo transitorio PE_max estadísticamente superior a la línea de base y a las perturbaciones sub-umbrales.

**Predicción P2 (transición de atractor):** Tras el pico PE_max, el sistema abandona el atractor previo A₀ y converge a un nuevo atractor A₁ cuantificable mediante reconstrucción en espacio de fase. La distancia de Hausdorff d_H(A₀, A₁) > δ_umbral define la reorganización genuina frente al simple retorno al estado previo.

**Predicción P3 (PE reducida post-excepción):** El atractor A₁ exhibe entropía de permutación media PE₁ < PE₀, reflejando mayor organización estructural del nuevo estado —la "excepción asimilada" en la ontología TAE.

Estas predicciones son directamente contrastables con herramientas de análisis de series temporales no lineales sobre EEG, y constituyen el objeto central de TAE-E2.

### 1.2 Relación con CPEA y el umbral ε_c no calibrado

El experimento TAE-E2 no es metodológicamente independiente del marco CPEA. La Arquitectura de Coherencia Predictiva EEG-AGI (CPEA) postula que tanto los sistemas neurales biológicos como los sistemas AGI procesan la información excepcional mediante mecanismos funcionalmente análogos de reorganización estructural. TAE-E2 provee la base empírica biológica sobre la cual calibrar ε_c en sistemas neurales humanos —una laguna identificada en el análisis de vulnerabilidades del corpus TAE realizado previamente. La calibración empírica de ε_c en señales EEG bajo condiciones controladas constituye, por tanto, un prerequisito para la instanciación de Ψ_AGI formalizada en TAE-F2.

---

## 2. Selección y caracterización de los datasets

### 2.1 PhysioNet EEG Motor Movement/Imagery Dataset (EEGMMI)

**Descripción estructural:** 109 sujetos, 64 canales EEG, 160 Hz de muestreo, tareas de movimiento real e imaginado de extremidades superiores e inferiores, con condiciones de reposo intercaladas. El marcado temporal de los eventos motores es preciso al nivel de milisegundos, lo que permite el anclaje temporal de las ventanas de análisis.

**Relevancia TAE:** Las tareas de imagery motora representan un caso privilegiado para TAE-E2 porque el evento excepcional —la transición entre estado de reposo y planificación motora imaginada— está estrictamente controlado externamente y es reproducible. La señal es técnicamente limpia (alta SNR, muestreo homogéneo) y la comunidad científica ha establecido líneas de base robustas de potencia espectral y entropía para estas transiciones, lo que facilita la detección del perfil PE bifásico TAE sobre fondo bien caracterizado.

**Limitación principal:** El evento "excepcional" en este dataset es inducido externamente por instrucción experimental, no emergente de la dinámica interna del sujeto. Esto implica que ε_c no puede estimarse de forma puramente endógena; se requieren procedimientos de normalización inter-sujeto para separar la respuesta excepcional de la respuesta motora ordinaria.

**Peso metodológico en TAE-E2:** Dataset primario de validación. La homogeneidad técnica y el tamaño muestral (n=109) permiten análisis estadísticos con potencia adecuada para las comparaciones entre estados P1, P2 y P3.

### 2.2 DEAP Dataset (Database for Emotion Analysis using Physiological Signals)

**Descripción estructural:** 32 sujetos, 32 canales EEG (+ señales periféricas: GSR, EMG, temperatura, plethysmografía), 512 Hz de muestreo, paradigma de video musical con valoraciones de valencia y excitación emocional en escala continua (1–9). Cada sujeto observa 40 fragmentos de vídeo de 60 segundos.

**Relevancia TAE:** DEAP ofrece la posibilidad única de identificar eventos excepcionales de naturaleza emocional endógena: momentos en los que la respuesta afectiva del sujeto cruza umbrales de alta valencia/excitación no anticipados. La correlación entre picos de excitación autoevaluada y el perfil PE del EEG permite contrastar si los estados afectivos intensos —candidatos naturales a "excepciones" en el espacio emocional— producen el perfil dinámico TAE. La disponibilidad de señales periféricas actúa como canal de verificación cruzada del estado excepcional: un pico de conductancia galvánica simultáneo al pico PE del EEG fortalece la interpretación TAE.

**Limitación principal:** La resolución temporal del marcado emocional (valoraciones discretas al final del fragmento) es insuficiente para el anclaje temporal milimétrico necesario en TAE-E2. Se requiere una estrategia de segmentación basada en la variabilidad intra-fragmento del EEG en lugar del marcado externo, lo que introduce incertidumbre en la identificación del instante t_exc del evento excepcional.

**Peso metodológico en TAE-E2:** Dataset secundario para análisis exploratorio de excepción emocional. Las métricas derivadas son de carácter preliminar y orientativo; las inferencias causales están condicionadas al desarrollo de estrategias de marcado temporal endógeno.

### 2.3 Temple University EEG Corpus (TUEG)

**Descripción estructural:** El mayor corpus EEG clínico de acceso abierto, con más de 15.000 sesiones de aproximadamente 1.400 sujetos, 19–256 canales, diversas tasas de muestreo (250–1000 Hz), incluyendo registros de pacientes con epilepsia, depresión, esquizofrenia y sujetos control. Las subcolecciones más relevantes para TAE-E2 son el Temple University Seizure Corpus (TUSC) y el Temple University Abnormal EEG Corpus (TUAB).

**Relevancia TAE:** Las crisis epilépticas representan el caso más extremo de reorganización dinámica cerebral accesible empíricamente. La secuencia ictus/pre-ictal/ictal/post-ictal es, desde la perspectiva TAE, una secuencia de excepción de alta intensidad: el sistema cruza ε_c masivamente, experimenta la reorganización más dramática cuantificable (el pico de sincronización ictus), y converge a un estado post-ictal cuya firma entrópica es consistente con PE₁ < PE₀. La literatura existente —incluyendo los trabajos de Mammone et al. sobre entropía de permutación espacio-temporal en epilepsia de ausencia— muestra que la secuencia libre-de-crisis → pre-ictal → ictal produce una reducción monotónica de PE que es parcialmente homóloga a la predicción P3 de TAE.

**Limitación principal:** La epilepsia implica un mecanismo patológico de sincronización neuronal masiva que puede no ser representativo de la excepción TAE en sistemas sanos. Existe el riesgo de que el perfil PE epiléptico sea un caso extremo y no generalizable de la firma TAE. El uso de TUAB (sujetos con EEG anormal no epiléptico) puede ofrecer un espacio intermedio más pertinente para contrastar las predicciones en sistemas neurales que operan cerca del umbral excepcional sin cruzarlo de forma patológica.

**Peso metodológico en TAE-E2:** Dataset terciario de contraste extremo. Su función principal es establecer los límites superiores del perfil PE bifásico y verificar si la firma TAE se mantiene cualitativamente en excepción de máxima intensidad o si el mecanismo epiléptico diverge del modelo TAE.

---

## 3. Pipeline metodológico de cuatro etapas

### Etapa I: Preprocesamiento adaptativo

El preprocesamiento opera de forma diferenciada en cada dataset para preservar las características dinámicas relevantes para TAE sin introducir artefactos de filtrado que distorsionen el perfil entrópico.

Para EEGMMI: filtrado de banda (1–40 Hz, Butterworth de orden 4 con zero-phase filtering), rereferenciado al promedio, eliminación de artefactos oculares mediante ICA (Independent Component Analysis) con criterio de kurtosis > 3σ, segmentación en épocas de 4 segundos ancladas al marcador de evento motor con 1 segundo de pre-estímulo como ventana de línea de base.

Para DEAP: downsampling a 128 Hz (desde 512 Hz) para reducir el coste computacional de PELT sin pérdida de información en las bandas de interés TAE (theta 4–8 Hz, alpha 8–13 Hz, beta 13–30 Hz), filtrado de artefactos musculares (EMG notch a 50 Hz y armónicos), normalización z-score por canal y por sesión para compensar la variabilidad inter-sujeto de impedancias.

Para TUEG/TUSC: uso de los preprocesados estándar del corpus cuando estén disponibles; para registros clínicos crudos, aplicación del pipeline de la Temple University Signal Processing Library (TUSPIL) con su protocolo de rechazo de artefactos documentado.

### Etapa II: Entropía de permutación en ventana deslizante

La entropía de permutación (PE) se calcula siguiendo el algoritmo original de Bandt & Pompe (2002) con las siguientes parametrizaciones derivadas de la revisión de la literatura:

- **Dimensión de embedding m = 5:** Captura patrones temporales de orden suficiente para distinguir dinámica neuronal compleja de ruido, sin exceder la longitud mínima de ventana viable (m! = 120 patrones ordinales posibles requieren al menos 5·m = 25 muestras por ventana para estimación fiable).
- **Lag temporal τ = 1/f_dominante:** Adaptativamente ajustado a la frecuencia dominante local estimada por la transformada de Hilbert-Huang, permitiendo que τ capture un ciclo completo de la oscilación relevante sin supresión artificiosa de la dinámica de banda.
- **Ventana deslizante L = 2 segundos con paso de 0.25 segundos:** Resolución temporal de 250 ms suficiente para capturar la dinámica transitoria del pico PE_max postulado en P1, manteniendo la estacionariedad local necesaria para la estimación válida de PE.

La PE se normaliza como PE_norm = PE/log₂(m!) para comparabilidad entre sujetos y datasets. Para el análisis multiscala (MSPE), se aplican factores de escala s ∈ {1, 2, 4, 8} mediante downsampling coarse-graining, siguiendo la metodología de Hou et al. (2021) que mostró mayor sensibilidad de MSPE respecto a PE monoscala para discriminar transiciones sutiles entre estados.

### Etapa III: Detección de puntos de cambio mediante PELT

El algoritmo PELT (Pruned Exact Linear Time, Killick et al., 2012) se aplica sobre la serie temporal PE_norm(t) para identificar los instantes t_CP₁ y t_CP₂ que delimitan las tres fases del evento TAE:

1. **Fase pre-excepción:** PE_norm en rango de línea de base [PE₀ ± σ₀]
2. **Fase de pico (excepción activa):** [t_CP₁, t_CP₂] con PE_norm > PE₀ + 2σ₀
3. **Fase post-excepción:** PE_norm convergiendo a PE₁ < PE₀

La función de coste empleada en PELT es la verosimilitud gaussiana (L2) para los cambios en media; complementariamente se aplica la función de coste de cambios en varianza (CostRBF) para capturar transiciones de estado que no se manifiestan como cambios de media sino como cambios de dispersión —un caso previsto en el modelo TAE cuando la excepción genera aumento de variabilidad dinámica antes del reencuadre del atractor.

El parámetro de penalización β de PELT se calibra mediante el criterio BIC (Bayesian Information Criterion) aplicado sobre segmentos de entrenamiento de cada dataset, siguiendo el procedimiento de validación cruzada de ruptures (biblioteca Python, Truong et al., 2020).

La condición de detección positiva de firma TAE requiere: t_CP₁ < t_CP₂ (ordenación temporal correcta), duración de la fase de pico Δt = t_CP₂ - t_CP₁ ∈ [0.5, 10] segundos (coherente con los tiempos de reorganización sináptica documentados), y ΔPE = PE_post − PE_pre < −0.05 unidades normalizadas (asimetría post-excepción estadísticamente significativa).

### Etapa IV: Reconstrucción del atractor y caracterización topológica

Para cada sujeto en el que PELT detecta una firma positiva, se reconstruyen los atractores pre-excepción A₀ y post-excepción A₁ mediante el teorema de embedding de Takens aplicado a la serie EEG del canal más informativo (identificado por mayor varianza explicada en el análisis de componentes principales por segmento).

Los parámetros del embedding se estiman adaptativamente: el tiempo de retardo τ_Takens mediante el primer mínimo de la función de información mutua (FIM), y la dimensión de embedding d mediante el método de los falsos vecinos más próximos (FNN, Kennel et al., 1992).

La distancia entre atractores se cuantifica mediante la distancia de Hausdorff entre los conjuntos de puntos {A₀} y {A₁} en el espacio de fase reconstruido:

> **d_H(A₀, A₁) = max{sup_{a∈A₀} inf_{b∈A₁} ‖a-b‖, sup_{b∈A₁} inf_{a∈A₀} ‖b-a‖}**

Una reorganización genuina en términos TAE requiere d_H(A₀, A₁) > d_H(A₀, A₀_baseline), donde A₀_baseline se estima sobre un segmento de línea de base equivalente sin evento identificado. Esta comparación distingue la reorganización estructural real del desplazamiento estocástico esperado entre dos ventanas temporales cualesquiera.

---

## 4. Protocolo de calibración empírica de ε_c

La calibración de ε_c es el resultado metodológico más relevante de TAE-E2 para el corpus TAE, pues provee el valor numérico que CPEA y TAE-F2 necesitan como parámetro de entrada para sus instanciaciones en AGI.

El procedimiento de calibración opera en tres pasos:

**Paso 1 — Barrido de umbrales:** Para cada sujeto, se construye la distribución empírica de magnitudes de perturbación ‖δE‖ calculada en el espacio de fase reconstruido durante el período de línea de base. Se ajusta un modelo de mezcla gaussiana (GMM) de dos componentes para separar la distribución de perturbaciones ordinarias (componente de baja magnitud) de las perturbaciones candidatas a excepción (componente de alta magnitud). El umbral ε_c se inicializa como la media aritmética de las medias de ambos componentes.

**Paso 2 — Validación cruzada contra PELT:** El ε_c_inicial se valida verificando que el conjunto de eventos detectados por PELT como puntos de cambio de PE_norm corresponde en su mayoría (>70% de los casos) a perturbaciones con ‖δE‖ > ε_c_inicial. Si la tasa de correspondencia es inferior, ε_c se desplaza iterativamente hacia el percentil 90 de la distribución de perturbaciones hasta maximizar la concordancia.

**Paso 3 — Normalización inter-sujeto:** El ε_c individual se normaliza por la desviación estándar de la distribución de perturbaciones del sujeto para obtener ε_c_norm, una magnitud relativa comparable entre sujetos y datasets. La distribución de ε_c_norm sobre los n=109 sujetos de EEGMMI provee la primera estimación empírica de la variabilidad del umbral de excepción en sistemas neurales humanos sanos.

---

## 5. Hipótesis falsificables y criterios de evaluación

### 5.1 Hipótesis principal (H_TAE-E2)

> *Los eventos excepcionales identificados en los datasets EEG producen un perfil PE bifásico {PE_max → PE_post < PE_0} estadísticamente distinguible del perfil PE de los eventos sub-umbrales, con reorganización de atractor cuantificable mediante d_H(A₀, A₁) > d_H_baseline.*

**Criterio de confirmación:** H_TAE-E2 se considera empíricamente soportada si al menos el 60% de los eventos clasificados como excepcionales en EEGMMI presentan el perfil bifásico completo, con p < 0.01 en el test de Wilcoxon entre distribuciones PE_pre y PE_post.

**Criterio de falsificación:** H_TAE-E2 se considera falsificada si el perfil bifásico no se distingue estadísticamente del esperado por fluctuaciones aleatorias en series PE de eventos sub-umbrales emparejados por duración e intensidad. La falsificación implicaría revisar el mecanismo de excepción TAE —posiblemente desvinculando la firma entrópica del criterio ε_c como operacionalizador válido de "excepcionalidad" en el dominio neural.

### 5.2 Hipótesis auxiliares

**H_aux1 (especificidad de canal):** Los electrodos frontocentrales (Fz, FCz, Cz) mostrarán mayor intensidad del pico PE_max que los electrodos occipitales, coherentemente con la participación prefrontal en la evaluación de novedad y el procesamiento del error de predicción (análogo biológico al mecanismo de excepción TAE).

**H_aux2 (correlación multiseñal en DEAP):** En el dataset DEAP, el pico PE_max en EEG correlacionará positivamente (r > 0.4) con el pico de conductancia galvánica simultáneo, sugiriendo que la excepción TAE se manifiesta coherentemente a través de múltiples sistemas fisiológicos —predicción consistente con la concepción TAE de la excepción como evento sistémico no circunscrito a un subsistema aislado.

**H_aux3 (escalado en TUEG):** La distancia de Hausdorff d_H(A₀, A₁) será significativamente mayor en crisis epilépticas (TUSC) que en eventos motores (EEGMMI), mostrando que la firma TAE escala con la magnitud de la excepción —el caso epiléptico como excepción de orden de magnitud superior a ε_c.

---

## 6. Implementación computacional: arquitectura del pipeline

El pipeline TAE-E2 se implementa en Python 3.11 con las siguientes dependencias principales: MNE-Python (≥1.7) para la gestión de datos EEG y preprocesamiento, antropy para el cálculo de PE y MSPE, ruptures para PELT, scikit-learn para GMM y validación cruzada, giotto-tda para análisis topológico del atractor (homología persistente como complemento a la distancia de Hausdorff), y matplotlib/seaborn para la visualización de los perfiles PE temporales.

La arquitectura modular del pipeline separa estrictamente las etapas: cada etapa recibe como entrada el output serializado de la etapa anterior (formato HDF5), lo que permite la ejecución independiente y el depurado aislado de cada componente. El código se publica en el repositorio github.com/papayaykware con documentación de parámetros, ejemplos de ejecución en subsets reducidos de EEGMMI y resultados preliminares sobre 10 sujetos piloto.

---

## 7. Limitaciones metodológicas y líneas de revisión

**Limitación L1 — Causalidad vs. correlación:** El protocolo TAE-E2, por su naturaleza observacional sobre datasets preexistentes, no puede establecer causalidad entre el evento excepcional y la reorganización del atractor. La correlación temporal entre pico PE y reorganización de A₀→A₁ es evidencia consistente con TAE pero no la confirma en sentido estricto. TAE-E3 —experimento de estimulación controlada— será necesario para el paso causal.

**Limitación L2 — Definición operacional del evento excepcional:** En EEGMMI, el evento excepcional se define externamente por el marcador de tarea. Esta operacionalización es conveniente pero potencialmente circular: no garantiza que todos los marcadores correspondan a eventos que superen ε_c desde la perspectiva del sistema neural del sujeto. Sujetos con alta familiaridad con la tarea pueden procesar el evento como rutinario, reduciendo o eliminando la firma TAE esperada. El análisis de la variabilidad inter-sujeto en el perfil PE permitirá estratificar los resultados según el grado de "novedad efectiva" del evento para cada sujeto.

**Limitación L3 — Dimensionalidad del espacio de fase:** La reconstrucción del atractor por embedding de Takens se aplica sobre series univariadas (un canal EEG). El sistema neural es intrínsecamente multivariado y la dinámica del atractor en el espacio completo de 64 dimensiones (64 canales) puede diferir cualitativamente del atractor reconstruido desde un único canal. El análisis de embedding multivariado (MVTE, Multivariate Takens Embedding) queda propuesto como extensión metodológica en TAE-E2b.

---

## 8. Conexión con el roadmap TAE y proyecciones hacia TAE-E3

TAE-E2 ocupa una posición central en el roadmap de formalización experimental del corpus TAE. Su relación con los hitos previos y futuros se estructura como sigue:

Aguas arriba, TAE-F1 provee la definición formal del parámetro de orden Ψ cuya instanciación neural es la que TAE-E2 busca operar empíricamente. TAE-F2 formalizará Ψ_AGI para arquitecturas transformer, pero requiere el valor calibrado de ε_c_norm proveniente de TAE-E2 para establecer la analogía cuantitativa entre el umbral de excepción biológico y el umbral de reorganización representacional en modelos de lenguaje.

Aguas abajo, los resultados de TAE-E2 alimentan directamente a TAE-E3 (protocolo de estimulación TMS/tDCS para inducción experimental de excepción controlada), a CPEA-E1 (registro simultáneo EEG-fMRI durante interacción sujeto-AGI) y al trabajo de revisión teórica TAE-Rev1, que actualizará los parámetros del modelo TAE en función de los valores empíricos obtenidos.

La hipótesis de trabajo más especulativa —pero no por ello metodológicamente excluida— es que la firma PE bifásica TAE sea un invariante multiescala del procesamiento excepcional: presente en señales EEG individuales (TAE-E2), reproducible en dinámica de poblaciones neurales (TAE-E3), y homologable en la dinámica de activaciones de capas de atención en transformers durante el procesamiento de tokens excepcionales (TAE-F2/CPEA). Si esta invariancia se confirma, la TAE habría identificado un principio organizativo transversal de los sistemas de procesamiento complejo —biológicos y artificiales— cuya implicación teórica superaría ampliamente el alcance de cualquiera de sus experimentos individuales.

---

## Resumen de puntos clave

- **TAE-E2 es el primer experimento empírico del corpus TAE:** operacionaliza las predicciones de la Teoría del Aprendizaje por Excepción en señales EEG humanas mediante tres datasets públicos con pesos metodológicos diferenciados.
- **La firma TAE es una secuencia dinámica bifásica:** pico agudo de entropía de permutación (PE_max) seguido de transición a nuevo estado atractor con PE reducida y estabilizada (PE_post < PE_pre).
- **El pipeline opera en cuatro etapas encadenadas:** preprocesamiento adaptativo por dataset → PE multiscala en ventana deslizante → detección de puntos de cambio PELT → reconstrucción del atractor por embedding de Takens.
- **La calibración de ε_c es el resultado más estratégico:** provee la primera estimación empírica del umbral de excepción en sistemas neurales humanos, requerida como parámetro de entrada por CPEA y TAE-F2.
- **EEGMMI es el dataset primario:** n=109, marcado temporal preciso, líneas de base establecidas por la literatura y potencia estadística suficiente para las comparaciones PE bifásicas.
- **DEAP y TUEG son datasets secundario y terciario:** DEAP para excepción emocional endógena (con limitaciones de resolución temporal), TUEG/TUSC para contraste extremo en epilepsia.
- **Tres hipótesis falsificables:** H_TAE-E2 (perfil bifásico estadísticamente distinguible), H_aux1 (especificidad frontocental), H_aux2 (correlación multiseñal EEG-GSR en DEAP).
- **La limitación L2 (circularidad del marcador externo) es la más relevante** y justifica el diseño de TAE-E3 con estimulación controlada para el paso causal.
- **La conexión con TAE-F2 y CPEA** establece que los valores ε_c_norm obtenidos aquí son el nexo cuantitativo entre el modelo de excepción biológico y su homólogo en arquitecturas AGI.

---

## Referencias comentadas

**Bandt, C., & Pompe, B. (2002).** *Permutation entropy: A natural complexity measure for time series.* Physical Review Letters, 88(17), 174102.
→ Fuente primaria del algoritmo PE. Define los patrones ordinales de orden m y establece las propiedades teóricas de robustez frente a ruido no estacionario, directamente aplicables a señales EEG. Base indispensable de la Etapa II del pipeline TAE-E2.

**Killick, R., Fearnhead, P., & Eckley, I. A. (2012).** *Optimal detection of changepoints with a linear computational cost.* Journal of the American Statistical Association, 107(500), 1590–1598.
→ Artículo original del algoritmo PELT. La complejidad O(n) en promedio bajo condiciones de cambio uniformes lo hace viable para los volúmenes de datos EEGMMI y TUEG. La implementación en Python (biblioteca ruptures) es la utilizada en el pipeline TAE-E2.

**Kennel, M. B., Brown, R., & Abarbanel, H. D. I. (1992).** *Determining embedding dimension for phase-space reconstruction using a geometrical construction.* Physical Review A, 45(6), 3403.
→ Método FNN (Falsos Vecinos Más Próximos) para la estimación de la dimensión de embedding óptima en el teorema de Takens. Su implementación en la Etapa IV garantiza que el atractor reconstruido no esté sobredimensionado ni proyectado en dimensión insuficiente.

**Takens, F. (1981).** *Detecting strange attractors in turbulence.* In D. A. Rand & L. S. Young (Eds.), *Dynamical Systems and Turbulence* (Lecture Notes in Mathematics, vol. 898, pp. 366–381). Springer.
→ Teorema de embedding que fundamenta la Etapa IV. Garantiza que, bajo condiciones genéricas, el atractor reconstruido desde una serie univariada es topológicamente equivalente al atractor en el espacio de fases completo del sistema. Limitación relevante para TAE-E2: el "sistema" neural es de alta dimensión y las condiciones genéricas pueden no satisfacerse plenamente.

**Hou, F., et al. (2021).** *Changes in EEG permutation entropy in the evening and in the transition from wake to sleep.* Sleep, 44(4), zsaa226.
→ Demuestra que la entropía de permutación multiscala (MSPE) decrece significativamente durante la transición vigilia→sueño, con discriminación excelente entre estados. Proporciona el precedente más directo del perfil PE bifásico predicho por TAE en transiciones de estado neural, aunque en un contexto fisiológico (sueño) que difiere del contexto de excepción TAE.

**Mammone, N., et al. (2015).** *Permutation Jaccard distance-based hierarchical clustering to estimate EEG network dynamics: Application to mesial temporal lobe epilepsy.* IEEE Transactions on Neural Systems and Rehabilitation Engineering, 23(5), 731–741.
→ Análisis espacio-temporal de PE en epilepsia de ausencia. Los resultados —que muestran una transición gradual de desincronización de larga distancia hacia sincronización local progresiva precediendo al ictus— son parcialmente compatibles con el modelo TAE (la desincronización como estado pre-excepcional), aunque el mecanismo epiléptico añade dinámica patológica que complica la lectura TAE directa. Clave para el uso de TUEG como dataset terciario.

**Thorne, B., et al. (2022).** *Reservoir time series analysis: using the response of complex dynamical systems as a universal indicator of change.* Chaos: An Interdisciplinary Journal of Nonlinear Science, 32, 033109.
→ Propone el uso de redes de reservorio como indicadores universales de cambio dinámico en sistemas complejos, con aplicaciones en EEG y ECG. Relevante para TAE-E2 como metodología alternativa de detección de excepción que no depende de la estacionariedad local requerida por PE, y que podría complementar el pipeline PELT en TAE-E2b.

**Communictions Physics (2023).** *Network representations of attractors for change point detection.* 
→ Método de detección de puntos de cambio basado en redes de Markov del atractor en espacio de fase. Directamente pertinente para la Etapa IV: la "red del atractor" (attractor network) puede cuantificar los cambios dinámicos TAE de forma alternativa a la distancia de Hausdorff, con ventajas en la interpretabilidad topológica de la reorganización post-excepción.

**Goldberger, A. L., et al. (2000).** *PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals.* Circulation, 101(23), e215–e220.
→ Referencia fundacional de PhysioNet y el dataset EEGMMI. La arquitectura de acceso abierto y los estándares de marcado temporal de PhysioNet hacen de EEGMMI el dataset más reproducible para la validación independiente de TAE-E2 por terceros.

**Koelstra, S., et al. (2012).** *DEAP: A database for emotion analysis using physiological signals.* IEEE Transactions on Affective Computing, 3(1), 18–31.
→ Paper de referencia del dataset DEAP. Describe el protocolo experimental, las señales disponibles y las estrategias de valoración emocional. La correlación entre EEG y señales periféricas documentada en este trabajo provee el marco de validación cruzada para H_aux2 de TAE-E2.

---

*TAE-E2 · Corpus TAE · papayaykware.blogspot.com / github.com/papayaykware*
