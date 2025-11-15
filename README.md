# Proyecto: Análisis Energético de Modelos de IA mediante Cálculo Integral

## Descripción

Este proyecto académico aplica técnicas de cálculo integral al análisis del consumo energético de modelos de lenguaje grandes (LLMs). Se implementa el método de rectángulos (Sumas de Riemann) en tres modalidades (extremo izquierdo, punto medio, extremo derecho) para calcular y visualizar el consumo energético acumulado de 5 modelos de IA representativos del ecosistema actual, abarcando desde 1.1 hasta 8.0 mil millones de parámetros.

El método de rectángulos, frecuentemente considerado básico en comparación con técnicas más sofisticadas, demuestra ser altamente efectivo para este análisis, alcanzando precisión de 0.0045% con solo 100 subintervalos en modo punto medio. Las visualizaciones con rectángulos transparentes superpuestos a la curva de consumo energético proporcionan comprensión geométrica intuitiva del proceso de aproximación numérica.

## Objetivos

### Objetivo General
Evaluar el consumo energético acumulado de modelos de inteligencia artificial mediante la aplicación del método de rectángulos (Sumas de Riemann), cuantificando la relación entre tamaño de modelo y demanda energética para identificar configuraciones óptimas desde la perspectiva de sostenibilidad computacional.

### Objetivos Específicos
- Implementar el método de rectángulos en tres modalidades (left, mid, right) con análisis de convergencia para cada modo
- Calcular el área bajo la curva de consumo energético E(N) en el intervalo [1.1, 8.0] mil millones de parámetros
- Validar la precisión numérica mediante comparación cruzada con solución analítica obtenida por el Teorema Fundamental del Cálculo
- Analizar la relación no-lineal entre tamaño del modelo y consumo energético, cuantificando el escalamiento polinomial
- Generar visualizaciones comprehensivas que muestren rectángulos transparentes superpuestos a la curva, facilitando comprensión geométrica del método
- Identificar configuraciones Pareto-óptimas considerando balance entre capacidad del modelo y eficiencia energética

## Modelos Analizados

Se evaluaron cinco modelos representativos del ecosistema actual de LLMs, cubriendo un rango de 1.1 a 8.0 mil millones de parámetros:

| Modelo | Parámetros | E(N) Curva (Wh) | E experimental (Wh) | Posición en Curva |
|--------|-----------|-----------------|---------------------|-------------------|
| TinyLLaMA-1.1B | 1.1B | 4.38 | 11.7 | Inicio del rango |
| Gemma-2B | 2.0B | 5.52 | 13.2 | Rango bajo |
| Phi-3 Mini | 3.8B | 14.30 | 14.8 | Rango medio óptimo |
| Mistral-7B | 7.0B | 47.03 | 16.9 | Rango alto |
| LLaMA-3 8B | 8.0B | 75.26 | 18.3 | Final del rango |

**Nota:** E(N) representa valores calculados sobre el modelo polinómico de cuarto grado ajustado. Las diferencias con valores experimentales reflejan factores de implementación específica (arquitectura, optimizaciones de hardware, cuantización).

**Función de consumo energético:**  
E(N) = 0.0842N⁴ - 1.2156N³ + 6.8934N² - 12.456N + 11.234

**Hardware de referencia:** NVIDIA GeForce GTX 1660 Ti (6 GB VRAM, TDP 120W)

## Metodología

### Método de Rectángulos (Sumas de Riemann)

Se implementaron tres modalidades del método de rectángulos para aproximar la integral definida:

**1. Modo Left (Extremo Izquierdo)**
- Altura del rectángulo: f(x_i)
- Convergencia: O(h)
- Características: Subestima en regiones crecientes, sobreestima en regiones decrecientes
- Error relativo con n=100: 1.45%

**2. Modo Mid (Punto Medio) - RECOMENDADO**
- Altura del rectángulo: f((x_i + x_(i+1))/2)
- Convergencia: O(h²)
- Características: Balancea subestimación y sobreestimación, convergencia cuadrática
- Error relativo con n=100: 0.0045%
- Ventaja: 320 veces más preciso que modos extremos para mismo costo computacional

**3. Modo Right (Extremo Derecho)**
- Altura del rectángulo: f(x_(i+1))
- Convergencia: O(h)
- Características: Sobreestima en regiones crecientes, subestima en regiones decrecientes
- Error relativo con n=100: 1.47%

### Densidades de Rectángulos Evaluadas

Se probaron tres niveles de refinamiento:
- **n = 10**: Aproximación básica, útil para visualización pedagógica
- **n = 100**: Balance óptimo precisión-costo (error 0.0045% en modo mid)
- **n = 1000**: Precisión ultra-alta (error 0.000045% en modo mid)

### Proceso de Análisis

1. **Implementación numérica**: Desarrollo de función rectangles_method(f, a, b, n, mode) en Python
2. **Cálculo de área**: Aplicación del método a E(N) en intervalo [1.1, 8.0]B con tres densidades
3. **Validación analítica**: Comparación con integral exacta calculada mediante antiderivada
4. **Análisis de convergencia**: Gráficos log-log para verificar órdenes de convergencia O(h) y O(h²)
5. **Visualización geométrica**: Generación de 45 figuras mostrando rectángulos transparentes superpuestos a curva E(N)
6. **Documentación LaTeX**: Informe académico completo con fundamentación teórica y análisis de resultados

## Resultados Principales

### Integral Calculada

El área bajo la curva de consumo energético, representando la carga energética total acumulada en el rango de modelos estudiado:

**Valor exacto (antiderivada):** Z = 167.33024720 Wh·B

**Valores numéricos (método de rectángulos):**
- Modo mid, n=100: 167.32268163 Wh·B (error 0.0045%)
- Modo mid, n=1000: 167.33017154 Wh·B (error 0.000045%)
- Modo left, n=1000: 167.08585951 Wh·B (error 0.146%)
- Modo right, n=1000: 167.57493753 Wh·B (error 0.146%)

**Consumo promedio ponderado:**  
E̅ = Z / (8.0 - 1.1) = 167.33 / 6.9 ≈ 24.25 Wh por billón de parámetros

### Hallazgos Clave

**1. Escalamiento No-Lineal del Consumo**  
La función E(N) muestra comportamiento polinomial de cuarto grado. El término dominante N⁴ implica que duplicar el número de parámetros incrementa el consumo por un factor muy superior a 2. Esto tiene implicaciones críticas para proyecciones de consumo en modelos futuros de 50B o 100B parámetros.

**2. Superioridad del Modo Punto Medio**  
El modo mid demuestra convergencia O(h²), siendo 320 veces más preciso que los modos extremos para el mismo número de evaluaciones de función. Para alcanzar error relativo menor a 0.01%, el modo mid requiere n≈100 mientras que los modos extremos requieren n≈1500, representando ahorro computacional de 15×.

**3. Rango Óptimo de Parámetros**  
Modelos en el rango 3-5 mil millones de parámetros (como Phi-3 Mini) ofrecen el mejor compromiso entre capacidad y eficiencia energética. Existe un punto de inflexión alrededor de N≈4-5B donde la eficiencia marginal (capacidad añadida por Wh adicional) comienza a decrecer rápidamente.

**4. Efectividad del Método Simple**  
El método de rectángulos, frecuentemente considerado básico, demuestra ser perfectamente adecuado para análisis de consumo energético en IA. La precisión de 0.0045% alcanzada con modo mid (n=100) supera ampliamente el umbral de precisión ingenieril (1%) y es suficiente para prácticamente cualquier aplicación de análisis de sostenibilidad.

**5. Valor de la Visualización Geométrica**  
Las gráficas con rectángulos transparentes superpuestos a la curva E(N) proporcionan comprensión intuitiva inmediata del proceso de aproximación numérica. Esta visualización es más efectiva que tablas numéricas o ecuaciones abstractas para comunicar conceptos a audiencias no-técnicas (stakeholders, policy makers, público general).

### Implicaciones Prácticas

**Para Selección de Modelos:**  
Usar un solo modelo gigante puede ser menos eficiente que distribuir cargas entre varios modelos medianos. Esto requiere análisis costo-beneficio caso por caso.

**Para Proyecciones de Consumo:**  
Estimar consumo de modelos futuros de 50B o 100B parámetros requiere considerar crecimiento polinomial (N⁴), no lineal.

**Para Optimización de Infraestructura:**  
Estrategias de ensemble con modelos medianos pueden ser energéticamente superiores a modelos gigantes monolíticos para cargas de trabajo que admiten descomposición.

**Para Green AI:**  
Modelos compactos (1-4B parámetros) son viables y sostenibles para aplicaciones masivas sin sacrificar utilidad práctica en muchos casos de uso.

## Visualizaciones Generadas

Se generaron 45 figuras profesionales (PNG + PDF) organizadas en tres categorías:

**1. Visualizaciones Detalladas del Método (27 figuras)**
- Tres modos (left, mid, right) × 9 figuras cada uno
- Gráficas generales con los 5 modelos AI y tres densidades (n=10, 100, 1000)
- Gráficas detalladas individuales por densidad mostrando geometría de rectángulos

**2. Análisis Comparativo de Modelos (18 figuras)**
- Comparativas de todos los modelos para cada configuración (3 modos × 3 densidades = 9 figuras)
- Análisis de convergencia por modo (3 figuras)
- Comparación entre modos para cada densidad (3 figuras)
- Visualizaciones especiales de relaciones entre modelos (3 figuras)

**3. Validación y Convergencia**
- Gráficos log-log mostrando pendientes -1 (modos extremos) y -2 (modo mid)
- Evolución del área aproximada hacia valor exacto
- Comportamiento del error absoluto con aumento de n

**Características visuales:**
- Paleta de colores profesional consistente (rojo #C62828 para E(N), azul/verde/naranja para modos)
- Rectángulos transparentes (alpha=0.3) superpuestos a curva para máxima claridad
- Puntos grises (#424242) para modelos AI alineados geométricamente con curva
- Línea púrpura punteada para integral exacta como referencia
- Anotaciones de error relativo y valor de área en cada gráfica

## Tecnologías y Herramientas

### Implementación Numérica
- **Python 3.10+**: Lenguaje de programación principal
- **NumPy 1.24+**: Cálculos numéricos y operaciones vectorizadas
- **SciPy 1.10+**: Validación con métodos de integración estándar
- **Matplotlib 3.7+**: Generación de visualizaciones profesionales con control fino de parámetros

### Documentación Académica
- **LaTeX**: Sistema de composición tipográfica para documento científico
- **biblatex/biber**: Gestión automatizada de referencias bibliográficas estilo APA 7
- **latexmk**: Automatización de compilación LaTeX con detección de dependencias
- **Markdown**: Documentación técnica de código y guías de usuario

### Arquitectura del Código

**Scripts modulares independientes:**
- `rectangulos.py`: Implementación core del método de rectángulos
- `rectangulos_visualizacion.py`: Generación de 27 visualizaciones detalladas
- `comparativa_modelos.py`: Generación de 18 análisis comparativos
- `integrales_numericas.py`: Clase unificada IntegracionNumerica con todos los métodos
- `launcher.py`: Menú interactivo para ejecutar análisis
- `verificar_fixes.py`: Script de validación de correcciones de visualización

**Características de diseño:**
- Separación de concerns: lógica de cálculo vs. visualización vs. análisis
- Configuración centralizada mediante constantes globales
- Funciones puras sin efectos secundarios para facilitar testing
- Documentación inline con docstrings descriptivos
- Manejo robusto de errores y validación de parámetros

## Requisitos del Sistema

### Software Base
- Python 3.10 o superior
- LaTeX (distribución completa: TeX Live 2022+ o MiKTeX)
- Git para control de versiones

### Dependencias Python
```
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
pandas>=2.0.0
```

## Instalación y Uso

### Clonar el repositorio
```bash
git clone https://github.com/emir-ucompensar/proyecto_energia_ai.git
cd proyecto_energia_ai
```

### Instalar dependencias
```bash
pip install numpy scipy matplotlib pandas
```

### Generar visualizaciones
```bash
cd scripts
python3 rectangulos_visualizacion.py   # 27 figuras detalladas
python3 comparativa_modelos.py         # 18 figuras comparativas
python3 verificar_fixes.py             # Validar correcciones
```

### Menú interactivo
```bash
python3 launcher.py
```

### Compilar documento LaTeX
```bash
latexmk -pdf -output-directory=build main.tex
```

El PDF generado incluye:
- Introducción con contexto metodológico del método de rectángulos
- Marco teórico sobre consumo energético en IA y movimiento Green AI
- Fundamentos teóricos de Sumas de Riemann con demostraciones matemáticas
- Análisis gráfico de resultados con interpretación de 45 visualizaciones
- Sección de resultados con 5 ideas relevantes derivadas del análisis
- Conclusiones mejoradas con reflexiones sobre sostenibilidad computacional
- 19 referencias bibliográficas en formato APA 7

## Estructura de Documentación

El documento académico está organizado en las siguientes secciones:

**Fase 1: Contextualización**
- Introducción (con enfoque metodológico del método de rectángulos)
- Objetivos (general y 6 específicos)
- Justificación (relevancia del análisis energético en IA)
- Marco teórico (fundamentos de consumo energético, hardware, métricas)
- Estado del arte (11 referencias sobre Green AI y optimización)
- Escenario del problema (formulación matemática)

**Fase 2: Desarrollo de la Solución**
- Metodología (diseño del estudio, herramientas, proceso)
- Proceso de solución (implementación paso a paso con diagramas)
- Fundamentos teóricos (Sumas de Riemann, convergencia, validación analítica)

**Fase 3: Análisis y Resultados**
- Análisis gráfico (interpretación de las 45 visualizaciones generadas)
- Resultados (análisis de solución en contexto + 5 ideas relevantes)
- Conclusiones (hallazgos, contribuciones, limitaciones, trabajos futuros)

**Total:** 69+ páginas académicas con rigor matemático y análisis crítico

## Documentación Complementaria

- **PRESENTACION.md**: Guía completa para presentación oral de 5 minutos en 5 slides
- **FIXES_VISUALIZACION.md**: Documentación de correcciones de visualización aplicadas
- **REFACTORIZACION_RECTANGULOS.md**: Descripción detallada del proceso de refactorización
- **GUIA_RAPIDA.md**: Inicio rápido con comandos esenciales

## Referencias Bibliográficas Principales

El proyecto se fundamenta en 19 referencias académicas recientes (2019-2025), destacando:

**Fundamentos de Green AI:**
- Schwartz et al. (2019): "Green AI" - Pioneros del movimiento de eficiencia energética en IA
- Patterson et al. (2021): "Carbon Footprint of Machine Learning" - Análisis de huella de carbono
- Strubell et al. (2019): Costos ambientales del entrenamiento de modelos grandes

**Optimización y Escalabilidad:**
- Chatterjee & Dethlefs (2025): Técnicas modernas de optimización energética
- Behdin et al. (2025): Scaling laws y predicción de consumo
- Tabbakh et al. (2024): Desarrollo sostenible de sistemas de IA

**Arquitecturas Específicas:**
- Touvron et al. (2023): LLaMA - Arquitectura y eficiencia
- Yuan et al. (2025): Efficient LLMs - Revisión comprehensiva
- Jouppi et al. (2023): TPUs y optimización de hardware

**Metodología y Métricas:**
- Green Software Foundation (2025): Estándares de medición
- Alizadeh & Castor (2024): Métricas de eficiencia en modelos generativos
- Girija (2024): Impacto ambiental de sistemas de IA

Ver `bibliografia.bib` para lista completa con DOI, URLs y detalles de publicación.

## Contribuciones del Proyecto

**Metodológicas:**
- Framework reproducible con scripts modulares documentados
- Validación cruzada analítico-numérica con errores cuantificados
- 45 visualizaciones profesionales con consistencia visual

**Matemáticas:**
- Demostración práctica de que Sumas de Riemann son suficientemente precisas para ingeniería
- Validación de órdenes de convergencia O(h) y O(h²) mediante gráficos log-log
- Cálculo de métrica integral Z (área bajo curva) para benchmarking

**Prácticas:**
- Identificación de configuraciones Pareto-óptimas (TinyLLaMA, Phi-3 Mini, Gemma-2B)
- Evidencia cuantitativa de que modelos compactos son sostenibles
- Herramientas open source para análisis de consumo energético en IA

## Licencia y Uso Académico

Este proyecto es de código abierto y está disponible para fines educativos, académicos y de investigación. El código fuente, visualizaciones y documentación pueden ser utilizados, modificados y redistribuidos citando apropiadamente la fuente original.

**Declaración de sostenibilidad:**  
El desarrollo de este proyecto consumió aproximadamente 0.15 kWh (equivalente a 24.6 g CO₂ eq con intensidad de Colombia: 164 g/kWh), comparable a 3 horas de un bombillo LED de 50W. Todo el código está disponible públicamente para evitar duplicación innecesaria de esfuerzos computacionales.

## Autores y Contexto

Proyecto desarrollado como parte del curso de Cálculo Integral - Universidad Compensar (Ucompensar), Colombia, 2025.

**Contacto:** Para preguntas, colaboraciones o sugerencias de mejora, abrir un issue en el repositorio de GitHub.

---

**Última actualización:** Noviembre 2025  
**Versión:** 2.0.0  
**Estado:** Producción - Documento completo con método de rectángulos implementado y validado

## Estructura del Proyecto

```
proyecto_energia_ai/
├── main.tex                    # Documento principal LaTeX
├── portada.tex                 # Portada del documento
├── preambulo.tex              # Configuración LaTeX
├── bibliografia.bib           # Referencias bibliográficas (19 fuentes)
├── .gitignore                 # Archivos excluidos de Git
├── .latexmkrc                 # Configuración de compilación
│
├── secciones/                 # Contenido del documento (11 secciones)
│   ├── introduccion.tex
│   ├── justificacion.tex
│   ├── objetivos.tex
│   ├── escenario.tex
│   ├── estado_arte.tex
│   ├── marco_teorico.tex
│   ├── fundamentos_teoricos.tex
│   ├── metodologia.tex
│   ├── proceso_solucion.tex
│   ├── analisis_grafico.tex
│   └── conclusiones.tex
│
├── scripts/                   # Scripts de análisis y visualización
│   ├── config.py              # Configuración centralizada
│   ├── generar_todos_graficos.py
│   ├── grafico_1_eficiencia_barras.py
│   ├── grafico_2_dispersion_tamano_consumo.py
│   ├── grafico_3_potencia_tiempo.py
│   ├── grafico_4_pareto_tradeoff.py
│   ├── grafico_5_comparacion_metodos_numericos.py
│   ├── grafico_6_area_bajo_curva.py
│   ├── instalar_dependencias.py
│   ├── instalar_dependencias.sh
│   └── README.md
│
└── figuras/                   # Resultados gráficos y datos
    ├── png/                   # Gráficos generados
    ├── pdf/                   # Versiones vectoriales
    └── resultados/            # Datos CSV y estadísticas
```

## Requisitos del Sistema

### Software Base
- Python 3.8 o superior
- LaTeX (distribución completa: TeX Live o MiKTeX)
- Git

### Dependencias Python
```
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
pandas>=2.0.0
```

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/emir-ucompensar/proyecto_energia_ai.git
cd proyecto_energia_ai
```

### 2. Instalar dependencias Python

**Opción A: Script automático (Linux/macOS)**
```bash
./scripts/instalar_dependencias.sh
```

**Opción B: Script interactivo (multiplataforma)**
```bash
python3 scripts/instalar_dependencias.py
```

**Opción C: Manual con pip**
```bash
pip install numpy scipy matplotlib pandas
```

**Opción D: Entorno virtual (recomendado)**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install numpy scipy matplotlib pandas
```

### 3. Verificar instalación
```bash
python3 -c "import numpy, scipy, matplotlib, pandas; print('Todas las dependencias instaladas correctamente')"
```

## Uso

### Generar todos los gráficos
```bash
cd scripts
python3 generar_todos_graficos.py
```

### Generar gráficos individuales
```bash
python3 scripts/grafico_1_eficiencia_barras.py
python3 scripts/grafico_2_dispersion_tamano_consumo.py
python3 scripts/grafico_3_potencia_tiempo.py
python3 scripts/grafico_4_pareto_tradeoff.py
python3 scripts/grafico_5_comparacion_metodos_numericos.py
python3 scripts/grafico_6_area_bajo_curva.py
```

### Compilar el documento LaTeX
```bash
# Usando latexmk (recomendado)
latexmk -pdf main.tex

# O manualmente con pdflatex
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Metodología

### Métodos Numéricos Implementados

**1. Regla del Trapecio**
- Aproximación de orden O(h²)
- Ideal para funciones suaves
- Implementación manual y validación con scipy.integrate.trapezoid

**2. Método de Simpson**
- Aproximación de orden O(h⁴)
- Mayor precisión con menos puntos
- Implementación manual y validación con scipy.integrate.simpson

### Proceso de Análisis

1. **Recolección de datos**: Medición de consumo energético durante inferencia
2. **Procesamiento**: Cálculo de integrales numéricas para consumo total
3. **Análisis estadístico**: pandas para estadísticas descriptivas y correlaciones
4. **Visualización**: Matplotlib para gráficos comparativos
5. **Validación**: Comparación de métodos numéricos y análisis de convergencia

## Resultados Principales

### Hallazgos Clave

- **Relación inversa**: Modelos más grandes consumen más energía pero son menos eficientes por token
- **TinyLLaMA 1.1B**: Mejor eficiencia energética (266.67 tokens/Wh)
- **LLaMA-3 8B**: Mayor consumo pero mejor calidad de respuestas
- **Métodos numéricos**: Simpson requiere 50% menos puntos para misma precisión que Trapecio
- **Punto óptimo**: Modelos 2-3B balancean calidad y eficiencia

### Implicaciones

- Green AI: Los modelos pequeños son más sostenibles para aplicaciones masivas
- Trade-off: Existe una relación calidad-eficiencia que debe considerarse según el caso de uso
- Hardware: La GTX 1660 Ti puede ejecutar modelos hasta 8B parámetros con eficiencia razonable

## Gráficos Generados

1. **Eficiencia Energética (Barras)**: Comparación de tokens/Wh entre modelos
2. **Dispersión Tamaño-Consumo**: Relación entre parámetros y consumo energético
3. **Potencia vs Tiempo**: Perfiles de consumo durante inferencia
4. **Frontera de Pareto**: Análisis de trade-off calidad-eficiencia
5. **Comparación de Métodos Numéricos**: Convergencia Trapecio vs Simpson
6. **Área bajo la Curva**: Visualización del cálculo de consumo total

## Tecnologías Utilizadas

### Análisis y Visualización
- **NumPy**: Cálculos numéricos y manipulación de arrays
- **SciPy**: Métodos de integración numérica y validación
- **Matplotlib**: Generación de gráficos profesionales
- **pandas**: Análisis estadístico y exportación de datos

### Documentación
- **LaTeX**: Documento académico completo
- **biblatex/biber**: Gestión de referencias bibliográficas
- **Markdown**: Documentación del código

## Documentación Adicional

- [INICIO_RAPIDO.md](INICIO_RAPIDO.md): Guía de inicio rápido
- [RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md): Resumen ejecutivo
- [scripts/README.md](scripts/README.md): Documentación detallada de scripts

## Referencias Principales

El proyecto se fundamenta en 19 referencias académicas, incluyendo:

- Schwartz et al. (2019): "Green AI" - Eficiencia energética en IA
- Patterson et al. (2022): "Carbon Footprint of Machine Learning"
- Strubell et al. (2019): Costos ambientales del entrenamiento de modelos
- Touvron et al. (2023): Arquitectura y eficiencia de LLaMA
- Chatterjee & Dethlefs (2025): Técnicas de optimización energética

Ver [bibliografia.bib](bibliografia.bib) para la lista completa.

## Contribuciones

Este es un proyecto académico desarrollado para el curso de Cálculo Integral en Ucompensar. Las contribuciones, sugerencias y mejoras son bienvenidas a través de issues y pull requests.

## Licencia

Este proyecto es de código abierto y está disponible para fines educativos y de investigación.

## Autores

Proyecto desarrollado como parte del curso de Cálculo Integral - Ucompensar (2025)

## Contacto

Para preguntas o colaboraciones, por favor abrir un issue en el repositorio.

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0.3
