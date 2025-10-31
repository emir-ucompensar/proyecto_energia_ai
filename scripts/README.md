# Scripts de Análisis Gráfico
## Proyecto: Análisis Energético de Modelos de IA con Cálculo Integral

Este directorio contiene scripts Python modulares y documentados para generar todos los análisis gráficos del proyecto.

## [DIR] Estructura de Archivos

```
scripts/
├── config.py                              # Configuración centralizada
├── grafico_1_eficiencia_barras.py         # Comparación eficiencia energética
├── grafico_2_dispersion_tamano_consumo.py # Relación tamaño vs consumo
├── grafico_3_potencia_tiempo.py           # Perfiles de potencia temporal
├── grafico_4_pareto_tradeoff.py           # Análisis Pareto multi-objetivo
├── grafico_5_comparacion_metodos_numericos.py # Trapecio vs Simpson
├── grafico_6_area_bajo_curva.py           # Regresión y área Z
├── generar_todos_graficos.py              # Script maestro
└── README.md                              # Este archivo
```

## [RUN] Inicio Rápido

### [PKG] Instalación de Dependencias (NUEVO)

**Método 1: Script Python Interactivo (Recomendado)**

```bash
python3 instalar_dependencias.py
```

El script detecta automáticamente tu sistema y ofrece las mejores opciones:
- [OK] Crear entorno virtual (recomendado para desarrollo)
- [OK] Instalar con APT (Ubuntu/Debian, requiere sudo)
- [OK] Instalar con pip --user (sin sudo)

**Método 2: Script Bash (Rápido)**

```bash
chmod +x instalar_dependencias.sh
./instalar_dependencias.sh
```

**Método 3: Manual - Entorno Virtual**

```bash
# Crear entorno virtual
python3 -m venv ../venv

# Activar
source ../venv/bin/activate  # Linux/Mac
# ..\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install numpy>=1.24.0 scipy>=1.10.0 matplotlib>=3.7.0 pandas>=2.0.0
pip install psutil  # Opcional
```

**Método 4: APT (Ubuntu/Debian)**

```bash
sudo apt update
sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pandas
```

### Requisitos del Sistema

- **Python** >= 3.8
- **NumPy** >= 1.24.0 - Cálculos numéricos
- **SciPy** >= 1.10.0 - Integración numérica (trapezoid, simpson)
- **Matplotlib** >= 3.7.0 - Visualización
- **pandas** >= 2.0.0 - Análisis de datos y exportación CSV
- **psutil** (opcional) - Monitoreo del sistema

### Ejecución Individual

```bash
# Si usaste entorno virtual, activalo primero
source ../venv/bin/activate

# Navegar al directorio
cd scripts/

# Ejecutar un script específico
python grafico_1_eficiencia_barras.py
```

### Ejecución Completa

```bash
# Generar todos los gráficos automáticamente
python generar_todos_graficos.py
```

Los gráficos se guardarán en `../figuras/` en formatos PNG y PDF.

## [STATS] Descripción de Scripts

### 1. `config.py`
**Propósito**: Configuración centralizada de parámetros.

**Configurables**:
- Datos experimentales de modelos
- Duración de simulaciones
- Parámetros de métodos numéricos
- Configuración de visualización (colores, tamaños, DPI)
- Rutas de salida

**Uso**: Importado por todos los demás scripts.

```python
from config import MODELOS, TAMANO_FIGURA, DPI
```

---

### 2. `grafico_1_eficiencia_barras.py`
**Propósito**: Gráfico de barras comparativo de eficiencia energética (tokens/Wh).

**Salidas**:
- `grafico_1_eficiencia_barras.png`
- `grafico_1_eficiencia_barras.pdf`

**Parámetros configurables en `config.py`**:
- `MODELOS['eficiencia']`: Valores de eficiencia
- `COLORES`: Paleta de colores

**Métricas mostradas**:
- Eficiencia por modelo (tokens/Wh)
- Energía total consumida
- Promedio de eficiencia

---

### 3. `grafico_2_dispersion_tamano_consumo.py`
**Propósito**: Correlación entre tamaño del modelo y consumo energético con ajuste potencial.

**Salidas**:
- `grafico_2_dispersion_tamano_consumo.png`
- `grafico_2_dispersion_tamano_consumo.pdf`

**Análisis incluido**:
- Ajuste de curva potencial: E = a × N^b
- Cálculo de R²
- Coeficiente de correlación

**Parámetros configurables**:
- `MODELOS['parametros']`: Tamaños de modelos
- `MODELOS['energia_total']`: Consumos medidos

---

### 4. `grafico_3_potencia_tiempo.py`
**Propósito**: Simulación de perfiles de potencia GPU en el tiempo.

**Salidas**:
- `grafico_3_potencia_tiempo.png`
- `grafico_3_potencia_tiempo.pdf`

**Características**:
- Fase de warmup exponencial
- Oscilaciones por ciclos de carga
- Ruido estocástico realista
- Picos ocasionales de carga

**Parámetros configurables**:
- `DURACION_SIMULACION`: Duración total (default: 600s)
- `NUM_PUNTOS`: Resolución temporal (default: 600)
- `PERFIL_CONFIG`: Parámetros del modelo de potencia

**Modelo matemático**:
```
P(t) = P_nom × (1 - e^(-t/τ)) × (1 + A·sin(ωt) + ε(t))
```

---

### 5. `grafico_4_pareto_tradeoff.py`
**Propósito**: Análisis de Pareto para identificar configuraciones óptimas.

**Salidas**:
- `grafico_4_pareto_tradeoff.png`
- `grafico_4_pareto_tradeoff.pdf`

**Análisis**:
- Identificación de frente de Pareto
- Trade-off rendimiento vs consumo
- Clasificación de modelos dominados/óptimos

**Criterio Pareto**:
Un punto (E_i, T_i) es óptimo si no existe (E_j, T_j) tal que:
- E_j < E_i AND T_j > T_i

---

### 6. `grafico_5_comparacion_metodos_numericos.py`
**Propósito**: Evaluar precisión de métodos de integración numérica.

**Salidas**:
- `grafico_5_comparacion_metodos_numericos.png`
- `grafico_5_comparacion_metodos_numericos.pdf`

**Métodos evaluados**:
- Regla del Trapecio: O(h²)
- Regla de Simpson 1/3: O(h⁴)

**Análisis incluido**:
- Convergencia del error (escala log-log)
- Tiempo de cómputo
- Tabla de resultados numéricos

**Parámetros configurables**:
- `N_INTERVALOS`: Lista de subintervalos a probar
- `A_LIMITE_INFERIOR`, `B_LIMITE_SUPERIOR`: Límites de integración

---

### 7. `grafico_6_area_bajo_curva.py` **PRINCIPAL**
**Propósito**: Regresión, selección del modelo óptimo y cálculo del área bajo la curva Z.

**Salidas**:
- `grafico_6_area_bajo_curva.png`
- `grafico_6_area_bajo_curva.pdf`
- `resultados_ajuste.txt` (reporte detallado)

**Análisis completo**:
1. **Regresión**: Prueba 4 familias de funciones
   - Polinomial (grados 1-5)
   - Exponencial
   - Potencial
   - Logarítmica

2. **Selección**: Basada en R² máximo

3. **Integración definida**: Calcula área Z
   ```
   Z = ∫[a,b] f(x) dx
   ```

4. **Validación**: Análisis de residuos

**Parámetros configurables**:
- `GRADO_POLINOMIO_MAX`: Grado máximo polinomial (default: 5)
- `R2_MINIMO`: Umbral mínimo de R² (default: 0.80)
- `TIPOS_AJUSTE`: Familias de funciones a probar

---

### 8. `generar_todos_graficos.py`
**Propósito**: Script maestro que ejecuta todos los análisis secuencialmente.

**Uso**:
```bash
python generar_todos_graficos.py
```

**Características**:
- Ejecución automática de 6 scripts
- Manejo de errores con continuación opcional
- Resumen final de éxitos/fallos
- Verificación de dependencias

---

## [TOOL] Personalización de Parámetros

### Modificar Datos Experimentales

Editar `config.py`:

```python
MODELOS = {
    'nombres': ['Modelo1', 'Modelo2', 'Modelo3'],
    'parametros': [1.0, 3.0, 7.0],  # Billones
    'energia_total': [10.0, 15.0, 20.0],  # Wh
    # ... más campos
}
```

### Cambiar Configuración de Gráficos

```python
# Tamaño de figuras (pulgadas)
TAMANO_FIGURA = (14, 10)  # Default: (12, 8)

# Resolución
DPI = 600  # Default: 300

# Colores personalizados
COLORES = {
    'principal': '#FF5733',
    # ...
}
```

### Ajustar Parámetros de Simulación

```python
# Duración (segundos)
DURACION_SIMULACION = 1200  # Default: 600

# Puntos de muestreo
NUM_PUNTOS = 1200  # Default: 600

# Warmup time (segundos)
PERFIL_CONFIG = {
    'warmup_time': 60,  # Default: 30
    # ...
}
```

---

## [UP] Interpretación de Resultados

### Eficiencia Energética (Gráfico 1)
- **Valores altos** (>1500 tokens/Wh): Modelos muy eficientes
- **Valores medios** (800-1500): Eficiencia moderada
- **Valores bajos** (<800): Modelos menos eficientes

### R² en Regresión (Gráfico 6)
- **R² > 0.95**: Ajuste excelente
- **R² 0.80-0.95**: Ajuste bueno
- **R² < 0.80**: Ajuste pobre, considerar otro modelo

### Área bajo la Curva Z
Representa el consumo energético acumulado integrado sobre el rango de tamaños evaluados.

**Unidades**: Wh·B (watt-hora × billones de parámetros)

**Interpretación**:
- Métrica holística de consumo en el espectro completo
- Útil para benchmarking entre infraestructuras
- Permite comparaciones normalizadas

---

## Solución de Problemas

### Error: ModuleNotFoundError
```bash
pip install numpy scipy matplotlib
```

### Error: "config.py not found"
Asegúrate de ejecutar desde el directorio `/scripts/`:
```bash
cd scripts/
python grafico_X_nombre.py
```

### Gráficos no se generan
Verifica que existe el directorio de salida:
```bash
mkdir -p ../figuras/
```

### Advertencias de matplotlib
Agregar al inicio del script:
```python
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
```

---

## Dependencias Detalladas

```
numpy>=1.20.0       # Operaciones numéricas
scipy>=1.7.0        # Integración y optimización
matplotlib>=3.4.0   # Visualización
```

Instalación completa:
```bash
pip install numpy scipy matplotlib
```

---

## [TARGET] Orden Recomendado de Ejecución

Para generar el reporte completo en orden lógico:

1. `grafico_1_eficiencia_barras.py` - Visión general
2. `grafico_2_dispersion_tamano_consumo.py` - Correlaciones
3. `grafico_3_potencia_tiempo.py` - Dinámicas temporales
4. `grafico_4_pareto_tradeoff.py` - Optimización
5. `grafico_5_comparacion_metodos_numericos.py` - Validación matemática
6. `grafico_6_area_bajo_curva.py` - Análisis integral principal

O simplemente:
```bash
python generar_todos_graficos.py
```

---

## [NOTE] Notas Adicionales

### Reproducibilidad
Todos los scripts usan semilla aleatoria fija (`SEMILLA_ALEATORIA = 42` en `config.py`) para garantizar resultados reproducibles.

### Formatos de Salida
Por defecto, cada gráfico se guarda en:
- PNG (alta resolución, 300 DPI)
- PDF (vectorial, ideal para publicaciones)

Configurar en `config.py`:
```python
FORMATOS_EXPORTACION = ['png', 'pdf', 'svg']  # Añadir SVG
```

### Rendimiento
Todos los scripts se ejecutan en <5 segundos en hardware moderno. El script completo (`generar_todos_graficos.py`) tarda ~20-30 segundos.

---

## Contribuciones

Para extender los análisis:

1. Crear nuevo script `grafico_X_nombre.py`
2. Importar `config.py` para parámetros
3. Seguir estructura de funciones existentes:
   - `crear_grafico_X()`: Genera figura
   - `guardar_grafico()`: Exporta archivos
   - `main()`: Función principal

4. Añadir al `generar_todos_graficos.py`:
```python
SCRIPTS = [
    # ... scripts existentes
    'grafico_X_nombre.py',
]
```

---

## Soporte

Para problemas o preguntas:
1. Revisar esta documentación
2. Verificar configuración en `config.py`
3. Ejecutar scripts individualmente para aislar errores

---

## Licencia

Scripts desarrollados como parte del proyecto académico "Análisis Energético de Modelos de IA con Cálculo Integral".

Código abierto para fines educativos y de investigación.

---

**Última actualización**: Octubre 2025
**Versión**: 1.0
**Autor**: Proyecto Energía AI
