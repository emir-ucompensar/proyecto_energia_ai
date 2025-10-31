"""
grafico_4_pareto_tradeoff.py
==============================
Genera una curva de Pareto que visualiza el trade-off entre
rendimiento (tokens/s) y consumo energético.

Este análisis identifica configuraciones Pareto-óptimas donde
no es posible mejorar un criterio sin empeorar el otro.

Uso:
    python grafico_4_pareto_tradeoff.py

Salida:
    - grafico_4_pareto_tradeoff.png
    - grafico_4_pareto_tradeoff.pdf
"""

import matplotlib.pyplot as plt
import numpy as np
from config import (
    MODELOS, TAMANO_FIGURA, DPI, COLORES,
    configurar_semilla, guardar_figura
)
import os

def identificar_frente_pareto(objetivos):
    """
    Identifica puntos en el frente de Pareto.
    
    Para este problema de minimización de energía y maximización de tokens/s:
    Un punto es Pareto-óptimo si no existe otro punto que sea mejor en
    ambos objetivos simultáneamente.
    
    Args:
        objetivos: Array Nx2 con [energia, tokens_s]
        
    Returns:
        Array booleano indicando puntos Pareto-óptimos
    """
    n_puntos = objetivos.shape[0]
    es_pareto = np.ones(n_puntos, dtype=bool)
    
    for i in range(n_puntos):
        for j in range(n_puntos):
            if i != j:
                # j domina a i si consume menos energía Y genera más tokens
                if (objetivos[j, 0] < objetivos[i, 0] and 
                    objetivos[j, 1] > objetivos[i, 1]):
                    es_pareto[i] = False
                    break
    
    return es_pareto

def crear_grafico_pareto():
    """
    Crea un gráfico de Pareto con frente óptimo.
    
    Returns:
        matplotlib.figure.Figure: Figura generada
    """
    configurar_semilla()
    
    # Crear figura
    fig, ax = plt.subplots(figsize=TAMANO_FIGURA, dpi=DPI)
    
    # Datos (energía, tokens/s)
    energia = np.array(MODELOS['energia_total'])
    tokens_s = np.array(MODELOS['tokens_por_seg'])
    nombres = MODELOS['nombres_cortos']
    parametros = np.array(MODELOS['parametros'])
    
    # Preparar datos para análisis Pareto
    objetivos = np.column_stack((energia, tokens_s))
    
    # Identificar frente de Pareto
    es_pareto = identificar_frente_pareto(objetivos)
    
    # Separar puntos Pareto y no-Pareto
    pareto_indices = np.where(es_pareto)[0]
    no_pareto_indices = np.where(~es_pareto)[0]
    
    # Graficar puntos no-Pareto
    if len(no_pareto_indices) > 0:
        scatter_no_pareto = ax.scatter(
            energia[no_pareto_indices],
            tokens_s[no_pareto_indices],
            s=300, c='lightgray', marker='o',
            edgecolors='black', linewidths=2,
            label='No Pareto-óptimo', alpha=0.6
        )
    
    # Graficar puntos Pareto-óptimos
    scatter_pareto = ax.scatter(
        energia[pareto_indices],
        tokens_s[pareto_indices],
        s=400, c=parametros[pareto_indices],
        cmap='viridis', marker='*',
        edgecolors='red', linewidths=2.5,
        label='Pareto-óptimo', alpha=0.9
    )
    
    # Barra de color para tamaño del modelo
    cbar = plt.colorbar(scatter_pareto, ax=ax, label='Tamaño (B parámetros)')
    cbar.ax.tick_params(labelsize=11)
    
    # Dibujar línea de frente de Pareto
    if len(pareto_indices) > 1:
        # Ordenar puntos Pareto por energía
        pareto_orden = pareto_indices[np.argsort(energia[pareto_indices])]
        ax.plot(energia[pareto_orden], tokens_s[pareto_orden],
               'r--', linewidth=2, alpha=0.7, label='Frente de Pareto')
    
    # Añadir etiquetas para cada punto
    for i, nombre in enumerate(nombres):
        offset_x = 0.3 if es_pareto[i] else 0.2
        offset_y = 1.5 if es_pareto[i] else 1.0
        
        ax.annotate(
            nombre,
            (energia[i], tokens_s[i]),
            xytext=(offset_x, offset_y),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold' if es_pareto[i] else 'normal',
            bbox=dict(
                boxstyle='round,pad=0.5',
                facecolor='yellow' if es_pareto[i] else 'lightblue',
                alpha=0.8
            ),
            arrowprops=dict(
                arrowstyle='->',
                connectionstyle='arc3,rad=0.2',
                color='red' if es_pareto[i] else 'blue'
            )
        )
    
    # Añadir cuadrantes de referencia
    energia_media = np.mean(energia)
    tokens_media = np.mean(tokens_s)
    
    ax.axvline(x=energia_media, color='gray', linestyle=':', alpha=0.5)
    ax.axhline(y=tokens_media, color='gray', linestyle=':', alpha=0.5)
    
    # Etiquetas de cuadrantes
    ax.text(energia_media * 0.95, tokens_media * 1.05, 'Óptimo\n(↓E, ↑T)',
            ha='right', va='bottom', fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    ax.text(energia_media * 1.05, tokens_media * 0.95, 'Sub-óptimo\n(↑E, ↓T)',
            ha='left', va='top', fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
    
    # Configuración de ejes y título
    ax.set_xlabel('Consumo Energético (Wh)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Rendimiento (tokens/s)', fontsize=14, fontweight='bold')
    ax.set_title('Frontera de Pareto: Trade-off Rendimiento vs. Consumo\n' +
                 'Análisis de Optimización Multi-Objetivo',
                 fontsize=16, fontweight='bold', pad=20)
    
    # Grid y leyenda
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    # Invertir eje X para que menor energía esté a la derecha
    ax.invert_xaxis()
    
    # Ajustar layout
    plt.tight_layout()
    
    return fig

def analizar_pareto():
    """Imprime análisis detallado del frente de Pareto."""
    energia = np.array(MODELOS['energia_total'])
    tokens_s = np.array(MODELOS['tokens_por_seg'])
    nombres = MODELOS['nombres']
    
    objetivos = np.column_stack((energia, tokens_s))
    es_pareto = identificar_frente_pareto(objetivos)
    
    print("\nAnálisis de Pareto:")
    print("=" * 70)
    print("\nModelos Pareto-óptimos:")
    for i, es_opt in enumerate(es_pareto):
        if es_opt:
            print(f"  [*] {nombres[i]:20} | {energia[i]:5.1f} Wh | "
                  f"{tokens_s[i]:5.1f} tokens/s")
    
    print("\nModelos dominados (no Pareto-óptimos):")
    for i, es_opt in enumerate(es_pareto):
        if not es_opt:
            print(f"    {nombres[i]:20} | {energia[i]:5.1f} Wh | "
                  f"{tokens_s[i]:5.1f} tokens/s")
    
    print(f"\nPorcentaje de modelos Pareto-óptimos: "
          f"{np.sum(es_pareto) / len(es_pareto) * 100:.1f}%")

def guardar_grafico(fig, nombre_base='4_pareto_tradeoff'):
    """Guarda el gráfico usando la función centralizada."""
    guardar_figura(fig, nombre_base, dpi=DPI)

def main():
    """Función principal."""
    print("=" * 70)
    print("Generando Gráfico 4: Curva de Pareto (Trade-off)")
    print("=" * 70)
    
    # Análisis
    analizar_pareto()
    
    # Crear gráfico
    fig = crear_grafico_pareto()
    
    # Guardar
    guardar_grafico(fig)
    
    print("\n[OK] Proceso completado exitosamente")
    plt.show()

if __name__ == '__main__':
    main()
