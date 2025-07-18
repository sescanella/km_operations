import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd  # type: ignore

# Agregar el directorio backend al path para importar módulos
sys.path.append(str(Path(__file__).parent / "backend"))

from backend.app.services.etapa_2.excel_reader import (
    get_available_excel_files,
    read_excel_to_sale_note,
    validate_excel_structure,
    get_spools_from_excel
)
from backend.app.services.etapa_1.excel_generator import generate_empty_excel
from backend.app.services.etapa_1.pdf_extraction import extract_text_from_pdf
from backend.app.core.config import OUTPUT_DIR_ETAPA_1_SALIDA, PDF_INPUT_DIR
from backend.app.services.etapa_2.json_converter import load_json_as_sale_note, save_sale_note_to_json

# Configuración de la página
st.set_page_config(
    page_title="Piping Reader",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🔧 Piping Reader - Sistema de Gestión de Tuberías")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("Navegación")
page = st.sidebar.selectbox(
    "Selecciona una sección:",
    [
        "📊 Dashboard",
        "📥 Etapa 1: Procesamiento PDF",
        "📋 Etapa 2: Lectura Excel",
        "🔄 Extracción Excel → JSON",
        "📝 Editor de Datos (JSON)",
        "🔧 Herramientas Adicionales",
        "📂 Ver JSONs Generados"
    ]
)

# Dashboard Principal
if page == "📊 Dashboard":
    st.header("Dashboard General")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Archivos Excel Disponibles",
            value=len(get_available_excel_files()),
            delta="Etapa 2"
        )
    
    with col2:
        # Contar PDFs disponibles
        try:
            pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.endswith('.pdf')]
            pdf_count = len(pdf_files)
        except:
            pdf_count = 0
        
        st.metric(
            label="PDFs de Entrada",
            value=pdf_count,
            delta="Etapa 1"
        )
    
    with col3:
        st.metric(
            label="Estado del Sistema",
            value="Operativo",
            delta="✅"
        )
    
    st.markdown("---")
    
    # Información del proyecto
    st.subheader("ℹ️ Información del Proyecto")
    st.info("""
    **Piping Reader** es un sistema para procesar documentos técnicos de tuberías:
    
    - **Etapa 1**: Extracción de texto desde PDFs
    - **Etapa 2**: Lectura y validación de archivos Excel con datos de materiales y uniones
    - **API REST**: Endpoints disponibles en FastAPI/Swagger UI
    - **Interfaz Streamlit**: Esta interfaz amigable para testing y visualización
    """)

# Etapa 1: Procesamiento PDF
elif page == "📥 Etapa 1: Procesamiento PDF":
    st.header("Etapa 1: Procesamiento de PDFs")
    
    tab1, tab2 = st.tabs(["📄 Extraer Texto", "📝 Generar Excel Vacío"])
    
    with tab1:
        st.subheader("Extracción de Texto desde PDF")
        
        # Listar PDFs disponibles
        try:
            pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.endswith('.pdf')]
            if pdf_files:
                selected_pdf = st.selectbox("Selecciona un archivo PDF:", pdf_files)
                
                if st.button("Extraer Texto"):
                    with st.spinner("Extrayendo texto..."):
                        try:
                            pdf_path = os.path.join(PDF_INPUT_DIR, selected_pdf)
                            extracted_text = extract_text_from_pdf(pdf_path)
                            
                            st.success("✅ Texto extraído exitosamente")
                            st.text_area(
                                "Texto extraído:",
                                extracted_text,
                                height=400
                            )
                        except Exception as e:
                            st.error(f"❌ Error al extraer texto: {str(e)}")
            else:
                st.warning("No se encontraron archivos PDF en el directorio de entrada")
        except Exception as e:
            st.error(f"Error al acceder al directorio PDF: {str(e)}")
    
    with tab2:
        st.subheader("Generador de Excel Vacío")
        
        filename = st.text_input("Nombre del archivo:", value="nv_data_empty.xlsx")
        
        if st.button("Generar Excel Vacío"):
            try:
                file_path = generate_empty_excel(OUTPUT_DIR_ETAPA_1_SALIDA, filename)
                st.success(f"✅ Archivo Excel vacío generado: {file_path}")
            except Exception as e:
                st.error(f"❌ Error al generar archivo: {str(e)}")

# Etapa 2: Lectura Excel
elif page == "📋 Etapa 2: Lectura Excel":
    st.header("Etapa 2: Lectura y Validación de Excel")
    
    # Obtener archivos Excel disponibles
    excel_files = get_available_excel_files()
    
    if not excel_files:
        st.warning("No se encontraron archivos Excel en el directorio de salida de Etapa 1")
        st.info("Asegúrate de que existan archivos .xlsx en el directorio configurado")
    else:
        # Selector de archivo
        selected_file = st.selectbox("Selecciona un archivo Excel:", excel_files)
        
        if selected_file:
            col1, col2 = st.columns([2, 1])
            
            with col2:
                # Botones de acción
                if st.button("🔍 Validar Estructura"):
                    with st.spinner("Validando estructura..."):
                        try:
                            is_valid, message = validate_excel_structure(selected_file)
                            if is_valid:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
                        except Exception as e:
                            st.error(f"❌ Error en validación: {str(e)}")
                
                if st.button("📊 Leer Datos Completos"):
                    with st.spinner("Leyendo datos..."):
                        try:
                            sale_note = read_excel_to_sale_note(selected_file)
                            st.session_state['sale_note'] = sale_note
                            st.success("✅ Datos leídos exitosamente")
                        except Exception as e:
                            st.error(f"❌ Error al leer datos: {str(e)}")
                
                if st.button("🏗️ Obtener Spools"):
                    with st.spinner("Obteniendo spools..."):
                        try:
                            spools = get_spools_from_excel(selected_file)
                            st.session_state['spools'] = spools
                            st.success(f"✅ {len(spools)} spools encontrados")
                        except Exception as e:
                            st.error(f"❌ Error al obtener spools: {str(e)}")
            
            with col1:
                # Mostrar resultados
                if 'sale_note' in st.session_state:
                    st.subheader(f"📋 Nota de Venta: {st.session_state['sale_note'].nv}")
                    
                    # Expandir para mostrar detalles
                    with st.expander("Ver detalles completos"):
                        for i, plan in enumerate(st.session_state['sale_note'].plans):
                            st.write(f"**Plan {i+1}:**")
                            st.write(f"- Plano: {plan.plano}")
                            st.write(f"- Spool: {plan.spool_data.spool}")
                            st.write(f"- Materiales: {len(plan.spool_data.materials)}")
                            st.write(f"- Uniones: {len(plan.spool_data.joints)}")
                            
                            # Mostrar materiales en tabla
                            if plan.spool_data.materials:
                                materials_data = []  # type: ignore
                                for mat in plan.spool_data.materials:
                                    materials_data.append({  # type: ignore
                                        "Número Interno": mat.mat_numero_interno,
                                        "Descripción": mat.mat_descripcion,
                                        "DN": mat.mat_dn,
                                        "SCH": mat.mat_sch,
                                        "Cantidad": mat.mat_qty
                                    })
                                st.write("**Materiales:**")
                                st.dataframe(pd.DataFrame(materials_data))  # type: ignore
                            
                            # Mostrar uniones en tabla
                            if plan.spool_data.joints:
                                joints_data = []  # type: ignore
                                for joint in plan.spool_data.joints:
                                    joints_data.append({  # type: ignore
                                        "Número": joint.union_numero,
                                        "DN": joint.union_dn,
                                        "Tipo": joint.union_tipo,
                                        "Armador": joint.armador,
                                        "Soldador Raíz": joint.soldador_raiz,
                                        "Soldador Remate": joint.soldador_remate
                                    })
                                st.write("**Uniones:**")
                                st.dataframe(pd.DataFrame(joints_data))  # type: ignore
                
                if 'spools' in st.session_state:
                    st.subheader("🏗️ Lista de Spools")
                    for spool in st.session_state['spools']:
                        st.write(f"- {spool}")

# Página de extracción Excel → JSON
elif page == "🔄 Extracción Excel → JSON":
    st.header("🔄 Extracción de Información Excel → JSON")
    st.markdown("Esta sección convierte archivos Excel en formato JSON para su posterior edición.")
    
    # Mostrar archivos Excel disponibles
    excel_files = get_available_excel_files()
    if not excel_files:
        st.warning("No se encontraron archivos Excel en 'data/etapa_1_salida/'")
        st.info("Usa la Etapa 1 para generar archivos Excel o coloca archivos manualmente en la carpeta.")
    else:
        st.success(f"Se encontraron {len(excel_files)} archivo(s) Excel disponible(s)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📁 Archivos Excel Disponibles")
            for file in excel_files:
                st.write(f"• {file}")
        
        with col2:
            st.subheader("⚙️ Conversión a JSON")
            selected_file = st.selectbox("Selecciona archivo para convertir:", excel_files)
            
            if st.button("🔄 Convertir a JSON", type="primary"):
                try:
                    with st.spinner("Procesando archivo Excel..."):
                        from backend.app.services.etapa_2.json_converter import convert_excel_to_json
                        json_path = convert_excel_to_json(selected_file)
                        st.success(f"✅ JSON creado exitosamente en: `{json_path}`")
                        
                        # Mostrar preview del JSON
                        import json
                        with open(json_path, 'r', encoding='utf-8') as f:
                            json_data = json.load(f)
                        
                        st.subheader("📋 Preview del JSON generado")
                        st.json(json_data)
                        
                except Exception as e:
                    st.error(f"❌ Error al procesar {selected_file}: {str(e)}")
    
    # Mostrar archivos JSON existentes
    st.markdown("---")
    st.subheader("📂 Archivos JSON Generados")
    json_dir = os.path.join("data", "json_data")
    if os.path.exists(json_dir):
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        if json_files:
            st.success(f"Archivos JSON disponibles: {len(json_files)}")
            cols = st.columns(min(len(json_files), 3))
            for i, json_file in enumerate(json_files):
                with cols[i % 3]:
                    st.metric(label="Archivo", value=json_file.replace('.json', ''))
                    json_path = os.path.join(json_dir, json_file)
                    file_size = os.path.getsize(json_path)
                    st.caption(f"Tamaño: {file_size} bytes")
        else:
            st.info("No hay archivos JSON generados aún.")
    else:
        st.info("Directorio de JSON no existe. Se creará al generar el primer archivo.")

# Página de edición de datos en tabla
elif page == "📝 Editor de Datos (JSON)":
    st.header("📝 Editor de Datos - JSON generado desde Excel")
    json_dir = os.path.join("data", "json_data")
    if not os.path.exists(json_dir):
        st.warning("No hay archivos JSON generados. Procesa primero un Excel.")
    else:
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        if not json_files:
            st.info("No hay archivos JSON disponibles.")
        else:
            selected_file = st.selectbox("Selecciona archivo JSON", json_files)
            nv = int(selected_file.replace('nv_', '').replace('.json', ''))
            sale_note = load_json_as_sale_note(nv)
            st.subheader(f"NV: {sale_note.nv}")
            for plan in sale_note.plans:
                st.markdown(f"### Plano: {plan.plano}")
                # Materiales
                st.markdown("**Materiales**")
                df_mat = pd.DataFrame([m.model_dump() for m in plan.spool_data.materials])
                edited_mat = st.data_editor(df_mat, num_rows="dynamic", use_container_width=True, key=f"mat_{plan.plano}")
                # Uniones
                st.markdown("**Uniones**")
                df_joints = pd.DataFrame([j.model_dump() for j in plan.spool_data.joints])
                edited_joints = st.data_editor(df_joints, num_rows="dynamic", use_container_width=True, key=f"joints_{plan.plano}")
                # Guardar cambios
                if st.button(f"💾 Guardar cambios {plan.plano}"):
                    # Actualizar objetos
                    for i, row in edited_mat.iterrows():  # type: ignore
                        for field in row.index:
                            setattr(plan.spool_data.materials[i], field, row[field])  # type: ignore
                    for i, row in edited_joints.iterrows():  # type: ignore
                        for field in row.index:
                            setattr(plan.spool_data.joints[i], field, row[field])  # type: ignore
                    save_sale_note_to_json(sale_note)
                    st.success(f"Cambios guardados en {selected_file}")

# Herramientas Adicionales
elif page == "🔧 Herramientas Adicionales":
    st.header("Herramientas Adicionales")
    
    tab1, tab2 = st.tabs(["🔗 API Info", "⚙️ Configuración"])
    
    with tab1:
        st.subheader("Información de la API")
        st.info("""
        **FastAPI/Swagger UI** también está disponible:
        
        Para iniciar el servidor FastAPI:
        ```bash
        cd backend
        uvicorn app.main:app --reload
        ```
        
        Luego visita: http://localhost:8000/docs
        """)
        
        st.subheader("Endpoints Disponibles")
        endpoints_info = """
        **Etapa 1:**
        - POST `/api/v1/pdf/extract` - Extraer texto de PDF
        - POST `/api/v1/excel/generate-empty` - Generar Excel vacío
        
        **Etapa 2:**
        - GET `/api/v2/excel-files` - Listar archivos Excel
        - GET `/api/v2/validate/{filename}` - Validar estructura
        - GET `/api/v2/read/{filename}` - Leer datos completos
        - GET `/api/v2/spools/{filename}` - Obtener lista de spools
        - GET `/api/v2/spool-details/{filename}/{spool_name}` - Detalles de spool específico
        """
        st.code(endpoints_info)
    
    with tab2:
        st.subheader("Configuración del Sistema")
        
        st.write("**Directorios configurados:**")
        st.code(f"""
        PDF Input: {PDF_INPUT_DIR}
        Excel Output: {OUTPUT_DIR_ETAPA_1_SALIDA}
        """)
        
        # Botón para limpiar cache de sesión
        if st.button("🗑️ Limpiar Cache de Sesión"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Cache limpiado")

# Footer

# Nueva sección para ver los JSONs generados
if page == "📂 Ver JSONs Generados":
    st.header("📂 Archivos JSON Generados")
    json_dir = os.path.join("data", "json_data")
    if not os.path.exists(json_dir):
        st.warning("No hay archivos JSON generados. Procesa primero un Excel.")
    else:
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        if not json_files:
            st.info("No hay archivos JSON disponibles.")
        else:
            selected_file = st.selectbox("Selecciona archivo JSON para visualizar", json_files)
            json_path = os.path.join(json_dir, selected_file)
            st.subheader(f"Visualizando: {selected_file}")
            try:
                import json
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                st.json(json_data)
            except Exception as e:
                st.error(f"Error al leer el archivo JSON: {str(e)}")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Piping Reader v1.0 - Sistema de Gestión de Tuberías"
    "</div>",
    unsafe_allow_html=True
)
