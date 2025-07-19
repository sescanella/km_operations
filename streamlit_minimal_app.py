"""
Aplicación Streamlit Minimalista para Conversión Excel a JSON y Edición
Autor: Asistente de Programación
Fecha: Julio 2025
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Excel to JSON Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Agregar el directorio backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

# CSS personalizado para diseño minimalista
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2E4057;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 400;
        color: #34495E;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ECF0F1;
        padding-bottom: 0.5rem;
    }
    .file-card {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498DB;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .file-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .success-box {
        background: #D5EDDA;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28A745;
        margin: 1rem 0;
    }
    .warning-box {
        background: #FFF3CD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FFC107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">📊 Excel to JSON Converter</h1>', unsafe_allow_html=True)

# Navegación simple
page = st.sidebar.selectbox(
    "Seleccionar Página",
    ["🏠 Inicio", "📄 Editor JSON"],
    index=0
)

if page == "🏠 Inicio":
    from pages import home_page
    home_page.show()
elif page == "📄 Editor JSON":
    from pages import json_editor_page
    json_editor_page.show()
