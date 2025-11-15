#!/bin/bash

# Script para exportar main.pdf a Descargas de Windows
# Uso: ./exportar_pdf.sh

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directorios
PROJECT_DIR="/home/gremory/ucompensar/calculo_integral/proyecto_energia_ai"
PDF_SOURCE="$PROJECT_DIR/build/main.pdf"
WINDOWS_USER="Rias Gremory"
DESCARGAS="/mnt/c/Users/$WINDOWS_USER/Downloads"
PDF_DEST="$DESCARGAS/proyecto_energia_ai.pdf"

echo -e "${YELLOW}=== Exportador de PDF ===${NC}"
echo ""

# Verificar que existe el PDF
if [ ! -f "$PDF_SOURCE" ]; then
    echo -e "${RED}✗ Error: No se encontró el archivo $PDF_SOURCE${NC}"
    echo -e "${YELLOW}  Compilando LaTeX...${NC}"
    cd "$PROJECT_DIR"
    latexmk -pdf -output-directory=build main.tex
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Error al compilar LaTeX${NC}"
        exit 1
    fi
fi

# Verificar que existe el directorio de Descargas
if [ ! -d "$DESCARGAS" ]; then
    echo -e "${RED}✗ Error: No se encontró el directorio $DESCARGAS${NC}"
    exit 1
fi

# Copiar el archivo
cp "$PDF_SOURCE" "$PDF_DEST"

if [ $? -eq 0 ]; then
    # Obtener tamaño del archivo
    SIZE=$(ls -lh "$PDF_DEST" | awk '{print $5}')
    echo -e "${GREEN}✓ PDF exportado correctamente${NC}"
    echo ""
    echo "  Origen:  $PDF_SOURCE"
    echo "  Destino: $PDF_DEST"
    echo "  Tamaño:  $SIZE"
    echo ""
    echo -e "${GREEN}El archivo está listo en tu carpeta de Descargas${NC}"
else
    echo -e "${RED}✗ Error al copiar el archivo${NC}"
    exit 1
fi
