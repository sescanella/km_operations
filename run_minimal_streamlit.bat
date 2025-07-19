@echo off
echo Iniciando aplicacion Streamlit minimalista...
echo.

REM Activar el entorno virtual si existe
if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Ejecutar la aplicacion Streamlit
echo Ejecutando aplicacion Streamlit...
streamlit run streamlit_minimal_app.py --server.port 8502

pause
