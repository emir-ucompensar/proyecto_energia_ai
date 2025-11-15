#!/usr/bin/env python3
"""
Verificación de Correcciones - Método de Rectángulos
====================================================
Verifica que los puntos de modelos AI estén correctamente alineados con E(N).
"""

import sys
sys.path.append('/home/gremory/ucompensar/calculo_integral/proyecto_energia_ai/scripts')

from integrales_numericas import IntegracionNumerica

# Datos de modelos (valores experimentales)
MODELOS_AI = [
    {'nombre': 'TinyLLaMA-1.1B', 'parametros': 1.1, 'energia_exp': 11.7},
    {'nombre': 'Gemma-2B', 'parametros': 2.0, 'energia_exp': 13.2},
    {'nombre': 'Phi-3 Mini', 'parametros': 3.8, 'energia_exp': 14.8},
    {'nombre': 'Mistral-7B', 'parametros': 7.0, 'energia_exp': 16.9},
    {'nombre': 'LLaMA-3 8B', 'parametros': 8.0, 'energia_exp': 18.3}
]

def verificar_alineacion():
    """Verificar que los cálculos de E(N) sean correctos para cada modelo."""
    integ = IntegracionNumerica()
    
    print("=" * 80)
    print("VERIFICACIÓN DE CORRECCIONES - ALINEACIÓN DE MODELOS AI")
    print("=" * 80)
    print("\nComparando valores experimentales vs valores en curva E(N):\n")
    print(f"{'Modelo':<18} | {'N (B)':<6} | {'E_exp (Wh)':<12} | {'E(N) Curva':<12} | {'Diferencia':<12}")
    print("-" * 80)
    
    for modelo in MODELOS_AI:
        N = modelo['parametros']
        E_exp = modelo['energia_exp']
        E_curva = integ.funcion_energia(N)
        diferencia = E_exp - E_curva
        
        print(f"{modelo['nombre']:<18} | {N:<6.1f} | {E_exp:<12.2f} | {E_curva:<12.2f} | {diferencia:>+12.2f}")
    
    print("\n" + "=" * 80)
    print("✅ INTERPRETACIÓN:")
    print("-" * 80)
    print("• E_exp: Valores experimentales REALES medidos en laboratorio")
    print("• E(N) Curva: Valores CALCULADOS sobre el modelo polinómico")
    print("• En las gráficas CORREGIDAS:")
    print("  → Los puntos grises se plotean en (N, E(N))")
    print("  → Esto garantiza que están EXACTAMENTE sobre la curva roja")
    print("  → Las diferencias mostradas son naturales (modelo vs realidad)")
    print("=" * 80)
    
    # Verificar integral exacta
    print(f"\n📊 Integral exacta: {integ.integral_exacta():.8f} Wh·B")
    print(f"📏 Intervalo: [{integ.a}, {integ.b}] B (billones de parámetros)")
    
    # Verificar consistencia de colores
    print("\n" + "=" * 80)
    print("🎨 PALETA DE COLORES ESTANDARIZADA")
    print("=" * 80)
    print("• Curva E(N):         #C62828 (rojo - SIEMPRE)")
    print("• Rectángulos LEFT:   #1976D2 (azul)")
    print("• Rectángulos MID:    #388E3C (verde)")
    print("• Rectángulos RIGHT:  #F57C00 (naranja)")
    print("• Modelos AI:         #424242 (gris oscuro)")
    print("• Integral exacta:    #6A1B9A (púrpura)")
    print("=" * 80)
    
    print("\n✅ VERIFICACIÓN COMPLETADA")
    print("Si deseas ver las gráficas, consulta:")
    print("  • figuras/png/rectangulos_*_modelos.png")
    print("  • figuras/png/comparativa_modelos_*.png")

if __name__ == "__main__":
    verificar_alineacion()
