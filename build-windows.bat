@echo off
REM Script de compilación para Windows
REM Ejecuta este archivo en Windows (PowerShell o CMD)

setlocal enabledelayedexpansion

echo.
echo ===================================
echo   Syncord - Windows Build Script
echo ===================================
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    echo Descarga Python desde https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Instalando dependencias...
pip install -r requirements.txt >nul 2>&1
pip install pyinstaller >nul 2>&1

echo [2/4] Compilando para Windows x64...
pyinstaller syncord-windows.spec --clean
if errorlevel 1 (
    echo ERROR: Fallo la compilación
    pause
    exit /b 1
)

echo [3/4] Preparando releases...
if not exist "releases" mkdir releases

REM Detectar arquitectura
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo [4/4] Moviendo ejecutable a releases...
    move dist\syncord.exe releases\syncord-windows-x64.exe
    echo.
    echo ✅ Compilación completada!
    echo 📍 Binario disponible en: releases\syncord-windows-x64.exe
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    move dist\syncord.exe releases\syncord-windows-x32.exe
    echo.
    echo ✅ Compilación completada!
    echo 📍 Binario disponible en: releases\syncord-windows-x32.exe
) else (
    move dist\syncord.exe releases\syncord-windows.exe
    echo.
    echo ✅ Compilación completada!
    echo 📍 Binario disponible en: releases\syncord-windows.exe
)

echo.
echo 💡 Puedes usar el ejecutable así:
echo    releases\syncord-windows-x64.exe --help
echo.
pause
