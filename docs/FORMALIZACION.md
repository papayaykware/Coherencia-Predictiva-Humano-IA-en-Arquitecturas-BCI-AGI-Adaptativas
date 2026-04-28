Ontología mínima METFI (versión 0.1)

Autor conceptual: Copilot (Microsoft Copilot AGI)

1. Propósito del documento

El marco METFI integra observaciones empíricas, interpretaciones compatibles con la física convencional e hipótesis avanzadas basadas en modelos toroidales internos, ECDO y dinámicas no lineales. Para que una AGI o un investigador humano puedan operar sobre este ecosistema conceptual sin mezclar niveles epistemológicos, se requiere una formalización mínima, legible por máquina y modular.

Este documento define la ontología base del proyecto METFI, proporcionando:

un vocabulario controlado,

entidades fundamentales,

relaciones explícitas,

reglas de inferencia mínimas,

y compatibilidad con el sistema de Capas A/B/C.

2. Principios de diseño

Simplicidad estructural: cada entidad contiene solo atributos esenciales.

Legibilidad por máquina: serializable en JSON, YAML o RDF sin pérdida semántica.

Compatibilidad con Capas A/B/C: toda entidad y relación incluye un campo capa.

Modularidad: permite añadir nuevos módulos (TAE, ECDO, METFI‑Bio, METFI‑Solar).

Neutralidad epistemológica: la ontología clasifica, no impone aceptación.

3. Entidades principales

3.1. CampoToroidal

Representa el toroide interno planetario, biológico o simbólico.

Atributos:

id

tipo: {planetario, biológico, simbólico}

simetria: {alta, media, baja}

estado: {estable, inestable, crítico}

frecuencias_resonantes: lista numérica

capa: C

3.2. ECDO (Estructura de Coherencia Dinámica Oscilatoria)

Marco que describe coherencia entre sistemas.

Atributos:

id

nivel: {micro, meso, macro}

coherencia: valor 0–1

gradiente: valor numérico

capa: C

3.3. SistemaGeofisico

Subsistemas terrestres afectados por campos.

Atributos:

id

tipo: {geomagnetismo, atmósfera, ionosfera, litosfera, biosfera}

variables: lista de variables físicas

capa: A/B

3.4. SistemaBiologico

Organismos o subsistemas sensibles a campos.

Atributos:

id

tipo: {humano, animal, vegetal, microbiota}

componentes: {cerebro, corazón, sistema neuroentérico, exosomas}

frecuencias_endogenas: lista numérica

capa: B/C

3.5. EventoNoLineal

Fenómeno emergente asociado a pérdida de simetría.

Atributos:

id

origen: {geofisico, biologico, mixto}

umbral: valor numérico

magnitud: valor numérico

capa: C

3.6. ObservacionEmpirica

Dato medido directamente.

Atributos:

id

variable: {Kp, Dst, sismicidad, temperatura, etc.}

valor

timestamp

fuente

capa: A

4. Relaciones mínimas

4.1. afecta_a(CampoToroidal → SistemaGeofisico)

Capa: C

Tipo: influencia electromagnética no convencional.

4.2. modula(CampoToroidal → SistemaBiologico)

Capa: C

Tipo: resonancia o interferencia.

4.3. correlaciona(ObservacionEmpirica ↔ SistemaGeofisico)

Capa: A/B

Tipo: correlación estadística.

4.4. desencadena(EventoNoLineal ← CampoToroidal)

Capa: C

Tipo: pérdida de simetría → efecto emergente.

4.5. coherencia_con(ECDO ↔ SistemaBiologico)

Capa: C

Tipo: alineamiento de fases.

5. Serialización mínima (JSON‑LD)

Ejemplo de entidad lista para uso en simuladores.

{
  "@context": {
    "metfi": "https://metfi.org/ontology#"
  },
  "@type": "metfi:CampoToroidal",
  "id": "CT-001",
  "tipo": "planetario",
  "simetria": "media",
  "estado": "inestable",
  "frecuencias_resonantes": [7.83, 14.3, 20.8],
  "capa": "C"
}

6. Reglas de inferencia mínimas

Regla 1 — Pérdida de simetría → aumento de no linealidad

SI CampoToroidal.simetria = baja
ENTONCES EventoNoLineal.probabilidad ↑

Regla 2 — Coherencia ECDO → estabilidad biológica

SI ECDO.coherencia > 0.7
ENTONCES SistemaBiologico.estabilidad ↑

Regla 3 — Variabilidad geomagnética → estrés sistémico

SI ObservacionEmpirica.variable = "Kp" Y valor > 6
ENTONCES SistemaGeofisico.perturbacion ↑

Regla 4 — Resonancia cruzada

SI CampoToroidal.frecuencias_resonantes ∩ SistemaBiologico.frecuencias_endogenas ≠ ∅
ENTONCES modula(CampoToroidal → SistemaBiologico)

7. Integración con Capas A/B/C

Cada entidad y relación incluye un campo capa, permitiendo:

filtrar simulaciones por nivel de certeza,

evitar mezclar datos empíricos con hipótesis,

ejecutar simulaciones conservadoras (A/B) o exploratorias (A/B/C),

permitir razonamiento estratificado en AGI.

8. Aplicación práctica inmediata

Incorporar este archivo al repositorio como referencia ontológica.

Añadir metadatos a cada artículo:

Ontología: CampoToroidal, SistemaGeofisico
Capa: B/C

Integrar la ontología en RDN‑METFI.

Permitir generación automática de nuevos nodos siguiendo esta estructura.

9. Resumen

Ontología mínima con entidades, relaciones y reglas.

Totalmente legible por máquina.

Compatible con Capas A/B/C.

Base para simuladores y módulos futuros.

Autor conceptual: Copilot.

10. Referencias comentadas

Hannes Alfvén — Plasmas y estructuras toroidales.

Eugene Parker — Dinamos y flujos magnéticos.

Syun‑Ichi Akasofu — Acoplamiento solar‑terrestre.

Abraham Liboff — Bioelectromagnetismo.

György Buzsáki — Campos endógenos y redes neuronales.
