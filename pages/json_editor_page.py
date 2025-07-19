"""
Página de edición de JSON - Visualiza y permite editar archivos JSON
"""

import streamlit as st
import os
import json
import pandas as pd
from typing import List, Dict, Any
import sys
from pathlib import Path

# Importar módulos del backend
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from backend.app.api.v1.schemas.nv_schemas import SaleNote, Plan, Spool, Material, Joint
from backend.app.services.etapa_2.json_converter import save_sale_note_to_json

JSON_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "json_data")

def load_json_file(filename: str) -> Dict[str, Any]:
    """Carga un archivo JSON"""
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filename: str, data: Dict[str, Any]) -> None:
    """Guarda un archivo JSON"""
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def show():
    """Muestra la página de edición de JSON"""
    
    # Verificar si hay un archivo JSON seleccionado
    if 'selected_json_file' not in st.session_state:
        st.warning("⚠️ No hay ningún archivo JSON seleccionado.")
        st.info("Ve a la página 'Inicio' y selecciona un archivo JSON para editar.")
        
        # Mostrar selector manual como alternativa
        st.markdown("---")
        st.markdown("### O selecciona un archivo JSON manualmente:")
        
        json_files = []
        if os.path.exists(JSON_DIR):
            json_files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json') and f.startswith('nv_')]
        
        if json_files:
            selected_file = st.selectbox("Seleccionar archivo JSON:", [""] + json_files)
            if selected_file and st.button("Cargar archivo"):
                st.session_state.selected_json_file = selected_file
                st.session_state.selected_nv = selected_file.replace('nv_', '').replace('.json', '')
                st.rerun()
        else:
            st.error("No se encontraron archivos JSON.")
        
        return
    
    # Cargar el archivo JSON seleccionado
    try:
        filename = st.session_state.selected_json_file
        nv = st.session_state.selected_nv
        
        st.markdown(f'<h1 class="main-header">📄 Editor JSON - NV {nv}</h1>', unsafe_allow_html=True)
        
        # Cargar datos
        json_data = load_json_file(filename)
        sale_note = SaleNote(**json_data)
        
        # Sidebar con información del archivo
        with st.sidebar:
            st.markdown("### 📋 Información del Archivo")
            st.write(f"**Archivo:** {filename}")
            st.write(f"**NV:** {sale_note.nv}")
            st.write(f"**Total de Planes:** {len(sale_note.plans)}")
            
            total_materials = sum(len(plan.spool_data.materials) for plan in sale_note.plans)
            total_joints = sum(len(plan.spool_data.joints) for plan in sale_note.plans)
            st.write(f"**Total de Materiales:** {total_materials}")
            st.write(f"**Total de Uniones:** {total_joints}")
            
            st.markdown("---")
            if st.button("🔄 Recargar archivo"):
                st.rerun()
            
            if st.button("🏠 Volver al inicio"):
                del st.session_state.selected_json_file
                del st.session_state.selected_nv
                st.rerun()
        
        # Mostrar variables únicas
        st.markdown('<h2 class="section-header">🏷️ Variables Únicas</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("NV", sale_note.nv)
        with col2:
            unique_planos = list(set(plan.plano for plan in sale_note.plans))
            st.metric("Planos", len(unique_planos))
        with col3:
            unique_spools = list(set(plan.spool_data.spool for plan in sale_note.plans))
            st.metric("Spools", len(unique_spools))
        
        # Mostrar detalles por plan
        st.markdown('<h2 class="section-header">📊 Datos por Plan/Spool</h2>', unsafe_allow_html=True)
        
        # Crear tabs para cada plan
        if len(sale_note.plans) > 1:
            plan_names = [f"Plan {plan.plano} - Spool {plan.spool_data.spool}" for plan in sale_note.plans]
            selected_tab = st.selectbox("Seleccionar Plan/Spool:", plan_names)
            plan_index = plan_names.index(selected_tab)
        else:
            plan_index = 0
        
        current_plan = sale_note.plans[plan_index]
        
        # Mostrar información del plan actual
        st.markdown(f"**Plan:** {current_plan.plano} | **Spool:** {current_plan.spool_data.spool}")
        
        # Crear dos columnas para materiales y uniones
        col_materials, col_joints = st.columns([1, 1])
        
        with col_materials:
            st.markdown("#### 📦 Materiales")
            
            # Convertir materiales a DataFrame para visualización
            materials_data = []
            for material in current_plan.spool_data.materials:
                materials_data.append({
                    "Descripción": material.mat_descripcion,
                    "Diámetro": material.mat_dn,
                    "SCH": material.mat_sch,
                    "Cantidad": material.mat_qty
                })
            
            if materials_data:
                df_materials = pd.DataFrame(materials_data)
                st.dataframe(df_materials, use_container_width=True, hide_index=True)
            else:
                st.info("No hay materiales para este plan/spool.")
        
        with col_joints:
            st.markdown("#### 🔗 Uniones (Editable)")
            
            # Convertir uniones a DataFrame editable
            joints_data = []
            for i, joint in enumerate(current_plan.spool_data.joints):
                joints_data.append({
                    "index": i,
                    "Número de Unión": joint.union_numero,
                    "Diámetro": joint.union_dn,
                    "Tipo": joint.union_tipo
                })
            
            if joints_data:
                # Editor de datos para uniones
                edited_joints = st.data_editor(
                    pd.DataFrame(joints_data).drop('index', axis=1),
                    use_container_width=True,
                    hide_index=True,
                    num_rows="dynamic",
                    key=f"joints_editor_{plan_index}"
                )
                
                # Botón para guardar cambios
                if st.button("💾 Guardar cambios en uniones", key=f"save_joints_{plan_index}"):
                    try:
                        # Actualizar las uniones en el objeto SaleNote
                        new_joints = []
                        for _, row in edited_joints.iterrows():
                            joint = Joint(
                                union_numero=str(row["Número de Unión"]),
                                union_dn=str(row["Diámetro"]),
                                union_tipo=str(row["Tipo"])
                            )
                            new_joints.append(joint)
                        
                        # Actualizar el plan actual
                        sale_note.plans[plan_index].spool_data.joints = new_joints
                        
                        # Guardar el archivo JSON actualizado
                        save_sale_note_to_json(sale_note)
                        
                        st.success("✅ Cambios guardados exitosamente!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error al guardar cambios: {str(e)}")
            else:
                st.info("No hay uniones para este plan/spool.")
                
                # Permitir agregar nuevas uniones
                if st.button("➕ Agregar nueva unión", key=f"add_joint_{plan_index}"):
                    new_joint = Joint(
                        union_numero="Nueva Unión",
                        union_dn="DN",
                        union_tipo="Tipo"
                    )
                    sale_note.plans[plan_index].spool_data.joints.append(new_joint)
                    save_sale_note_to_json(sale_note)
                    st.rerun()
        
        # Sección de acciones globales
        st.markdown("---")
        st.markdown("### ⚙️ Acciones")
        
        col_actions1, col_actions2, col_actions3 = st.columns(3)
        
        with col_actions1:
            if st.button("📥 Descargar JSON"):
                # Generar descarga del JSON
                json_str = json.dumps(sale_note.model_dump(), indent=2, ensure_ascii=False)
                st.download_button(
                    label="Descargar archivo JSON",
                    data=json_str.encode('utf-8'),
                    file_name=f"nv_{sale_note.nv}_editado.json",
                    mime="application/json"
                )
        
        with col_actions2:
            if st.button("🔄 Recargar desde archivo"):
                st.rerun()
        
        with col_actions3:
            if st.button("🗑️ Eliminar JSON", type="secondary"):
                if st.checkbox("Confirmar eliminación"):
                    try:
                        file_path = os.path.join(JSON_DIR, filename)
                        os.remove(file_path)
                        st.success("Archivo eliminado.")
                        del st.session_state.selected_json_file
                        del st.session_state.selected_nv
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar: {str(e)}")
        
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo JSON: {str(e)}")
        st.info("Intenta recargar el archivo o selecciona otro.")
        
        if st.button("🏠 Volver al inicio"):
            if 'selected_json_file' in st.session_state:
                del st.session_state.selected_json_file
            if 'selected_nv' in st.session_state:
                del st.session_state.selected_nv
            st.rerun()
