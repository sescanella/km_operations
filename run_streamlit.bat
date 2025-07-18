@echo off
echo Iniciando Piping Reader - Interfaz Streamlit
echo ==========================================
echo.

REM Configurar variables de entorno para evitar archivos .pyc
set PYTHONDONTWRITEBYTECODE=1
set PYTHONUNBUFFERED=1
echo Variables de entorno configuradas (no .pyc)

REM Verificar si el entorno virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Error: No se encontró el entorno virtual
    echo Ejecuta primero: python -m venv venv
    pause
    exit /b 1
)

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Ejecutando aplicación Streamlit...
echo.
echo La aplicación se abrirá en: http://localhost:8501
echo.
echo Para detener la aplicación, presiona Ctrl+C
echo.

venv\Scripts\python.exe -m streamlit run streamlit_app.py

pause
