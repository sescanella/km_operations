import os
import json
from backend.app.services.etapa_2.excel_reader import read_excel_to_sale_note
from backend.app.api.v1.schemas.nv_schemas import SaleNote
from backend.app.core.logger import setup_logger

logger = setup_logger()

JSON_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "json_data")
os.makedirs(JSON_DIR, exist_ok=True)

def convert_excel_to_json(filename: str) -> str:
    """Convierte Excel a JSON y lo guarda en data/json_data"""
    try:
        logger.info(f"Procesando Excel: {filename}")
        sale_note = read_excel_to_sale_note(filename)
        json_data = sale_note.model_dump()
        nv = sale_note.nv
        json_path = os.path.join(JSON_DIR, f"nv_{nv}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        logger.info(f"JSON generado: {json_path}")
        return json_path
    except Exception as e:
        logger.error(f"Error al convertir {filename}: {str(e)}")
        raise

def load_json_as_sale_note(nv: int) -> SaleNote:
    """Carga JSON y valida con Pydantic"""
    json_path = os.path.join(JSON_DIR, f"nv_{nv}.json")
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    return SaleNote(**json_data)

def save_sale_note_to_json(sale_note: SaleNote) -> str:
    nv = sale_note.nv
    json_path = os.path.join(JSON_DIR, f"nv_{nv}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sale_note.model_dump(), f, indent=2, ensure_ascii=False)
    logger.info(f"JSON actualizado: {json_path}")
    return json_path
