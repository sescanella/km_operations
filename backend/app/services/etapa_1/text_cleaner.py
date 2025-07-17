# backend/app/services/text_cleaner.py

def clean_text(raw_text: str) -> str:
    """
    Limpia el texto extraído del PDF.
    Aquí puedes agregar lógica para quitar saltos, espacios, etc.
    """
    # Por ahora, solo quitamos espacios al principio y final
    return raw_text.strip()
