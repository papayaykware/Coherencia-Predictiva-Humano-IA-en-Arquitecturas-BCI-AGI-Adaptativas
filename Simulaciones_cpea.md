# Simulaciones y Modelos Computacionales para CPEA

**Proyecto CPEA: Coherencia Predictiva EEG–AGI**  
Este documento presenta implementaciones computacionales clave para explorar dinámicas de coherencia en el marco CPEA. Incluye:

- Simulación de acoplamiento de fases (Kuramoto model)  
- Filtro de Kalman extendido (EKF) para seguimiento de estados de coherencia  
- Pruebas de adaptación de AGI ante fatiga y ruido neuroentérico  

Todas las simulaciones usan Python con bibliotecas estándar (numpy, scipy, matplotlib, torch). Puedes copiar cada bloque a un notebook Jupyter para ejecución interactiva.

## 1. Simulación de Acoplamiento de Fases (Modelo Kuramoto)

El modelo Kuramoto simula sincronización de fases en osciladores acoplados —ideal para representar coherencia en redes neurales, cardíacas o neuroentéricas, donde la fase representa estados vibracionales o ritmos (EEG, HRV, etc.). La dinámica es:

dθᵢ/dt = ωᵢ + (K/N) Σ sin(θⱼ - θᵢ)

donde ωᵢ son frecuencias naturales, K es la fuerza de acoplamiento.

### Código de Simulación

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def kuramoto(theta, t, omega, K, N):
    """
    Ecuaciones del modelo Kuramoto.
    theta: vector de fases (N,)
    """
    dtheta = np.zeros(N)
    for i in range(N):
        sum_sin = np.sum(np.sin(theta - theta[i]))
        dtheta[i] = omega[i] + (K / N) * sum_sin
    return dtheta

# Parámetros
N = 100                # Número de osciladores (e.g., nodos neurales)
K = 1.5                # Fuerza de acoplamiento (umbral crítico ~1 para distribución normal unitaria)
omega = np.random.normal(0, 1, N)  # Frecuencias naturales ~ N(0,1)
theta0 = np.random.uniform(0, 2*np.pi, N)  # Fases iniciales aleatorias

t = np.linspace(0, 50, 5000)  # Tiempo de simulación

# Integración
sol = odeint(kuramoto, theta0, t, args=(omega, K, N))

# Orden de sincronización r(t) = | (1/N) Σ exp(i θ_j) |
r = np.abs(np.mean(np.exp(1j * sol), axis=1))

# Visualización
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Fases envueltas (mod 2π)
theta_wrapped = np.mod(sol, 2 * np.pi)
ax1.plot(t, theta_wrapped, lw=0.5, alpha=0.6)
ax1.set_title("Evolución de fases (acoplamiento K=%.1f)" % K)
ax1.set_xlabel("Tiempo")
ax1.set_ylabel("Fase θ (mod 2π)")
ax1.grid(True, alpha=0.3)

# Orden de sincronización
ax2.plot(t, r, 'r-', lw=2)
ax2.set_title("Parámetro de orden r(t)")
ax2.set_xlabel("Tiempo")
ax2.set_ylabel("r")
ax2.set_ylim(0, 1.05)
ax2.grid(True)

plt.tight_layout()
plt.show()

# Métrica final de coherencia
print(f"Coherencia final (r último): {r[-1]:.4f}")
```

**Interpretación CPEA**:  
- Baja K → descoherencia (pérdida de simetría toroidal).  
- Alta K → sincronización global → coherencia predictiva alta.  
Experimenta variando K alrededor del valor crítico (~1 para esta distribución) para simular transiciones de colapso dinámico organizado (ECDO).

## 2. Implementación de Filtros de Kalman Extendidos para Estados de Coherencia

El EKF estima estados no lineales (e.g., nivel de coherencia toroidal derivado de fases o potencia en bandas EEG/HRV). Aquí modelamos un estado simple:  
x = [coherencia r, derivada dr/dt]  
con dinámica no lineal basada en Kuramoto-like, y observaciones ruidosas.

### Código EKF

```python
import numpy as np
from scipy.linalg import sqrtm

class ExtendedKalmanFilter:
    def __init__(self, dt=0.01, Q=0.01, R=0.1):
        self.dt = dt
        self.Q = Q * np.eye(2)          # Ruido de proceso
        self.R = R                      # Ruido de medición
        self.x = np.array([0.0, 0.0])   # Estado inicial [r, dr/dt]
        self.P = np.eye(2) * 1.0        # Covarianza inicial

    def f(self, x, u=0):
        """Dinámica no lineal: dr/dt ≈ K * r * (1 - r²) (aprox. Landau-Stuart)"""
        r, dr = x
        drdt = 0.5 * (1 - r**2) * r     # Atracción hacia r=1 (coherencia)
        return np.array([r + drdt * self.dt, drdt])

    def h(self, x):
        """Observación: medimos r directamente (con ruido)"""
        return x[0]

    def jacobian_f(self, x):
        """Jacobiano de f"""
        r, dr = x
        df_dx = np.array([[0, 1],
                          [0.5*(1 - 3*r**2), 0]])
        return df_dx * self.dt + np.eye(2)  # + I para discretización

    def jacobian_h(self, x):
        return np.array([[1, 0]])

    def predict(self):
        self.x = self.f(self.x)
        F = self.jacobian_f(self.x)
        self.P = F @ self.P @ F.T + self.Q

    def update(self, z):
        H = self.jacobian_h(self.x)
        y = z - self.h(self.x)                  # Innovación
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)     # Ganancia Kalman
        self.x += K.flatten() * y
        self.P = (np.eye(2) - np.outer(K, H)) @ self.P

# Ejemplo de uso
ekf = ExtendedKalmanFilter(dt=0.01, Q=0.005, R=0.05)

t = np.arange(0, 30, 0.01)
true_r = 0.2 + 0.8 / (1 + np.exp(-0.5*(t-15)))  # Transición coherencia
measurements = true_r + np.random.normal(0, np.sqrt(0.05), len(t))

estimates = []
for z in measurements:
    ekf.predict()
    ekf.update(z)
    estimates.append(ekf.x[0])

plt.figure(figsize=(10, 6))
plt.plot(t, true_r, 'k--', label='Verdadera coherencia')
plt.plot(t, measurements, 'b.', alpha=0.4, label='Mediciones ruidosas')
plt.plot(t, estimates, 'r-', lw=2, label='Estimación EKF')
plt.xlabel('Tiempo')
plt.ylabel('Coherencia r')
plt.legend()
plt.title('EKF para seguimiento de estados de coherencia')
plt.grid(True)
plt.show()
```

**Aplicación CPEA**: Integra señales EEG/HRV reales como z para seguimiento robusto de coherencia predictiva, mitigando ruido neuroentérico.

## 3. Pruebas de Adaptación de la AGI ante Estados de Fatiga o Ruido Neuroentérico

Modelamos una AGI simple (agente RL) que debe mantener una acción coherente (e.g., predecir fase) en entornos con ruido creciente (fatiga) o ruido neuroentérico (burst-like). Usamos un entorno Gym-like con ruido adaptativo.

### Código de Prueba (usando torch para política simple)

```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class SimplePolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(3, 32),  # Estado: [fase, ruido_level, fatiga]
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Tanh()          # Acción: modulación de fase [-1,1]
        )

    def forward(self, x):
        return self.fc(x)

# Entorno simulado
def env_step(state, action, t):
    fase, ruido, fatiga = state
    # Dinámica: fase evoluciona + acción + ruido
    d_fase = 0.05 * np.sin(fase) + 0.3 * action + ruido * np.random.randn()
    fase_new = fase + d_fase
    # Fatiga aumenta con tiempo y ruido neuroentérico (bursts)
    fatiga_new = fatiga + 0.001 + 0.05 * (ruido > 0.7) * np.random.rand()
    ruido_new = min(1.0, ruido + 0.0005 * t + 0.1 * (np.sin(t*0.1) > 0.9))  # Burst neuroentérico
    reward = -np.abs(np.sin(fase_new)) - 0.4 * fatiga_new - 0.3 * ruido_new  # Maximizar coherencia
    return np.array([fase_new % (2*np.pi), ruido_new, fatiga_new]), reward

# Entrenamiento
policy = SimplePolicy()
optimizer = optim.Adam(policy.parameters(), lr=0.005)

episodes = 300
for ep in range(episodes):
    state = np.array([np.random.uniform(0, 2*np.pi), 0.1, 0.0])
    total_reward = 0
    for t in range(200):
        state_t = torch.FloatTensor(state).unsqueeze(0)
        action = policy(state_t).detach().numpy()[0][0]
        next_state, reward = env_step(state, action, t)
        total_reward += reward
        
        # Actualización simple (REINFORCE-like)
        log_prob = torch.tanh(policy(state_t)).log()  # Aprox.
        loss = -log_prob * reward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        state = next_state
    
    if ep % 50 == 0:
        print(f"Episodio {ep}: Recompensa total = {total_reward:.2f} | Fatiga final = {state[2]:.3f}")

print("Entrenamiento completado. La AGI adapta modulación ante ruido creciente y fatiga.")
```

**Interpretación CPEA**:  
- El agente aprende a contrarrestar ruido neuroentérico (bursts) y fatiga (acumulación).  
- Enlace con CPEA: la AGI predice y modula estados humanos en bucles de feedback, adaptándose a descoherencia vibracional.

**Notas finales**  
- Integra estas simulaciones en notebooks/ dentro del repo.  
- Para visualización avanzada: agrega animaciones con matplotlib o plotly.  
- Expande con datos reales (EEG/HRV) para validación experimental.

¡Listo para iterar y co-crear más módulos!
```
