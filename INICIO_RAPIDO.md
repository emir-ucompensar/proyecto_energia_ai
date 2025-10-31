# INICIO RÁPIDO

## [ENERGY] Generar Todos los Gráficos (5 minutos)

```bash
# 1. Instalar dependencias (solo primera vez)
pip install numpy scipy matplotlib

# 2. Navegar a scripts
cd scripts/

# 3. ¡Ejecutar!
python generar_todos_graficos.py

# Los gráficos se guardarán en ../figuras/
```

---

## Recompilar el Documento PDF

```bash
# Desde la raíz del proyecto
cd ../proyecto_energia_ai

# Compilación completa (3 pasos necesarios)
pdflatex -output-directory=build main.tex
biber build/main
pdflatex -output-directory=build main.tex
pdflatex -output-directory=build main.tex

# El PDF estará en: build/main.pdf
```

---

## Ejecutar un Solo Gráfico

```bash
cd scripts/

# Ejemplo: Gráfico 1 (Eficiencia)
python grafico_1_eficiencia_barras.py

# Ver todos los scripts disponibles
ls -1 grafico_*.py
```

---

## Personalizar Parámetros

Editar `scripts/config.py`:

```python
# Modificar datos de modelos
MODELOS = {
    'nombres': ['MiModelo1', 'MiModelo2'],
    'parametros': [2.0, 5.0],
    'energia_total': [12.0, 18.0],
    # ... más campos
}

# Cambiar configuración de gráficos
TAMANO_FIGURA = (14, 10)  # Tamaño en pulgadas
DPI = 600                  # Resolución
```

---

## Ver Documentación Completa

```bash
# README de scripts Python
cat scripts/README.md

# Resumen completo del proyecto
cat RESUMEN_PROYECTO.md
```

---

## Verificar Estado del Proyecto

```bash
# Ver estructura
tree -L 2 -I 'build|__pycache__'

# Ver estadísticas del PDF
pdfinfo build/main.pdf

# Contar líneas de código Python
find scripts/ -name "*.py" | xargs wc -l
```

---

## Lista de Verificación

- [ ] Dependencias instaladas (`numpy`, `scipy`, `matplotlib`)
- [ ] Scripts Python ejecutados exitosamente
- [ ] 6 gráficos generados en `figuras/`
- [ ] Documento LaTeX compilado sin errores
- [ ] PDF final revisado (81 páginas)

---

## Solución Rápida de Problemas

### Error: "ModuleNotFoundError: No module named 'numpy'"
```bash
pip install numpy scipy matplotlib
```

### Error: Scripts no encuentran config.py
```bash
# Asegúrate de ejecutar desde /scripts/
cd scripts/
python grafico_X.py
```

### Advertencia: Gráficos no se ven en el PDF
```bash
# 1. Generar gráficos primero
cd scripts/ && python generar_todos_graficos.py

# 2. Luego recompilar LaTeX
cd .. && pdflatex -output-directory=build main.tex
```

---

## Contacto y Soporte

Para dudas específicas:
1. Revisa `RESUMEN_PROYECTO.md` - Visión general completa
2. Consulta `scripts/README.md` - Guía detallada de scripts
3. Inspecciona el código - Todos los scripts están documentados

---

## Objetivos Completados

- Fundamentos teóricos con 11 referencias bibliográficas
- 6 análisis gráficos especializados
- Scripts Python modulares y documentados
- Sección de Análisis Gráfico (nueva)
- Sección de Conclusiones (nueva)
- Documento LaTeX compilable (81 páginas)
- Área bajo la curva Z calculada
- Metodología reproducible

---

**¡Listo para usar!**

Ejecuta `python scripts/generar_todos_graficos.py` y disfruta de los resultados.
