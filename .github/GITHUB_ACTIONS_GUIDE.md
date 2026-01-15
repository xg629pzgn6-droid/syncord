# 🚀 Guía de GitHub Actions para Syncord

Este documento explica cómo usar GitHub Actions para compilar y distribuir Syncord automáticamente.

## 📋 ¿Qué hace el workflow?

El archivo `.github/workflows/build.yml` automatiza:

1. **Build para macOS** (`build-macos`)
   - Compila para macOS ARM64 (Apple Silicon)
   - Genera ejecutable optimizado con PyInstaller
   - Crea artifact descargable

2. **Build para Windows** (`build-windows`)
   - Compila para Windows x64
   - Genera `.exe` listo para usar
   - Crea artifact descargable

3. **Build para Linux** (`build-linux`)
   - Compila para Linux x64
   - Genera ejecutable ELF
   - Crea artifact descargable

4. **Build de Docker** (`docker-build`)
   - Valida que el Dockerfile sea correcto
   - Crea imagen Docker optimizada

5. **Validación** (`validate`)
   - Comprueba sintaxis Python
   - Ejecuta linter (pylint)

## 🔄 Disparadores

El workflow se ejecuta automáticamente cuando:

- Haces **push** a las ramas `main` o `develop`
- Abres un **pull request** hacia `main` o `develop`

```yaml
on: 
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

## 📊 Estado del Build

Para ver el estado del build:

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña **Actions**
3. Selecciona el workflow más reciente

O directamente: `https://github.com/TU_USUARIO/syncord/actions`

## 📥 Descargar Artifacts

Después de que se completa un build exitoso:

1. Ve a **Actions** → **Build Syncord for Multiple Platforms**
2. Selecciona el run más reciente
3. En **Artifacts**, descarga:
   - `syncord-macos-arm64` (macOS)
   - `syncord-windows-x64` (Windows)
   - `syncord-linux-x64` (Linux)

## 🔧 Personalizar el Workflow

### Cambiar ramas disparadoras

Edita `.github/workflows/build.yml`:

```yaml
on: 
  push:
    branches: [ main, develop, staging ]  # Agrega más ramas
  pull_request:
    branches: [ main, develop, staging ]
```

### Cambiar versión de Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Cambia aquí
```

### Ejecutar solo algunos jobs

Comenta los jobs que no quieras:

```yaml
# build-macos:  # Comentado - no se ejecutará
#   runs-on: macos-latest
```

## 🚀 Publicar Releases

Para crear releases automáticos con los artifacts:

1. Crea un tag en git:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. En GitHub, ve a **Releases** → **Create a new release**

3. Selecciona el tag y GitHub mostrará los artifacts construidos

## 📋 Monitorear Logs

Si un build falla:

1. Ve a **Actions**
2. Haz clic en el workflow fallido
3. Expande el job que falló
4. Lee los logs para encontrar el error

## 🔐 Secretos (si necesitas)

Para agregar variables privadas (tokens, APIs, etc.):

1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. Haz clic en **New repository secret**
3. Agrega el secreto
4. Úsalo en el workflow:

```yaml
- name: Mi paso
  run: mi_comando
  env:
    MI_TOKEN: ${{ secrets.MI_TOKEN }}
```

## 🐛 Solución de Problemas

### El build falla por dependencias

```bash
# Verifica que requirements.txt esté actualizado
pip freeze > requirements.txt
```

### El build es lento

Los builds pueden tardarse 5-10 minutos. Es normal:
- macOS: ~7 minutos
- Windows: ~6 minutos  
- Linux: ~5 minutos
- Docker: ~3 minutos

### No veo los artifacts

1. Verifica que el build fue exitoso (✅)
2. Los artifacts se eliminan después de 90 días
3. Comprueba que `path:` en `upload-artifact` sea correcto

## 📊 Estadísticas de Builds

Para ver histórico de builds:
- Ve a **Actions**
- Ordena por fecha
- Filtra por rama

## ✅ Verificar que todo está configurado

```bash
# Verifica que el archivo existe
ls -la .github/workflows/build.yml

# Valida la sintaxis YAML
cat .github/workflows/build.yml | python -m yaml

# O usa un validador online: https://www.yamllint.com/
```

## 🎯 Próximos pasos

Después de confirmar que el workflow funciona:

1. **Automatizar releases**: Crear versiones automáticamente con cada tag
2. **Notificaciones**: Recibir emails cuando falle un build
3. **Caché**: Agregar caché de dependencias para builds más rápidos
4. **Testing**: Agregar tests automáticos

## 📚 Referencias

- [GitHub Actions Docs](https://docs.github.com/es/actions)
- [PyInstaller + GitHub Actions](https://github.com/pyinstaller/pyinstaller/discussions/5873)
- [YAML Validator](https://www.yamllint.com/)
