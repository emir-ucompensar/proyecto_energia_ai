"""
rectangulos_visualizacion.py
=============================
Visualización de método de rectángulos con modelos AI.
Genera gráficas con rectángulos semi-transparentes, curva visible y puntos de modelos.

Uso:
    python rectangulos_visualizacion.py
"""

import numpy as np
import matplotlib.pyplot as plt
from integrales_numericas import IntegracionNumerica
import os

# Paleta de colores estandarizada - CONSISTENCIA VISUAL
COLOR_CURVA = '#C62828'        # SIEMPRE ROJO para E(N) - curva principal
COLOR_RECTS_LEFT = '#1976D2'   # Azul formal para left
COLOR_RECTS_MID = '#388E3C'    # Verde formal para mid  
COLOR_RECTS_RIGHT = '#F57C00'  # Naranja formal para right
COLOR_EXACTA = '#6A1B9A'       # Púrpura para integral exacta
COLOR_MODELOS = '#424242'      # Gris oscuro para puntos de modelos (sobre la curva)

# Datos de modelos AI del proyecto
# IMPORTANTE: energia_exp es solo para referencia de validación
# Los puntos se grafican usando E(parametros) calculado para estar SOBRE LA CURVA
MODELOS_AI = [
    {'nombre': 'TinyLLaMA-1.1B', 'parametros': 1.1, 'energia_exp': 11.7, 'label': 'TinyLLaMA\n1.1B'},
    {'nombre': 'Gemma-2B', 'parametros': 2.0, 'energia_exp': 13.2, 'label': 'Gemma\n2B'},
    {'nombre': 'Phi-3 Mini', 'parametros': 3.8, 'energia_exp': 14.8, 'label': 'Phi-3\n3.8B'},
    {'nombre': 'Mistral-7B', 'parametros': 7.0, 'energia_exp': 16.9, 'label': 'Mistral\n7B'},
    {'nombre': 'LLaMA-3 8B', 'parametros': 8.0, 'energia_exp': 18.3, 'label': 'LLaMA-3\n8B'}
]


def rectangles_method(f, a, b, n, mode='mid'):
    """
    Calcular aproximación de integral mediante método de rectángulos.
    
    Retorna:
    --------
    tuple : (aprox_area, x_rects, heights, width)
    """
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


def graficar_rectangulos_con_modelos(n_values=[10, 100, 1000], mode='mid'):
    """
    Generar gráficas de rectángulos para diferentes valores de n con puntos de modelos.
    
    Parámetros:
    -----------
    n_values : list
        Lista de valores de n a graficar
    mode : str
        Modo: 'left', 'right', 'mid'
    """
    integ = IntegracionNumerica()
    
    # Color según modo
    color_mode = {'left': COLOR_RECTS_LEFT, 'mid': COLOR_RECTS_MID, 'right': COLOR_RECTS_RIGHT}
    color_rect = color_mode.get(mode, COLOR_RECTS_MID)
    
    # Crear figura con subplots
    fig, axes = plt.subplots(1, len(n_values), figsize=(6*len(n_values), 5))
    if len(n_values) == 1:
        axes = [axes]
    
    fig.suptitle(f'Método de Rectángulos ({mode.upper()}) - Modelos de IA', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    # Generar curva suave para referencia
    N_curva = np.linspace(integ.a, integ.b, 500)
    E_curva = integ.funcion_energia(N_curva)
    
    for idx, n in enumerate(n_values):
        ax = axes[idx]
        
        # Calcular rectángulos
        aprox_area, x_rects, heights, width = rectangles_method(
            integ.funcion_energia, integ.a, integ.b, n, mode
        )
        
        # Dibujar rectángulos (semi-transparentes, zorder bajo)
        ax.bar(x_rects, heights, width=width, align='edge',
               alpha=0.3, color=color_rect, edgecolor=color_rect, 
               linewidth=1.5, zorder=2, label=f'Rectángulos (n={n})')
        
        # Dibujar curva (siempre encima, zorder alto)
        ax.plot(N_curva, E_curva, linewidth=3, color=COLOR_CURVA, 
                zorder=5, label='E(N) - Función energía')
        
        # Marcar puntos de modelos (encima de todo)
        # CRÍTICO: Usar E(parametros) calculado para que estén SOBRE LA CURVA
        for modelo in MODELOS_AI:
            N_modelo = modelo['parametros']
            E_modelo = integ.funcion_energia(N_modelo)  # Calcular valor en la curva
            ax.plot(N_modelo, E_modelo, 
                   'o', markersize=10, color=COLOR_MODELOS, 
                   markeredgecolor='white', markeredgewidth=2,
                   zorder=10)
            # Anotación con nombre del modelo (fuera del área)
            ax.annotate(modelo['label'], 
                       xy=(N_modelo, E_modelo),
                       xytext=(0, 15), textcoords='offset points',
                       ha='center', fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                edgecolor=COLOR_MODELOS, alpha=0.8),
                       zorder=11)
        
        # Configuración del subplot
        ax.set_xlabel('Parámetros (Billones)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Consumo Energético (Wh)', fontsize=11, fontweight='bold')
        ax.set_title(f'n = {n}\nÁrea ≈ {aprox_area:.4f} Wh·B', 
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.25, linestyle=':', zorder=1)
        ax.set_xlim(integ.a - 0.2, integ.b + 0.2)
        ax.set_ylim(10, max(E_curva) * 1.15)
        
        # Leyenda solo en el primer subplot
        if idx == 0:
            ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
    
    plt.tight_layout()
    
    # Guardar figuras
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    filename = f'rectangulos_{mode}_modelos'
    fig.savefig(f'../figuras/png/{filename}.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'../figuras/pdf/{filename}.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Gráfica guardada: {filename}.png / {filename}.pdf")
    
    return aprox_area


def graficar_comparativa_n_individual(n_list=[10, 100, 1000], mode='mid'):
    """
    Generar gráficas individuales para cada valor de n (más detalladas).
    """
    integ = IntegracionNumerica()
    color_mode = {'left': COLOR_RECTS_LEFT, 'mid': COLOR_RECTS_MID, 'right': COLOR_RECTS_RIGHT}
    color_rect = color_mode.get(mode, COLOR_RECTS_MID)
    
    N_curva = np.linspace(integ.a, integ.b, 500)
    E_curva = integ.funcion_energia(N_curva)
    
    for n in n_list:
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Calcular rectángulos
        aprox_area, x_rects, heights, width = rectangles_method(
            integ.funcion_energia, integ.a, integ.b, n, mode
        )
        
        # Calcular error
        exact = integ.integral_exacta()
        error_abs = abs(aprox_area - exact)
        error_rel = (error_abs / exact) * 100
        
        # Dibujar rectángulos
        ax.bar(x_rects, heights, width=width, align='edge',
               alpha=0.25, color=color_rect, edgecolor=color_rect, 
               linewidth=1.2, zorder=2, label=f'Rectángulos ({mode}, n={n})')
        
        # Dibujar curva
        ax.plot(N_curva, E_curva, linewidth=3.5, color=COLOR_CURVA, 
                zorder=5, label='E(N) - Consumo energético')
        
        # Marcar modelos con mejor visibilidad - SOBRE LA CURVA
        for i, modelo in enumerate(MODELOS_AI):
            color_marker = plt.cm.Set1(i)
            N_modelo = modelo['parametros']
            E_modelo = integ.funcion_energia(N_modelo)  # Calcular en curva
            ax.plot(N_modelo, E_modelo, 
                   'o', markersize=12, color=color_marker, 
                   markeredgecolor='white', markeredgewidth=2.5,
                   zorder=10, label=modelo['nombre'])
        
        # Título con información detallada
        ax.set_title(f'Método de Rectángulos ({mode.upper()}) - n = {n} rectángulos\n' + 
                    f'Área aproximada: {aprox_area:.6f} Wh·B | ' +
                    f'Error: {error_abs:.2e} Wh·B ({error_rel:.4f}%)',
                    fontsize=13, fontweight='bold', pad=15)
        
        ax.set_xlabel('Número de Parámetros (Billones)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Consumo Energético (Wh)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle=':', zorder=1)
        ax.set_xlim(integ.a - 0.3, integ.b + 0.3)
        ax.set_ylim(10, max(E_curva) * 1.12)
        ax.legend(fontsize=10, loc='upper left', framealpha=0.95, ncol=2)
        
        plt.tight_layout()
        
        # Guardar
        os.makedirs('../figuras/png', exist_ok=True)
        os.makedirs('../figuras/pdf', exist_ok=True)
        
        filename = f'rectangulos_{mode}_n{n}_detalle'
        fig.savefig(f'../figuras/png/{filename}.png', dpi=300, bbox_inches='tight')
        fig.savefig(f'../figuras/pdf/{filename}.pdf', bbox_inches='tight')
        plt.close()
        
        print(f"Gráfica detallada guardada: {filename}.png / {filename}.pdf")


def generar_tabla_comparativa(n_values=[10, 100, 1000], modes=['left', 'mid', 'right']):
    """
    Generar tabla comparativa de resultados para diferentes n y modos.
    """
    integ = IntegracionNumerica()
    exact = integ.integral_exacta()
    
    print("\n" + "=" * 90)
    print("TABLA COMPARATIVA - MÉTODO DE RECTÁNGULOS")
    print("=" * 90)
    print(f"\nIntegral exacta (antiderivada): {exact:.8f} Wh·B")
    print("\n" + "-" * 90)
    print(f"{'Modo':>8} | {'n':>6} | {'Área Aprox.':>14} | {'Error Abs.':>12} | {'Error Rel. %':>12}")
    print("-" * 90)
    
    for mode in modes:
        for n in n_values:
            aprox_area, _, _, _ = rectangles_method(
                integ.funcion_energia, integ.a, integ.b, n, mode
            )
            error_abs = abs(aprox_area - exact)
            error_rel = (error_abs / exact) * 100
            
            print(f"{mode:>8} | {n:>6} | {aprox_area:>14.8f} | {error_abs:>12.2e} | {error_rel:>12.6f}")
        
        if mode != modes[-1]:
            print("-" * 90)
    
    print("=" * 90)


def main():
    """Ejecutar todas las visualizaciones."""
    print("=" * 70)
    print("GENERANDO VISUALIZACIONES - MÉTODO DE RECTÁNGULOS")
    print("=" * 70)
    
    # Generar gráficas comparativas para cada modo
    for mode in ['left', 'mid', 'right']:
        print(f"\n--- Modo: {mode.upper()} ---")
        
        # Gráfica con 3 subplots
        graficar_rectangulos_con_modelos([10, 100, 1000], mode)
        
        # Gráficas individuales detalladas
        graficar_comparativa_n_individual([10, 100, 1000], mode)
    
    # Tabla comparativa
    generar_tabla_comparativa()
    
    print("\n" + "=" * 70)
    print("PROCESO COMPLETADO")
    print("Todas las gráficas han sido guardadas en:")
    print("  - figuras/png/")
    print("  - figuras/pdf/")
    print("=" * 70)


if __name__ == '__main__':
    main()
