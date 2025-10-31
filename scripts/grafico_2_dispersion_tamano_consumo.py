"""
grafico_2_dispersion_tamano_consumo.py
========================================
Genera un gráfico de dispersión que relaciona el tamaño del modelo
(número de parámetros) con el consumo energético total.

Este análisis permite identificar la relación entre complejidad
del modelo y demanda energética.

Uso:
    python grafico_2_dispersion_tamano_consumo.py

Salida:
    - grafico_2_dispersion_tamano_consumo.png
    - grafico_2_dispersion_tamano_consumo.pdf
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from config import (
    MODELOS, TAMANO_FIGURA, DPI, COLORES, DIR_SALIDA,
    configurar_semilla, guardar_figura
)
import os

def modelo_potencial(x, a, b):
    """Función potencial: y = a * x^b"""
    return a * np.power(x, b)

def crear_grafico_dispersion():
    """
    Crea un gráfico de dispersión con línea de tendencia.
    
    Returns:
        matplotlib.figure.Figure: Figura generada
    """
    configurar_semilla()
    
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=TAMANO_FIGURA, dpi=DPI)
    
    # Datos
    parametros = np.array(MODELOS['parametros'])
    energia = np.array(MODELOS['energia_total'])
    nombres = MODELOS['nombres_cortos']
    
    # Ajuste de curva potencial
    try:
        popt, _ = curve_fit(modelo_potencial, parametros, energia, p0=[10, 0.5])
        a_opt, b_opt = popt
        
        # Generar curva suave
        x_curva = np.linspace(min(parametros), max(parametros), 100)
        y_curva = modelo_potencial(x_curva, a_opt, b_opt)
        
        # Calcular R²
        residuos = energia - modelo_potencial(parametros, a_opt, b_opt)
        ss_res = np.sum(residuos**2)
        ss_tot = np.sum((energia - np.mean(energia))**2)
        r2 = 1 - (ss_res / ss_tot)
        
        # Dibujar curva de ajuste
        ax.plot(x_curva, y_curva, 'r--', linewidth=2.5, alpha=0.7,
                label=f'Ajuste: E = {a_opt:.2f} × N^{b_opt:.2f} (R² = {r2:.3f})')
    except:
        print("Advertencia: No se pudo ajustar curva potencial")
    
    # Scatter plot con tamaños proporcionales a tokens/s
    tokens_s = np.array(MODELOS['tokens_por_seg'])
    tamanios = (tokens_s / max(tokens_s)) * 500 + 100  # Normalizar tamaños
    
    scatter = ax.scatter(parametros, energia, s=tamanios, c=energia, 
                        cmap='plasma', alpha=0.7, edgecolors='black', 
                        linewidths=2)
    
    # Añadir etiquetas para cada punto
    for i, nombre in enumerate(nombres):
        ax.annotate(nombre, 
                   (parametros[i], energia[i]),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # Barra de color
    cbar = plt.colorbar(scatter, ax=ax, label='Energía Total (Wh)')
    cbar.ax.tick_params(labelsize=11)
    
    # Configuración de ejes y título
    ax.set_xlabel('Tamaño del Modelo (Billones de Parámetros)', 
                  fontsize=14, fontweight='bold')
    ax.set_ylabel('Consumo Energético Total (Wh)', 
                  fontsize=14, fontweight='bold')
    ax.set_title('Relación entre Tamaño del Modelo y Consumo Energético\n' +
                 'Test de 10 minutos - Tamaño de punto proporcional a tokens/s',
                 fontsize=16, fontweight='bold', pad=20)
    
    # Grid y leyenda
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=11)
    
    # Ajustar layout
    plt.tight_layout()
    
    return fig

def guardar_grafico(fig, nombre_base='2_dispersion_tamano_consumo'):
    """Guarda el gráfico usando la función centralizada."""
    guardar_figura(fig, nombre_base, dpi=DPI)

def main():
    """Función principal."""
    print("=" * 70)
    print("Generando Gráfico 2: Dispersión Tamaño vs Consumo")
    print("=" * 70)
    
    # Crear gráfico
    fig = crear_grafico_dispersion()
    
    # Guardar
    guardar_grafico(fig)
    
    # Análisis de correlación
    parametros = np.array(MODELOS['parametros'])
    energia = np.array(MODELOS['energia_total'])
    correlacion = np.corrcoef(parametros, energia)[0, 1]
    
    print(f"\nCoeficiente de correlación: {correlacion:.3f}")
    print(f"Interpretación: {'Fuerte' if abs(correlacion) > 0.7 else 'Moderada' if abs(correlacion) > 0.4 else 'Débil'}")
    
    print("\n[OK] Proceso completado exitosamente")
    plt.show()

if __name__ == '__main__':
    main()
