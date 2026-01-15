# 🔨 Guía Rápida de Compilación

## 📊 Estado de Binarios Disponibles

| Plataforma | Arquitectura | Estado | Comando |
|-----------|-------------|--------|---------|
| macOS | arm64 (Apple Silicon) | ✅ Listo | `./releases/syncord-macos-arm64 --help` |
| macOS | x86_64 (Intel) | 🔧 Manual | Ver instrucciones abajo |
| Windows | x64 (64-bit) | 🔧 Usa script | `build-windows.bat` |
| Windows | x32 (32-bit) | 🔧 Usa script | `build-windows.bat` |
| Linux | x64 | 🔧 Usa script | `./build-linux.sh` |
| Linux | arm64 | 🔧 Usa script | `./build-linux.sh` |

---

## 🚀 Compilación Rápida por Plataforma

### 🍎 En macOS

```bash
# Para tu arquitectura actual (automático)
./build-all.sh

# Resultado: releases/syncord-macos-arm64
```

### 🪟 En Windows

```bash
# Ejecuta en PowerShell o CMD
build-windows.bat

# Resultado: releases/syncord-windows-x64.exe (o x32)
```

### 🐧 En Linux

```bash
# Ejecuta en tu terminal
./build-linux.sh

# Resultado: releases/syncord-linux-x64 (o arm64)
```

---

## 📋 Instrucciones Detalladas

### Compilar para macOS x86_64 (Intel)

**Solo funciona en una Mac Intel o con herramientas especiales:**

```bash
# Opción 1: En una Mac Intel (lo más simple)
pyinstaller syncord-x86_64.spec
mv dist/syncord-x86_64 releases/syncord-macos-x86_64
chmod +x releases/syncord-macos-x86_64

# Opción 2: Usar Rosetta 2 (en Apple Silicon)
# Esto requiere compilar todas las dependencias en arquitectura x86_64
# Es complejo - ver COMPILATION.md para más detalles
```

### Compilar para Windows x32 (32-bit)

```bash
# Necesitas Python 32-bit instalado
# Descargarlo desde https://www.python.org/downloads/ (Windows x86)

# Luego en CMD/PowerShell:
build-windows.bat

# O manualmente:
pyinstaller syncord-windows.spec
```

### Compilar en otra máquina Linux (ARM64)

```bash
# En una Raspberry Pi u otra máquina ARM
./build-linux.sh

# Compilará automáticamente para tu arquitectura
```

---

## 🔧 Compilación Manual

Si los scripts no funcionan, puedes compilar manualmente:

```bash
# 1. Instalar dependencias
pip install -r requirements.txt
pip install pyinstaller

# 2. Compilar (elige uno según tu plataforma)
pyinstaller syncord.spec              # macOS arm64 / Linux
pyinstaller syncord-x86_64.spec       # macOS Intel
pyinstaller syncord-windows.spec      # Windows

# 3. Mover a releases
mkdir -p releases
mv dist/syncord releases/
chmod +x releases/syncord              # (solo en macOS/Linux)
```

---

## 📦 Distribución de Binarios Compilados

Todos los binarios terminados deben ir en `releases/`:

```
releases/
├── syncord-macos-arm64           ← Tu binario (macOS Apple Silicon)
├── syncord-macos-x86_64          ← Desde Mac Intel
├── syncord-windows-x64.exe       ← Desde Windows 64-bit
├── syncord-windows-x32.exe       ← Desde Windows 32-bit
├── syncord-linux-x64             ← Desde Linux x64
└── syncord-linux-arm64           ← Desde Raspberry Pi / Linux ARM
```

---

## ✅ Verificar Compilación

Prueba que el binario funciona:

```bash
# macOS/Linux
./releases/syncord-macos-arm64 --help

# Windows
releases\syncord-windows-x64.exe --help
```

Deberías ver la ayuda del programa.

---

## 🐛 Problemas Comunes

### "ModuleNotFoundError: No module named 'yaml'"

```bash
pip install PyYAML
```

### "pyinstaller: command not found"

```bash
pip install pyinstaller
```

### El binario es muy grande (>100MB)

Esto es normal para aplicaciones Python compiladas. Para reducir tamaño:

```bash
# Instalar UPX
brew install upx  # macOS
# o para Windows: descarga desde https://upx.github.io/

# Los specs ya incluyen upx=True, así que se usará automáticamente
```

### "Error: This machine doesn't support arm64 execution"

Necesitas compilar en la arquitectura correcta:
- Para x86_64: Usa una Mac Intel
- Para x32: Usa Python 32-bit en Windows

---

## 🔗 Para más información

Ver [COMPILATION.md](./COMPILATION.md) para:
- Configuración CI/CD (GitHub Actions)
- Compilación para múltiples arquitecturas
- Solución avanzada de problemas
- Optimizaciones de tamaño

---

## 📝 Tabla de Compatibilidad

```
Mi Máquina → Puedo compilar para:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
macOS arm64  → macOS arm64 ✅
macOS Intel  → macOS Intel ✅
Windows 64   → Windows x64 ✅
Windows 32   → Windows x32 ✅
Linux x64    → Linux x64 ✅
Linux arm64  → Linux arm64 ✅
```

✅ = Puedes compilar directamente en esa máquina
🔧 = Requiere configuración especial o máquina de destino

---

¡Listo! 🎉 Elige tu plataforma y ejecuta el script correspondiente.
