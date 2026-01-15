# 🔨 Guía de Compilación para Múltiples Plataformas

Este documento explica cómo compilar Syncord para diferentes plataformas y arquitecturas.

## 📋 Requisitos Previos

En todas las plataformas necesitas:
- Python 3.11+ 
- pip
- PyInstaller

```bash
pip install -r requirements.txt
pip install pyinstaller
```

---

## 🍎 macOS

### macOS arm64 (Apple Silicon M1/M2/M3)

**En tu máquina actual (arm64):**

```bash
./build-all.sh
```

O manualmente:

```bash
pyinstaller syncord.spec
mv dist/syncord releases/syncord-macos-arm64
chmod +x releases/syncord-macos-arm64
```

### macOS x86_64 (Intel)

**Opción 1: Compilar en una Mac Intel**

```bash
pyinstaller syncord-x86_64.spec
mv dist/syncord-x86_64 releases/syncord-macos-x86_64
chmod +x releases/syncord-macos-x86_64
```

**Opción 2: Compilar con arquitectura cruzada (requiere dependencias universales)**

Para crear binarios universales (arm64 + x86_64) necesitas instalar todas las dependencias en modo universal:

```bash
# Crear venv con soporte universal
python3 -m venv .venv-universal --upgrade-deps

# Instalar dependencias compiladas para universal2
# Esto es complejo y requiere homebrew con soporte universal
```

---

## 🪟 Windows

### Windows x64 (64-bit)

**En una máquina Windows:**

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller syncord-windows.spec
move dist\syncord.exe releases\syncord-windows-x64.exe
```

### Windows x32 (32-bit)

**Necesitas Python 32-bit:**

```bash
# Descargar Python 32-bit desde python.org
# Instalar con el Python 32-bit

pip install -r requirements.txt
pip install pyinstaller
pyinstaller syncord-windows.spec
move dist\syncord.exe releases\syncord-windows-x32.exe
```

---

## 🐧 Linux

### Linux x64

**En una máquina Linux:**

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller syncord.spec
mv dist/syncord releases/syncord-linux-x64
chmod +x releases/syncord-linux-x64
```

### Linux arm64 (Raspberry Pi, etc)

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller syncord.spec
mv dist/syncord releases/syncord-linux-arm64
chmod +x releases/syncord-linux-arm64
```

---

## 📦 Distribución de Binarios Compilados

Una vez compilados todos los binarios, puedes distribuirlos:

```
releases/
├── syncord-macos-arm64          (macOS Apple Silicon)
├── syncord-macos-x86_64         (macOS Intel)
├── syncord-windows-x64.exe      (Windows 64-bit)
├── syncord-windows-x32.exe      (Windows 32-bit)
├── syncord-linux-x64            (Linux 64-bit)
└── syncord-linux-arm64          (Linux ARM 64-bit)
```

---

## 🔧 Automatización con CI/CD

Para automatizar la compilación en múltiples plataformas, puedes usar GitHub Actions:

**.github/workflows/build.yml**

```yaml
name: Build Syncord for Multiple Platforms

on: [push, pull_request]

jobs:
  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pyinstaller
      - run: pyinstaller syncord.spec
      - uses: actions/upload-artifact@v3
        with:
          name: syncord-macos-arm64
          path: dist/syncord

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pyinstaller
      - run: pyinstaller syncord-windows.spec
      - uses: actions/upload-artifact@v3
        with:
          name: syncord-windows-x64
          path: dist/syncord.exe

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pyinstaller
      - run: pyinstaller syncord.spec
      - uses: actions/upload-artifact@v3
        with:
          name: syncord-linux-x64
          path: dist/syncord
```

---

## 📝 Notas Importantes

1. **Compatibilidad**: Los binarios compilados en una plataforma NO funcionan en otras plataformas
2. **Arquitectura**: Los binarios compilados en arm64 NO funcionan en x86_64 (Intel) en macOS
3. **Dependencias**: Algunas dependencias (como cryptography) pueden requerir compilación en cada plataforma
4. **Tamaño**: Los binarios compilados suelen ser 100-150 MB después de comprimir

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'yaml'"

Asegúrate de que todas las dependencias estén instaladas:

```bash
pip install -r requirements.txt
```

### Error: "IncompatibleBinaryArchError"

Este error ocurre cuando intentas compilar para una arquitectura diferente. Necesitas:
- Compilar en la máquina/arquitectura de destino, O
- Usar herramientas de cross-compilation (complejo)

### El ejecutable es muy grande

Puedes reducir el tamaño con UPX (ya habilitado en los specs):

```bash
brew install upx  # En macOS
```

---

## ✅ Verificar Compilación

Para verificar que el binario funciona:

```bash
./syncord --help
```

Si ves la ayuda, ¡la compilación fue exitosa!
