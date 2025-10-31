# Directorio de Figuras - Estructura Organizada

Este directorio contiene todas las visualizaciones generadas para el proyecto de análisis energético de modelos de IA.

## Estructura del Directorio

```
figuras/
├── png/               # Imágenes PNG (300 DPI) para LaTeX
├── pdf/               # Gráficos vectoriales PDF de alta calidad
├── resultados/        # Archivos de texto con resultados numéricos
└── README.md          # Este archivo
```

## Contenido

### PNG (Para documento LaTeX)
Imágenes rasterizadas de 300 DPI optimizadas para inclusión en el documento LaTeX:
- `grafico_1_eficiencia_barras.png` - Comparación de eficiencia energética (252 KB)
- `grafico_2_dispersion_tamano_consumo.png` - Correlación tamaño-consumo (319 KB)
- `grafico_3_potencia_tiempo.png` - Perfiles temporales de potencia (971 KB)
- `grafico_4_pareto_tradeoff.png` - Análisis de frontera Pareto (302 KB)
- `grafico_5_comparacion_metodos_numericos.png` - Convergencia de métodos (511 KB)
- `grafico_6_area_bajo_curva.png` - Regresión y área Z (484 KB)

### PDF (Gráficos vectoriales)
Versiones de alta calidad en formato vectorial para presentaciones y publicaciones:
- `grafico_1_eficiencia_barras.pdf` - 28 KB
- `grafico_2_dispersion_tamano_consumo.pdf` - 36 KB
- `grafico_3_potencia_tiempo.pdf` - 42 KB
- `grafico_4_pareto_tradeoff.pdf` - 42 KB
- `grafico_5_comparacion_metodos_numericos.pdf` - 49 KB
- `grafico_6_area_bajo_curva.pdf` - 54 KB

### Resultados
Archivos de texto con resultados numéricos detallados:
- `resultados_ajuste.txt` - Análisis completo de regresión y área bajo la curva

## Regeneración de Gráficos

Para regenerar todos los gráficos:

```bash
cd ../scripts
python3 generar_todos_graficos.py
```

Para regenerar un gráfico individual:

```bash
cd ../scripts
python3 grafico_1_eficiencia_barras.py  # Ejemplo para gráfico 1
```

## Configuración

Todos los gráficos se generan usando la configuración centralizada en `scripts/config.py`:
- **Resolución PNG:** 300 DPI
- **Tamaño figura:** 12×8 pulgadas (gráficos estándar), 14×10 (gráficos grandes)
- **Estilo:** seaborn-v0_8-darkgrid
- **Paleta de colores:** Personalizada de 5 colores

## Notas

- Los archivos PNG se usan automáticamente en el documento LaTeX (`main.tex`)
- Los archivos PDF son ideales para presentaciones y escalado sin pérdida de calidad
- La estructura separada permite mantener organizados formatos múltiples sin duplicación
- Los gráficos se generan automáticamente desde datos experimentales en `config.py`

## Limpieza

Para eliminar todos los gráficos generados:

```bash
rm -rf png/*.png pdf/*.pdf resultados/*.txt
```

---
**Última actualización:** Octubre 2025  
**Scripts relacionados:** `../scripts/grafico_*.py`, `../scripts/config.py`
