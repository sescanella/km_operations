# 📊 Excel to JSON Converter - Aplicación Minimalista

Una aplicación Streamlit simple y funcional para convertir archivos Excel a JSON y editarlos de manera intuitiva.

## 🎯 Funcionalidades

### ✅ Conversión Excel a JSON
- Selecciona archivos Excel desde una lista
- Convierte automáticamente a formato JSON estructurado
- Extrae variables únicas: NV, PLANO, SPOOL
- Organiza datos en dos tablas: Materiales y Uniones

### ✅ Visualización y Edición de JSON
- Visualiza variables únicas (NV, PLANO, SPOOL)
- Muestra tablas de materiales y uniones
- **Editor en vivo** para la tabla de uniones
- Guarda cambios automáticamente

## 🚀 Cómo usar

### 1. Ejecutar la aplicación

**Windows (Batch):**
```batch
run_minimal_streamlit.bat
```

**Windows (PowerShell):**
```powershell
.\run_minimal_streamlit.ps1
```

**Manual:**
```bash
streamlit run streamlit_minimal_app.py --server.port 8502
```

### 2. Navegación

La aplicación se abre en: `http://localhost:8502`

**🏠 Página de Inicio:**
- Lista archivos Excel disponibles para convertir
- Lista archivos JSON generados para editar
- Haz clic en "Convertir" para procesar Excel
- Haz clic en "Editar" para abrir JSON

**📄 Editor JSON:**
- Visualiza variables únicas del proyecto
- Muestra datos organizados por Plan/Spool
- Edita uniones directamente en la tabla
- Guarda cambios con un clic

## 📁 Estructura de archivos

```
piping_reader/
├── streamlit_minimal_app.py      # Aplicación principal
├── pages/                        # Páginas de la aplicación
│   ├── home_page.py              # Página de inicio
│   └── json_editor_page.py       # Editor de JSON
├── run_minimal_streamlit.bat     # Ejecutor Windows (Batch)
├── run_minimal_streamlit.ps1     # Ejecutor Windows (PowerShell)
├── data/
│   ├── etapa_1_salida/          # Archivos Excel de entrada
│   └── json_data/               # Archivos JSON generados
└── backend/                     # Lógica de procesamiento
```

## 📋 Formato de Excel esperado

### Hoja "Materials" o "materiales"
| nv | plano | spool | mat_descripcion | mat_dn | mat_sch | mat_qty |
|----|-------|-------|-----------------|---------|---------|---------|
| 193 | P001 | SP01 | Pipe ASTM A106 | DN150 | SCH40 | 5 |

### Hoja "Joints" o "uniones"
| nv | plano | spool | union_numero | union_dn | union_tipo |
|----|-------|-------|--------------|----------|------------|
| 193 | P001 | SP01 | J001 | DN150 | Soldada |

## 🎨 Características del diseño

- **Minimalista**: Interfaz limpia y sin distracciones
- **Responsive**: Se adapta a diferentes tamaños de pantalla
- **Intuitivo**: Navegación simple con sidebar
- **Eficiente**: Operaciones rápidas y directas

## 🔧 Requisitos técnicos

- Python 3.8+
- Streamlit
- Pandas
- Pydantic

Las dependencias se instalan automáticamente según `requirements.txt`.

## 📝 Notas importantes

1. **Archivos Excel**: Deben estar en `data/etapa_1_salida/`
2. **Archivos JSON**: Se generan en `data/json_data/`
3. **Puerto**: La aplicación corre en puerto 8502 (diferente al principal)
4. **Edición**: Solo las uniones son editables (los materiales son solo lectura)
5. **Autosave**: Los cambios se guardan automáticamente al hacer clic en "Guardar"

## 🚨 Solución de problemas

**Error: "No se encontraron archivos Excel"**
- Verifica que los archivos estén en `data/etapa_1_salida/`
- Asegúrate de que tengan extensión `.xlsx` o `.xls`

**Error: "Estructura del Excel inválida"**
- Verifica que existan las hojas "Materials" y "Joints"
- Revisa que tengan las columnas requeridas

**Error al cargar JSON**
- Verifica que el archivo JSON no esté corrupto
- Intenta recargar la página

---

💡 **Tip**: Esta aplicación está diseñada para ser simple y funcional. Para funcionalidades avanzadas, usa la aplicación principal `streamlit_app.py`.
