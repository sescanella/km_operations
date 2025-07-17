# backend/app/services/file_manager.py

import os

def save_text_file(path_txt: str, text: str):
    """
    Guarda un texto en un archivo .txt
    """
    with open(path_txt, "w", encoding="utf-8") as f:
        f.write(text)

def build_output_path(path_pdf: str, output_dir: str) -> str:
    """
    Construye la ruta completa del archivo TXT
    a partir del nombre del PDF.
    """
    filename = os.path.basename(path_pdf).replace(".pdf", ".txt")
    return os.path.join(output_dir, filename)
