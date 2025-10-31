"""
grafico_5_comparacion_metodos_numericos.py
============================================
Compara la precisión de los métodos de integración numérica
(Trapecio vs Simpson) frente al método analítico.

Este script evalúa el error de aproximación en función del
número de subintervalos utilizados.

Uso:
    python grafico_5_comparacion_metodos_numericos.py

Salida:
    - grafico_5_comparacion_metodos_numericos.png
    - grafico_5_comparacion_metodos_numericos.pdf
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import integrate
from scipy.integrate import trapezoid, simpson
from config import (
    N_INTERVALOS, A_LIMITE_INFERIOR, B_LIMITE_SUPERIOR,
    TAMANO_FIGURA_GRANDE, DPI, COLORES,
    configurar_semilla, guardar_figura, DIR_RESULTADOS
)
import os

# Función de ejemplo: perfil de potencia realista
def funcion_potencia(t):
    """
    Función que modela un perfil de potencia GPU realista.
    
    P(t) = P0 * (1 - exp(-t/τ)) * (1 + 0.1*sin(ωt))
    
    Args:
        t: Tiempo (escalar o array)
        
    Returns:
        Potencia en el tiempo
    """
    P0 = 100  # Potencia nominal (W)
    tau = 2   # Constante de tiempo warmup
    omega = 0.5  # Frecuencia de oscilación
    
    return P0 * (1 - np.exp(-t / tau)) * (1 + 0.1 * np.sin(omega * t))

def integral_analitica(a, b):
    """
    Calcula la integral analítica (referencia exacta).
    
    Usa scipy.integrate.quad con alta precisión.
    
    Args:
        a: Límite inferior
        b: Límite superior
        
    Returns:
        Valor de la integral
    """
    resultado, _ = integrate.quad(funcion_potencia, a, b, epsabs=1e-12)
    return resultado

def metodo_trapecio(f, a, b, n):
    """
    Implementa la regla del trapecio (implementación manual).
    
    Args:
        f: Función a integrar
        a: Límite inferior
        b: Límite superior
        n: Número de subintervalos
        
    Returns:
        Aproximación de la integral
    """
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    
    # Fórmula del trapecio
    integral = h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])
    return integral

def metodo_trapecio_scipy(f, a, b, n):
    """
    Usa scipy.integrate.trapezoid (recomendado).
    
    Args:
        f: Función a integrar
        a: Límite inferior
        b: Límite superior
        n: Número de subintervalos
        
    Returns:
        Aproximación de la integral
    """
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return trapezoid(y, x)

def metodo_simpson(f, a, b, n):
    """
    Implementa la regla de Simpson 1/3 (implementación manual).
    
    Args:
        f: Función a integrar
        a: Límite inferior
        b: Límite superior
        n: Número de subintervalos (debe ser par)
        
    Returns:
        Aproximación de la integral
    """
    if n % 2 != 0:
        n += 1  # Asegurar que n sea par
    
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    
    # Fórmula de Simpson 1/3
    integral = h / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 
                        2 * np.sum(y[2:-2:2]) + y[-1])
    return integral

def metodo_simpson_scipy(f, a, b, n):
    """
    Usa scipy.integrate.simpson (recomendado).
    
    Args:
        f: Función a integrar
        a: Límite inferior
        b: Límite superior
        n: Número de subintervalos (debe ser par)
        
    Returns:
        Aproximación de la integral
    """
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return simpson(y, x)

def crear_grafico_comparacion():
    """
    Crea gráfico comparativo de métodos numéricos.
    
    Returns:
        matplotlib.figure.Figure: Figura generada
    """
    configurar_semilla()
    
    # Calcular valor exacto
    valor_exacto = integral_analitica(A_LIMITE_INFERIOR, B_LIMITE_SUPERIOR)
    
    # Arrays para almacenar resultados
    errores_trapecio = []
    errores_simpson = []
    tiempos_computacion_t = []
    tiempos_computacion_s = []
    
    # Evaluar cada método con diferentes números de intervalos
    import time
    
    for n in N_INTERVALOS:
        # Trapecio
        t0 = time.time()
        aprox_trapecio = metodo_trapecio(
            funcion_potencia, A_LIMITE_INFERIOR, B_LIMITE_SUPERIOR, n
        )
        t1 = time.time()
        tiempos_computacion_t.append((t1 - t0) * 1000)  # ms
        
        error_trapecio = abs(aprox_trapecio - valor_exacto) / valor_exacto * 100
        errores_trapecio.append(error_trapecio)
        
        # Simpson
        t0 = time.time()
        aprox_simpson = metodo_simpson(
            funcion_potencia, A_LIMITE_INFERIOR, B_LIMITE_SUPERIOR, n
        )
        t1 = time.time()
        tiempos_computacion_s.append((t1 - t0) * 1000)  # ms
        
        error_simpson = abs(aprox_simpson - valor_exacto) / valor_exacto * 100
        errores_simpson.append(error_simpson)
    
    # Crear figura con 3 subplots
    fig = plt.figure(figsize=TAMANO_FIGURA_GRANDE, dpi=DPI)
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, :])  # Error vs n (log-log)
    ax2 = fig.add_subplot(gs[1, 0])  # Función original
    ax3 = fig.add_subplot(gs[1, 1])  # Tiempo de cómputo
    
    # Subplot 1: Error relativo vs número de intervalos (escala log-log)
    ax1.loglog(N_INTERVALOS, errores_trapecio, 'o-', 
              color=COLORES['trapecio'], linewidth=2.5, markersize=8,
              label='Trapecio (O(h²))')
    ax1.loglog(N_INTERVALOS, errores_simpson, 's-', 
              color=COLORES['simpson'], linewidth=2.5, markersize=8,
              label='Simpson 1/3 (O(h⁴))')
    
    # Líneas de referencia para pendientes teóricas
    h_ref = np.array(N_INTERVALOS, dtype=float)
    ax1.loglog(h_ref, errores_trapecio[0] * (h_ref[0] / h_ref)**2, 
              '--', color='gray', alpha=0.5, label='Pendiente O(h²)')
    ax1.loglog(h_ref, errores_simpson[0] * (h_ref[0] / h_ref)**4, 
              '--', color='black', alpha=0.5, label='Pendiente O(h⁴)')
    
    ax1.set_xlabel('Número de Subintervalos (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Error Relativo (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Convergencia de Métodos Numéricos de Integración',
                  fontsize=14, fontweight='bold')
    ax1.legend(loc='lower left', fontsize=10)
    ax1.grid(True, which='both', alpha=0.3, linestyle='--')
    
    # Subplot 2: Función original
    t_plot = np.linspace(A_LIMITE_INFERIOR, B_LIMITE_SUPERIOR, 1000)
    p_plot = funcion_potencia(t_plot)
    
    ax2.plot(t_plot, p_plot, linewidth=2.5, color=COLORES['analitico'])
    ax2.fill_between(t_plot, 0, p_plot, alpha=0.3, color=COLORES['analitico'])
    ax2.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Potencia (W)', fontsize=11, fontweight='bold')
    ax2.set_title('Función Integrada: P(t)', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.text(0.5, 0.95, f'Integral exacta = {valor_exacto:.4f}',
            transform=ax2.transAxes, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
            fontsize=10, fontweight='bold')
    
    # Subplot 3: Tiempo de cómputo
    ax3.plot(N_INTERVALOS, tiempos_computacion_t, 'o-',
            color=COLORES['trapecio'], linewidth=2, markersize=7,
            label='Trapecio')
    ax3.plot(N_INTERVALOS, tiempos_computacion_s, 's-',
            color=COLORES['simpson'], linewidth=2, markersize=7,
            label='Simpson')
    ax3.set_xlabel('Número de Subintervalos (n)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Tiempo de Cómputo (ms)', fontsize=11, fontweight='bold')
    ax3.set_title('Eficiencia Computacional', fontsize=12, fontweight='bold')
    ax3.legend(loc='upper left', fontsize=10)
    ax3.grid(alpha=0.3, linestyle='--')
    
    plt.suptitle('Comparación de Métodos de Integración Numérica',
                fontsize=16, fontweight='bold', y=0.98)
    
    return fig, valor_exacto, errores_trapecio, errores_simpson

def imprimir_tabla_resultados(valor_exacto, errores_t, errores_s):
    """Imprime tabla comparativa de resultados."""
    print("\nTabla de Resultados Numéricos:")
    print("=" * 80)
    print(f"{'n':>6} | {'Trapecio':>12} | {'Error (%)':>10} | "
          f"{'Simpson':>12} | {'Error (%)':>10}")
    print("-" * 80)
    
    for i, n in enumerate(N_INTERVALOS):
        aprox_t = metodo_trapecio(funcion_potencia, A_LIMITE_INFERIOR, 
                                  B_LIMITE_SUPERIOR, n)
        aprox_s = metodo_simpson(funcion_potencia, A_LIMITE_INFERIOR, 
                                 B_LIMITE_SUPERIOR, n)
        
        print(f"{n:>6} | {aprox_t:>12.6f} | {errores_t[i]:>10.6f} | "
              f"{aprox_s:>12.6f} | {errores_s[i]:>10.6f}")
    
    print("-" * 80)
    print(f"Valor exacto (referencia): {valor_exacto:.10f}")

def guardar_grafico(fig, nombre_base='5_comparacion_metodos_numericos'):
    """Guarda el gráfico usando la función centralizada."""
    guardar_figura(fig, nombre_base, dpi=DPI)

def main():
    """Función principal."""
    print("=" * 70)
    print("Generando Gráfico 5: Comparación Métodos Numéricos")
    print("=" * 70)
    
    # Crear gráfico
    fig, valor_exacto, errores_t, errores_s = crear_grafico_comparacion()
    
    # Imprimir resultados
    imprimir_tabla_resultados(valor_exacto, errores_t, errores_s)
    
    # Guardar
    guardar_grafico(fig)
    
    # Exportar resultados a CSV usando pandas
    print("\n" + "=" * 70)
    print("Exportando resultados de convergencia con pandas")
    print("=" * 70)
    
    # Crear DataFrame con resultados
    resultados_data = []
    for i, n in enumerate(N_INTERVALOS):
        aprox_t = metodo_trapecio(funcion_potencia, A_LIMITE_INFERIOR, 
                                  B_LIMITE_SUPERIOR, n)
        aprox_s = metodo_simpson(funcion_potencia, A_LIMITE_INFERIOR, 
                                 B_LIMITE_SUPERIOR, n)
        
        # Usar también scipy para comparar
        aprox_t_scipy = metodo_trapecio_scipy(funcion_potencia, A_LIMITE_INFERIOR,
                                              B_LIMITE_SUPERIOR, n)
        aprox_s_scipy = metodo_simpson_scipy(funcion_potencia, A_LIMITE_INFERIOR,
                                             B_LIMITE_SUPERIOR, n)
        
        resultados_data.append({
            'n_intervalos': n,
            'valor_exacto': valor_exacto,
            'trapecio_manual': aprox_t,
            'trapecio_scipy': aprox_t_scipy,
            'simpson_manual': aprox_s,
            'simpson_scipy': aprox_s_scipy,
            'error_trapecio_pct': errores_t[i],
            'error_simpson_pct': errores_s[i]
        })
    
    df_resultados = pd.DataFrame(resultados_data)
    
    # Guardar resultados
    ruta_csv = os.path.join(DIR_RESULTADOS, 'convergencia_metodos_numericos.csv')
    df_resultados.to_csv(ruta_csv, index=False, float_format='%.10f')
    print(f"[OK] Resultados exportados: {ruta_csv}")
    
    # Mostrar resumen estadístico
    print("\n[STATS] Resumen de Errores (con pandas):")
    print(df_resultados[['n_intervalos', 'error_trapecio_pct', 'error_simpson_pct']].to_string(index=False))
    
    print("\n[OK] Proceso completado exitosamente")
    plt.show()

if __name__ == '__main__':
    main()
