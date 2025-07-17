# backend/app/api/v1/endpoints/etapa2_routes.py

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.app.services.etapa_2 import (
    read_excel_to_sale_note,
    get_available_excel_files,
    validate_excel_structure
)
from backend.app.api.v1.schemas.nv_schemas import SaleNote
from pydantic import BaseModel


class ExcelFileResponse(BaseModel):
    available_files: List[str]


class ValidationResponse(BaseModel):
    filename: str
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: Dict[str, Any]


class SaleNoteResponse(BaseModel):
    filename: str
    sale_note: SaleNote


router = APIRouter(prefix="/etapa2", tags=["Etapa 2"])


@router.get("/excel-files", response_model=ExcelFileResponse)
def list_available_excel_files():
    """
    Obtiene la lista de archivos Excel disponibles en el directorio de etapa 1.
    """
    try:
        available_files = get_available_excel_files()
        return ExcelFileResponse(available_files=available_files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar archivos: {str(e)}")


@router.get("/validate/{filename}", response_model=ValidationResponse)
def validate_excel_file(filename: str):
    """
    Valida la estructura de un archivo Excel específico.
    
    Args:
        filename: Nombre del archivo Excel a validar (ej: "nv_data_ejemplo.xlsx")
    """
    try:
        validation = validate_excel_structure(filename)
        return ValidationResponse(
            filename=filename,
            valid=validation["valid"],
            errors=validation["errors"],
            warnings=validation["warnings"],
            info=validation["info"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al validar archivo: {str(e)}")


@router.get("/read/{filename}", response_model=SaleNoteResponse)
def read_excel_file(filename: str):
    """
    Lee un archivo Excel y convierte los datos a una estructura SaleNote.
    
    Args:
        filename: Nombre del archivo Excel a leer (ej: "nv_data_ejemplo.xlsx")
    """
    try:
        sale_note = read_excel_to_sale_note(filename)
        return SaleNoteResponse(filename=filename, sale_note=sale_note)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {filename}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/spools/{filename}")
def get_spools_from_excel(filename: str) -> Dict[str, Any]:
    """
    Obtiene una lista simplificada de spools disponibles en un archivo Excel.
    Útil para permitir al usuario seleccionar un spool específico.
    
    Args:
        filename: Nombre del archivo Excel a analizar
    """
    try:
        sale_note = read_excel_to_sale_note(filename)
        
        spools_info: List[Dict[str, Any]] = []
        for plan in sale_note.plans:
            spool_info: Dict[str, Any] = {
                "nv": sale_note.nv,
                "plano": plan.plano,
                "spool": plan.spool_data.spool,
                "total_materials": len(plan.spool_data.materials),
                "total_joints": len(plan.spool_data.joints),
                "materials_summary": [
                    {
                        "descripcion": mat.mat_descripcion,
                        "dn": mat.mat_dn,
                        "qty": mat.mat_qty
                    } for mat in plan.spool_data.materials[:3]  # Solo los primeros 3
                ],
                "joints_summary": [
                    {
                        "numero": joint.union_numero,
                        "tipo": joint.union_tipo,
                        "dn": joint.union_dn
                    } for joint in plan.spool_data.joints[:3]  # Solo los primeros 3
                ]
            }
            spools_info.append(spool_info)
        
        return {
            "filename": filename,
            "nv": sale_note.nv,
            "total_plans": len(sale_note.plans),
            "spools": spools_info
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {filename}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/spool-details/{filename}/{spool_name}")
def get_spool_details(filename: str, spool_name: str) -> Dict[str, Any]:
    """
    Obtiene los detalles completos de un spool específico.
    
    Args:
        filename: Nombre del archivo Excel
        spool_name: Nombre del spool a consultar
    """
    try:
        sale_note = read_excel_to_sale_note(filename)
        
        # Buscar el spool específico
        for plan in sale_note.plans:
            if plan.spool_data.spool == spool_name:
                return {
                    "filename": filename,
                    "nv": sale_note.nv,
                    "plano": plan.plano,
                    "spool_data": plan.spool_data
                }
        
        raise HTTPException(
            status_code=404, 
            detail=f"Spool '{spool_name}' no encontrado en el archivo '{filename}'"
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {filename}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
