# Script PowerShell para ejecutar Streamlit
Write-Host "Iniciando Piping Reader - Interfaz Streamlit" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Configurar variables de entorno para evitar archivos .pyc
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONUNBUFFERED = "1"
Write-Host "Variables de entorno configuradas (no .pyc)" -ForegroundColor Green

# Verificar si el entorno virtual existe
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Error: No se encontró el entorno virtual" -ForegroundColor Red
    Write-Host "Ejecuta primero: python -m venv venv" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Usando Python del entorno virtual..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Ejecutando aplicación Streamlit..." -ForegroundColor Cyan
Write-Host ""
Write-Host "La aplicación se abrirá en: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para detener la aplicación, presiona Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Ejecutar streamlit usando la ruta completa del entorno virtual
& "venv\Scripts\python.exe" -m streamlit run streamlit_app.py
