# backend/app/services/etapa_2/excel_reader.py

import pandas as pd  # type: ignore
import os
from typing import List
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
        df_materials = pd.read_excel(file_path, sheet_name=materials_sheet)  # type: ignore
        df_joints = pd.read_excel(file_path, sheet_name=joints_sheet)  # type: ignore
        
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


def _create_plans_from_dataframes(df_materials, df_joints) -> List[Plan]:  # type: ignore
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
    
    for plan_name in unique_plans:  # type: ignore
        # Filtrar datos por plano
        plan_materials = df_materials[df_materials['plano'] == plan_name]  # type: ignore
        plan_joints = df_joints[df_joints['plano'] == plan_name]  # type: ignore
        
        # Obtener todos los spools únicos para este plano
        unique_spools = plan_materials['spool'].unique()  # type: ignore
        
        # Para cada spool en este plano, crear un Plan separado
        # (basado en la estructura del modelo que sugiere un Plan por Spool)
        for spool_name in unique_spools:  # type: ignore
            spool_name_str = str(spool_name)  # type: ignore
            spool_materials = plan_materials[plan_materials['spool'] == spool_name]  # type: ignore
            spool_joints = plan_joints[plan_joints['spool'] == spool_name]  # type: ignore
            
            # Crear el objeto Spool
            spool = _create_spool_from_dataframes(spool_name_str, spool_materials, spool_joints)  # type: ignore
            
            # Crear el Plan
            plan = Plan(plano=str(plan_name), spool_data=spool)  # type: ignore
            plans.append(plan)
    
    return plans


def _create_spool_from_dataframes(spool_name: str, df_materials, df_joints) -> Spool:  # type: ignore
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
            union_tipo=str(row['union_tipo'])  # type: ignore
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


def validate_excel_structure(filename: str) -> tuple[bool, str]:
    """
    Valida que un archivo Excel tenga la estructura esperada.
    
    Args:
        filename: Nombre del archivo Excel a validar
        
    Returns:
        tuple[bool, str]: (Es válido, Mensaje descriptivo)
    """
    file_path = os.path.join(OUTPUT_DIR_ETAPA_1_SALIDA, filename)
    
    if not os.path.exists(file_path):
        return False, f"Archivo no encontrado: {filename}"
    
    try:
        # Verificar que existan las hojas requeridas
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        
        # Buscar las hojas de materiales y uniones
        materials_sheet = None
        joints_sheet = None
        
        for sheet in sheet_names:
            if isinstance(sheet, str) and sheet.lower() in ['materials', 'materiales']:
                materials_sheet = sheet
            elif isinstance(sheet, str) and sheet.lower() in ['joints', 'uniones']:
                joints_sheet = sheet
        
        if not materials_sheet:
            return False, "No se encontró hoja de materiales (buscar: 'Materials' o 'materiales')"
        
        if not joints_sheet:
            return False, "No se encontró hoja de uniones (buscar: 'Joints' o 'uniones')"
        
        # Leer las hojas
        df_materials = pd.read_excel(file_path, sheet_name=materials_sheet)  # type: ignore
        df_joints = pd.read_excel(file_path, sheet_name=joints_sheet)  # type: ignore
        
        # Verificar columnas requeridas
        required_material_columns = ['nv', 'plano', 'spool', 'mat_descripcion', 'mat_dn', 'mat_sch', 'mat_qty']
        required_joint_columns = ['nv', 'plano', 'spool', 'union_numero', 'union_dn', 'union_tipo']
        
        missing_material_columns = [col for col in required_material_columns if col not in df_materials.columns]
        missing_joint_columns = [col for col in required_joint_columns if col not in df_joints.columns]
        
        if missing_material_columns:
            return False, f"Columnas faltantes en Materials: {missing_material_columns}"
        
        if missing_joint_columns:
            return False, f"Columnas faltantes en Joints: {missing_joint_columns}"
        
        # Todo está bien
        total_materials = len(df_materials)
        total_joints = len(df_joints)
        unique_spools = df_materials['spool'].nunique()  # type: ignore
        
        return True, f"✅ Archivo válido: {total_materials} materiales, {total_joints} uniones, {unique_spools} spools"
        
    except Exception as e:
        return False, f"Error al validar el archivo: {str(e)}"


def get_spools_from_excel(filename: str) -> List[str]:
    """
    Extrae la lista única de spools desde un archivo Excel.
    
    Args:
        filename: Nombre del archivo Excel
        
    Returns:
        List[str]: Lista única de nombres de spools encontrados
    """
    file_path = os.path.join(OUTPUT_DIR_ETAPA_1_SALIDA, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    
    try:
        # Leer hoja de materiales para obtener spools
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        
        materials_sheet = None
        for sheet in sheet_names:
            if isinstance(sheet, str) and sheet.lower() in ['materials', 'materiales']:
                materials_sheet = sheet
                break
        
        if not materials_sheet:
            raise ValueError("No se encontró hoja de materiales")
        
        df_materials = pd.read_excel(file_path, sheet_name=materials_sheet)  # type: ignore
        
        # Obtener spools únicos (ignorar valores nulos)
        unique_spools = df_materials['spool'].dropna().unique()  # type: ignore
        spools_list = [str(spool) for spool in unique_spools]  # type: ignore
        return sorted(spools_list)  # Devolver ordenados
        
    except Exception as e:
        raise ValueError(f"Error al leer spools del archivo Excel: {str(e)}")
