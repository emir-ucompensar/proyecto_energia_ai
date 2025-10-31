#!/bin/bash
# =============================================================================
# instalar_dependencias.sh
# =============================================================================
# Script bash alternativo para instalar dependencias del proyecto.
# Detecta automáticamente el mejor método de instalación.
#
# Uso:
#   chmod +x instalar_dependencias.sh
#   ./instalar_dependencias.sh
# =============================================================================

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# FUNCIONES
# =============================================================================

print_banner() {
    echo "======================================================================"
    echo "  INSTALADOR DE DEPENDENCIAS - Proyecto Energía IA"
    echo "======================================================================"
    echo ""
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_error() {
    echo -e "${RED}[X]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# =============================================================================
# VERIFICACIONES INICIALES
# =============================================================================

print_banner

# Verificar Python
if ! check_command python3; then
    print_error "Python3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION detectado"

# =============================================================================
# DETECTAR SISTEMA Y MÉTODO
# =============================================================================

echo ""
echo "======================================================================"
echo "  DETECTANDO SISTEMA"
echo "======================================================================"

if check_command apt; then
    print_info "Sistema Debian/Ubuntu detectado (APT disponible)"
    TIENE_APT=true
else
    print_warning "APT no disponible"
    TIENE_APT=false
fi

# Verificar si estamos en un venv
if [[ -n "$VIRTUAL_ENV" ]]; then
    print_success "Ya estás en un entorno virtual: $VIRTUAL_ENV"
    EN_VENV=true
else
    print_info "No estás en un entorno virtual"
    EN_VENV=false
fi

# =============================================================================
# MENÚ DE INSTALACIÓN
# =============================================================================

if [ "$EN_VENV" = true ]; then
    echo ""
    echo "======================================================================"
    echo "  INSTALANDO EN ENTORNO VIRTUAL ACTIVO"
    echo "======================================================================"
    echo ""
    
    print_info "Instalando dependencias con pip..."
    pip install numpy>=1.24.0 scipy>=1.10.0 matplotlib>=3.7.0 pandas>=2.0.0
    
    print_info "Instalando dependencias opcionales..."
    pip install psutil || print_warning "psutil no pudo instalarse (opcional)"
    
    print_success "Instalación completada en el entorno virtual"
    
else
    echo ""
    echo "======================================================================"
    echo "  MÉTODOS DE INSTALACIÓN DISPONIBLES"
    echo "======================================================================"
    echo ""
    echo "1. Usar script Python interactivo (recomendado)"
    echo "2. Crear entorno virtual y activarlo manualmente"
    if [ "$TIENE_APT" = true ]; then
        echo "3. Instalar con APT (requiere sudo)"
    fi
    echo "0. Salir"
    echo ""
    
    read -p "Selecciona una opción: " OPCION
    
    case $OPCION in
        1)
            print_info "Ejecutando instalador Python interactivo..."
            python3 instalar_dependencias.py
            ;;
        2)
            print_info "Creando entorno virtual..."
            VENV_DIR="../venv"
            
            if [ -d "$VENV_DIR" ]; then
                print_warning "Ya existe un entorno virtual en $VENV_DIR"
                read -p "¿Desea recrearlo? (s/n): " RECREAR
                if [ "$RECREAR" = "s" ] || [ "$RECREAR" = "S" ]; then
                    rm -rf "$VENV_DIR"
                    print_info "Entorno virtual anterior eliminado"
                fi
            fi
            
            if [ ! -d "$VENV_DIR" ]; then
                python3 -m venv "$VENV_DIR"
                print_success "Entorno virtual creado en $VENV_DIR"
            fi
            
            print_info "Instalando dependencias en el entorno virtual..."
            source "$VENV_DIR/bin/activate"
            pip install --upgrade pip
            pip install numpy>=1.24.0 scipy>=1.10.0 matplotlib>=3.7.0 pandas>=2.0.0
            pip install psutil || print_warning "psutil no pudo instalarse (opcional)"
            
            echo ""
            echo "======================================================================"
            print_success "ENTORNO VIRTUAL CONFIGURADO"
            echo "======================================================================"
            echo ""
            echo "[DIR] Ubicación: $VENV_DIR"
            echo ""
            echo "[RUN] Para activar el entorno virtual:"
            echo "   source $VENV_DIR/bin/activate"
            echo ""
            echo "[NOTE] Para ejecutar los scripts:"
            echo "   source $VENV_DIR/bin/activate"
            echo "   python generar_todos_graficos.py"
            echo ""
            ;;
        3)
            if [ "$TIENE_APT" = true ]; then
                print_info "Instalando dependencias con APT..."
                echo ""
                print_warning "Este método requiere permisos de sudo"
                
                sudo apt update
                sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pandas python3-psutil
                
                print_success "Dependencias instaladas con APT"
            else
                print_error "APT no está disponible en este sistema"
            fi
            ;;
        0)
            print_info "Saliendo..."
            exit 0
            ;;
        *)
            print_error "Opción inválida"
            exit 1
            ;;
    esac
fi

# =============================================================================
# VERIFICACIÓN FINAL
# =============================================================================

echo ""
echo "======================================================================"
echo "  VERIFICANDO INSTALACIÓN"
echo "======================================================================"
echo ""

# Verificar cada paquete
python3 -c "import numpy; print('[OK] NumPy:', numpy.__version__)" 2>/dev/null && print_success "NumPy instalado" || print_error "NumPy NO instalado"
python3 -c "import scipy; print('[OK] SciPy:', scipy.__version__)" 2>/dev/null && print_success "SciPy instalado" || print_error "SciPy NO instalado"
python3 -c "import matplotlib; print('[OK] Matplotlib:', matplotlib.__version__)" 2>/dev/null && print_success "Matplotlib instalado" || print_error "Matplotlib NO instalado"
python3 -c "import pandas; print('[OK] pandas:', pandas.__version__)" 2>/dev/null && print_success "pandas instalado" || print_error "pandas NO instalado"
python3 -c "import psutil; print('[OK] psutil:', psutil.__version__)" 2>/dev/null && print_success "psutil instalado (opcional)" || print_warning "psutil no instalado (opcional)"

echo ""
echo "======================================================================"
print_success "PROCESO COMPLETADO"
echo "======================================================================"
echo ""
print_info "Ahora puedes ejecutar los scripts:"
echo "   python generar_todos_graficos.py"
echo "   python grafico_1_eficiencia_barras.py"
echo ""
