# Piping Reader - Interfaz Streamlit

Esta aplicación Streamlit proporciona una interfaz web amigable para probar y usar las funcionalidades del sistema Piping Reader.

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Windows)
```bash
# Ejecutar con doble clic o desde terminal
run_streamlit.bat
```

### Opción 2: PowerShell
```powershell
.\run_streamlit.ps1
```

### Opción 3: Manual
```bash
# Activar entorno virtual (si aplica)
venv\Scripts\activate

# Instalar dependencias (si es necesario)
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run streamlit_app.py
```

## 📋 Funcionalidades Disponibles

### 📊 Dashboard
- Vista general del sistema
- Métricas de archivos disponibles
- Estado del sistema

### 📥 Etapa 1: Procesamiento PDF
- **Extracción de Texto**: Procesa archivos PDF y extrae texto
- **Generador de Excel**: Crea plantillas Excel vacías con estructura correcta

### 📋 Etapa 2: Lectura Excel
- **Validación de Estructura**: Verifica que el Excel tenga el formato correcto
- **Lectura Completa**: Lee y muestra todos los datos estructurados
- **Lista de Spools**: Extrae únicamente los nombres de spools
- **Visualización de Datos**: Tablas interactivas con materiales y uniones

### 🔄 Extracción Excel → JSON
- **Conversión Automática**: Transforma archivos Excel en formato JSON estructurado
- **Preview de Datos**: Muestra vista previa del JSON generado
- **Gestión de Archivos**: Lista archivos Excel disponibles y JSONs generados
- **Validación Pydantic**: Garantiza consistencia y validez de los datos extraídos

### 📝 Editor de Datos (JSON)
- **Edición en Tabla**: Modifica datos directamente en tablas interactivas
- **Guardado Automático**: Actualiza archivos JSON con cambios del usuario
- **Vista por Plano**: Organiza edición por planos y spools
- **Validación de Tipos**: Mantiene integridad de datos durante la edición

### 🔧 Herramientas Adicionales
- **Información de API**: Enlaces y documentación de FastAPI/Swagger
- **Configuración**: Ajustes del sistema y limpieza de cache

## 🔗 Integración con FastAPI

Esta interfaz Streamlit complementa (no reemplaza) la API REST de FastAPI:

- **Streamlit**: Interfaz amigable para testing manual y visualización
- **FastAPI/Swagger**: API REST para integración con otros sistemas

### Para usar FastAPI simultáneamente:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Luego visita:
- **Streamlit**: http://localhost:8501
- **Swagger UI**: http://localhost:8000/docs

## 📁 Estructura de Archivos

```
streamlit_app.py          # Aplicación principal de Streamlit
run_streamlit.bat         # Script de inicio para Windows
run_streamlit.ps1         # Script de inicio para PowerShell
backend/                  # Servicios y lógica de negocio
  app/
    services/
      etapa_1/            # Servicios de procesamiento PDF
      etapa_2/            # Servicios de lectura Excel y conversión JSON
data/                     # Archivos de datos (ignorado en git)
  pdf_entradas/           # PDFs de entrada
  etapa_1_salida/         # Archivos Excel de salida
  json_data/              # Archivos JSON generados desde Excel
  logs/                   # Logs del sistema
```

## 🛠️ Configuración

Los directorios se configuran en `backend/app/core/config.py`:

- `PDF_INPUT_DIR`: Directorio de PDFs de entrada
- `OUTPUT_DIR_ETAPA_1_SALIDA`: Directorio de archivos Excel

### Configuración Anti-Cache Python

El proyecto está configurado para **NO generar archivos `__pycache__`** automáticamente:

1. **Variables de Entorno**: Los scripts de inicio configuran `PYTHONDONTWRITEBYTECODE=1`
2. **VS Code Settings**: El archivo `.vscode/settings.json` excluye archivos cache de búsquedas y visualización
3. **Git Ignore**: El archivo `.gitignore` evita que se suban archivos cache al repositorio

**Scripts con configuración anti-cache:**
- `run_streamlit.bat` y `run_streamlit.ps1` configuran variables automáticamente
- `setup_python_env.ps1` configura variables permanentes en Windows

Si aparecen archivos `__pycache__`, puedes eliminarlos con:
```powershell
# PowerShell - eliminar todos los __pycache__ del proyecto
Get-ChildItem -Path . -Recurse -Name "__pycache__" -Directory | 
    ForEach-Object { Remove-Item -Path ".\$_" -Recurse -Force }
```

## 📝 Notas de Uso

1. **Archivos de Datos**: Asegúrate de tener archivos en los directorios configurados
2. **Formato Excel**: Los archivos deben tener hojas "materiales" y "uniones"
3. **Estructura de Columnas**: Debe coincidir con el schema definido en `nv_schemas.py`

## 🐛 Solución de Problemas

### Error: "No se encontraron archivos Excel"
- Verifica que existan archivos .xlsx en `data/etapa_1_salida/`
- Usa el generador de Excel vacío en Etapa 1

### Error: "Import could not be resolved"
- Instala las dependencias: `pip install -r requirements.txt`
- Activa el entorno virtual si aplica

### Error: "FileNotFoundError"
- Verifica que los directorios de datos existan
- Crea la estructura de carpetas manualmente si es necesario

## 🔄 Próximas Funcionalidades

- [x] Editor de datos inline
- [x] Extracción Excel → JSON
- [ ] Exportación de reportes
- [ ] Carga de archivos via drag & drop
- [ ] Filtros avanzados
- [ ] Modo dark/light theme
