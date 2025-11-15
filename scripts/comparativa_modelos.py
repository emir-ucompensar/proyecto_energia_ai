"""
comparativa_modelos.py
======================
Comparación visual entre múltiples modelos de IA usando método de rectángulos.
Genera gráficas comparativas con todos los modelos superpuestos.

Uso:
    python comparativa_modelos.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from integrales_numericas import IntegracionNumerica
import os

# Paleta de colores estandarizada - CONSISTENCIA VISUAL
COLOR_CURVA = '#C62828'        # SIEMPRE ROJO para E(N) - curva principal
COLORS_MODES = {
    'left': '#1976D2',   # Azul formal
    'mid': '#388E3C',    # Verde formal
    'right': '#F57C00'   # Naranja formal
}

# Datos de modelos AI - usar E(N) calculado para estar sobre la curva
MODELOS_AI = [
    {'nombre': 'TinyLLaMA-1.1B', 'parametros': 1.1, 'energia_exp': 11.7, 'color': '#E91E63'},
    {'nombre': 'Gemma-2B', 'parametros': 2.0, 'energia_exp': 13.2, 'color': '#9C27B0'},
    {'nombre': 'Phi-3 Mini', 'parametros': 3.8, 'energia_exp': 14.8, 'color': '#3F51B5'},
    {'nombre': 'Mistral-7B', 'parametros': 7.0, 'energia_exp': 16.9, 'color': '#00BCD4'},
    {'nombre': 'LLaMA-3 8B', 'parametros': 8.0, 'energia_exp': 18.3, 'color': '#4CAF50'}
]


def rectangles_method(f, a, b, n, mode='mid'):
    """Calcular método de rectángulos."""
    h = (b - a) / n
    
    if mode == 'left':
        x_eval = np.array([a + i * h for i in range(n)])
    elif mode == 'right':
        x_eval = np.array([a + (i + 1) * h for i in range(n)])
    elif mode == 'mid':
        x_eval = np.array([a + (i + 0.5) * h for i in range(n)])
    else:
        raise ValueError("mode debe ser 'left', 'right' o 'mid'")
    
    heights = f(x_eval)
    aprox_area = h * np.sum(heights)
    x_rects = np.array([a + i * h for i in range(n)])
    
    return aprox_area, x_rects, heights, h


def comparar_todos_modelos_mismo_n(n=100, mode='mid'):
    """
    Generar gráfica comparativa con todos los modelos en un mismo valor de n.
    """
    integ = IntegracionNumerica()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Curva de función
    N_curva = np.linspace(integ.a, integ.b, 500)
    E_curva = integ.funcion_energia(N_curva)
    
    # Calcular rectángulos
    aprox_area, x_rects, heights, width = rectangles_method(
        integ.funcion_energia, integ.a, integ.b, n, mode
    )
    
    # Dibujar rectángulos (muy transparentes)
    ax.bar(x_rects, heights, width=width, align='edge',
           alpha=0.15, color=COLORS_MODES[mode], edgecolor=COLORS_MODES[mode],
           linewidth=0.8, zorder=2, label=f'Rectángulos (n={n}, {mode})')
    
    # Dibujar curva principal
    ax.plot(N_curva, E_curva, linewidth=4, color=COLOR_CURVA,
            zorder=5, label='E(N) - Función de consumo', alpha=0.9)
    
    # Marcar cada modelo con su color único - SOBRE LA CURVA
    for modelo in MODELOS_AI:
        N_modelo = modelo['parametros']
        E_modelo = integ.funcion_energia(N_modelo)  # Calcular valor en curva
        ax.plot(N_modelo, E_modelo,
               'o', markersize=14, color=modelo['color'],
               markeredgecolor='white', markeredgewidth=2.5,
               zorder=10, label=modelo['nombre'])
        
        # Línea vertical al eje x
        ax.vlines(N_modelo, 0, E_modelo,
                 colors=modelo['color'], linestyles='--',
                 linewidth=1.5, alpha=0.4, zorder=3)
    
    # Información de aproximación
    exact = integ.integral_exacta()
    error_abs = abs(aprox_area - exact)
    error_rel = (error_abs / exact) * 100
    
    # Título y labels
    ax.set_title(f'Comparativa de Modelos de IA - Método de Rectángulos ({mode.upper()})\n' +
                f'n = {n} | Área ≈ {aprox_area:.6f} Wh·B | Error: {error_rel:.4f}%',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Número de Parámetros (Billones)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Consumo Energético (Wh)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle=':', zorder=1)
    ax.set_xlim(integ.a - 0.4, integ.b + 0.4)
    ax.set_ylim(0, max(E_curva) * 1.15)
    ax.legend(fontsize=10, loc='upper left', framealpha=0.95, ncol=2)
    
    plt.tight_layout()
    
    # Guardar
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    filename = f'comparativa_modelos_n{n}_{mode}'
    fig.savefig(f'../figuras/png/{filename}.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'../figuras/pdf/{filename}.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Comparativa guardada: {filename}.png / {filename}.pdf")


def comparar_tres_n_mismo_modo(mode='mid'):
    """
    Generar gráfica con 3 subplots mostrando n=10, 100, 1000 para mismo modo.
    """
    integ = IntegracionNumerica()
    n_values = [10, 100, 1000]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f'Convergencia del Método de Rectángulos ({mode.upper()}) - Modelos de IA',
                fontsize=16, fontweight='bold', y=1.02)
    
    N_curva = np.linspace(integ.a, integ.b, 500)
    E_curva = integ.funcion_energia(N_curva)
    exact = integ.integral_exacta()
    
    for idx, n in enumerate(n_values):
        ax = axes[idx]
        
        # Calcular rectángulos
        aprox_area, x_rects, heights, width = rectangles_method(
            integ.funcion_energia, integ.a, integ.b, n, mode
        )
        error_abs = abs(aprox_area - exact)
        error_rel = (error_abs / exact) * 100
        
        # Dibujar rectángulos
        ax.bar(x_rects, heights, width=width, align='edge',
               alpha=0.25, color=COLORS_MODES[mode], edgecolor=COLORS_MODES[mode],
               linewidth=1, zorder=2)
        
        # Dibujar curva
        ax.plot(N_curva, E_curva, linewidth=3, color=COLOR_CURVA,
                zorder=5, label='E(N)')
        
        # Modelos - SOBRE LA CURVA
        for modelo in MODELOS_AI:
            N_modelo = modelo['parametros']
            E_modelo = integ.funcion_energia(N_modelo)
            ax.plot(N_modelo, E_modelo,
                   'o', markersize=10, color=modelo['color'],
                   markeredgecolor='white', markeredgewidth=2,
                   zorder=10)
        
        # Configuración
        ax.set_title(f'n = {n}\nÁrea ≈ {aprox_area:.4f} Wh·B\nError: {error_rel:.3f}%',
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Parámetros (B)', fontsize=10, fontweight='bold')
        if idx == 0:
            ax.set_ylabel('Energía (Wh)', fontsize=10, fontweight='bold')
            ax.legend(fontsize=9, loc='upper left')
        ax.grid(True, alpha=0.25, linestyle=':')
        ax.set_xlim(integ.a - 0.2, integ.b + 0.2)
        ax.set_ylim(10, max(E_curva) * 1.12)
    
    plt.tight_layout()
    
    # Guardar
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    filename = f'comparativa_convergencia_{mode}'
    fig.savefig(f'../figuras/png/{filename}.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'../figuras/pdf/{filename}.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Convergencia guardada: {filename}.png / {filename}.pdf")


def comparar_tres_modos_mismo_n(n=100):
    """
    Generar gráfica con 3 subplots mostrando left, mid, right para mismo n.
    """
    integ = IntegracionNumerica()
    modes = ['left', 'mid', 'right']
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f'Comparación de Modos - n = {n} rectángulos',
                fontsize=16, fontweight='bold', y=1.02)
    
    N_curva = np.linspace(integ.a, integ.b, 500)
    E_curva = integ.funcion_energia(N_curva)
    exact = integ.integral_exacta()
    
    for idx, mode in enumerate(modes):
        ax = axes[idx]
        
        # Calcular rectángulos
        aprox_area, x_rects, heights, width = rectangles_method(
            integ.funcion_energia, integ.a, integ.b, n, mode
        )
        error_abs = abs(aprox_area - exact)
        error_rel = (error_abs / exact) * 100
        
        # Dibujar rectángulos
        ax.bar(x_rects, heights, width=width, align='edge',
               alpha=0.3, color=COLORS_MODES[mode], edgecolor=COLORS_MODES[mode],
               linewidth=1.2, zorder=2, label=f'Rectángulos ({mode})')
        
        # Dibujar curva
        ax.plot(N_curva, E_curva, linewidth=3, color=COLOR_CURVA,
                zorder=5, label='E(N)')
        
        # Modelos - SOBRE LA CURVA
        for modelo in MODELOS_AI:
            N_modelo = modelo['parametros']
            E_modelo = integ.funcion_energia(N_modelo)
            ax.plot(N_modelo, E_modelo,
                   'o', markersize=10, color=modelo['color'],
                   markeredgecolor='white', markeredgewidth=2,
                   zorder=10)
        
        # Configuración
        ax.set_title(f'Modo: {mode.upper()}\nÁrea ≈ {aprox_area:.4f} Wh·B\nError: {error_rel:.3f}%',
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Parámetros (B)', fontsize=10, fontweight='bold')
        if idx == 0:
            ax.set_ylabel('Energía (Wh)', fontsize=10, fontweight='bold')
        ax.legend(fontsize=9, loc='upper left')
        ax.grid(True, alpha=0.25, linestyle=':')
        ax.set_xlim(integ.a - 0.2, integ.b + 0.2)
        ax.set_ylim(10, max(E_curva) * 1.12)
    
    plt.tight_layout()
    
    # Guardar
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    filename = f'comparativa_modos_n{n}'
    fig.savefig(f'../figuras/png/{filename}.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'../figuras/pdf/{filename}.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Comparación de modos guardada: {filename}.png / {filename}.pdf")


def generar_tabla_resultados():
    """Generar tabla con resultados para todos los modelos y configuraciones."""
    integ = IntegracionNumerica()
    exact = integ.integral_exacta()
    
    print("\n" + "=" * 100)
    print("TABLA DE RESULTADOS - MÉTODO DE RECTÁNGULOS CON MODELOS DE IA")
    print("=" * 100)
    print(f"\nIntegral exacta: {exact:.8f} Wh·B")
    print(f"Intervalo: [{integ.a}, {integ.b}] (TinyLLaMA 1.1B → LLaMA-3 8B)")
    
    print("\n" + "-" * 100)
    print("Modelos evaluados:")
    for modelo in MODELOS_AI:
        print(f"  • {modelo['nombre']:<15} : {modelo['parametros']:>4.1f}B parámetros, " +
              f"{modelo['energia_exp']:>5.1f} Wh consumo experimental")
    
    print("\n" + "=" * 100)
    print(f"{'Modo':>8} | {'n':>6} | {'Área Aprox.':>14} | {'Error Abs.':>12} | " +
          f"{'Error Rel. %':>12} | {'Precisión':>12}")
    print("-" * 100)
    
    modes = ['left', 'mid', 'right']
    n_values = [10, 100, 1000]
    
    for mode in modes:
        for n in n_values:
            aprox_area, _, _, _ = rectangles_method(
                integ.funcion_energia, integ.a, integ.b, n, mode
            )
            error_abs = abs(aprox_area - exact)
            error_rel = (error_abs / exact) * 100
            
            # Clasificar precisión
            if error_rel < 0.01:
                precision = "Ultra-alta"
            elif error_rel < 0.1:
                precision = "Muy alta"
            elif error_rel < 1:
                precision = "Alta"
            elif error_rel < 5:
                precision = "Media"
            else:
                precision = "Baja"
            
            print(f"{mode:>8} | {n:>6} | {aprox_area:>14.8f} | {error_abs:>12.2e} | " +
                  f"{error_rel:>12.6f} | {precision:>12}")
        
        if mode != modes[-1]:
            print("-" * 100)
    
    print("=" * 100)


def main():
    """Ejecutar todas las comparativas."""
    print("=" * 80)
    print("GENERANDO COMPARATIVAS DE MODELOS - MÉTODO DE RECTÁNGULOS")
    print("=" * 80)
    
    # Comparativas por n (todos los modos)
    for mode in ['left', 'mid', 'right']:
        print(f"\nGenerando comparativas para modo: {mode.upper()}")
        for n in [10, 100, 1000]:
            comparar_todos_modelos_mismo_n(n, mode)
    
    # Convergencia por modo
    for mode in ['left', 'mid', 'right']:
        print(f"\nGenerando convergencia para modo: {mode.upper()}")
        comparar_tres_n_mismo_modo(mode)
    
    # Comparación de modos
    for n in [10, 100, 1000]:
        print(f"\nGenerando comparación de modos para n={n}")
        comparar_tres_modos_mismo_n(n)
    
    # Tabla de resultados
    generar_tabla_resultados()
    
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO")
    print("Todas las comparativas han sido guardadas en:")
    print("  - figuras/png/")
    print("  - figuras/pdf/")
    print("=" * 80)


if __name__ == '__main__':
    main()
