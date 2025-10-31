"""
generar_todos_graficos.py
==========================
Script maestro que ejecuta todos los análisis gráficos en secuencia.

Uso:
    python generar_todos_graficos.py

Este script genera todos los gráficos del proyecto en el orden correcto.
"""

import subprocess
import sys
import os

# Lista de scripts a ejecutar en orden
SCRIPTS = [
    'grafico_1_eficiencia_barras.py',
    'grafico_2_dispersion_tamano_consumo.py',
    'grafico_3_potencia_tiempo.py',
    'grafico_4_pareto_tradeoff.py',
    'grafico_5_comparacion_metodos_numericos.py',
    'grafico_6_area_bajo_curva.py',
]

def ejecutar_script(nombre_script):
    """
    Ejecuta un script de Python y captura su salida.
    
    Args:
        nombre_script: Nombre del archivo .py a ejecutar
        
    Returns:
        bool: True si exitoso, False si falla
    """
    print("\n" + "=" * 80)
    print(f"EJECUTANDO: {nombre_script}")
    print("=" * 80)
    
    try:
        resultado = subprocess.run(
            [sys.executable, nombre_script],
            capture_output=True,
            text=True,
            check=True
        )
        print(resultado.stdout)
        if resultado.stderr:
            print("ADVERTENCIAS:", resultado.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR al ejecutar {nombre_script}")
        print(f"Código de salida: {e.returncode}")
        print(f"Salida estándar:\n{e.stdout}")
        print(f"Error estándar:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {nombre_script}")
        return False

def main():
    """Función principal."""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + "  GENERACIÓN AUTOMÁTICA DE TODOS LOS GRÁFICOS".center(78) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('config.py'):
        print("\nERROR: Debes ejecutar este script desde el directorio /scripts/")
        print("   Ejecuta: cd scripts && python generar_todos_graficos.py")
        sys.exit(1)
    
    # Contadores
    exitosos = 0
    fallidos = 0
    
    # Ejecutar cada script
    for i, script in enumerate(SCRIPTS, 1):
        print(f"\n[{i}/{len(SCRIPTS)}] Procesando {script}...")
        
        if ejecutar_script(script):
            exitosos += 1
            print(f"[OK] {script} completado exitosamente")
        else:
            fallidos += 1
            print(f"[X] {script} falló")
            
            # Preguntar si continuar
            respuesta = input("\n¿Deseas continuar con los demás scripts? (s/n): ")
            if respuesta.lower() != 's':
                print("\nProceso interrumpido por el usuario.")
                break
    
    # Resumen final
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + "  RESUMEN FINAL".center(78) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    print(f"\nTotal de scripts ejecutados: {exitosos + fallidos}")
    print(f"[OK] Exitosos: {exitosos}")
    print(f"[X] Fallidos: {fallidos}")
    
    if fallidos == 0:
        print("\n¡TODOS LOS GRÁFICOS GENERADOS EXITOSAMENTE!")
        print(f"\nRevisa la carpeta '../figuras/' para ver los resultados.")
    else:
        print(f"\n[WARN] Algunos scripts fallaron. Revisa los errores anteriores.")
    
    print("\n" + "#" * 80 + "\n")

if __name__ == '__main__':
    main()
