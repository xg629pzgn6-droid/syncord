#!/bin/bash
# Script de compilación para Linux

set -e

echo "=================================="
echo "  Syncord - Linux Build Script"
echo "=================================="
echo ""

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Instálalo con: sudo apt-get install python3 python3-pip"
    exit 1
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/4] Instalando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1
pip install pyinstaller > /dev/null 2>&1

echo "[2/4] Compilando para Linux..."
pyinstaller syncord.spec --clean

echo "[3/4] Preparando releases..."
mkdir -p releases

# Detectar arquitectura
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)
        BINARY_NAME="syncord-linux-x64"
        ;;
    aarch64)
        BINARY_NAME="syncord-linux-arm64"
        ;;
    armv7l)
        BINARY_NAME="syncord-linux-armv7"
        ;;
    *)
        BINARY_NAME="syncord-linux-$ARCH"
        ;;
esac

echo "[4/4] Moviendo ejecutable a releases..."
mv dist/syncord "releases/$BINARY_NAME"
chmod +x "releases/$BINARY_NAME"

echo ""
echo "✅ Compilación completada!"
echo "📍 Binario disponible en: releases/$BINARY_NAME"
echo ""
echo "💡 Puedes usar el ejecutable así:"
echo "   ./releases/$BINARY_NAME --help"
echo ""
