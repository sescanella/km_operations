# test_excel_reader.py - Script de prueba para el servicio excel_reader

import sys
import os

# Agregar el directorio backend al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.etapa_2.excel_reader import (
    read_excel_to_sale_note,
    get_available_excel_files,
    validate_excel_structure
)


def test_excel_reader():
    """Función de prueba para el servicio excel_reader"""
    
    print("=== Prueba del servicio Excel Reader ===\n")
    
    # 1. Listar archivos disponibles
    print("1. Archivos Excel disponibles:")
    available_files = get_available_excel_files()
    print(f"Archivos encontrados: {available_files}")
    print()
    
    if not available_files:
        print("No se encontraron archivos Excel para probar.")
        return
    
    # 2. Usar el primer archivo disponible para las pruebas
    test_file = available_files[0]
    print(f"2. Probando con archivo: {test_file}")
    print()
    
    # 3. Validar estructura del archivo
    print("3. Validando estructura del archivo:")
    validation = validate_excel_structure(test_file)
    print(f"Válido: {validation['valid']}")
    if validation['errors']:
        print(f"Errores: {validation['errors']}")
    if validation['warnings']:
        print(f"Advertencias: {validation['warnings']}")
    if validation['info']:
        print(f"Información: {validation['info']}")
    print()
    
    if not validation['valid']:
        print("El archivo no tiene una estructura válida. Cancelando prueba.")
        return
    
    # 4. Leer el archivo y convertir a SaleNote
    print("4. Leyendo archivo y convirtiendo a SaleNote:")
    try:
        sale_note = read_excel_to_sale_note(test_file)
        print(f"NV: {sale_note.nv}")
        print(f"Número de planes: {len(sale_note.plans)}")
        
        for i, plan in enumerate(sale_note.plans):
            print(f"  Plan {i+1}: {plan.plano}")
            print(f"    Spool: {plan.spool_data.spool}")
            print(f"    Materiales: {len(plan.spool_data.materials)}")
            print(f"    Uniones: {len(plan.spool_data.joints)}")
            
            if plan.spool_data.materials:
                print(f"    Primer material: {plan.spool_data.materials[0].mat_descripcion}")
            if plan.spool_data.joints:
                print(f"    Primera unión: Tipo {plan.spool_data.joints[0].union_tipo}, DN {plan.spool_data.joints[0].union_dn}")
            print()
        
        print("✅ Prueba completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al leer el archivo: {str(e)}")


if __name__ == "__main__":
    test_excel_reader()
