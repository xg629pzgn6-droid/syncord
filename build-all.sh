#!/bin/bash
# Script de compilación para múltiples plataformas

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$PROJECT_DIR/releases"
VENV_DIR="$PROJECT_DIR/.venv"

# Crear directorio de releases
mkdir -p "$OUTPUT_DIR"

echo "🔨 Compilando Syncord para múltiples plataformas..."
echo ""

# Función para compilar
compile_for_platform() {
    local platform=$1
    local spec_file=$2
    local output_name=$3
    
    echo "📦 Compilando para $platform..."
    
    # Limpiar build anterior
    rm -rf "$PROJECT_DIR/build" "$PROJECT_DIR/dist"
    
    # Compilar
    "$VENV_DIR/bin/pyinstaller" "$spec_file" --clean > /dev/null 2>&1
    
    # Mover a releases
    if [ -f "$PROJECT_DIR/dist/syncord" ] || [ -f "$PROJECT_DIR/dist/syncord.exe" ]; then
        if [ "$platform" == "macOS arm64" ]; then
            mv "$PROJECT_DIR/dist/syncord" "$OUTPUT_DIR/syncord-macos-arm64"
            chmod +x "$OUTPUT_DIR/syncord-macos-arm64"
            echo "✅ $platform compilado: syncord-macos-arm64"
        elif [ "$platform" == "macOS x86_64" ]; then
            mv "$PROJECT_DIR/dist/syncord-x86_64" "$OUTPUT_DIR/syncord-macos-x86_64"
            chmod +x "$OUTPUT_DIR/syncord-macos-x86_64"
            echo "✅ $platform compilado: syncord-macos-x86_64"
        fi
    fi
    echo ""
}

# Compilar para arm64 (Apple Silicon) - plataforma actual
compile_for_platform "macOS arm64" "$PROJECT_DIR/syncord.spec" "syncord-macos-arm64"

echo "🎉 Compilación completada!"
echo ""
echo "📍 Binarios disponibles en: $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR/" | tail -n +2 | awk '{print "   - " $9 " (" $5 ")"}'
echo ""
echo "💡 Para compilar para otras plataformas:"
echo "   - macOS Intel (x86_64): Necesitas una Mac Intel o Rosetta 2"
echo "   - Windows (x32/x64): Compila en Windows o usa una VM"
echo "   - Linux: Compila en Linux"
echo ""
