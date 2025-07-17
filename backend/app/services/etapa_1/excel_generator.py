import pandas as pd
import os

def generate_empty_excel(output_dir: str, filename: str = "nv_data_empty.xlsx") -> str:
    """
    Genera un archivo Excel vacío con las hojas y columnas definidas,
    pero sin datos (solo los headers).
    """

    # Definir columnas de cada hoja
    materials_columns = [
        "nv",
        "plano",
        "spool",
        "mat_numero_interno",
        "mat_descripcion",
        "mat_dn",
        "mat_sch",
        "mat_qty"
    ]

    joints_columns = [
        "nv",
        "plano",
        "spool",
        "union_numero",
        "union_dn",
        "union_tipo",
        "armador",
        "soldador_raiz",
        "soldador_remate"
    ]

    # Crear DataFrames vacíos
    df_materials = pd.DataFrame(columns=materials_columns)
    df_joints = pd.DataFrame(columns=joints_columns)

    # Crear carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    path_excel = os.path.join(output_dir, filename)

    # Guardar Excel multi-hoja
    with pd.ExcelWriter(path_excel) as writer:
        df_materials.to_excel(writer, sheet_name="materiales", index=False)  # type: ignore
        df_joints.to_excel(writer, sheet_name="uniones", index=False)  # type: ignore

    return path_excel
