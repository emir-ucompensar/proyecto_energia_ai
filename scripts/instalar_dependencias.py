#!/usr/bin/env python3
"""
instalar_dependencias.py
=========================
Script para instalar todas las dependencias necesarias del proyecto.

Detecta automáticamente el sistema y usa el método apropiado:
- En sistemas con entorno gestionado externamente: crea un venv
- En sistemas sin restricciones: usa pip directamente

Uso:
    python3 instalar_dependencias.py
    
O darle permisos de ejecución:
    chmod +x instalar_dependencias.py
    ./instalar_dependencias.py
"""

import subprocess
import sys
import os
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN DE DEPENDENCIAS
# =============================================================================

DEPENDENCIAS_PIP = [
    'numpy>=1.24.0',
    'scipy>=1.10.0',
    'matplotlib>=3.7.0',
    'pandas>=2.0.0',
]

DEPENDENCIAS_APT = [
    'python3-numpy',
    'python3-scipy',
    'python3-matplotlib',
    'python3-pandas',
]

DEPENDENCIAS_OPCIONALES = [
    'psutil',  # Para monitoreo de CPU/RAM
]

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def print_banner():
    """Imprime el banner del script."""
    print("=" * 70)
    print("INSTALADOR DE DEPENDENCIAS - Proyecto Energía IA")
    print("=" * 70)
    print()

def check_python_version():
    """Verifica que la versión de Python sea >= 3.8"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERROR] ERROR: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    else:
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro} detectado")

def check_venv():
    """Verifica si estamos en un entorno virtual."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

def run_command(command, check=True, capture_output=False):
    """
    Ejecuta un comando del sistema.
    
    Args:
        command: Lista con el comando y argumentos
        check: Si True, lanza excepción en caso de error
        capture_output: Si True, captura stdout y stderr
        
    Returns:
        subprocess.CompletedProcess
    """
    try:
        if capture_output:
            result = subprocess.run(
                command,
                check=check,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(command, check=check)
        return result
    except subprocess.CalledProcessError as e:
        return None

def is_apt_available():
    """Verifica si apt está disponible (sistema Debian/Ubuntu)."""
    result = run_command(['which', 'apt'], check=False, capture_output=True)
    return result and result.returncode == 0

def check_package_installed(package_name):
    """Verifica si un paquete de Python está instalado."""
    try:
        __import__(package_name.split('>=')[0].split('[')[0])
        return True
    except ImportError:
        return False

# =============================================================================
# MÉTODOS DE INSTALACIÓN
# =============================================================================

def install_with_apt():
    """Intenta instalar dependencias usando apt (Ubuntu/Debian)."""
    print("\n[PKG] Método 1: Instalación con APT (sistema)")
    print("-" * 70)
    
    if not is_apt_available():
        print("[ERROR] APT no está disponible en este sistema")
        return False
    
    print("[INFO]  Este método requiere permisos de superusuario (sudo)")
    response = input("¿Desea continuar? (s/n): ").strip().lower()
    
    if response != 's':
        print("[SKIP]  Saltando instalación con APT")
        return False
    
    print("\n[...] Actualizando índice de paquetes...")
    result = run_command(['sudo', 'apt', 'update'], check=False)
    
    if result is None or result.returncode != 0:
        print("[WARN]  Error al actualizar el índice de paquetes")
        return False
    
    print("\n[...] Instalando dependencias con APT...")
    for pkg in DEPENDENCIAS_APT:
        print(f"   Instalando {pkg}...")
        result = run_command(['sudo', 'apt', 'install', '-y', pkg], check=False)
        
        if result is None or result.returncode != 0:
            print(f"   [WARN]  Error instalando {pkg}")
    
    print("\n[OK] Instalación con APT completada")
    return True

def create_and_use_venv():
    """Crea un entorno virtual e instala dependencias."""
    print("\n[PKG] Método 2: Crear entorno virtual")
    print("-" * 70)
    
    venv_path = Path(__file__).parent.parent / 'venv'
    
    if venv_path.exists():
        print(f"[INFO]  Ya existe un entorno virtual en: {venv_path}")
        response = input("¿Desea recrearlo? (s/n): ").strip().lower()
        
        if response == 's':
            print("[DEL]  Eliminando entorno virtual anterior...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("[SKIP]  Usando entorno virtual existente")
    
    if not venv_path.exists():
        print(f"\n[...] Creando entorno virtual en: {venv_path}")
        result = run_command([sys.executable, '-m', 'venv', str(venv_path)], check=False)
        
        if result is None or result.returncode != 0:
            print("[ERROR] Error al crear el entorno virtual")
            print("   Asegúrate de tener python3-venv instalado:")
            print("   sudo apt install python3-venv python3-full")
            return False
    
    # Determinar el ejecutable de pip en el venv
    if os.name == 'nt':  # Windows
        pip_path = venv_path / 'Scripts' / 'pip'
        python_path = venv_path / 'Scripts' / 'python'
    else:  # Unix/Linux/Mac
        pip_path = venv_path / 'bin' / 'pip'
        python_path = venv_path / 'bin' / 'python'
    
    # Actualizar pip
    print("\n[...] Actualizando pip en el entorno virtual...")
    run_command([str(python_path), '-m', 'pip', 'install', '--upgrade', 'pip'], check=False)
    
    # Instalar dependencias
    print("\n[...] Instalando dependencias con pip...")
    for dep in DEPENDENCIAS_PIP:
        print(f"   Instalando {dep}...")
        result = run_command([str(pip_path), 'install', dep], check=False)
        
        if result and result.returncode == 0:
            print(f"   [OK] {dep} instalado")
        else:
            print(f"   [WARN]  Error instalando {dep}")
    
    # Instalar dependencias opcionales
    print("\n[...] Instalando dependencias opcionales...")
    for dep in DEPENDENCIAS_OPCIONALES:
        print(f"   Instalando {dep}...")
        result = run_command([str(pip_path), 'install', dep], check=False)
        
        if result and result.returncode == 0:
            print(f"   [OK] {dep} instalado")
        else:
            print(f"   [WARN]  {dep} no pudo instalarse (opcional)")
    
    print("\n" + "=" * 70)
    print("[OK] ENTORNO VIRTUAL CONFIGURADO EXITOSAMENTE")
    print("=" * 70)
    print(f"\n[DIR] Ubicación: {venv_path}")
    print("\n[RUN] Para activar el entorno virtual:")
    if os.name == 'nt':
        print(f"   {venv_path}\\Scripts\\activate")
    else:
        print(f"   source {venv_path}/bin/activate")
    
    print("\n[NOTE] Para ejecutar los scripts con el entorno virtual:")
    print(f"   {python_path} grafico_1_eficiencia_barras.py")
    print("   O después de activar:")
    print("   python grafico_1_eficiencia_barras.py")
    
    return True

def install_with_pip_user():
    """Instala dependencias en el directorio del usuario (--user)."""
    print("\n[PKG] Método 3: Instalación con pip --user")
    print("-" * 70)
    print("[INFO]  Este método instala paquetes solo para tu usuario")
    
    response = input("¿Desea continuar? (s/n): ").strip().lower()
    
    if response != 's':
        print("[SKIP]  Saltando instalación con pip --user")
        return False
    
    print("\n[...] Instalando dependencias con pip --user...")
    for dep in DEPENDENCIAS_PIP:
        print(f"   Instalando {dep}...")
        result = run_command([sys.executable, '-m', 'pip', 'install', '--user', dep], check=False)
        
        if result and result.returncode == 0:
            print(f"   [OK] {dep} instalado")
        else:
            print(f"   [WARN]  Error instalando {dep}")
    
    print("\n[OK] Instalación con pip --user completada")
    return True

def verify_installations():
    """Verifica qué paquetes están instalados correctamente."""
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE INSTALACIÓN")
    print("=" * 70)
    
    required_modules = {
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'matplotlib': 'Matplotlib',
        'pandas': 'pandas',
    }
    
    optional_modules = {
        'psutil': 'psutil',
    }
    
    all_ok = True
    
    print("\n[OK] Paquetes requeridos:")
    for module, name in required_modules.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'desconocida')
            print(f"   [OK] {name:15} {version}")
        except ImportError:
            print(f"   [ERROR] {name:15} NO INSTALADO")
            all_ok = False
    
    print("\n[TOOL] Paquetes opcionales:")
    for module, name in optional_modules.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'desconocida')
            print(f"   [OK] {name:15} {version}")
        except ImportError:
            print(f"   [WARN]  {name:15} no instalado (opcional)")
    
    return all_ok

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal del instalador."""
    print_banner()
    
    # Verificar versión de Python
    check_python_version()
    
    # Verificar si ya estamos en un venv
    if check_venv():
        print("\n[OK] Ya estás en un entorno virtual")
        print("  Instalando dependencias directamente con pip...\n")
        
        for dep in DEPENDENCIAS_PIP:
            print(f"Instalando {dep}...")
            run_command([sys.executable, '-m', 'pip', 'install', dep], check=False)
        
        for dep in DEPENDENCIAS_OPCIONALES:
            print(f"Instalando {dep} (opcional)...")
            run_command([sys.executable, '-m', 'pip', 'install', dep], check=False)
        
        verify_installations()
        return
    
    # Verificar instalaciones actuales
    print("\n[SEARCH] Verificando instalaciones actuales...")
    if verify_installations():
        print("\n[OK] Todas las dependencias ya están instaladas")
        response = input("\n¿Desea reinstalar de todas formas? (s/n): ").strip().lower()
        if response != 's':
            print("\n[BYE] ¡Listo! Puedes ejecutar los scripts.")
            return
    
    print("\n" + "=" * 70)
    print("MÉTODOS DE INSTALACIÓN DISPONIBLES")
    print("=" * 70)
    print("\n1. APT (recomendado para Ubuntu/Debian)")
    print("   - Instala desde repositorios oficiales del sistema")
    print("   - Requiere sudo")
    
    print("\n2. Entorno Virtual (recomendado para desarrollo)")
    print("   - Crea un entorno aislado")
    print("   - No requiere sudo")
    print("   - Más flexible")
    
    print("\n3. pip --user")
    print("   - Instala solo para tu usuario")
    print("   - Puede causar conflictos")
    
    print("\n4. Salir")
    
    while True:
        print("\n" + "=" * 70)
        opcion = input("Selecciona un método (1-4): ").strip()
        
        if opcion == '1':
            if install_with_apt():
                break
        elif opcion == '2':
            if create_and_use_venv():
                verify_installations()
                return
        elif opcion == '3':
            if install_with_pip_user():
                break
        elif opcion == '4':
            print("\n[BYE] Saliendo...")
            return
        else:
            print("[ERROR] Opción inválida. Por favor selecciona 1-4.")
    
    # Verificación final
    print("\n" + "=" * 70)
    if verify_installations():
        print("\n[SUCCESS] ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    else:
        print("\n[WARN]  Algunas dependencias no se instalaron correctamente")
        print("   Intenta con otro método de instalación")
    
    print("\n--> Ahora puedes ejecutar los scripts:")
    print("   python generar_todos_graficos.py")
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[BYE] Instalación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        sys.exit(1)
