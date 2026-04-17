El **MVP (Minimum Viable Prototype) de CPEA-X**: un sistema pequeño pero **capaz de producir evolución de comportamiento inteligente**. La meta es que sea **implementable en ~1500–2500 líneas de Python**.

La idea es construir **4 módulos simples pero potentes**:

1️⃣ entorno persistente
2️⃣ agentes con cerebro
3️⃣ aprendizaje durante la vida
4️⃣ evolución entre generaciones

---

# Arquitectura mínima del prototipo

```text
CPEA-X-MVP
│
├── environment.py
├── agent.py
├── brain.py
├── evolution.py
├── culture.py (opcional en MVP)
└── simulation.py
```

---

# 1️⃣ Entorno (Environment)

Usaremos un **grid world persistente**.

Cada celda contiene:

```python
class Cell:
    food: float
    terrain: int
```

El mapa:

```python
class Environment:
    grid_size = 64
    food_regeneration = 0.01
    
    agents = []
    
    def step():
        regenerate_food()
        update_agents()
```

Propiedades importantes:

| elemento | función           |
| -------- | ----------------- |
| comida   | energía           |
| terreno  | navegación        |
| recursos | presión evolutiva |

---

## Observación del agente

Cada agente ve un **campo local**.

Ejemplo:

```python
vision = 5
```

Observación:

```python
observation = {
    "local_food",
    "local_agents",
    "energy",
}
```

Esto crea **limitación cognitiva realista**.

---

# 2️⃣ Agente

Cada agente tiene:

```python
class Agent:

    genome
    brain
    energy
    age
    position
```

---

## Acciones

Acciones discretas:

```python
actions = [
    MOVE_UP,
    MOVE_DOWN,
    MOVE_LEFT,
    MOVE_RIGHT,
    EAT,
    SIGNAL
]
```

---

## Ciclo de vida

```python
def step(self, observation):

    action = brain.forward(observation)

    execute(action)

    energy -= metabolism
```

---

# 3️⃣ Cerebro del agente

Usaremos un **cerebro pequeño pero evolutivo**.

Arquitectura:

```python
input → hidden → hidden → action
```

Ejemplo PyTorch:

```python
class Brain(nn.Module):

    def __init__(self, genome):

        self.net = nn.Sequential(
            nn.Linear(genome.input_size, genome.hidden),
            nn.ReLU(),
            nn.Linear(genome.hidden, genome.hidden),
            nn.ReLU(),
            nn.Linear(genome.hidden, genome.actions)
        )
```

---

## Genoma

Define arquitectura y parámetros.

```python
class Genome:

    hidden_size
    learning_rate
    curiosity
```

Mutación:

```python
def mutate(genome):

    genome.hidden_size += random.choice([-4,0,4])
    genome.learning_rate *= random.uniform(0.8,1.2)
```

---

# 4️⃣ Aprendizaje durante la vida

Los agentes pueden **aprender mientras viven**.

Regla simple:

```python
loss = reward_prediction_error
optimizer.step()
```

Reward:

```python
reward =
    food_eaten
    + survival_time
```

Esto combina:

* evolución
* aprendizaje

---

# 5️⃣ Evolución entre generaciones

Después de una simulación larga:

```python
generation_length = 2000 steps
```

Seleccionamos los mejores agentes.

Fitness:

```python
fitness =
    survival_time
    + food_collected
```

---

## Selección

```python
top_agents = select_top(population, 20%)
```

---

## Reproducción

```python
child_genome = crossover(parentA, parentB)
mutate(child_genome)
```

Luego creamos nuevos agentes.

---

# 6️⃣ Cultura (opcional en MVP)

Podemos añadir señales simples.

Acción:

```python
SIGNAL
```

Los agentes transmiten un número:

```python
signal_value = brain.output
```

Otros agentes lo observan.

Esto permite estudiar:

* comunicación emergente
* cooperación

---

# 7️⃣ Loop principal de simulación

Archivo:

```python
simulation.py
```

Bucle principal:

```python
env = Environment()

for generation in range(1000):

    population = create_population()

    for step in range(2000):

        env.step()

    fitness = evaluate(population)

    population = evolve(population)
```

---

# 8️⃣ Métricas que debes registrar

Para ver evolución real:

```python
average_survival
food_collected
policy_entropy
cooperation_rate
```

Visualizar:

```python
matplotlib
tensorboard
```

---

# 9️⃣ Qué deberías observar

Si funciona bien, en pocas generaciones aparecerán:

### etapa 1

movimiento eficiente

### etapa 2

búsqueda de comida

### etapa 3

evitación de otros agentes

### etapa 4

comportamientos cooperativos

---

# 10️⃣ Escala del MVP

Configuración inicial:

```python
agents = 200
grid = 64x64
steps_per_generation = 2000
generations = 500
```

Esto ya puede producir **evolución interesante**.

---

# 11️⃣ Cómo mantenerlo en ~2000 líneas

Aproximación:

| módulo        | líneas |
| ------------- | ------ |
| environment   | 300    |
| agent         | 200    |
| brain         | 200    |
| evolution     | 300    |
| simulation    | 200    |
| visualization | 200    |

Total aproximado:

**1400–1800 líneas**

---

# 12️⃣ Qué hace poderoso a este prototipo

Aunque sea pequeño, ya tiene:

✔ evolución
✔ aprendizaje
✔ multi-agente
✔ entorno persistente
✔ presión ecológica

Eso es suficiente para **comportamientos emergentes**.

---

y que se acercaría mucho a un **simulador de civilización artificial**.
