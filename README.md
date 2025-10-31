# Proyecto: Análisis Energético de Modelos de IA mediante Cálculo Integral

## Descripción

Este proyecto académico aplica técnicas de cálculo integral al análisis del consumo energético de modelos de lenguaje grandes (LLMs). Se implementan métodos numéricos de integración (Regla del Trapecio y Método de Simpson) para calcular y comparar el consumo energético de 5 modelos de IA durante tareas de inferencia en hardware de consumo.

## Objetivos

### Objetivo General
Evaluar el consumo energético de modelos de inteligencia artificial mediante la aplicación de técnicas de cálculo integral, con el fin de identificar patrones de eficiencia y proponer recomendaciones para la optimización del uso de recursos computacionales.

### Objetivos Específicos
- Calcular el consumo energético total de diferentes modelos de IA utilizando la Regla del Trapecio
- Comparar la precisión de métodos numéricos (Trapecio vs Simpson) en la evaluación del consumo energético
- Analizar la relación entre el tamaño del modelo y su eficiencia energética
- Desarrollar visualizaciones que faciliten la interpretación de los datos energéticos

## Modelos Analizados

| Modelo | Parámetros | Consumo Promedio | Eficiencia |
|--------|-----------|------------------|-----------|
| TinyLLaMA 1.1B | 1.1B | 45 W | 266.67 tokens/Wh |
| Phi-2 2.7B | 2.7B | 65 W | 184.62 tokens/Wh |
| Gemma-2 2B | 2.0B | 55 W | 218.18 tokens/Wh |
| LLaMA-3.2 3B | 3.0B | 75 W | 160.00 tokens/Wh |
| LLaMA-3 8B | 8.0B | 125 W | 96.00 tokens/Wh |

**Hardware utilizado:** NVIDIA GeForce GTX 1660 Ti (6 GB VRAM, TDP 120W)

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

**Última actualización:** Octubre 2025  
**Versión:** 1.0.0
