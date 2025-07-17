# backend/app/services/etapa_2/excel_reader_clean.py

import pandas as pd
import os
from typing import List, Dict, Any
from backend.app.api.v1.schemas.nv_schemas import SaleNote, Plan, Spool, Material, Joint
from backend.app.core.config import OUTPUT_DIR_ETAPA_1_SALIDA


def read_excel_to_sale_note(filename: str) -> SaleNote:
    """
    Lee un archivo Excel y convierte los datos a una instancia de SaleNote
    con toda la jerarquía de datos estructurada.
    
    Args:
        filename: Nombre del archivo Excel (ej: "nv_data_ejemplo.xlsx")
        
    Returns:
        SaleNote: Objeto estructurado con toda la jerarquía de datos
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato del Excel no es válido
    """
    # Construir la ruta completa del archivo
    file_path = os.path.join(OUTPUT_DIR_ETAPA_1_SALIDA, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    
    try:
        # Detectar los nombres de las hojas (pueden estar en español o inglés)
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        
        materials_sheet = None
        joints_sheet = None
        
        # Buscar la hoja de materiales
        for sheet in sheet_names:
            if isinstance(sheet, str) and sheet.lower() in ['materials', 'materiales']:
                materials_sheet = sheet
            elif isinstance(sheet, str) and sheet.lower() in ['joints', 'uniones']:
                joints_sheet = sheet
        
        if not materials_sheet:
            raise ValueError("No se encontró hoja de materiales (buscar: 'Materials' o 'materiales')")
        if not joints_sheet:
            raise ValueError("No se encontró hoja de uniones (buscar: 'Joints' o 'uniones')")
        
        # Leer las hojas del Excel
        df_materials: pd.DataFrame = pd.read_excel(file_path, sheet_name=materials_sheet)  # type: ignore
        df_joints: pd.DataFrame = pd.read_excel(file_path, sheet_name=joints_sheet)  # type: ignore
        
        # Validar que las hojas no estén vacías
        if df_materials.empty:
            raise ValueError(f"La hoja '{materials_sheet}' está vacía")
        if df_joints.empty:
            raise ValueError(f"La hoja '{joints_sheet}' está vacía")
            
        # Obtener el número de NV (asumiendo que todas las filas tienen el mismo NV)
        nv = str(df_materials['nv'].iloc[0])  # type: ignore
        
        # Agrupar por plano para crear la estructura jerárquica
        plans = _create_plans_from_dataframes(df_materials, df_joints)
        
        # Crear y retornar el objeto SaleNote
        return SaleNote(nv=nv, plans=plans)
        
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo Excel: {str(e)}")


def _create_plans_from_dataframes(df_materials: pd.DataFrame, df_joints: pd.DataFrame) -> List[Plan]:
    """
    Crea una lista de Plans a partir de los DataFrames de materiales y uniones.
    
    Args:
        df_materials: DataFrame con los datos de materiales
        df_joints: DataFrame con los datos de uniones
        
    Returns:
        List[Plan]: Lista de planes estructurados
    """
    plans: List[Plan] = []
    
    # Obtener todos los planos únicos
    unique_plans = df_materials['plano'].unique()  # type: ignore
    
    for plan_name in unique_plans:
        # Filtrar datos por plano
        plan_materials = df_materials[df_materials['plano'] == plan_name]  # type: ignore
        plan_joints = df_joints[df_joints['plano'] == plan_name]  # type: ignore
        
        # Obtener todos los spools únicos para este plano
        unique_spools = plan_materials['spool'].unique()  # type: ignore
        
        # Para cada spool en este plano, crear un Plan separado
        # (basado en la estructura del modelo que sugiere un Plan por Spool)
        for spool_name in unique_spools:
            spool_materials = plan_materials[plan_materials['spool'] == spool_name]  # type: ignore
            spool_joints = plan_joints[plan_joints['spool'] == spool_name]  # type: ignore
            
            # Crear el objeto Spool
            spool = _create_spool_from_dataframes(str(spool_name), spool_materials, spool_joints)
            
            # Crear el Plan
            plan = Plan(plano=str(plan_name), spool_data=spool)
            plans.append(plan)
    
    return plans


def _create_spool_from_dataframes(spool_name: str, df_materials: pd.DataFrame, df_joints: pd.DataFrame) -> Spool:
    """
    Crea un objeto Spool a partir de los DataFrames filtrados de materiales y uniones.
    
    Args:
        spool_name: Nombre del spool
        df_materials: DataFrame con los materiales del spool
        df_joints: DataFrame con las uniones del spool
        
    Returns:
        Spool: Objeto spool estructurado
    """
    # Crear lista de materiales
    materials: List[Material] = []
    for _, row in df_materials.iterrows():  # type: ignore
        material = Material(
            mat_numero_interno=str(row['mat_numero_interno']),  # type: ignore
            mat_descripcion=str(row['mat_descripcion']),  # type: ignore
            mat_dn=str(row['mat_dn']),  # type: ignore
            mat_sch=str(row['mat_sch']),  # type: ignore
            mat_qty=int(row['mat_qty'])  # type: ignore
        )
        materials.append(material)
    
    # Crear lista de uniones
    joints: List[Joint] = []
    for _, row in df_joints.iterrows():  # type: ignore
        joint = Joint(
            union_numero=str(row['union_numero']),  # type: ignore
            union_dn=str(row['union_dn']),  # type: ignore
            union_tipo=str(row['union_tipo']),  # type: ignore
            # Estos campos son opcionales y pueden no estar en el Excel
            armador=str(row.get('armador', '')) if pd.notna(row.get('armador')) else None,  # type: ignore
            soldador_raiz=str(row.get('soldador_raiz', '')) if pd.notna(row.get('soldador_raiz')) else None,  # type: ignore
            soldador_remate=str(row.get('soldador_remate', '')) if pd.notna(row.get('soldador_remate')) else None  # type: ignore
        )
        joints.append(joint)
    
    return Spool(spool=spool_name, materials=materials, joints=joints)


def get_available_excel_files() -> List[str]:
    """
    Obtiene una lista de todos los archivos Excel disponibles en el directorio de etapa 1.
    
    Returns:
        List[str]: Lista de nombres de archivos Excel
    """
    if not os.path.exists(OUTPUT_DIR_ETAPA_1_SALIDA):
        return []
    
    excel_files: List[str] = []
    for file in os.listdir(OUTPUT_DIR_ETAPA_1_SALIDA):
        if file.endswith(('.xlsx', '.xls')):
            excel_files.append(file)
    
    return excel_files


def validate_excel_structure(filename: str) -> Dict[str, Any]:
    """
    Valida que un archivo Excel tenga la estructura esperada.
    
    Args:
        filename: Nombre del archivo Excel a validar
        
    Returns:
        Dict[str, Any]: Diccionario con información de validación
    """
    file_path = os.path.join(OUTPUT_DIR_ETAPA_1_SALIDA, filename)
    
    validation_result: Dict[str, Any] = {
        "valid": False,
        "errors": [],
        "warnings": [],
        "info": {}
    }
    
    if not os.path.exists(file_path):
        validation_result["errors"].append(f"Archivo no encontrado: {filename}")
        return validation_result
    
    try:
        # Verificar que existan las hojas requeridas
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        
        # Buscar las hojas de materiales y uniones (pueden estar en español o inglés)
        materials_sheet = None
        joints_sheet = None
        
        for sheet in sheet_names:
            if isinstance(sheet, str) and sheet.lower() in ['materials', 'materiales']:
                materials_sheet = sheet
            elif isinstance(sheet, str) and sheet.lower() in ['joints', 'uniones']:
                joints_sheet = sheet
        
        if not materials_sheet:
            validation_result["errors"].append("No se encontró hoja de materiales (buscar: 'Materials' o 'materiales')")
            return validation_result
        
        if not joints_sheet:
            validation_result["errors"].append("No se encontró hoja de uniones (buscar: 'Joints' o 'uniones')")
            return validation_result
        
        # Leer las hojas
        df_materials: pd.DataFrame = pd.read_excel(file_path, sheet_name=materials_sheet)  # type: ignore
        df_joints: pd.DataFrame = pd.read_excel(file_path, sheet_name=joints_sheet)  # type: ignore
        
        # Verificar columnas requeridas
        required_material_columns = ['nv', 'plano', 'spool', 'mat_numero_interno', 'mat_descripcion', 'mat_dn', 'mat_sch', 'mat_qty']
        required_joint_columns = ['nv', 'plano', 'spool', 'union_numero', 'union_dn', 'union_tipo']
        
        missing_material_columns = [col for col in required_material_columns if col not in df_materials.columns]
        missing_joint_columns = [col for col in required_joint_columns if col not in df_joints.columns]
        
        if missing_material_columns:
            validation_result["errors"].append(f"Columnas faltantes en Materials: {missing_material_columns}")
        
        if missing_joint_columns:
            validation_result["errors"].append(f"Columnas faltantes en Joints: {missing_joint_columns}")
        
        if validation_result["errors"]:
            return validation_result
        
        # Información adicional
        validation_result["info"] = {
            "total_materials": len(df_materials),
            "total_joints": len(df_joints),
            "unique_nvs": df_materials['nv'].nunique(),  # type: ignore
            "unique_plans": df_materials['plano'].nunique(),  # type: ignore
            "unique_spools": df_materials['spool'].nunique()  # type: ignore
        }
        
        # Advertencias
        if df_materials['nv'].nunique() > 1:  # type: ignore
            validation_result["warnings"].append("Se encontraron múltiples NVs en el archivo")
        
        validation_result["valid"] = True
        
    except Exception as e:
        validation_result["errors"].append(f"Error al validar el archivo: {str(e)}")
    
    return validation_result
