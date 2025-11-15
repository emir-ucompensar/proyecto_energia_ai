"""
rectangulos.py
==============
Integración numérica mediante Método de los Rectángulos (Sumas de Riemann).
Implementa left, mid, right Riemann sums con análisis de convergencia y visualización.

Uso:
    python rectangulos.py [n] [mode]
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from integrales_numericas import IntegracionNumerica
import time

# Paleta de colores estandarizada - CONSISTENCIA VISUAL
COLOR_PRINCIPAL = '#C62828'    # SIEMPRE ROJO para curva E(N)
COLOR_SECUNDARIO = '#8B3A62'   # Púrpura profesional
COLOR_ACENTO = '#5C946E'       # Verde profesional
COLOR_RECTS_LEFT = '#1976D2'   # Azul formal para left
COLOR_RECTS_MID = '#388E3C'    # Verde formal para mid
COLOR_RECTS_RIGHT = '#F57C00'  # Naranja formal para right
COLOR_EXACTA = '#6A1B9A'       # Púrpura para integral exacta

# Datos de modelos AI del proyecto
MODELOS_AI = [
    {'nombre': 'TinyLLaMA-1.1B', 'parametros': 1.1, 'energia_exp': 11.7, 'tokens_s': 38.9},
    {'nombre': 'Gemma-2B', 'parametros': 2.0, 'energia_exp': 13.2, 'tokens_s': 31.2},
    {'nombre': 'Phi-3 Mini', 'parametros': 3.8, 'energia_exp': 14.8, 'tokens_s': 23.4},
    {'nombre': 'Mistral-7B', 'parametros': 7.0, 'energia_exp': 16.9, 'tokens_s': 19.8},
    {'nombre': 'LLaMA-3 8B', 'parametros': 8.0, 'energia_exp': 18.3, 'tokens_s': 17.1}
]


def rectangles_method(f, a, b, n, mode='mid'):
    """
    Calcular aproximación de integral mediante método de rectángulos (Sumas de Riemann).
    
    Parámetros:
    -----------
    f : callable
        Función a integrar
    a : float
        Límite inferior
    b : float
        Límite superior
    n : int
        Número de rectángulos/subintervalos
    mode : str
        Modo de evaluación: 'left', 'right', 'mid' (default: 'mid')
    
    Retorna:
    --------
    tuple : (aprox_area, x_rects, heights)
        aprox_area : float - Área aproximada
        x_rects : array - Posiciones x de los rectángulos
        heights : array - Alturas de los rectángulos
    """
    h = (b - a) / n
    
    if mode == 'left':
        # Usar extremo izquierdo de cada subintervalo
        x_eval = np.array([a + i * h for i in range(n)])
    elif mode == 'right':
        # Usar extremo derecho de cada subintervalo
        x_eval = np.array([a + (i + 1) * h for i in range(n)])
    elif mode == 'mid':
        # Usar punto medio de cada subintervalo
        x_eval = np.array([a + (i + 0.5) * h for i in range(n)])
    else:
        raise ValueError("mode debe ser 'left', 'right' o 'mid'")
    
    # Evaluar función en puntos seleccionados
    heights = f(x_eval)
    
    # Calcular área aproximada
    aprox_area = h * np.sum(heights)
    
    # Posiciones x para dibujar rectángulos (extremo izquierdo)
    x_rects = np.array([a + i * h for i in range(n)])
    
    return aprox_area, x_rects, heights


def ejecutar_rectangulos(n=None, mode='mid'):
    """
    Ejecutar análisis de método de rectángulos.
    
    Parámetros:
    -----------
    n : int, opcional
        Número de rectángulos. Si es None, solicita entrada.
    mode : str
        Modo de evaluación: 'left', 'right', 'mid'
    """
    integ = IntegracionNumerica()
    
    # Entrada del usuario si no se proporciona
    if n is None:
        print("=" * 70)
        print("MÉTODO DE LOS RECTÁNGULOS - SUMAS DE RIEMANN")
        print("=" * 70)
        print("\nFunción: E(N) = 0.0842*N^4 - 1.2156*N^3 + 6.8934*N^2 - 12.456*N + 11.234")
        print("Intervalo: [1.1, 8.0] (TinyLLaMA a LLaMA-3 8B)")
        print("Orden de convergencia: O(h) - Método básico de integración numérica")
        print("\nIntegral exacta (Antiderivada): Z = {:.6f} Wh·B".format(integ.integral_exacta()))
        print("\n" + "-" * 70)
        
        while True:
            try:
                n_input = input("\nIngrese número de rectángulos (n >= 4): ").strip()
                n = int(n_input)
                if n >= 4:
                    break
                else:
                    print("Error: n debe ser al menos 4")
            except ValueError:
                print("Error: Entrada no válida. Ingrese un número entero.")
        
        print("\nModos disponibles:")
        print("  left  - Extremo izquierdo de cada subintervalo")
        print("  mid   - Punto medio de cada subintervalo (más preciso)")
        print("  right - Extremo derecho de cada subintervalo")
        mode_input = input("\nSeleccione modo (default: mid): ").strip().lower()
        if mode_input in ['left', 'right', 'mid']:
            mode = mode_input
    
    # Medir tiempo de ejecución
    start_time = time.time()
    
    # Cálculo
    aprox_area, x_rects, heights = rectangles_method(
        integ.funcion_energia, integ.a, integ.b, n, mode
    )
    
    exec_time = time.time() - start_time
    
    integral_exact = integ.integral_exacta()
    error_abs = abs(aprox_area - integral_exact)
    error_rel = (error_abs / integral_exact) * 100
    
    # Resultados
    print("\n" + "=" * 70)
    print(f"RESULTADOS - MÉTODO DE RECTÁNGULOS ({mode.upper()})")
    print("=" * 70)
    print(f"\nNúmero de rectángulos (n): {n}")
    print(f"Tamaño de paso (h): {(integ.b - integ.a) / n:.6f}")
    print(f"Modo de evaluación: {mode}")
    print(f"\nIntegral aproximada: {aprox_area:.8f} Wh·B")
    print(f"Integral exacta:     {integral_exact:.8f} Wh·B")
    print(f"\nError absoluto: {error_abs:.2e} Wh·B")
    print(f"Error relativo: {error_rel:.6f}%")
    print(f"Tiempo de ejecución: {exec_time*1000:.3f} ms")
    
    # Análisis de convergencia
    print("\n" + "-" * 70)
    print("ANÁLISIS DE CONVERGENCIA")
    print("-" * 70)
    
    n_values = [10, 20, 50, 100, 200, 500, 1000]
    if n not in n_values:
        n_values = sorted(list(set(n_values + [n])))
    
    reporte = analizar_convergencia_rectangulos(integ, n_values, mode)
    
    print(f"\n{'n':>6} | {'Integral':>14} | {'Error Abs.':>12} | {'Error Rel. %':>10} | {'Tiempo (ms)':>12}")
    print("-" * 75)
    for i, n_val in enumerate(reporte['n']):
        integral = reporte['integrales'][i]
        error_abs = reporte['errores_absoluto'][i]
        error_rel = (error_abs / integral_exact) * 100
        exec_t = reporte['tiempos'][i]
        
        print(f"{n_val:>6} | {integral:>14.8f} | {error_abs:>12.2e} | {error_rel:>10.6f} | {exec_t:>12.3f}")
    
    # Generar gráfico
    print("\n" + "-" * 70)
    print("GENERANDO VISUALIZACIÓN")
    print("-" * 70)
    
    generar_grafico_rectangulos(reporte, integ, mode)
    
    print(f"\nArchivo guardado: ../figuras/png/rectangulos_{mode}_convergencia.png")
    print(f"Archivo guardado: ../figuras/pdf/rectangulos_{mode}_convergencia.pdf")
    print("\n" + "=" * 70)


def analizar_convergencia_rectangulos(integ, valores_n, mode='mid'):
    """
    Analizar convergencia del método de rectángulos para múltiples valores de n.
    
    Parámetros:
    -----------
    integ : IntegracionNumerica
        Objeto de integración
    valores_n : list
        Lista de valores de n a probar
    mode : str
        Modo de evaluación
    
    Retorna:
    --------
    dict
        Resultados con claves: n, integrales, errores_absoluto, tiempos
    """
    resultados = {
        'n': [],
        'integrales': [],
        'errores_absoluto': [],
        'tiempos': []
    }
    
    exact = integ.integral_exacta()
    
    for n in valores_n:
        start_time = time.time()
        aprox_area, _, _ = rectangles_method(
            integ.funcion_energia, integ.a, integ.b, n, mode
        )
        exec_time = (time.time() - start_time) * 1000  # en ms
        
        error_abs = abs(aprox_area - exact)
        
        resultados['n'].append(n)
        resultados['integrales'].append(aprox_area)
        resultados['errores_absoluto'].append(error_abs)
        resultados['tiempos'].append(exec_time)
    
    return resultados


def generar_grafico_rectangulos(reporte, integ, mode):
    """
    Generar gráfico de convergencia para método de rectángulos.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'Análisis de Convergencia - Método de Rectángulos ({mode.upper()})', 
                 fontsize=14, fontweight='bold')
    
    exact = integ.integral_exacta()
    
    # Color según modo
    color_mode = {'left': COLOR_RECTS_LEFT, 'mid': COLOR_RECTS_MID, 'right': COLOR_RECTS_RIGHT}
    color = color_mode.get(mode, COLOR_RECTS_MID)
    
    # Gráfica 1: Convergencia de aproximación integral
    ax1.plot(reporte['n'], reporte['integrales'], 'o-', linewidth=2, markersize=8, 
             label=f'Aproximación Rectángulos ({mode})', color=color)
    ax1.axhline(y=exact, color=COLOR_EXACTA, linestyle='--', linewidth=2, 
                label='Integral exacta')
    ax1.set_xlabel('Número de rectángulos (n)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Valor de integral (Wh·B)', fontsize=11, fontweight='bold')
    ax1.set_title('Convergencia de la Integral', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.25, linestyle=':')
    ax1.legend(fontsize=10)
    
    # Gráfica 2: Convergencia de error (escala log-log)
    errores_abs_nonzero = [e if e > 0 else 1e-16 for e in reporte['errores_absoluto']]
    ax2.loglog(reporte['n'], errores_abs_nonzero, 'o-', linewidth=2, markersize=8, 
               label=f'Error absoluto ({mode})', color=color)
    
    # Línea teórica: O(h) → O(n^-1)
    h_ref = (integ.b - integ.a) / 10
    error_ref = h_ref
    n_line = np.array([10, 1000])
    h_line = (integ.b - integ.a) / n_line
    error_line = error_ref * (h_ref / h_line)
    ax2.loglog(n_line, error_line, 'k--', linewidth=1.5, alpha=0.5, label='Referencia O(h)')
    
    ax2.set_xlabel('Número de rectángulos (n)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Error absoluto (escala log)', fontsize=11, fontweight='bold')
    ax2.set_title('Convergencia del Error (Log-Log)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.25, linestyle=':', which='both')
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    
    # Guardar figuras
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    fig.savefig(f'../figuras/png/rectangulos_{mode}_convergencia.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'../figuras/pdf/rectangulos_{mode}_convergencia.pdf', bbox_inches='tight')
    plt.close()


def main():
    """Punto de ejecución principal."""
    n = None
    mode = 'mid'
    
    # Analizar argumentos de línea de comandos
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Error: El primer argumento debe ser un número entero (n)")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        mode_arg = sys.argv[2].lower()
        if mode_arg in ['left', 'right', 'mid']:
            mode = mode_arg
        else:
            print("Error: El segundo argumento debe ser 'left', 'right' o 'mid'")
            sys.exit(1)
    
    ejecutar_rectangulos(n, mode)


if __name__ == '__main__':
    main()
