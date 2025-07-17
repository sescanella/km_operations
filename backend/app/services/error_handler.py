# backend/app/services/error_handler.py

from typing import Dict

def format_error(e: Exception) -> Dict[str, str]:
    """
    Devuelve un diccionario con el detalle de un error.
    """
    return {
        "status": "error",
        "message": str(e)
    }
