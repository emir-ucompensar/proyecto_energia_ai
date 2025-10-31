"""
grafico_3_potencia_tiempo.py
==============================
Simula y visualiza perfiles de potencia en el tiempo para diferentes modelos.

Este script genera perfiles realistas de consumo de potencia GPU considerando:
- Fase de warmup inicial
- Variaciones estocásticas
- Picos ocasionales de carga

Uso:
    python grafico_3_potencia_tiempo.py

Salida:
    - grafico_3_potencia_tiempo.png
    - grafico_3_potencia_tiempo.pdf
"""

import matplotlib.pyplot as plt
import numpy as np
from config import (
    MODELOS, DURACION_SIMULACION, NUM_PUNTOS, PERFIL_CONFIG,
    TAMANO_FIGURA_GRANDE, DPI, configurar_semilla, guardar_figura
)
import os

def generar_perfil_potencia(potencia_nominal, duracion, num_puntos):
    """
    Genera un perfil realista de potencia en el tiempo.
    
    Args:
        potencia_nominal: Potencia promedio en watts
        duracion: Duración total en segundos
        num_puntos: Número de puntos de muestreo
        
    Returns:
        tuple: (tiempo, potencia)
    """
    t = np.linspace(0, duracion, num_puntos)
    
    # Fase de warmup exponencial
    warmup_time = PERFIL_CONFIG['warmup_time']
    warmup_factor = 1 - np.exp(-t / warmup_time)
    
    # Oscilación base (ciclos de carga)
    freq = PERFIL_CONFIG['frecuencia_oscilacion']
    oscilacion = 0.03 * np.sin(2 * np.pi * freq * t)
    
    # Ruido estocástico
    variacion = PERFIL_CONFIG['variacion_max']
    ruido = np.random.normal(0, variacion * 0.3, num_puntos)
    
    # Picos ocasionales de carga (cada ~60 segundos)
    picos = np.zeros_like(t)
    for pico_t in range(60, int(duracion), 60):
        idx = int(pico_t * num_puntos / duracion)
        if idx < len(picos):
            picos[idx:idx+5] = variacion * potencia_nominal * 0.5
    
    # Combinar componentes
    potencia = potencia_nominal * warmup_factor * (1 + oscilacion + ruido) + picos
    
    # Asegurar valores positivos
    potencia = np.maximum(potencia, potencia_nominal * 0.7)
    
    return t, potencia

def crear_grafico_potencia_tiempo():
    """
    Crea un gráfico de líneas con perfiles de potencia.
    
    Returns:
        matplotlib.figure.Figure: Figura generada
    """
    configurar_semilla()
    
    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=TAMANO_FIGURA_GRANDE, dpi=DPI)
    
    # Seleccionar 3 modelos representativos para claridad
    indices_seleccionados = [0, 2, 4]  # Phi-3, Mistral, TinyLLaMA
    colores_lineas = ['#2E86AB', '#F18F01', '#6A994E']
    
    # Subplot 1: Perfiles completos
    for idx, color in zip(indices_seleccionados, colores_lineas):
        nombre = MODELOS['nombres_cortos'][idx]
        potencia_nominal = MODELOS['potencia_gpu'][idx]
        
        t, potencia = generar_perfil_potencia(
            potencia_nominal, 
            DURACION_SIMULACION, 
            NUM_PUNTOS
        )
        
        ax1.plot(t, potencia, label=f'{nombre} ({potencia_nominal}W nominal)',
                linewidth=2, color=color, alpha=0.8)
    
    ax1.set_xlabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Potencia GPU (W)', fontsize=12, fontweight='bold')
    ax1.set_title('Perfiles de Potencia Simulados - Vista Completa (10 minutos)',
                  fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right', fontsize=10)
    ax1.grid(alpha=0.3, linestyle='--')
    
    # Subplot 2: Zoom en los primeros 60 segundos (fase de warmup)
    for idx, color in zip(indices_seleccionados, colores_lineas):
        nombre = MODELOS['nombres_cortos'][idx]
        potencia_nominal = MODELOS['potencia_gpu'][idx]
        
        t, potencia = generar_perfil_potencia(
            potencia_nominal, 
            DURACION_SIMULACION, 
            NUM_PUNTOS
        )
        
        # Filtrar primeros 60 segundos
        mask = t <= 60
        ax2.plot(t[mask], potencia[mask], label=f'{nombre}',
                linewidth=2.5, color=color, alpha=0.9)
    
    ax2.set_xlabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Potencia GPU (W)', fontsize=12, fontweight='bold')
    ax2.set_title('Fase de Warmup - Primeros 60 segundos',
                  fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=10)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.axvspan(0, PERFIL_CONFIG['warmup_time'], alpha=0.2, color='yellow',
                label='Periodo de warmup')
    
    # Ajustar layout
    plt.tight_layout()
    
    return fig

def calcular_energia_simulada():
    """Calcula la energía total usando los perfiles simulados."""
    print("\nEnergía calculada por integración numérica (Trapecio):")
    print("-" * 60)
    
    for i, nombre in enumerate(MODELOS['nombres_cortos']):
        potencia_nominal = MODELOS['potencia_gpu'][i]
        energia_medida = MODELOS['energia_total'][i]
        
        t, potencia = generar_perfil_potencia(
            potencia_nominal,
            DURACION_SIMULACION,
            NUM_PUNTOS
        )
        
        # Integración numérica (regla del trapecio)
        dt = t[1] - t[0]
        energia_simulada = np.trapz(potencia, dx=dt) / 3600  # Convertir J a Wh
        
        error = abs(energia_simulada - energia_medida) / energia_medida * 100
        
        print(f"{nombre:15} | Medida: {energia_medida:5.1f} Wh | "
              f"Simulada: {energia_simulada:5.1f} Wh | Error: {error:4.1f}%")

def guardar_grafico(fig, nombre_base='3_potencia_tiempo'):
    """Guarda el gráfico usando la función centralizada."""
    guardar_figura(fig, nombre_base, dpi=DPI)

def main():
    """Función principal."""
    print("=" * 70)
    print("Generando Gráfico 3: Potencia en el Tiempo")
    print("=" * 70)
    
    # Crear gráfico
    fig = crear_grafico_potencia_tiempo()
    
    # Calcular energías
    calcular_energia_simulada()
    
    # Guardar
    guardar_grafico(fig)
    
    print("\n[OK] Proceso completado exitosamente")
    plt.show()

if __name__ == '__main__':
    main()
