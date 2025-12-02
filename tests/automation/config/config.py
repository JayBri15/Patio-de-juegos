"""
Configuración central para pruebas de automatización
"""
import os
from datetime import datetime

# URLs
BASE_URL = "http://localhost:8000/HTML"
INDEX_URL = f"{BASE_URL}/Index.html"
CREAR_URL = f"{BASE_URL}/Crear.html"
LISTA_URL = f"{BASE_URL}/Lista.html"
EDITAR_URL = f"{BASE_URL}/Editar.html"
CARRITO_URL = f"{BASE_URL}/Carrito.html"

# Credenciales
ADMIN_USER = "admin"
ADMIN_PASSWORD = "123"
TEST_USER = "test_user"
TEST_PASSWORD = "password123"

# Timeouts
WAIT_TIMEOUT = 15
EXPLICIT_WAIT = 10

# Rutas para reportes y capturas
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../../reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Crear directorios si no existen
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Información del navegador
BROWSER = "chrome"  # Options: chrome, firefox, edge
HEADLESS = True  # Para debug, cambiar a False
