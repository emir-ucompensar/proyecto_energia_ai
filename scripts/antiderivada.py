"""
antiderivada.py
===============
Integración analítica usando antiderivadas (Teorema Fundamental del Cálculo).
Calcula la integral definida exacta sin aproximación numérica.

Uso:
    python antiderivada.py
"""

import numpy as np
import matplotlib.pyplot as plt
from integrales_numericas import IntegracionNumerica

# Paleta de colores profesional
COLOR_PRINCIPAL = '#1F4788'    # Azul oscuro profesional
COLOR_SECUNDARIO = '#8B3A62'   # Púrpura profesional
COLOR_ACENTO = '#5C946E'       # Verde profesional


def ejecutar_antiderivada():
    """
    Ejecutar integración analítica mediante antiderivada.
    """
    integ = IntegracionNumerica()
    
    print("=" * 70)
    print("INTEGRACIÓN ANALÍTICA - TEOREMA FUNDAMENTAL DEL CÁLCULO")
    print("=" * 70)
    
    print("\nFunción: E(N) = 0.0842*N^4 - 1.2156*N^3 + 6.8934*N^2 - 12.456*N + 11.234")
    print("Intervalo: [1.1, 8.0] (TinyLLaMA a LLaMA-3 8B)")
    
    print("\n" + "-" * 70)
    print("CÁLCULO DE LA ANTIDERIVADA")
    print("-" * 70)
    
    print("\nF(N) = 0.01684*N^5 - 0.3039*N^4 + 2.2978*N^3 - 6.228*N^2 + 11.234*N")
    print("\ndonde:")
    print("  F(N) = integral de E(N)")
    print("  dF/dN = E(N)")
    
    a = integ.a
    b = integ.b
    
    F_a = integ.antiderivada_energia(a)
    F_b = integ.antiderivada_energia(b)
    Z = F_b - F_a
    
    print("\n" + "-" * 70)
    print("EVALUACIÓN EN LOS LÍMITES")
    print("-" * 70)
    
    print(f"\nF({a}) = {F_a:.8f}")
    print(f"F({b}) = {F_b:.8f}")
    
    print("\n" + "-" * 70)
    print("RESULTADO")
    print("-" * 70)
    
    print(f"\nZ = F({b}) - F({a})")
    print(f"Z = {F_b:.8f} - {F_a:.8f}")
    print(f"\nIntegral definida:")
    print(f"∫[{a:.1f},{b:.1f}] E(N) dN = {Z:.8f} Wh·B")
    print(f"\nÁrea bajo la curva: {Z:.6f} Wh·B")
    
    print("\n" + "-" * 70)
    print("VALIDACIÓN")
    print("-" * 70)
    
    # Comparar con métodos numéricos
    n_test = 1000
    trap_1000 = integ.trapecio(n_test)
    simp_1000 = integ.simpson(n_test)
    
    error_trap = abs(trap_1000 - Z)
    error_simp = abs(simp_1000 - Z)
    rel_error_trap = (error_trap / Z) * 100
    rel_error_simp = (error_simp / Z) * 100
    
    print(f"\nComparación con métodos numéricos (n={n_test}):")
    print(f"\nRegla del Trapecio:")
    print(f"  Aproximación: {trap_1000:.8f} Wh·B")
    print(f"  Error: {error_trap:.2e} (Relativo: {rel_error_trap:.6f}%)")
    
    print(f"\nRegla de Simpson 1/3:")
    print(f"  Aproximación: {simp_1000:.8f} Wh·B")
    print(f"  Error: {error_simp:.2e} (Relativo: {rel_error_simp:.6f}%)")
    
    # Generar visualización
    print("\n" + "-" * 70)
    print("GENERANDO VISUALIZACIÓN")
    print("-" * 70)
    
    generar_grafico_antiderivada(integ, Z)
    
    print("\nArchivo guardado: ../figuras/png/antiderivada_area.png")
    print("Archivo guardado: ../figuras/pdf/antiderivada_area.pdf")
    
    print("\n" + "=" * 70)


def generar_grafico_antiderivada(integ, area_exacta):
    """
    Generar visualización de función, antiderivada y área bajo la curva.
    """
    N = np.linspace(integ.a, integ.b, 500)
    E = integ.funcion_energia(N)
    F = integ.antiderivada_energia(N)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Integración Analítica: Antiderivadas', fontsize=14, fontweight='bold')
    
    # Gráfica 1: Función de energía y área bajo la curva
    ax1.fill_between(N, 0, E, alpha=0.25, color=COLOR_PRINCIPAL, label=f'Área = {area_exacta:.4f} Wh·B')
    ax1.plot(N, E, linewidth=2.5, color=COLOR_PRINCIPAL, label='E(N)')
    ax1.axvline(x=integ.a, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    ax1.axvline(x=integ.b, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    
    ax1.set_xlabel('Parámetros del Modelo (Billones)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Consumo Energético (Wh)', fontsize=11, fontweight='bold')
    ax1.set_title('Función de Energía E(N) con Área Bajo la Curva', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.25, linestyle=':')
    ax1.legend(fontsize=10, loc='upper left')
    ax1.set_ylim(bottom=0)
    
    # Gráfica 2: Función antiderivada
    ax2.plot(N, F, linewidth=2.5, color=COLOR_SECUNDARIO, label='F(N) - Antiderivada')
    ax2.plot(integ.a, integ.antiderivada_energia(integ.a), 'o', markersize=10, 
             color=COLOR_ACENTO, label=f'F({integ.a}) = {integ.antiderivada_energia(integ.a):.4f}')
    ax2.plot(integ.b, integ.antiderivada_energia(integ.b), 's', markersize=10, 
             color=COLOR_PRINCIPAL, label=f'F({integ.b}) = {integ.antiderivada_energia(integ.b):.4f}')
    
    # Línea vertical mostrando la diferencia
    ax2.vlines(integ.b, integ.antiderivada_energia(integ.a), 
               integ.antiderivada_energia(integ.b), colors=COLOR_PRINCIPAL, linestyles='--', 
               linewidth=1.5, alpha=0.5)
    
    ax2.set_xlabel('Parámetros del Modelo (Billones)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Función Antiderivada F(N)', fontsize=11, fontweight='bold')
    ax2.set_title('Antiderivada F(N) = ∫E(N)dN', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.25, linestyle=':')
    ax2.legend(fontsize=10, loc='upper left')
    
    plt.tight_layout()
    
    # Guardar figuras
    import os
    os.makedirs('../figuras/png', exist_ok=True)
    os.makedirs('../figuras/pdf', exist_ok=True)
    
    fig.savefig('../figuras/png/antiderivada_area.png', dpi=300, bbox_inches='tight')
    fig.savefig('../figuras/pdf/antiderivada_area.pdf', bbox_inches='tight')
    plt.close()


def main():
    """Punto de ejecución principal."""
    ejecutar_antiderivada()


if __name__ == '__main__':
    main()
