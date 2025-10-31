"""
grafico_1_eficiencia_barras.py
================================
Genera un gráfico de barras comparativo de la eficiencia energética
(tokens/Wh) entre diferentes modelos de lenguaje.

Este script visualiza la métrica de eficiencia energética, que cuantifica
cuántos tokens puede generar cada modelo por cada watt-hora consumido.

Uso:
    python grafico_1_eficiencia_barras.py

Salida:
    - grafico_1_eficiencia_barras.png
    - grafico_1_eficiencia_barras.pdf
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config import (
    MODELOS, DURACION_SIMULACION, DPI, COLORES, TAMANO_FIGURA,
    configurar_semilla, guardar_figura, obtener_dataframe_modelos,
    exportar_estadisticas_csv, calcular_estadisticas_avanzadas, DIR_RESULTADOS
)
import os

def crear_grafico_eficiencia():
    """
    Crea un gráfico de barras de eficiencia energética por modelo.
    
    Returns:
        matplotlib.figure.Figure: Figura generada
    """
    configurar_semilla()
    
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=TAMANO_FIGURA, dpi=DPI)
    
    # Datos
    nombres = MODELOS['nombres_cortos']
    eficiencia = MODELOS['eficiencia']
    energia = MODELOS['energia_total']
    
    # Colores basados en eficiencia (gradiente)
    colores = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(nombres)))
    
    # Crear barras
    barras = ax.bar(nombres, eficiencia, color=colores, edgecolor='black', 
                    linewidth=1.5, alpha=0.85)
    
    # Añadir valores sobre las barras
    for i, (barra, valor, energia_val) in enumerate(zip(barras, eficiencia, energia)):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
                f'{valor:.0f}\ntokens/Wh\n({energia_val} Wh)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Configuración de ejes y título
    ax.set_xlabel('Modelo de Lenguaje', fontsize=14, fontweight='bold')
    ax.set_ylabel('Eficiencia Energética (tokens/Wh)', fontsize=14, fontweight='bold')
    ax.set_title('Comparación de Eficiencia Energética entre Modelos LLM\n' +
                 'Test de 10 minutos - GTX 1660 Ti',
                 fontsize=16, fontweight='bold', pad=20)
    
    # Línea de referencia (promedio)
    promedio = np.mean(eficiencia)
    ax.axhline(y=promedio, color='red', linestyle='--', linewidth=2, 
               label=f'Promedio: {promedio:.0f} tokens/Wh', alpha=0.7)
    
    # Grid y leyenda
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=11)
    
    # Ajustar layout
    plt.tight_layout()
    
    return fig

def guardar_grafico(fig, nombre_base='1_eficiencia_barras'):
    """
    Guarda el gráfico en los formatos configurados.
    
    Args:
        fig: Figura de matplotlib a guardar
        nombre_base: Nombre base del archivo (sin prefijo grafico_)
    """
    guardar_figura(fig, nombre_base, dpi=DPI)

def main():
    """Función principal."""
    print("=" * 70)
    print("Generando Gráfico 1: Eficiencia Energética (Barras)")
    print("=" * 70)
    
    # Crear DataFrame con pandas para análisis avanzado
    df = obtener_dataframe_modelos()
    
    # Crear gráfico
    fig = crear_grafico_eficiencia()
    
    # Guardar
    guardar_grafico(fig)
    
    # Calcular y mostrar estadísticas avanzadas con pandas
    print("\n" + "=" * 70)
    print("Estadísticas Avanzadas (usando pandas)")
    print("=" * 70)
    
    stats = calcular_estadisticas_avanzadas(df)
    print(f"\n[STATS] Total de modelos evaluados: {stats['total_modelos']}")
    print(f"[ENERGY] Energía total consumida: {stats['energia_total']:.2f} Wh")
    print(f"[UP] Energía promedio: {stats['energia_promedio']:.2f} ± {stats['energia_std']:.2f} Wh")
    print(f"\n[TOP] Modelo más eficiente: {stats['modelo_mas_eficiente']}")
    print(f"   Eficiencia: {stats['eficiencia_max']:.2f} tokens/Wh")
    print(f"[DOWN] Modelo menos eficiente: {stats['modelo_menos_eficiente']}")
    print(f"   Eficiencia: {stats['eficiencia_min']:.2f} tokens/Wh")
    print(f"[STATS] Eficiencia promedio: {stats['eficiencia_promedio']:.2f} tokens/Wh")
    print(f"[LINK] Correlación tamaño-energía: {stats['correlacion_tamano_energia']:.4f}")
    
    # Exportar estadísticas descriptivas a CSV
    print("\n" + "=" * 70)
    print("Exportando datos a CSV con pandas")
    print("=" * 70)
    
    # Guardar DataFrame completo
    ruta_datos = os.path.join(DIR_RESULTADOS, 'datos_modelos_completos.csv')
    df.to_csv(ruta_datos, index=False)
    print(f"[OK] Datos completos exportados: {ruta_datos}")
    
    # Guardar estadísticas descriptivas
    exportar_estadisticas_csv(df, 'estadisticas_descriptivas.csv')
    
    # Crear tabla de resumen con pandas
    resumen = df[['Modelo', 'Parametros_B', 'Eficiencia_tokens_Wh', 'Energia_Total_Wh']].copy()
    resumen = resumen.sort_values('Eficiencia_tokens_Wh', ascending=False)
    print("\n[LIST] Ranking de eficiencia (ordenado):")
    print(resumen.to_string(index=False))
    
    print("\n[OK] Proceso completado exitosamente")
    plt.show()

if __name__ == '__main__':
    main()
