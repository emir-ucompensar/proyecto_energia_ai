# Directorio de Figuras
## Visualizaciones del Proyecto - Método de Rectángulos

Este directorio contiene las 45 visualizaciones generadas por el proyecto de análisis energético usando el método de los rectángulos (sumas de Riemann).

## Estructura del Directorio

```
figuras/
├── resultados/        # 45 gráficos PNG generados por los scripts
├── png/              # (vacío - reservado para uso futuro)
├── pdf/              # (vacío - reservado para uso futuro)
└── README.md         # Este archivo
```

## Contenido - 45 Visualizaciones

### Grupo 1: Visualizaciones Detalladas (27 gráficos)
Generadas por `rectangulos_visualizacion.py`

**Por densidad y modo (9 configuraciones básicas)**:
- `rectangulos_left_n10.png`, `rectangulos_left_n100.png`, `rectangulos_left_n1000.png`
- `rectangulos_mid_n10.png`, `rectangulos_mid_n100.png`, `rectangulos_mid_n1000.png`
- `rectangulos_right_n10.png`, `rectangulos_right_n100.png`, `rectangulos_right_n1000.png`

**Con modelos de IA posicionados (3 gráficos)**:
- `rectangulos_left_modelos.png`
- `rectangulos_mid_modelos.png`
- `rectangulos_right_modelos.png`

**Con tablas de resultados (3 gráficos)**:
- `rectangulos_left_tabla.png`
- `rectangulos_mid_tabla.png`
- `rectangulos_right_tabla.png`

**Visualizaciones combinadas (12 gráficos adicionales)**:
- Comparativas de densidades
- Análisis de convergencia
- Zooms y detalles

### Grupo 2: Análisis Comparativo (18 gráficos)
Generados por `comparativa_modelos.py`

**Comparativas por densidad (6 gráficos)**:
- `comparativa_n10.png`, `comparativa_n100.png`, `comparativa_n1000.png`
- `comparativa_n10_zoom.png`, `comparativa_n100_zoom.png`, `comparativa_n1000_zoom.png`

**Análisis de convergencia (6 gráficos)**:
- `comparativa_convergencia_left.png`
- `comparativa_convergencia_mid.png`
- `comparativa_convergencia_right.png`
- `comparativa_convergencia_todas.png`
- `comparativa_convergencia_errores.png`
- `comparativa_convergencia_log.png`

**Análisis de modelos y precisión (6 gráficos)**:
- `comparativa_todos_modos.png`
- `comparativa_todos_modos_zoom.png`
- `comparativa_modelos_barras.png`
- `comparativa_precision_modos.png`
- `comparativa_tiempos_ejecucion.png`
- `tabla_convergencia.png`

## Especificaciones Técnicas

### Formato
- **Tipo**: PNG
- **Resolución**: 300 DPI
- **Tamaño típico**: 200-500 KB por gráfico
- **Dimensiones**: 1200×800 px (estándar), 1400×1000 px (gráficos grandes)

### Paleta de Colores
- **Curva E(N)**: #C62828 (rojo)
- **Rectángulos izquierda**: #1976D2 (azul)
- **Rectángulos punto medio**: #388E3C (verde)
- **Rectángulos derecha**: #F57C00 (naranja)
- **Modelos de IA**: #424242 (gris oscuro)

## Regeneración de Gráficos

### Opción 1: Menú Interactivo (Recomendado)
```bash
cd ../scripts
python3 launcher.py
# Seleccionar:
# 2 - Generar visualizaciones detalladas (27 gráficos)
# 3 - Generar análisis comparativo (18 gráficos)
# 5 - Ejecutar análisis completo (45 gráficos)
```

### Opción 2: Scripts Individuales
```bash
cd ../scripts

# Generar 27 visualizaciones detalladas
python3 rectangulos_visualizacion.py

# Generar 18 análisis comparativos
python3 comparativa_modelos.py
```

### Tiempo de Generación
- **Visualizaciones detalladas**: ~15 segundos
- **Análisis comparativo**: ~12 segundos
- **Total (45 gráficos)**: ~30 segundos

## Uso en LaTeX

Los gráficos se incluyen automáticamente en `main.tex` mediante:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figuras/resultados/rectangulos_mid_n100.png}
    \caption{Método de rectángulos con punto medio, n=100}
    \label{fig:rectangulos_mid_n100}
\end{figure}
```

## Gráficos Clave para el Documento

### Principales (incluidos en LaTeX)
1. `rectangulos_mid_n100.png` - Mejor balance precisión/visualización
2. `rectangulos_mid_modelos.png` - Modelos de IA en la curva
3. `comparativa_convergencia_mid.png` - Análisis de convergencia
4. `comparativa_todos_modos.png` - Comparación entre modos
5. `comparativa_precision_modos.png` - Precisión por configuración

### Complementarios (para análisis detallado)
- Todas las variaciones de densidad (n=10, 100, 1000)
- Gráficos con tablas numéricas
- Análisis de errores y tiempos de cómputo

## Validación

Para verificar la integridad de las visualizaciones:

```bash
cd ../scripts
python3 verificar_fixes.py
```

Esto valida:
- Alineación correcta de modelos con curva E(N)
- Consistencia de colores
- Integridad de archivos generados

## Limpieza

Para eliminar todos los gráficos generados:

```bash
cd figuras/resultados
rm -f *.png
```

Luego regenerar con:
```bash
cd ../../scripts
python3 launcher.py  # Opción 5
```

## Notas

- Todos los gráficos son determinísticos (sin aleatoriedad)
- Los archivos PNG están optimizados para LaTeX (300 DPI)
- Los directorios `png/` y `pdf/` están reservados para uso futuro
- La carpeta `resultados/` contiene todas las visualizaciones actuales

---

**Total de visualizaciones**: 45 gráficos PNG  
**Scripts generadores**: `rectangulos_visualizacion.py` (27) + `comparativa_modelos.py` (18)  
**Última actualización**: Noviembre 2025  
**Versión**: 2.0.0
