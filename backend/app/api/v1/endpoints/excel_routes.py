from fastapi import APIRouter
from backend.app.services.etapa_1.excel_generator import generate_empty_excel
from backend.app.core.config import OUTPUT_DIR_ETAPA_1_SALIDA

router = APIRouter()

@router.post("/generate-empty-excel/")
def generate_excel():
    path_excel = generate_empty_excel(output_dir=OUTPUT_DIR_ETAPA_1_SALIDA)
    return {
        "status": "success",
        "message": "Excel vacío generado correctamente.",
        "file_path": path_excel
    }
