# Script para ejecutar la aplicación Streamlit minimalista
# PowerShell

Write-Host "Iniciando aplicación Streamlit minimalista..." -ForegroundColor Green
Write-Host ""

# Activar el entorno virtual si existe
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Ejecutar la aplicación Streamlit
Write-Host "Ejecutando aplicación Streamlit..." -ForegroundColor Yellow
streamlit run streamlit_minimal_app.py --server.port 8502

Write-Host "Presiona cualquier tecla para continuar..." -ForegroundColor Gray
Read-Host
