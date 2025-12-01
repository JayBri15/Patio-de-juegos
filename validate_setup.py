#!/usr/bin/env python3
"""
Script de validación del proyecto de automatización
Verifica que todas las dependencias y configuraciones están correctas
"""

import sys
import os

def check_python_version():
    """Verifica versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (Requiere 3.7+)")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    dependencies = {
        'selenium': 'Selenium',
        'pytest': 'pytest',
        'pytest_html': 'pytest-html',
        'webdriver_manager': 'webdriver-manager'
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} instalado")
        except ImportError:
            print(f"✗ {name} NO instalado")
            all_ok = False
    
    return all_ok

def check_directory_structure():
    """Verifica que la estructura de directorios sea correcta"""
    required_dirs = [
        'tests/automation/config',
        'tests/automation/pages',
        'tests/automation/test_cases',
        'tests/automation/utils',
        'reports'
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✓ Directorio {dir_path}/ existe")
        else:
            print(f"✗ Directorio {dir_path}/ NO existe")
            all_ok = False
    
    return all_ok

def check_files():
    """Verifica que los archivos principales existan"""
    required_files = [
        'tests/automation/conftest.py',
        'tests/automation/config/config.py',
        'tests/automation/pages/base_page.py',
        'tests/automation/pages/index_page.py',
        'tests/automation/pages/crear_page.py',
        'tests/automation/pages/lista_page.py',
        'tests/automation/pages/editar_page.py',
        'tests/automation/pages/carrito_page.py',
        'tests/automation/test_cases/test_login.py',
        'tests/automation/test_cases/test_crear.py',
        'tests/automation/test_cases/test_lista.py',
        'tests/automation/test_cases/test_editar.py',
        'tests/automation/test_cases/test_eliminar.py',
        'tests/automation/test_cases/test_carrito.py',
        'pytest.ini',
        'requirements.txt',
        'run_tests.sh'
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"✓ Archivo {file_path} existe")
        else:
            print(f"✗ Archivo {file_path} NO existe")
            all_ok = False
    
    return all_ok

def check_server_connectivity():
    """Verifica si el servidor web está disponible"""
    import urllib.request
    
    try:
        response = urllib.request.urlopen('http://localhost:8000', timeout=2)
        print("✓ Servidor web disponible en http://localhost:8000")
        return True
    except (urllib.error.URLError, TimeoutError):
        print("⚠ Servidor web NO disponible en http://localhost:8000")
        print("  (Inicia con: cd docs && python3 -m http.server 8000)")
        return False

def check_config():
    """Verifica configuración"""
    try:
        from tests.automation.config.config import BASE_URL, ADMIN_USER, ADMIN_PASSWORD
        print(f"✓ Configuración cargada correctamente")
        print(f"  - BASE_URL: {BASE_URL}")
        print(f"  - ADMIN_USER: {ADMIN_USER}")
        return True
    except ImportError as e:
        print(f"✗ Error cargando configuración: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("VALIDACIÓN DEL PROYECTO DE AUTOMATIZACIÓN")
    print("=" * 60)
    print()
    
    checks = [
        ("Python 3.7+", check_python_version),
        ("Dependencias", check_dependencies),
        ("Estructura de directorios", check_directory_structure),
        ("Archivos principales", check_files),
        ("Configuración", check_config),
        ("Servidor web", check_server_connectivity),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n--- {check_name} ---")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"✗ Error en validación: {e}")
            results.append((check_name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    all_ok = True
    for check_name, result in results:
        status = "✓ OK" if result else "✗ FALLO"
        print(f"{status}: {check_name}")
        if not result:
            all_ok = False
    
    print("=" * 60)
    
    if all_ok:
        print("\n✓ TODAS LAS VALIDACIONES PASARON")
        print("\nPuedes ejecutar las pruebas con:")
        print("  ./run_tests.sh")
        print("\nO manualmente:")
        print("  cd tests/automation")
        print("  python3 -m pytest test_cases/ -v --html=../../reports/test_report.html")
        return 0
    else:
        print("\n✗ ALGUNAS VALIDACIONES FALLARON")
        print("\nSoluciona los problemas anteriores antes de ejecutar las pruebas.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
