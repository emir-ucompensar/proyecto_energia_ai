"""
trapecio.py
===========
Integración numérica mediante Regla del Trapecio para análisis de consumo energético.
Implementa método de convergencia O(h^2) con seguimiento de errores y visualización.

Uso:
    python trapecio.py [número_de_intervalos]
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from integrales_numericas import IntegracionNumerica

# Paleta de colores profesional
COLOR_PRINCIPAL = '#1F4788'    # Azul oscuro profesional
COLOR_SECUNDARIO = '#8B3A62'   # Púrpura profesional
COLOR_ACENTO = '#5C946E'       # Verde profesional


def ejecutar_trapecio(n=None):
    """
    Ejecutar análisis de regla del trapecio.
    
    Parámetros:
    -----------
    n : int, opcional
        Número de intervalos. Si es None, solicita entrada del usuario.
    """
    integ = IntegracionNumerica()
    
    # Entrada del usuario para número de intervalos si no se proporciona
    if n is None:
        print("=" * 70)
        print("REGLA DEL TRAPECIO - INTEGRACIÓN NUMÉRICA")
        print("=" * 70)
        print("\nFunción: E(N) = 0.0842*N^4 - 1.2156*N^3 + 6.8934*N^2 - 12.456*N + 11.234")
        print("Intervalo: [1.1, 8.0] (TinyLLaMA a LLaMA-3 8B)")
        print("Orden de convergencia: O(h^2)")
        print("\nIntegral exacta (Antiderivada): Z = {:.6f} Wh·B".format(integ.integral_exacta()))
        print("\n" + "-" * 70)
        
        while True:
            try:
                n_input = input("\nIngrese número de intervalos (n >= 4): ").strip()
                n = int(n_input)
                if n >= 4:
                    break
                else:
                    print("Error: n debe ser al menos 4")
            except ValueError:
                print("Error: Entrada no válida. Ingrese un número entero.")
    
    # Cálculo
    integral_trap = integ.trapecio(n)
    integral_exact = integ.integral_exacta()
    error_abs = abs(integral_trap - integral_exact)
    error_rel = (error_abs / integral_exact) * 100
    
    # Resultados
    print("\n" + "=" * 70)
    print("RESULTADOS - REGLA DEL TRAPECIO")
    print("=" * 70)
    print(f"\nNúmero de intervalos (n): {n}")
    print(f"Tamaño de paso (h): {(8.0 - 1.1) / n:.6f}")
    print(f"\nIntegral aproximada: {integral_trap:.8f} Wh·B")
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
    
    reporte = integ.analizar_convergencia_trapecio(n_values)
    
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
    
    generar_grafico_trapecio(reporte, integ)
    
    print("\nArchivo guardado: ../figuras/png/trapecio_convergencia.png")
    print("Archivo guardado: ../figuras/pdf/trapecio_convergencia.pdf")
    print("\n" + "=" * 70)


def generar_grafico_trapecio(reporte, integ):
    """
    Generar gráfico de convergencia para regla del trapecio.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análisis de Convergencia - Regla del Trapecio', fontsize=14, fontweight='bold')
    
    exact = integ.integral_exacta()
    
    # Gráfica 1: Convergencia de aproximación integral
    ax1.plot(reporte['n'], reporte['integrales'], 'o-', linewidth=2, markersize=8, 
             label='Aproximación trapecio', color=COLOR_PRINCIPAL)
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
               label='Error absoluto (O(h²))', color=COLOR_SECUNDARIO)
    
    # Línea teórica: O(h^2) → O(n^-2)
    h_ref = (8.0 - 1.1) / 10
    error_ref = h_ref**2
    n_line = np.array([10, 1000])
    h_line = (8.0 - 1.1) / n_line
    error_line = error_ref * (h_ref / h_line)**2
    ax2.loglog(n_line, error_line, 'k--', linewidth=1.5, alpha=0.5, label='Referencia O(h²)')
    
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
    
    fig.savefig('../figuras/png/trapecio_convergencia.png', dpi=300, bbox_inches='tight')
    fig.savefig('../figuras/pdf/trapecio_convergencia.pdf', bbox_inches='tight')
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
    
    ejecutar_trapecio(n)


if __name__ == '__main__':
    main()
