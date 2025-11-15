"""
simpson.py
==========
Integración numérica mediante Regla de Simpson para análisis de consumo energético.
Implementa método de convergencia O(h^4) - superior al trapecio - con visualización.

Uso:
    python simpson.py [número_de_intervalos]
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from integrales_numericas import IntegracionNumerica

# Paleta de colores profesional
COLOR_PRINCIPAL = '#1F4788'    # Azul oscuro profesional
COLOR_SECUNDARIO = '#8B3A62'   # Púrpura profesional
COLOR_ACENTO = '#5C946E'       # Verde profesional


def ejecutar_simpson(n=None):
    """
    Ejecutar análisis de regla de Simpson.
    
    Parámetros:
    -----------
    n : int, opcional
        Número de intervalos (debe ser par). Si es None, solicita entrada.
    """
    integ = IntegracionNumerica()
    
    # Entrada del usuario para número de intervalos si no se proporciona
    if n is None:
        print("=" * 70)
        print("REGLA DE SIMPSON - INTEGRACIÓN NUMÉRICA")
        print("=" * 70)
        print("\nFunción: E(N) = 0.0842*N^4 - 1.2156*N^3 + 6.8934*N^2 - 12.456*N + 11.234")
        print("Intervalo: [1.1, 8.0] (TinyLLaMA a LLaMA-3 8B)")
        print("Orden de convergencia: O(h^4) - SUPERIOR al Trapecio O(h^2)")
        print("\nIntegral exacta (Antiderivada): Z = {:.6f} Wh·B".format(integ.integral_exacta()))
        print("\n" + "-" * 70)
        
        while True:
            try:
                n_input = input("\nIngrese número de intervalos (n >= 4, debe ser par): ").strip()
                n = int(n_input)
                if n >= 4 and n % 2 == 0:
                    break
                else:
                    print("Error: n debe ser par y al menos 4")
            except ValueError:
                print("Error: Entrada no válida. Ingrese un número entero.")
    
    # Validar que n sea par
    if n % 2 != 0:
        n += 1
        print(f"Ajustando n a {n} (debe ser par para Simpson)")
    
    # Cálculo
    integral_simp = integ.simpson(n)
    integral_exact = integ.integral_exacta()
    error_abs = abs(integral_simp - integral_exact)
    error_rel = (error_abs / integral_exact) * 100
    
    # Resultados
    print("\n" + "=" * 70)
    print("RESULTADOS - REGLA DE SIMPSON")
    print("=" * 70)
    print(f"\nNúmero de intervalos (n): {n}")
    print(f"Tamaño de paso (h): {(8.0 - 1.1) / n:.6f}")
    print(f"\nIntegral aproximada: {integral_simp:.8f} Wh·B")
    print(f"Integral exacta:    {integral_exact:.8f} Wh·B")
    print(f"\nError absoluto: {error_abs:.2e} Wh·B")
    print(f"Error relativo: {error_rel:.6f}%")
    
    # Análisis de convergencia
    print("\n" + "-" * 70)
    print("ANÁLISIS DE CONVERGENCIA")
    print("-" * 70)
    
    n_values = [10, 20, 50, 100, 200, 500, 1000]
    if n not in n_values:
        n_values = sorted(list(set(n_values + [n])))
    
    reporte = integ.analizar_convergencia_simpson(n_values)
    
    print(f"\n{'n':>6} | {'Integral':>14} | {'Error Abs.':>12} | {'Error Rel. %':>10}")
    print("-" * 70)
    for i, n_val in enumerate(reporte['n']):
        integral = reporte['integrales'][i]
        error_abs = reporte['errores_absoluto'][i]
        error_rel = reporte['errores_relativo'][i]
        
        error_rel_str = f"{error_rel:.4f}" if error_rel is not None else "---"
        print(f"{n_val:>6} | {integral:>14.8f} | {error_abs:>12.2e} | {error_rel_str:>10}")
    
    # Generar gráfico
    print("\n" + "-" * 70)
    print("GENERANDO VISUALIZACIÓN")
    print("-" * 70)
    
    generar_grafico_simpson(reporte, integ)
    
    print("\nArchivo guardado: ../figuras/png/simpson_convergencia.png")
    print("Archivo guardado: ../figuras/pdf/simpson_convergencia.pdf")
    print("\n" + "=" * 70)


def generar_grafico_simpson(reporte, integ):
    """
    Generar gráfico de convergencia para regla de Simpson.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análisis de Convergencia - Regla de Simpson', fontsize=14, fontweight='bold')
    
    exact = integ.integral_exacta()
    
    # Gráfica 1: Convergencia de aproximación integral
    ax1.plot(reporte['n'], reporte['integrales'], 'o-', linewidth=2, markersize=8, 
             label='Aproximación Simpson', color=COLOR_PRINCIPAL)
    ax1.axhline(y=exact, color=COLOR_ACENTO, linestyle='--', linewidth=2, 
                label='Integral exacta')
    ax1.set_xlabel('Número de intervalos (n)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Valor de integral (Wh·B)', fontsize=11, fontweight='bold')
    ax1.set_title('Convergencia de la Integral', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.25, linestyle=':')
    ax1.legend(fontsize=10)
    
    # Gráfica 2: Convergencia de error (escala log-log)
    errores_abs_nonzero = [e if e > 0 else 1e-16 for e in reporte['errores_absoluto']]
    ax2.loglog(reporte['n'], errores_abs_nonzero, 'o-', linewidth=2, markersize=8, 
               label='Error absoluto (O(h⁴))', color=COLOR_SECUNDARIO)
    
    # Línea teórica: O(h^4) → O(n^-4)
    h_ref = (8.0 - 1.1) / 10
    error_ref = h_ref**4
    n_line = np.array([10, 1000])
    h_line = (8.0 - 1.1) / n_line
    error_line = error_ref * (h_ref / h_line)**4
    ax2.loglog(n_line, error_line, 'k--', linewidth=1.5, alpha=0.5, label='Referencia O(h⁴)')
    
    ax2.set_xlabel('Número de intervalos (n)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Error absoluto (escala log)', fontsize=11, fontweight='bold')
    ax2.set_title('Convergencia del Error (Log-Log)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.25, linestyle=':', which='both')
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    
    # Guardar figuras
    import os
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    fig.savefig('../figuras/png/simpson_convergencia.png', dpi=300, bbox_inches='tight')
    fig.savefig('../figuras/pdf/simpson_convergencia.pdf', bbox_inches='tight')
    plt.close()


def main():
    """Punto de ejecución principal."""
    n = None
    
    # Analizar argumento de línea de comandos si se proporciona
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Error: El argumento debe ser un número entero")
            sys.exit(1)
    
    ejecutar_simpson(n)


if __name__ == '__main__':
    main()

import sys
import numpy as np
import matplotlib.pyplot as plt
from integrales_numericas import IntegracionNumerica


def ejecutar_simpson(n=None):
    """
    Execute Simpson's 1/3 rule analysis.
    
    Parameters:
    -----------
    n : int, optional
        Number of intervals. If None, prompts user input.
        Automatically adjusted to even number if necessary.
    """
    integ = IntegracionNumerica()
    
    # User input for number of intervals if not provided
    if n is None:
        print("=" * 70)
        print("SIMPSON'S 1/3 RULE - NUMERICAL INTEGRATION")
        print("=" * 70)
        print("\nFunction: E(N) = 0.0842*N^4 - 1.2156*N^3 + 6.8934*N^2 - 12.456*N + 11.234")
        print("Interval: [1.1, 8.0] (TinyLLaMA to LLaMA-3 8B)")
        print("Convergence Order: O(h^4)")
        print("\nExact Integral (Antiderivative): Z = {:.6f} Wh·B".format(integ.integral_exacta()))
        print("\n" + "-" * 70)
        
        while True:
            try:
                n_input = input("\nEnter number of intervals (n >= 4, even): ").strip()
                n = int(n_input)
                if n % 2 != 0:
                    n += 1
                    print(f"Note: Adjusted to even number n = {n}")
                if n >= 4:
                    break
                else:
                    print("Error: n must be at least 4")
            except ValueError:
                print("Error: Invalid input. Enter an integer.")
    else:
        # Ensure n is even
        if n % 2 != 0:
            n += 1
    
    # Computation
    integral_simp = integ.simpson(n)
    integral_exact = integ.integral_exacta()
    error_abs = abs(integral_simp - integral_exact)
    error_rel = (error_abs / integral_exact) * 100
    
    # Results
    print("\n" + "=" * 70)
    print("RESULTS - SIMPSON'S 1/3 RULE")
    print("=" * 70)
    print(f"\nNumber of intervals (n): {n}")
    print(f"Step size (h): {(8.0 - 1.1) / n:.6f}")
    print(f"\nApproximate integral: {integral_simp:.8f} Wh·B")
    print(f"Exact integral:      {integral_exact:.8f} Wh·B")
    print(f"\nError absoluto: {error_abs:.2e} Wh·B")
    print(f"Error relativo: {error_rel:.6f}%")
    
    # Análisis de convergencia
    print("\n" + "-" * 70)
    print("ANÁLISIS DE CONVERGENCIA")
    print("-" * 70)
    
    n_values = [10, 20, 50, 100, 200, 500, 1000]
    if n not in n_values:
        n_values = sorted(list(set(n_values + [n])))
    
    reporte = integ.analizar_convergencia_simpson(n_values)
    
    print(f"\n{'n':>6} | {'Integral':>14} | {'Error Abs.':>12} | {'Error Rel. %':>10}")
    print("-" * 70)
    for i, n_val in enumerate(reporte['n']):
        integral = reporte['integrales'][i]
        error_abs = reporte['errores_absoluto'][i]
        error_rel = reporte['errores_relativo'][i]
        
        error_rel_str = f"{error_rel:.4f}" if error_rel is not None else "---"
        print(f"{n_val:>6} | {integral:>14.8f} | {error_abs:>12.2e} | {error_rel_str:>10}")
    
    # Generar gráfico
    print("\n" + "-" * 70)
    print("GENERANDO VISUALIZACIÓN")
    print("-" * 70)
    
    generar_grafico_simpson(reporte, integ)
    
    print("\nArchivo guardado: ../figuras/png/simpson_convergencia.png")
    print("Archivo guardado: ../figuras/pdf/simpson_convergencia.pdf")
    print("\n" + "=" * 70)


def generar_grafico_simpson(reporte, integ):
    """
    Generar gráfico de convergencia para regla de Simpson.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análisis de Convergencia - Regla de Simpson', fontsize=14, fontweight='bold')
    
    exact = integ.integral_exacta()
    
    # Gráfica 1: Convergencia de aproximación integral
    ax1.plot(reporte['n'], reporte['integrales'], 'o-', linewidth=2, markersize=8, 
             label='Aproximación Simpson', color=COLOR_PRINCIPAL)
    ax1.axhline(y=exact, color=COLOR_ACENTO, linestyle='--', linewidth=2, 
                label='Integral exacta')
    ax1.set_xlabel('Número de intervalos (n)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Valor de integral (Wh·B)', fontsize=11, fontweight='bold')
    ax1.set_title('Convergencia de la Integral', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.25, linestyle=':')
    ax1.legend(fontsize=10)
    
    # Gráfica 2: Convergencia de error (escala log-log)
    errores_abs_nonzero = [e if e > 0 else 1e-16 for e in reporte['errores_absoluto']]
    ax2.loglog(reporte['n'], errores_abs_nonzero, 'o-', linewidth=2, markersize=8, 
               label='Error absoluto (O(h⁴))', color=COLOR_SECUNDARIO)
    
    # Línea teórica: O(h^4) → O(n^-4)
    h_ref = (8.0 - 1.1) / 10
    error_ref = h_ref**4
    n_line = np.array([10, 1000])
    h_line = (8.0 - 1.1) / n_line
    error_line = error_ref * (h_ref / h_line)**4
    ax2.loglog(n_line, error_line, 'k--', linewidth=1.5, alpha=0.5, label='Referencia O(h⁴)')
    
    ax2.set_xlabel('Número de intervalos (n)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Error absoluto (escala log)', fontsize=11, fontweight='bold')
    ax2.set_title('Convergencia del Error (Log-Log)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.25, linestyle=':', which='both')
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    
    # Guardar figuras
    import os
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    fig.savefig('../figuras/png/simpson_convergencia.png', dpi=300, bbox_inches='tight')
    fig.savefig('../figuras/pdf/simpson_convergencia.pdf', bbox_inches='tight')
    plt.close()


def main():
    """Punto de ejecución principal."""
    n = None
    
    # Analizar argumento de línea de comandos si se proporciona
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Error: El argumento debe ser un número entero")
            sys.exit(1)
    
    ejecutar_simpson(n)


if __name__ == '__main__':
    main()
