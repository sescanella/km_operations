"""
Página de inicio - Lista archivos Excel y JSONs disponibles
"""

import streamlit as st
import os
from typing import List
import sys
from pathlib import Path

# Importar módulos del backend
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from backend.app.services.etapa_2.excel_reader_clean import (
    get_available_excel_files,
    read_excel_to_sale_note,
    validate_excel_structure
)
from backend.app.services.etapa_2.json_converter import convert_excel_to_json
from backend.app.core.config import OUTPUT_DIR_ETAPA_1_SALIDA

JSON_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "json_data")

def get_available_json_files() -> List[str]:
    """Obtiene lista de archivos JSON disponibles"""
    if not os.path.exists(JSON_DIR):
        return []
    
    json_files = []
    for file in os.listdir(JSON_DIR):
        if file.endswith('.json') and file.startswith('nv_'):
            json_files.append(file)
    
    return sorted(json_files)

def show():
    """Muestra la página principal"""
    
    # Crear dos columnas principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="section-header">📁 Archivos Excel</h2>', unsafe_allow_html=True)
        
        # Obtener archivos Excel disponibles
        excel_files = get_available_excel_files()
        
        if not excel_files:
            st.warning("No se encontraron archivos Excel en el directorio.")
            st.info(f"Directorio: `{OUTPUT_DIR_ETAPA_1_SALIDA}`")
        else:
            st.success(f"Se encontraron {len(excel_files)} archivo(s) Excel")
            
            # Mostrar cada archivo Excel como una tarjeta clickeable
            for excel_file in excel_files:
                with st.container():
                    st.markdown(f'<div class="file-card">', unsafe_allow_html=True)
                    
                    col_info, col_action = st.columns([3, 1])
                    
                    with col_info:
                        st.write(f"**{excel_file}**")
                        
                        # Mostrar información básica del archivo
                        try:
                            validation = validate_excel_structure(excel_file)
                            if validation["valid"]:
                                info = validation["info"]
                                st.write(f"📊 {info['total_materials']} materiales, {info['total_joints']} uniones")
                                st.write(f"🏗️ {info['unique_plans']} plano(s), {info['unique_spools']} spool(s)")
                            else:
                                st.error("⚠️ Archivo con errores de estructura")
                        except:
                            st.write("📄 Archivo Excel")
                    
                    with col_action:
                        if st.button(f"Convertir", key=f"convert_{excel_file}"):
                            with st.spinner("Convirtiendo Excel a JSON..."):
                                try:
                                    json_path = convert_excel_to_json(excel_file)
                                    st.success("✅ Conversión exitosa!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h2 class="section-header">📄 Archivos JSON</h2>', unsafe_allow_html=True)
        
        # Obtener archivos JSON disponibles
        json_files = get_available_json_files()
        
        if not json_files:
            st.warning("No se encontraron archivos JSON generados.")
            st.info("Convierte un archivo Excel para generar JSONs.")
        else:
            st.success(f"Se encontraron {len(json_files)} archivo(s) JSON")
            
            # Mostrar cada archivo JSON como una tarjeta clickeable
            for json_file in json_files:
                with st.container():
                    st.markdown(f'<div class="file-card">', unsafe_allow_html=True)
                    
                    col_info, col_action = st.columns([3, 1])
                    
                    with col_info:
                        st.write(f"**{json_file}**")
                        
                        # Extraer número de NV del nombre del archivo
                        nv = json_file.replace('nv_', '').replace('.json', '')
                        st.write(f"🏷️ NV: {nv}")
                        
                        # Mostrar información del archivo
                        file_path = os.path.join(JSON_DIR, json_file)
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            st.write(f"📏 Tamaño: {file_size:,} bytes")
                    
                    with col_action:
                        if st.button(f"Editar", key=f"edit_{json_file}"):
                            # Guardar el archivo seleccionado en session_state
                            st.session_state.selected_json_file = json_file
                            st.session_state.selected_nv = nv
                            st.success(f"JSON {json_file} seleccionado. Ve a la página 'Editor JSON'.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # Información adicional en la parte inferior
    st.markdown("---")
    st.markdown("""
    ### 💡 Instrucciones de uso:
    
    1. **Convertir Excel a JSON**: Haz clic en "Convertir" junto a cualquier archivo Excel para transformarlo a formato JSON.
    2. **Editar JSON**: Haz clic en "Editar" junto a cualquier archivo JSON para abrirlo en el editor.
    3. **Navegación**: Usa el menú lateral para cambiar entre páginas.
    
    **Formato esperado del Excel:**
    - Hoja "Materials" o "materiales" con columnas: nv, plano, spool, mat_descripcion, mat_dn, mat_sch, mat_qty
    - Hoja "Joints" o "uniones" con columnas: nv, plano, spool, union_numero, union_dn, union_tipo
    """)
