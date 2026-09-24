#!/bin/bash

# Colores para la terminal
VERDE='\033[0;32m'
AZUL='\033[0;34m'
ROJO='\033[0;31m'
NC='\033[0;33m' # Sin color
NC='\033[0m'

echo -e "${AZUL}=========================================${NC}"
echo -e "${AZUL}   Instalador de la Calculadora BCV      ${NC}"
echo -e "${AZUL}=========================================${NC}"

# 1. Verificar e instalar dependencias necesarias en Arch/CachyOS
echo -e "\n${AZUL}[1/4] Verificando dependencias del sistema...${NC}"
DEPENDENCIAS=(python-requests python-beautifulsoup4 python)
FALTANTES=()

for dep in "${DEPENDENCIAS[@]}"; do
    if ! pacman -Qi "$dep" &> /dev/null; then
        FALTANTES+=("$dep")
    fi
done

if [ ${#FALTANTES[@]} -ne 0 ]; then
    echo -e "${NC}Instalando dependencias faltantes vía pacman...${NC}"
    sudo pacman -S --needed --noconfirm "${FALTANTES[@]}"
else
    echo -e "${VERDE}✓ Todas las dependencias de pacman están instaladas.${VERDE}"
fi

# 2. Crear estructura de directorios internos
echo -e "\n${AZUL}[2/4] Creando directorios de la aplicación...${NC}"
TARGET_DIR="$HOME/.local/share/bcv-calculator"
APP_DIR="$HOME/.local/share/applications"

mkdir -p "$TARGET_DIR"
mkdir -p "$APP_DIR"
echo -e "${VERDE}✓ Directorios listos en $TARGET_DIR${NC}"

# 3. Copiar archivos del proyecto
echo -e "\n${AZUL}[3/4] Copiando archivos de la aplicación...${NC}"
if [ -f "bcv_ticker.py" ] && [ -f "calculadora.html" ]; then
    cp bcv_ticker.py "$TARGET_DIR/bcv_ticker.py"
    cp calculadora.html "$TARGET_DIR/calculadora.html"
    chmod +x "$TARGET_DIR/bcv_ticker.py"
    echo -e "${VERDE}✓ Archivos del núcleo copiados y configurados.${NC}"
else
    echo -e "${ROJO}❌ Error: No se encuentran bcv_ticker.py o calculadora.html en el directorio actual.${NC}"
    exit 1
fi

# 4. Crear el Lanzador de Escritorio (.desktop) dinámico para el usuario actual
echo -e "\n${AZUL}[4/4] Registrando acceso en el menú de aplicaciones de KDE...${NC}"

cat <<EOF > "$APP_DIR/calculadora-bcv.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=Calculadora BCV
Comment=Calculadora interactiva con historial y tasas en vivo del BCV
Exec=bash -c "python3 \$HOME/.local/share/bcv-calculator/bcv_ticker.py && cd \$HOME/.local/share/bcv-calculator && if ! ss -tuln | grep -q ':8080 '; then python3 -m http.server 8080 & sleep 1; fi && xdg-open http://localhost:8080/calculadora.html"
Icon=accessories-calculator
Terminal=false
Categories=Utility;Application;
StartupNotify=true
EOF

chmod +x "$APP_DIR/calculadora-bcv.desktop"
echo -e "${VERDE}✓ Lanzador registrado exitosamente.${NC}"

echo -e "\n${VERDE}=========================================${NC}"
echo -e "${VERDE} 🎉 ¡Instalación Completada con Éxito!     ${NC}"
echo -e "${VERDE} Puedes buscar 'Calculadora BCV' en tu     ${NC}"
echo -e "${VERDE} menú de inicio de KDE Plasma.           ${NC}"
echo -e "${VERDE}=========================================${NC}"
