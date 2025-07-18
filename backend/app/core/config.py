# backend/app/core/config.py

import os

# Carpeta donde están los PDFs de entrada
INPUT_DIR = os.getenv("INPUT_DIR", "data/pdf_entradas/")
PDF_INPUT_DIR = INPUT_DIR  # Alias para compatibilidad

# Carpeta donde se guardan los TXT generados
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data/pdf_salidas/")

# Carpeta para la etapa 1 de salida
OUTPUT_DIR_ETAPA_1_SALIDA = os.getenv("OUTPUT_DIR_ETAPA_1", "data/etapa_1_salida/")
