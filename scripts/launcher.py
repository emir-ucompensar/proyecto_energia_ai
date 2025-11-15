"""
launcher.py
===========
Lanzador interactivo para métodos de integración numérica.
Proporciona interfaz unificada para ejecutar Regla del Trapecio, Regla de Simpson o Integración Analítica.

Uso:
    python launcher.py
"""

import sys
import os

# Paleta de colores profesional
COLOR_PRINCIPAL = '#1F4788'    # Azul oscuro profesional
COLOR_SECUNDARIO = '#8B3A62'   # Púrpura profesional
COLOR_ACENTO = '#5C946E'       # Verde profesional


def mostrar_menu():
    """Mostrar menú principal."""
    print("\n" + "=" * 70)
    print("LANZADOR DE INTEGRACIÓN NUMÉRICA")
    print("Análisis de Consumo Energético - Proyecto de Cálculo Integral")
    print("=" * 70)
    print("\nSeleccione método de integración numérica:")
    print("\n  1. Método de Rectángulos (Sumas de Riemann)")
    print("  2. Visualización de Rectángulos con Modelos AI")
    print("  3. Comparativa de Modelos AI")
    print("  4. Regla del Trapecio (convergencia O(h^2))")
    print("  5. Regla de Simpson 1/3 (convergencia O(h^4))")
    print("  6. Integración Analítica (Antiderivadas)")
    print("  7. Comparación de todos los métodos")
    print("  8. Salir")
    print("\n" + "-" * 70)


def ejecutar_trapecio():
    """Ejecutar script de regla del trapecio."""
    from trapecio import ejecutar_trapecio
    ejecutar_trapecio()


def ejecutar_simpson():
    """Ejecutar script de regla de Simpson 1/3."""
    from simpson import ejecutar_simpson
    ejecutar_simpson()


def ejecutar_antiderivada():
    """Ejecutar script de integración analítica."""
    from antiderivada import ejecutar_antiderivada
    ejecutar_antiderivada()


def ejecutar_rectangulos():
    """Ejecutar script de método de rectángulos."""
    from rectangulos import ejecutar_rectangulos
    ejecutar_rectangulos()


def ejecutar_visualizacion_rectangulos():
    """Ejecutar visualización de rectángulos con modelos."""
    from rectangulos_visualizacion import main as viz_main
    viz_main()


def ejecutar_comparativa_modelos():
    """Ejecutar comparativa de modelos AI."""
    from comparativa_modelos import main as comp_main
    comp_main()


def ejecutar_comparacion():
    """Ejecutar comparación de todos los métodos."""
    from integrales_numericas import IntegracionNumerica
    import numpy as np
    
    print("=" * 70)
    print("COMPARACIÓN EXHAUSTIVA DE MÉTODOS")
    print("=" * 70)
    
    integ = IntegracionNumerica()
    integral_exacta = integ.integral_exacta()
    
    print("\nIntegral exacta (Teorema Fundamental): {:.8f} Wh·B".format(integral_exacta))
    print("\n" + "-" * 70)
    
    # Solicitar precisión
    while True:
        try:
            n = int(input("Ingrese nivel de precisión (número de intervalos, n >= 4): ").strip())
            if n >= 4:
                break
            else:
                print("Error: n debe ser al menos 4")
        except ValueError:
            print("Error: Entrada no válida")
    
    # Computar aproximaciones
    rect_left = integ.rectangulos(n, 'left')
    rect_mid = integ.rectangulos(n, 'mid')
    rect_right = integ.rectangulos(n, 'right')
    trap = integ.trapecio(n)
    simp = integ.simpson(n)
    
    # Computar errores
    error_rect_left_abs = abs(rect_left - integral_exacta)
    error_rect_mid_abs = abs(rect_mid - integral_exacta)
    error_rect_right_abs = abs(rect_right - integral_exacta)
    error_trap_abs = abs(trap - integral_exacta)
    error_simp_abs = abs(simp - integral_exacta)
    
    error_rect_left_rel = (error_rect_left_abs / integral_exacta) * 100
    error_rect_mid_rel = (error_rect_mid_abs / integral_exacta) * 100
    error_rect_right_rel = (error_rect_right_abs / integral_exacta) * 100
    error_trap_rel = (error_trap_abs / integral_exacta) * 100
    error_simp_rel = (error_simp_abs / integral_exacta) * 100
    
    # Tabla de resultados
    print("\n" + "=" * 80)
    print("RESULTADOS PARA n = {}".format(n))
    print("=" * 80)
    print("\n{:<25} | {:<15} | {:<15} | {:<15}".format(
        "Método", "Aproximación", "Error Abs.", "Error Rel. %"))
    print("-" * 80)
    print("{:<25} | {:<15.8f} | {:<15.2e} | {:<15.6f}".format(
        "Exacta (Antiderivada)", integral_exacta, 0, 0))
    print("{:<25} | {:<15.8f} | {:<15.2e} | {:<15.6f}".format(
        "Rectángulos (left)", rect_left, error_rect_left_abs, error_rect_left_rel))
    print("{:<25} | {:<15.8f} | {:<15.2e} | {:<15.6f}".format(
        "Rectángulos (mid)", rect_mid, error_rect_mid_abs, error_rect_mid_rel))
    print("{:<25} | {:<15.8f} | {:<15.2e} | {:<15.6f}".format(
        "Rectángulos (right)", rect_right, error_rect_right_abs, error_rect_right_rel))
    print("{:<25} | {:<15.8f} | {:<15.2e} | {:<15.6f}".format(
        "Trapecio O(h^2)", trap, error_trap_abs, error_trap_rel))
    print("{:<25} | {:<15.8f} | {:<15.2e} | {:<15.6f}".format(
        "Simpson O(h^4)", simp, error_simp_abs, error_simp_rel))
    
    # Análisis
    print("\n" + "-" * 80)
    print("ANÁLISIS")
    print("-" * 80)
    
    print(f"\nMejor método de rectángulos: mid (error: {error_rect_mid_rel:.4f}%)")
    print(f"Simpson es el más preciso (error: {error_simp_rel:.6f}%)")
    
    if error_rect_mid_rel < 1:
        print(f"\nRectángulos (mid) alcanza alta precisión con n={n}")
    
    print("\n" + "=" * 80)


def main():
    """Bucle de ejecución principal."""
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Ingrese opción (1-8): ").strip()
            
            if opcion == '1':
                print("\n")
                ejecutar_rectangulos()
            
            elif opcion == '2':
                print("\n")
                ejecutar_visualizacion_rectangulos()
            
            elif opcion == '3':
                print("\n")
                ejecutar_comparativa_modelos()
            
            elif opcion == '4':
                print("\n")
                ejecutar_trapecio()
            
            elif opcion == '5':
                print("\n")
                ejecutar_simpson()
            
            elif opcion == '6':
                print("\n")
                ejecutar_antiderivada()
            
            elif opcion == '7':
                print("\n")
                ejecutar_comparacion()
            
            elif opcion == '8':
                print("\n" + "=" * 70)
                print("Cerrando lanzador. Hasta luego.")
                print("=" * 70 + "\n")
                sys.exit(0)
            
            else:
                print("\nError: Opción no válida. Seleccione 1-8.")
            
            # Preguntar para continuar
            print("\n" + "-" * 70)
            continuar = input("Presione Enter para continuar o escriba 'q' para salir: ").strip().lower()
            if continuar == 'q':
                print("\n" + "=" * 70)
                print("Cerrando lanzador. Hasta luego.")
                print("=" * 70 + "\n")
                sys.exit(0)
        
        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print("Operación cancelada por el usuario.")
            print("=" * 70 + "\n")
            sys.exit(0)
        
        except Exception as e:
            print(f"\nError: {e}")
            print("Por favor, intente de nuevo.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nError fatal: {e}")
        sys.exit(1)
