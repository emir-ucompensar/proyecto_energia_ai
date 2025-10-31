"""
grafico_6_area_bajo_curva.py
==============================
ANÁLISIS PRINCIPAL: Encuentra la función que mejor ajusta los datos experimentales,
calcula el área bajo la curva (Z) mediante integración definida, y visualiza el resultado.

Este script implementa:
1. Regresión con múltiples modelos (polinomial, exponencial, potencial, logarítmica)
2. Selección del mejor modelo basado en R²
3. Cálculo del área bajo la curva mediante integración definida
4. Visualización completa del análisis

Uso:
    python grafico_6_area_bajo_curva.py

Salida:
    - grafico_6_area_bajo_curva.png
    - grafico_6_area_bajo_curva.pdf
    - resultados_ajuste.txt
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import integrate
from config import (
    MODELOS, GRADO_POLINOMIO_MAX, R2_MINIMO,
    TAMANO_FIGURA_GRANDE, DPI,
    configurar_semilla, guardar_figura
)
import os

# =============================================================================
# DEFINICIÓN DE FUNCIONES DE AJUSTE
# =============================================================================

def modelo_polinomial(x, *coefs):
    """Modelo polinomial de grado variable."""
    return np.polyval(coefs, x)

def modelo_exponencial(x, a, b, c):
    """Modelo exponencial: y = a * exp(b * x) + c"""
    return a * np.exp(b * x) + c

def modelo_potencial(x, a, b, c):
    """Modelo potencial: y = a * x^b + c"""
    return a * np.power(x, b) + c

def modelo_logaritmico(x, a, b, c):
    """Modelo logarítmico: y = a * ln(x + b) + c"""
    return a * np.log(x + b) + c

# =============================================================================
# ANÁLISIS DE REGRESIÓN
# =============================================================================

def calcular_r2(y_real, y_pred):
    """
    Calcula el coeficiente de determinación R².
    
    Args:
        y_real: Valores reales
        y_pred: Valores predichos
        
    Returns:
        float: Coeficiente R² (entre 0 y 1)
    """
    ss_res = np.sum((y_real - y_pred) ** 2)
    ss_tot = np.sum((y_real - np.mean(y_real)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return r2

def ajustar_modelos(x_datos, y_datos):
    """
    Prueba múltiples modelos de ajuste y selecciona el mejor.
    
    Args:
        x_datos: Variable independiente (tamaño del modelo)
        y_datos: Variable dependiente (energía consumida)
        
    Returns:
        dict: Información del mejor modelo
    """
    mejor_modelo = {
        'tipo': None,
        'r2': -np.inf,
        'parametros': None,
        'funcion': None,
        'nombre': None
    }
    
    resultados_todos = []
    
    # 1. MODELOS POLINOMIALES (grados 1 a GRADO_POLINOMIO_MAX)
    for grado in range(1, GRADO_POLINOMIO_MAX + 1):
        try:
            coefs = np.polyfit(x_datos, y_datos, grado)
            y_pred = np.polyval(coefs, x_datos)
            r2 = calcular_r2(y_datos, y_pred)
            
            # Crear función lambda
            func = lambda x, coefs=coefs: np.polyval(coefs, x)
            
            nombre = f"Polinomial grado {grado}"
            if grado == 1:
                nombre += f": y = {coefs[0]:.3f}x + {coefs[1]:.3f}"
            else:
                nombre += f": y = {coefs[0]:.3f}x^{grado} + ..."
            
            resultado = {
                'tipo': f'polinomial_{grado}',
                'r2': r2,
                'parametros': coefs,
                'funcion': func,
                'nombre': nombre
            }
            resultados_todos.append(resultado)
            
            if r2 > mejor_modelo['r2']:
                mejor_modelo = resultado
                
        except Exception as e:
            print(f"Error en polinomial grado {grado}: {e}")
    
    # 2. MODELO EXPONENCIAL
    try:
        p0 = [1, 0.1, min(y_datos)]
        popt, _ = curve_fit(modelo_exponencial, x_datos, y_datos, p0=p0, maxfev=5000)
        y_pred = modelo_exponencial(x_datos, *popt)
        r2 = calcular_r2(y_datos, y_pred)
        
        func = lambda x, popt=popt: modelo_exponencial(x, *popt)
        nombre = f"Exponencial: y = {popt[0]:.3f} exp({popt[1]:.3f}x) + {popt[2]:.3f}"
        
        resultado = {
            'tipo': 'exponencial',
            'r2': r2,
            'parametros': popt,
            'funcion': func,
            'nombre': nombre
        }
        resultados_todos.append(resultado)
        
        if r2 > mejor_modelo['r2']:
            mejor_modelo = resultado
            
    except Exception as e:
        print(f"Error en exponencial: {e}")
    
    # 3. MODELO POTENCIAL
    try:
        p0 = [10, 0.5, 0]
        popt, _ = curve_fit(modelo_potencial, x_datos, y_datos, p0=p0, maxfev=5000)
        y_pred = modelo_potencial(x_datos, *popt)
        r2 = calcular_r2(y_datos, y_pred)
        
        func = lambda x, popt=popt: modelo_potencial(x, *popt)
        nombre = f"Potencial: y = {popt[0]:.3f} x^{popt[1]:.3f} + {popt[2]:.3f}"
        
        resultado = {
            'tipo': 'potencial',
            'r2': r2,
            'parametros': popt,
            'funcion': func,
            'nombre': nombre
        }
        resultados_todos.append(resultado)
        
        if r2 > mejor_modelo['r2']:
            mejor_modelo = resultado
            
    except Exception as e:
        print(f"Error en potencial: {e}")
    
    # 4. MODELO LOGARÍTMICO
    try:
        p0 = [5, 0.1, 10]
        popt, _ = curve_fit(modelo_logaritmico, x_datos, y_datos, p0=p0, maxfev=5000)
        y_pred = modelo_logaritmico(x_datos, *popt)
        r2 = calcular_r2(y_datos, y_pred)
        
        func = lambda x, popt=popt: modelo_logaritmico(x, *popt)
        nombre = f"Logarítmico: y = {popt[0]:.3f} ln(x + {popt[1]:.3f}) + {popt[2]:.3f}"
        
        resultado = {
            'tipo': 'logaritmico',
            'r2': r2,
            'parametros': popt,
            'funcion': func,
            'nombre': nombre
        }
        resultados_todos.append(resultado)
        
        if r2 > mejor_modelo['r2']:
            mejor_modelo = resultado
            
    except Exception as e:
        print(f"Error en logarítmico: {e}")
    
    return mejor_modelo, resultados_todos

# =============================================================================
# CÁLCULO DE ÁREA BAJO LA CURVA
# =============================================================================

def calcular_area_bajo_curva(funcion, a, b, metodo='quad'):
    """
    Calcula el área bajo la curva Z mediante integración definida.
    
    Args:
        funcion: Función a integrar
        a: Límite inferior
        b: Límite superior
        metodo: 'quad' (analítico) o 'trapz' (numérico)
        
    Returns:
        float: Área Z bajo la curva
    """
    if metodo == 'quad':
        # Integración numérica de alta precisión
        area, error = integrate.quad(funcion, a, b)
        return area, error
    else:
        # Método del trapecio
        x = np.linspace(a, b, 1000)
        y = funcion(x)
        area = np.trapz(y, x)
        return area, 0

# =============================================================================
# VISUALIZACIÓN
# =============================================================================

def crear_grafico_area_bajo_curva():
    """
    Crea el gráfico principal con el análisis completo.
    
    Returns:
        tuple: (figura, mejor_modelo, area_z)
    """
    configurar_semilla()
    
    # Datos experimentales
    x_datos = np.array(MODELOS['parametros'])
    y_datos = np.array(MODELOS['energia_total'])
    nombres = MODELOS['nombres_cortos']
    
    # Encontrar mejor ajuste
    print("\nBuscando mejor modelo de ajuste...")
    mejor_modelo, todos_modelos = ajustar_modelos(x_datos, y_datos)
    
    print(f"\n[OK] Mejor modelo encontrado: {mejor_modelo['nombre']}")
    print(f"  R² = {mejor_modelo['r2']:.6f}")
    
    # Calcular área bajo la curva
    a_lim = min(x_datos)
    b_lim = max(x_datos)
    
    area_z, error_integral = calcular_area_bajo_curva(
        mejor_modelo['funcion'], a_lim, b_lim, metodo='quad'
    )
    
    print(f"\n[OK] Área bajo la curva Z = {area_z:.6f}")
    print(f"  Límites de integración: [{a_lim:.2f}, {b_lim:.2f}]")
    print(f"  Error estimado de integración: {error_integral:.2e}")
    
    # Crear figura con subplots
    fig = plt.figure(figsize=TAMANO_FIGURA_GRANDE, dpi=DPI)
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
    
    ax_main = fig.add_subplot(gs[0, :])  # Gráfico principal
    ax_residuos = fig.add_subplot(gs[1, 0])  # Residuos
    ax_r2 = fig.add_subplot(gs[1, 1])  # Comparación R²
    
    # -------------------------------------------------------------------------
    # SUBPLOT PRINCIPAL: Datos + Ajuste + Área
    # -------------------------------------------------------------------------
    
    # Curva suave del modelo ajustado
    x_curva = np.linspace(a_lim, b_lim, 500)
    y_curva = mejor_modelo['funcion'](x_curva)
    
    # Área bajo la curva (sombreada)
    ax_main.fill_between(x_curva, 0, y_curva, alpha=0.3, color='cyan',
                        label=f'Área Z = {area_z:.3f}')
    
    # Línea del modelo
    ax_main.plot(x_curva, y_curva, 'r-', linewidth=3, label=mejor_modelo['nombre'])
    
    # Puntos experimentales
    ax_main.scatter(x_datos, y_datos, s=300, c='blue', marker='o',
                   edgecolors='black', linewidths=2, zorder=5,
                   label='Datos experimentales')
    
    # Etiquetas de puntos
    for i, nombre in enumerate(nombres):
        ax_main.annotate(
            nombre,
            (x_datos[i], y_datos[i]),
            xytext=(0, 15), textcoords='offset points',
            fontsize=9, ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5)
        )
    
    # Líneas verticales en los límites de integración
    ax_main.axvline(a_lim, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax_main.axvline(b_lim, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax_main.text(a_lim, ax_main.get_ylim()[1] * 0.95, f'a = {a_lim:.2f}',
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax_main.text(b_lim, ax_main.get_ylim()[1] * 0.95, f'b = {b_lim:.2f}',
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Ecuación de la integral
    ax_main.text(0.5, 0.05, 
                r'$Z = \int_{' + f'{a_lim:.1f}' + r'}^{' + f'{b_lim:.1f}' + 
                r'} f(x) \, dx = ' + f'{area_z:.3f}' + r'$',
                transform=ax_main.transAxes, fontsize=14, ha='center',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='orange', 
                         alpha=0.9, edgecolor='red', linewidth=2))
    
    ax_main.set_xlabel('Tamaño del Modelo (Billones de Parámetros)', 
                      fontsize=13, fontweight='bold')
    ax_main.set_ylabel('Consumo Energético (Wh)', fontsize=13, fontweight='bold')
    ax_main.set_title('Análisis de Regresión y Cálculo del Área Bajo la Curva (Z)\n' +
                     f'Modelo: {mejor_modelo["nombre"].split(":")[0]} | R² = {mejor_modelo["r2"]:.4f}',
                     fontsize=15, fontweight='bold')
    ax_main.legend(loc='upper left', fontsize=11, framealpha=0.95)
    ax_main.grid(alpha=0.3, linestyle='--')
    
    # -------------------------------------------------------------------------
    # SUBPLOT RESIDUOS: Análisis de errores
    # -------------------------------------------------------------------------
    
    y_pred = mejor_modelo['funcion'](x_datos)
    residuos = y_datos - y_pred
    
    ax_residuos.scatter(x_datos, residuos, s=150, c='red', marker='x', linewidths=3)
    ax_residuos.axhline(0, color='black', linestyle='-', linewidth=2)
    ax_residuos.axhline(np.std(residuos), color='gray', linestyle='--', alpha=0.5,
                       label=f'±σ = ±{np.std(residuos):.3f}')
    ax_residuos.axhline(-np.std(residuos), color='gray', linestyle='--', alpha=0.5)
    
    ax_residuos.set_xlabel('Tamaño del Modelo (B)', fontsize=11, fontweight='bold')
    ax_residuos.set_ylabel('Residuos (Wh)', fontsize=11, fontweight='bold')
    ax_residuos.set_title('Análisis de Residuos', fontsize=12, fontweight='bold')
    ax_residuos.legend(fontsize=9)
    ax_residuos.grid(alpha=0.3, linestyle='--')
    
    # -------------------------------------------------------------------------
    # SUBPLOT R²: Comparación de modelos
    # -------------------------------------------------------------------------
    
    # Ordenar modelos por R²
    todos_modelos_sorted = sorted(todos_modelos, key=lambda x: x['r2'], reverse=True)
    nombres_modelos = [m['tipo'] for m in todos_modelos_sorted[:5]]
    r2_valores = [m['r2'] for m in todos_modelos_sorted[:5]]
    
    colores_barras = ['green' if r2 == mejor_modelo['r2'] else 'lightblue' 
                     for r2 in r2_valores]
    
    barras = ax_r2.barh(nombres_modelos, r2_valores, color=colores_barras,
                        edgecolor='black', linewidth=1.5)
    
    # Añadir valores en las barras
    for i, (barra, valor) in enumerate(zip(barras, r2_valores)):
        ax_r2.text(valor - 0.05, i, f'{valor:.4f}', 
                  ha='right', va='center', fontsize=10, fontweight='bold', color='white')
    
    ax_r2.set_xlabel('Coeficiente de Determinación (R²)', fontsize=11, fontweight='bold')
    ax_r2.set_title('Comparación de Modelos de Ajuste', fontsize=12, fontweight='bold')
    ax_r2.set_xlim([0, 1])
    ax_r2.axvline(R2_MINIMO, color='red', linestyle='--', linewidth=2,
                 label=f'R² mínimo = {R2_MINIMO}')
    ax_r2.legend(fontsize=9)
    ax_r2.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.suptitle('ANÁLISIS INTEGRAL: Función de Ajuste y Área Bajo la Curva',
                fontsize=17, fontweight='bold', y=0.995)
    
    return fig, mejor_modelo, area_z, todos_modelos

# =============================================================================
# EXPORTACIÓN DE RESULTADOS
# =============================================================================

def guardar_resultados_txt(mejor_modelo, area_z, todos_modelos):
    """Guarda los resultados en un archivo de texto."""
    from config import DIR_RESULTADOS
    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    ruta = os.path.join(DIR_RESULTADOS, 'resultados_ajuste.txt')
    
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RESULTADOS DEL ANÁLISIS DE REGRESIÓN Y ÁREA BAJO LA CURVA\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("MEJOR MODELO ENCONTRADO:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Tipo: {mejor_modelo['tipo']}\n")
        f.write(f"Ecuación: {mejor_modelo['nombre']}\n")
        f.write(f"R² (coeficiente de determinación): {mejor_modelo['r2']:.8f}\n")
        f.write(f"Parámetros: {mejor_modelo['parametros']}\n\n")
        
        f.write("ÁREA BAJO LA CURVA (Z):\n")
        f.write("-" * 80 + "\n")
        f.write(f"Z = ∫[{min(MODELOS['parametros']):.2f}, {max(MODELOS['parametros']):.2f}] f(x) dx\n")
        f.write(f"Z = {area_z:.10f}\n\n")
        
        f.write("INTERPRETACIÓN:\n")
        f.write("-" * 80 + "\n")
        f.write(f"El área bajo la curva Z = {area_z:.3f} representa el consumo energético\n")
        f.write(f"acumulado integrado sobre el rango de tamaños de modelos evaluados\n")
        f.write(f"({min(MODELOS['parametros']):.1f}B a {max(MODELOS['parametros']):.1f}B parámetros).\n\n")
        
        f.write("TODOS LOS MODELOS EVALUADOS:\n")
        f.write("-" * 80 + "\n")
        for i, modelo in enumerate(sorted(todos_modelos, key=lambda x: x['r2'], reverse=True), 1):
            f.write(f"{i}. {modelo['tipo']:20} | R² = {modelo['r2']:.6f}\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"\n[OK] Resultados guardados en: {ruta}")

def guardar_grafico(fig, nombre_base='6_area_bajo_curva'):
    """Guarda el gráfico usando la función centralizada."""
    guardar_figura(fig, nombre_base, dpi=DPI)

def main():
    """Función principal."""
    print("=" * 80)
    print("ANÁLISIS PRINCIPAL: REGRESIÓN Y ÁREA BAJO LA CURVA")
    print("=" * 80)
    
    # Crear gráfico y análisis
    fig, mejor_modelo, area_z, todos_modelos = crear_grafico_area_bajo_curva()
    
    # Guardar resultados
    guardar_resultados_txt(mejor_modelo, area_z, todos_modelos)
    guardar_grafico(fig)
    
    print("\n" + "=" * 80)
    print("RESUMEN EJECUTIVO")
    print("=" * 80)
    print(f"[OK] Modelo óptimo: {mejor_modelo['tipo']}")
    print(f"[OK] Bondad de ajuste (R²): {mejor_modelo['r2']:.6f}")
    print(f"[OK] Área bajo la curva (Z): {area_z:.6f}")
    print(f"[OK] Número de modelos evaluados: {len(todos_modelos)}")
    print("=" * 80)
    
    print("\n[OK] Proceso completado exitosamente")
    plt.show()

if __name__ == '__main__':
    main()
