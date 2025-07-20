"""
Servicio para exportar objetos SaleNote a archivos Excel
Mantiene la estructura original pero incluye las nuevas variables.
"""

import pandas as pd
import io
from backend.app.api.v1.schemas.nv_schemas import SaleNote
from backend.app.core.logger import setup_logger

logger = setup_logger()

def sale_note_to_excel(sale_note: SaleNote) -> io.BytesIO:
    """
    Convierte un objeto SaleNote a un archivo Excel con las hojas Materials y Joints.
    Incluye tanto las columnas originales como las nuevas variables editables.
    
    Args:
        sale_note: Objeto SaleNote con todos los datos
        
    Returns:
        io.BytesIO: Archivo Excel en memoria listo para descarga
    """
    # Extraer materiales y juntas con las nuevas variables
    materials = []
    joints = []
    
    for plan in sale_note.plans:
        spool = plan.spool_data
        
        # Procesar materiales
        for mat in spool.materials:
            materials.append({
                "nv": sale_note.nv,
                "plano": plan.plano,
                "spool": spool.spool,
                "mat_descripcion": mat.mat_descripcion,
                "mat_dn": mat.mat_dn,
                "mat_sch": mat.mat_sch,
                "mat_qty": mat.mat_qty,
                "mat_numero_interno": mat.mat_numero_interno or "",
            })
        
        # Procesar uniones
        for joint in spool.joints:
            joints.append({
                "nv": sale_note.nv,
                "plano": plan.plano,
                "spool": spool.spool,
                "union_numero": joint.union_numero,
                "union_dn": joint.union_dn,
                "union_tipo": joint.union_tipo,
                "union_armador": joint.union_armador or "",
                "union_soldador_raiz": joint.union_soldador_raiz or "",
                "union_soldador_remate": joint.union_soldador_remate or "",
            })

    # Crear DataFrames con el orden de columnas correcto
    df_materials = pd.DataFrame(materials, columns=[
        "nv", "plano", "spool", "mat_descripcion", "mat_dn", "mat_sch", "mat_qty", "mat_numero_interno"
    ])
    
    df_joints = pd.DataFrame(joints, columns=[
        "nv", "plano", "spool", "union_numero", "union_dn", "union_tipo", 
        "union_armador", "union_soldador_raiz", "union_soldador_remate"
    ])

    # Crear archivo Excel en memoria
    output = io.BytesIO()
    
    try:
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            # Escribir hojas con nombres en español (como el formato original)
            df_materials.to_excel(writer, sheet_name="materiales", index=False)
            df_joints.to_excel(writer, sheet_name="uniones", index=False)
            
            # Obtener el workbook y las hojas para aplicar formato (opcional)
            workbook = writer.book
            materials_worksheet = writer.sheets["materiales"]
            joints_worksheet = writer.sheets["uniones"]
            
            # Aplicar autofit a las columnas (opcional)
            for worksheet in [materials_worksheet, joints_worksheet]:
                worksheet.autofit()
        
        output.seek(0)
        logger.info(f"Excel generado exitosamente para NV {sale_note.nv}")
        return output
        
    except Exception as e:
        logger.error(f"Error al generar Excel: {str(e)}")
        raise


def generate_excel_filename(sale_note: SaleNote, include_timestamp: bool = False) -> str:
    """
    Genera un nombre de archivo apropiado para el Excel exportado.
    
    Args:
        sale_note: Objeto SaleNote
        include_timestamp: Si incluir timestamp en el nombre
        
    Returns:
        str: Nombre del archivo
    """
    base_name = f"nv_{sale_note.nv}_actualizado"
    
    if include_timestamp:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.xlsx"
    
    return f"{base_name}.xlsx"
