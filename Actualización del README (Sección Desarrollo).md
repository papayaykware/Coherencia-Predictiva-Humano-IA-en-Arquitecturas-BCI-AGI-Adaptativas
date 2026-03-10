## **1. Badges para README**

### **`README.md` (Sección de Badges - Inicio del archivo)**

```markdown
# Coherencia Predictiva Humano–IA en Arquitecturas BCI-AGI Adaptativas (CPEA)

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://pycqa.github.io/isort/)
[![Linting: flake8](https://img.shields.io/badge/linting-flake8-yellowgreen)](https://flake8.pycqa.org/)
[![Tests](https://img.shields.io/github/actions/workflow/status/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas/ci.yml?branch=main&label=tests)](https://github.com/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas/actions)
[![Coverage](https://img.shields.io/codecov/c/github/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas)](https://codecov.io/gh/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas)
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen)](docs/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxxx)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas/blob/main/notebooks/01_baseline_demo.ipynb)
[![GitHub stars](https://img.shields.io/github/stars/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas?style=social)](https://github.com/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas/stargazers)

**Repositorio piloto para explorar la coherencia predictiva entre EEG humano y respuestas de modelos AGI mediante un pipeline adaptativo BCI-AGI.**

</div>
```

## **2. Integración Continua (CI) con GitHub Actions**

### **`.github/workflows/ci.yml`**

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt  # Dependencias de desarrollo
    
    - name: Lint with flake8
      run: |
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Check formatting with black
      run: |
        black --check src/ notebooks/
    
    - name: Check import sorting with isort
      run: |
        isort --check-only --diff src/ notebooks/
    
    - name: Type check with mypy
      run: |
        mypy src/ --ignore-missing-imports
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src/ --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false
    
    - name: Test synthetic data generation
      run: |
        python -c "from src.data.generate_synthetic_eeg import SyntheticEEGGenerator; SyntheticEEGGenerator().save_sample_trials(5)"
    
    - name: Test pipeline execution
      run: |
        python src/pipeline/run_pipeline.py --mode baseline --trials 5 --save

  build-docker:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: false
        tags: cpea:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## **3. Archivos de Configuración para Estandarización**

### **`pyproject.toml`** (Configuración centralizada)

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "cpea"
version = "0.1.0"
description = "Coherencia Predictiva Humano-IA en Arquitecturas BCI-AGI Adaptativas"
readme = "README.md"
authors = [
    {name = "Papayaykware", email = "tu-email@ejemplo.com"},
]
license = {text = "Apache 2.0"}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
]
dependencies = [
    "numpy>=1.24.0",
    "scipy>=1.10.0",
    "matplotlib>=3.7.0",
    "mne>=1.4.0",
    "scikit-learn>=1.2.0",
    "requests>=2.28.0",
]
requires-python = ">=3.9"

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pre-commit>=3.0.0",
    "ipykernel>=6.0.0",
    "jupyter>=1.0.0",
]
docs = [
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.0.0",
    "nbsphinx>=0.8.0",
]

[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
known_first_party = ["src"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
disallow_untyped_defs = true
disallow_any_unimported = false
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers"
testpaths = [
    "tests",
]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if __name__ == .__main__.:",
    "raise AssertionError",
    "raise NotImplementedError",
    "except ImportError",
    "return None",
    "pass",
]
```

### **`requirements-dev.txt`**

```txt
# Development dependencies
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
pre-commit>=3.0.0
ipykernel>=6.0.0
jupyter>=1.0.0
sphinx>=6.0.0
sphinx-rtd-theme>=1.0.0
nbsphinx>=0.8.0
```

## **4. Pre-commit Hooks**

### **`.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203,W503"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        args: ["--ignore-missing-imports"]
        additional_dependencies: [types-requests]

  - repo: https://github.com/nbQA-dev/nbQA
    rev: 1.7.0
    hooks:
      - id: nbqa-black
        args: ["--nbqa-mutate"]
      - id: nbqa-isort
        args: ["--nbqa-mutate", "--profile=black"]
      - id: nbqa-flake8
        args: ["--max-line-length=88", "--extend-ignore=E203,W503"]
```

## **5. Scripts de Utilidad**

### **`scripts/setup_dev_env.sh`**

```bash
#!/bin/bash
# Script para configurar entorno de desarrollo

echo "🔧 Configurando entorno de desarrollo para CPEA..."

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python -m venv venv
source venv/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
echo "🔨 Instalando pre-commit hooks..."
pre-commit install

# Crear directorios necesarios
echo "📁 Creando estructura de directorios..."
mkdir -p data/raw data/processed data/sample_eeg
mkdir -p results logs models/checkpoints

# Generar datos sintéticos de prueba
echo "🧪 Generando datos sintéticos de prueba..."
python -c "from src.data.generate_synthetic_eeg import SyntheticEEGGenerator; SyntheticEEGGenerator().save_sample_trials(10)"

echo "✅ Entorno de desarrollo configurado correctamente"
echo ""
echo "Para activar el entorno: source venv/bin/activate"
echo "Para ejecutar tests: pytest tests/"
echo "Para formatear código: black src/ notebooks/"
```

### **`Makefile`** (Comandos comunes)

```makefile
.PHONY: help install dev test lint format clean docker-run

help:
	@echo "Comandos disponibles:"
	@echo "  make install    Instalar dependencias"
	@echo "  make dev        Instalar dependencias de desarrollo"
	@echo "  make test       Ejecutar tests"
	@echo "  make lint       Ejecutar linters"
	@echo "  make format     Formatear código"
	@echo "  make clean      Limpiar archivos temporales"
	@echo "  make docker-run Ejecutar en Docker"

install:
	pip install -r requirements.txt

dev: install
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov=src/

lint:
	flake8 src/ notebooks/
	mypy src/ --ignore-missing-imports
	black --check src/ notebooks/
	isort --check-only src/ notebooks/

format:
	black src/ notebooks/
	isort src/ notebooks/
	nbqa black notebooks/
	nbqa isort notebooks/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

docker-run:
	docker build -t cpea .
	docker run --rm -v $(PWD)/data:/app/data cpea python src/pipeline/run_pipeline.py --mode baseline --trials 20
```

## **6. Tests Unitarios**

### **`tests/test_eeg_processor.py`**

```python
"""Tests para el procesador de EEG."""

import numpy as np
import pytest
from src.utils.eeg_processor import EEGProcessor


class TestEEGProcessor:
    """Suite de tests para EEGProcessor."""
    
    @pytest.fixture
    def processor(self):
        """Fixture que provee un procesador EEG con configuración por defecto."""
        return EEGProcessor(fs=256.0, lowcut=8.0, highcut=30.0)
    
    @pytest.fixture
    def sample_eeg(self):
        """Fixture que genera datos EEG sintéticos para pruebas."""
        np.random.seed(42)
        n_channels, n_samples = 4, 512  # 2 segundos a 256Hz
        return np.random.randn(n_channels, n_samples)
    
    def test_initialization(self, processor):
        """Test de inicialización correcta."""
        assert processor.fs == 256.0
        assert processor.lowcut == 8.0
        assert processor.highcut == 30.0
        assert hasattr(processor, 'b')
        assert hasattr(processor, 'a')
    
    def test_preprocess_output_shape(self, processor, sample_eeg):
        """Test que el preprocesamiento mantiene la forma."""
        processed = processor.preprocess(sample_eeg)
        assert processed.shape == sample_eeg.shape
    
    def test_preprocess_normalization(self, processor, sample_eeg):
        """Test que la normalización funciona."""
        processed = processor.preprocess(sample_eeg)
        
        # Cada canal debe tener media ~0 y std ~1
        for ch in range(processed.shape[0]):
            assert np.abs(np.mean(processed[ch, :])) < 0.1
            assert np.abs(np.std(processed[ch, :]) - 1.0) < 0.1
    
    def test_feature_extraction_shape(self, processor, sample_eeg):
        """Test que la extracción de features produce vector de longitud esperada."""
        processed = processor.preprocess(sample_eeg)
        features = processor.extract_features(processed)
        
        # 4 canales * 3 features (mu, beta, ratio) + asimetría = 13
        assert len(features) == 13
    
    def test_feature_extraction_values(self, processor, sample_eeg):
        """Test que los features tienen valores plausibles."""
        processed = processor.preprocess(sample_eeg)
        features = processor.extract_features(processed)
        
        # Todos los features deben ser finitos
        assert np.all(np.isfinite(features))
        
        # Las potencias deben ser no negativas
        mu_powers = features[0::3]  # Índices 0, 3, 6, 9
        beta_powers = features[1::3]  # Índices 1, 4, 7, 10
        assert np.all(mu_powers >= 0)
        assert np.all(beta_powers >= 0)
    
    def test_load_from_npy(self, processor, tmp_path):
        """Test de carga de archivos .npy."""
        # Crear archivo temporal
        test_data = np.random.randn(4, 256)
        test_path = tmp_path / "test_eeg.npy"
        np.save(test_path, test_data)
        
        # Cargar y verificar
        loaded = processor.load_from_npy(test_path)
        np.testing.assert_array_equal(loaded, test_data)
```

### **`tests/test_icp.py`**

```python
"""Tests para el Índice de Coherencia Predictiva."""

import numpy as np
import pytest
from src.metrics.icp import IndiceCoherenciaPredictiva


class TestICP:
    """Suite de tests para ICP."""
    
    @pytest.fixture
    def icp_calculator(self):
        """Fixture con configuración por defecto."""
        return IndiceCoherenciaPredictiva(pesos=[0.4, 0.3, 0.3])
    
    def test_initialization(self):
        """Test de inicialización con diferentes pesos."""
        icp = IndiceCoherenciaPredictiva(pesos=[0.5, 0.3, 0.2])
        assert icp.w_acc == 0.5
        assert icp.w_mi == 0.3
        assert icp.w_error == 0.2
        
        # Test que los pesos suman 1
        with pytest.raises(AssertionError):
            IndiceCoherenciaPredictiva(pesos=[0.5, 0.5, 0.5])
    
    def test_perfect_coherence(self, icp_calculator):
        """Test con coherencia perfecta."""
        y_true = np.array([0, 1, 0, 1])
        y_pred_class = np.array([0, 1, 0, 1])
        eeg_features = np.random.randn(4, 10)
        agi_embeddings = np.random.randn(4, 64)
        y_pred_prob_agi = np.array([0.0, 1.0, 0.0, 1.0])
        
        result = icp_calculator.calcular(
            y_true, y_pred_class, eeg_features, agi_embeddings, y_pred_prob_agi
        )
        
        # Accuracy debe ser 1.0
        assert result['componentes']['accuracy'] == 1.0
        
        # ICP debe ser alto (pero no necesariamente 1.0 por MI y error)
        assert result['icp'] > 0.7
    
    def test_random_coherence(self, icp_calculator):
        """Test con coherencia aleatoria (chance level)."""
        np.random.seed(42)
        n_trials = 100
        
        y_true = np.random.randint(0, 2, n_trials)
        y_pred_class = np.random.randint(0, 2, n_trials)
        eeg_features = np.random.randn(n_trials, 10)
        agi_embeddings = np.random.randn(n_trials, 64)
        y_pred_prob_agi = np.random.rand(n_trials)
        
        result = icp_calculator.calcular(
            y_true, y_pred_class, eeg_features, agi_embeddings, y_pred_prob_agi
        )
        
        # Accuracy debe ser ~0.5
        assert np.abs(result['componentes']['accuracy'] - 0.5) < 0.1
        
        # ICP debe ser bajo
        assert result['icp'] < 0.6
    
    def test_icp_range(self, icp_calculator):
        """Test que ICP siempre está en [0, 1]."""
        np.random.seed(42)
        
        for _ in range(10):
            n_trials = np.random.randint(5, 50)
            
            y_true = np.random.randint(0, 2, n_trials)
            y_pred_class = np.random.randint(0, 2, n_trials)
            eeg_features = np.random.randn(n_trials, 10)
            agi_embeddings = np.random.randn(n_trials, 64)
            y_pred_prob_agi = np.random.rand(n_trials)
            
            result = icp_calculator.calcular(
                y_true, y_pred_class, eeg_features, agi_embeddings, y_pred_prob_agi
            )
            
            assert 0 <= result['icp'] <= 1
            assert 0 <= result['componentes']['accuracy'] <= 1
            assert 0 <= result['componentes']['mutual_info'] <= 1
            assert 0 <= result['componentes']['agi_error'] <= 1
```

## **7. Actualización del README (Sección Desarrollo)**

Añade esta sección al README:

```markdown
## 👩‍💻 Desarrollo

### Configuración del entorno de desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas.git
cd Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas

# Ejecutar script de configuración (Linux/Mac)
bash scripts/setup_dev_env.sh

# O manualmente:
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

### Comandos útiles

```bash
# Formatear código
make format
# o
black src/ notebooks/
isort src/ notebooks/

# Ejecutar linters
make lint
# o
flake8 src/ notebooks/
mypy src/

# Ejecutar tests
make test
# o
pytest tests/ -v --cov=src/

# Limpiar archivos temporales
make clean
```

### Flujo de trabajo recomendado

1. **Antes de cada commit**: Los pre-commit hooks formatean y lintan automáticamente
2. **Antes de hacer push**: Ejecuta `make test` para asegurar que todo funciona
3. **CI Pipeline**: GitHub Actions verifica el código en múltiples Python versions

### Estándares de código

- **Formato**: Black (línea de 88 caracteres)
- **Imports**: isort con perfil black
- **Linting**: flake8 (ignorando E203, W503)
- **Tipos**: mypy (opcional pero recomendado)
- **Tests**: pytest con cobertura >80%
```
---
