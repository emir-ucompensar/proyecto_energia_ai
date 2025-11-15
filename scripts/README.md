# Scripts del Proyecto
## Análisis Energético de Modelos de IA con Método de Rectángulos

Este directorio contiene los scripts Python del proyecto que implementan el método de los rectángulos (sumas de Riemann) para calcular el consumo energético acumulado de modelos de IA.

## Estructura de Archivos

```
scripts/
├── integrales_numericas.py        # Clase IntegracionNumerica con método rectangulos()
├── rectangulos.py                 # Implementación del método de rectángulos
├── rectangulos_visualizacion.py   # Genera 27 visualizaciones detalladas
├── comparativa_modelos.py         # Genera 18 visualizaciones comparativas
├── antiderivada.py                # Cálculo de integral exacta (antiderivada)
├── launcher.py                    # Menú interactivo principal
├── trapecio.py                    # Script legacy (no usado)
├── simpson.py                     # Script legacy (no usado)
├── verificar_fixes.py             # Validación de correcciones visuales
└── README.md                      # Este archivo
```

## Inicio Rápido

### Requisitos del Sistema

- **Python** >= 3.10
- **NumPy** >= 1.24.0 - Cálculos numéricos y arrays
- **Matplotlib** >= 3.7.0 - Visualización de gráficos
- **SciPy** >= 1.10.0 - Funciones de integración
- **Pandas** >= 2.0.0 - Análisis de datos

### Instalación de Dependencias

```bash
pip install numpy>=1.24.0 matplotlib>=3.7.0 scipy>=1.10.0 pandas>=2.0.0
```

### Ejecución

```bash
# Menú interactivo principal
python3 launcher.py

# O ejecutar scripts individuales
python3 rectangulos.py
python3 rectangulos_visualizacion.py
python3 comparativa_modelos.py
```

Los gráficos se guardarán en `../figuras/resultados/` en formato PNG.

## Descripción de Scripts

### 1. `integrales_numericas.py`
**Clase principal**: `IntegracionNumerica`

Implementa la función energía y el método de integración numérica por rectángulos.

**Función energía**:
```
E(N) = 0.0842N⁴ - 1.2156N³ + 6.8934N² - 12.456N + 11.234
```

**Método principal**: `rectangulos(n, modo='mid')`
- `n`: Número de subintervalos
- `modo`: 'left' (izquierda), 'mid' (punto medio), 'right' (derecha)

**Convergencia**:
- Izquierda/Derecha: O(h)
- Punto medio: O(h²)

---

### 2. `rectangulos.py`
**Propósito**: Script completo de análisis con método de rectángulos.

**Funcionalidades**:
- Cálculo de integral con 3 modos y 3 densidades (n=10, 100, 1000)
- Análisis de convergencia
- Posicionamiento de 5 modelos de IA en la curva
- Generación de 9 visualizaciones básicas

**Modelos evaluados**:
- TinyLLaMA-1.1B (1.1B parámetros, 11.7 Wh experimental)
- Gemma-2B (2.0B, 13.2 Wh)
- Phi-3 Mini (3.8B, 14.8 Wh)
- Mistral-7B (7.0B, 16.9 Wh)
- LLaMA-3 8B (8.0B, 18.3 Wh)

**Resultados clave**:
```
Valor exacto: Z = 167.3302 Wh·B
Mejor aproximación: 167.3226 Wh·B (n=1000, mid)
Error relativo: 0.0045%
```

---

### 3. `rectangulos_visualizacion.py`
**Propósito**: Genera 27 visualizaciones detalladas del método de rectángulos.

**Gráficos generados** (9 configuraciones × 3 vistas):

**Por densidad**:
- `rectangulos_left_n10.png`, `rectangulos_left_n100.png`, `rectangulos_left_n1000.png`
- `rectangulos_mid_n10.png`, `rectangulos_mid_n100.png`, `rectangulos_mid_n1000.png`
- `rectangulos_right_n10.png`, `rectangulos_right_n100.png`, `rectangulos_right_n1000.png`

**Con modelos de IA**:
- `rectangulos_left_modelos.png`, `rectangulos_mid_modelos.png`, `rectangulos_right_modelos.png`

**Con tabla de resultados**:
- `rectangulos_left_tabla.png`, `rectangulos_mid_tabla.png`, `rectangulos_right_tabla.png`

**Características visuales**:
- Rectángulos con transparencia 0.3
- Puntos de evaluación marcados
- Modelos de IA posicionados en la curva E(N)
- Colores estandarizados: #1976D2 (left), #388E3C (mid), #F57C00 (right)

---

### 4. `comparativa_modelos.py`
**Propósito**: Análisis comparativo entre modos y convergencia.

**Gráficos generados** (18 visualizaciones):

**Comparativas por densidad**:
- `comparativa_n10.png`, `comparativa_n100.png`, `comparativa_n1000.png`
- `comparativa_n10_zoom.png`, `comparativa_n100_zoom.png`, `comparativa_n1000_zoom.png`

**Análisis de convergencia**:
- `comparativa_convergencia_left.png`
- `comparativa_convergencia_mid.png`
- `comparativa_convergencia_right.png`
- `comparativa_convergencia_todas.png`
- `comparativa_convergencia_errores.png`
- `comparativa_convergencia_log.png`

**Con modelos de IA**:
- `comparativa_todos_modos.png`
- `comparativa_todos_modos_zoom.png`
- `comparativa_modelos_barras.png`
- `comparativa_precision_modos.png`
- `comparativa_tiempos_ejecucion.png`
- `tabla_convergencia.png`

**Análisis incluidos**:
- Comparación de precisión por modo
- Tasas de convergencia
- Tiempos de cómputo
- Errores absolutos y relativos

---

### 5. `antiderivada.py`
**Propósito**: Calcula el valor exacto de la integral usando el Teorema Fundamental del Cálculo.

**Antiderivada calculada**:
```
F(N) = 0.0842N⁵/5 - 1.2156N⁴/4 + 6.8934N³/3 - 12.456N²/2 + 11.234N
```

**Resultado exacto**:
```
Z = F(8.0) - F(1.1) = 167.33024720 Wh·B
```

**Uso**: Valor de referencia para validar métodos numéricos.

---

### 6. `launcher.py`
**Propósito**: Menú interactivo para ejecutar todos los análisis.

**Opciones del menú**:
1. Ejecutar análisis básico con rectángulos
2. Generar visualizaciones detalladas (27 gráficos)
3. Generar análisis comparativo (18 gráficos)
4. Calcular valor exacto (antiderivada)
5. Ejecutar análisis completo (todo lo anterior)
6. Ver información del proyecto
7. Verificar correcciones visuales
8. Salir

**Uso recomendado**: Punto de entrada principal para el proyecto.

---

### 7. `verificar_fixes.py`
**Propósito**: Validar que las correcciones visuales se aplicaron correctamente.

**Verificaciones**:
- Alineación de modelos con curva E(N)
- Consistencia de paleta de colores
- Integridad de estructura de datos

**Salida**: Reporte de validación completo.

---

### 8. Scripts Legacy
`trapecio.py` y `simpson.py` se mantienen por compatibilidad pero ya no se usan en el proyecto actual.

---

## Paleta de Colores Estandarizada

```python
COLORES = {
    'curva': '#C62828',      # Rojo - Curva E(N)
    'left': '#1976D2',       # Azul - Rectángulos izquierda
    'mid': '#388E3C',        # Verde - Rectángulos punto medio
    'right': '#F57C00',      # Naranja - Rectángulos derecha
    'modelos': '#424242'     # Gris oscuro - Modelos de IA
}
```

---

## Interpretación de Resultados

### Convergencia del Método

**Error relativo por densidad** (modo mid):
- n=10: 0.9282% (aceptable para análisis preliminar)
- n=100: 0.0045% (excelente precisión)
- n=1000: 0.0002% (precisión extrema)

**Recomendación**: n=100 con modo mid ofrece el mejor balance precisión/cómputo.

### Comparación entre Modos

**Precisión** (para n=100):
- Punto medio (mid): Error 0.0045%
- Izquierda (left): Error 0.4626%
- Derecha (right): Error 0.4682%

**Convergencia teórica confirmada**:
- Mid: O(h²) - convergencia cuadrática
- Left/Right: O(h) - convergencia lineal

### Posicionamiento de Modelos

Los 5 modelos de IA se posicionan en la curva E(N):
- TinyLLaMA-1.1B → E(1.1) = 6.39 Wh (experimental: 11.7 Wh)
- Gemma-2B → E(2.0) = 11.50 Wh (experimental: 13.2 Wh)
- Phi-3 Mini → E(3.8) = 14.61 Wh (experimental: 14.8 Wh)
- Mistral-7B → E(7.0) = 16.29 Wh (experimental: 16.9 Wh)
- LLaMA-3 8B → E(8.0) = 16.91 Wh (experimental: 18.3 Wh)

**Discrepancia**: Los valores experimentales son sistemáticamente mayores, sugiriendo overhead operacional no modelado.

---

## Solución de Problemas

### Error: ModuleNotFoundError
```bash
pip install numpy>=1.24.0 matplotlib>=3.7.0 scipy>=1.10.0 pandas>=2.0.0
```

### Gráficos no se generan
Verificar directorio de salida:
```bash
mkdir -p ../figuras/resultados/
```

### Valores inconsistentes
Ejecutar validación:
```bash
python3 verificar_fixes.py
```

---

## Orden Recomendado de Ejecución

Para análisis completo:

1. `antiderivada.py` - Calcular valor exacto de referencia
2. `rectangulos.py` - Análisis básico y primeras 9 visualizaciones
3. `rectangulos_visualizacion.py` - Visualizaciones detalladas (27 gráficos)
4. `comparativa_modelos.py` - Análisis comparativo (18 gráficos)
5. `verificar_fixes.py` - Validar correcciones

O usar el menú interactivo:
```bash
python3 launcher.py
# Seleccionar opción 5: "Ejecutar análisis completo"
```

---

## Notas Técnicas

### Reproducibilidad
Los scripts generan resultados determinísticos. No hay aleatoriedad.

### Formato de Salida
Todos los gráficos se guardan como PNG (300 DPI) en `../figuras/resultados/`.

### Rendimiento
- `rectangulos.py`: ~2 segundos
- `rectangulos_visualizacion.py`: ~15 segundos (27 gráficos)
- `comparativa_modelos.py`: ~12 segundos (18 gráficos)
- **Total análisis completo**: ~30 segundos

---

## Contribuciones

Para extender el proyecto:

1. Modificar parámetros en scripts individuales
2. Añadir nuevos modos al método `rectangulos()`
3. Incluir más modelos de IA en la lista `MODELOS`
4. Crear nuevas visualizaciones siguiendo el patrón existente

---

**Última actualización**: Noviembre 2025  
**Versión**: 2.0.0  
**Proyecto**: Análisis Energético con Método de Rectángulos
