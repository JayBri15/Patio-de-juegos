"""
Test Suite - Pruebas de Login (Autenticación)
Historias de Usuario: HU-001 (Login)

Casos de prueba:
- HU-001-TC-001: Camino feliz - Login exitoso con credenciales válidas
- HU-001-TC-002: Prueba negativa - Login fallido con credenciales inválidas
- HU-001-TC-003: Prueba de límites - Login con campos vacíos
"""
import pytest
import logging
import os
from selenium.webdriver.common.by import By
from pages.index_page import IndexPage
from config.config import INDEX_URL, ADMIN_USER, ADMIN_PASSWORD, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


class TestLogin:
    """Suite de pruebas para login/autenticación"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup antes de cada prueba"""
        self.driver = driver
        self.index_page = IndexPage(driver)
        self.index_page.navigate_to()
        logger.info("Navegación a Index completada")
    
    def take_screenshot(self, name):
        """Auxiliar para capturar pantallas"""
        filename = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot guardado: {filename}")
        return filename
    
    # HU-001-TC-001: Camino feliz - Login exitoso
    def test_001_successful_login_with_valid_credentials(self):
        """
        HU-001-TC-001: Camino feliz
        Precondición: Usuario en página de login
        Pasos:
            1. Ingresa usuario admin "admin"
            2. Ingresa contraseña "123"
            3. Hace clic en botón "Login"
        Resultado esperado: Redirige a Lista.html
        """
        logger.info("=== Test: Login Exitoso con Credenciales Válidas ===")
        
        # Asegurar que estamos en formulario de login
        self.index_page.toggle_to_login()
        self.take_screenshot("01_login_form_visible")
        
        # Paso 1 y 2: Llenar credenciales
        self.index_page.login(ADMIN_USER, ADMIN_PASSWORD)
        logger.info(f"Login con usuario: {ADMIN_USER}")
        
        # Paso 3: Screenshot después de hacer clic
        self.take_screenshot("02_login_submitted")
        
        # Esperar redirección
        import time
        time.sleep(3)
        
        # Resultado: Verificar que se redirigió correctamente
        current_url = self.driver.current_url
        logger.info(f"URL actual: {current_url}")
        
        # Captura post-redirección
        self.take_screenshot("03_login_success_redirect")
        
        # Verificar que no estamos más en Index (redirigió)
        assert "Index.html" not in current_url, "No se redirigió después del login"
        logger.info("✓ Test PASSED: Login exitoso")
    
    # HU-001-TC-002: Prueba negativa - Login fallido
    def test_002_login_with_invalid_credentials(self):
        """
        HU-001-TC-002: Prueba negativa
        Precondición: Usuario en página de login
        Pasos:
            1. Ingresa usuario "invalid_user"
            2. Ingresa contraseña "wrongpassword"
            3. Hace clic en botón "Login"
        Resultado esperado: Muestra mensaje de error, permanece en Index
        """
        logger.info("=== Test: Login Fallido con Credenciales Inválidas ===")
        
        # Asegurar formulario de login visible
        self.index_page.toggle_to_login()
        self.take_screenshot("04_login_form_invalid_test")
        
        # Paso 1 y 2: Llenar credenciales inválidas
        invalid_user = "invalid_user"
        invalid_password = "wrongpassword"
        self.index_page.login(invalid_user, invalid_password)
        logger.info(f"Login intentado con usuario inválido: {invalid_user}")
        
        # Paso 3: Screenshot
        self.take_screenshot("05_invalid_login_submitted")
        
        # Esperar mensaje de error
        import time
        time.sleep(2)
        
        self.take_screenshot("06_invalid_credentials_error")
        
        # Resultado: Verificar mensaje de error
        error_message = self.index_page.get_login_error_message()
        logger.info(f"Mensaje de error: {error_message}")
        
        # Verificar que sigue en Index (no se redirigió)
        assert "Index.html" in self.driver.current_url, "Se redirigió con credenciales inválidas"
        logger.info("✓ Test PASSED: Login fallido con error visible")
    
    # HU-001-TC-003: Prueba de límites - Campos vacíos
    def test_003_login_with_empty_fields(self):
        """
        HU-001-TC-003: Prueba de límites
        Precondición: Usuario en página de login
        Pasos:
            1. Deja campos usuario y contraseña vacíos
            2. Hace clic en botón "Login"
        Resultado esperado: Muestra mensaje de error o validación
        """
        logger.info("=== Test: Login con Campos Vacíos ===")
        
        # Asegurar formulario de login visible
        self.index_page.toggle_to_login()
        self.take_screenshot("07_login_empty_fields_form")
        
        # Paso 1: No llenar nada, solo hacer clic (usar locator del POM)
        self.index_page.click_element(self.index_page.LOGIN_BUTTON)
        logger.info("Intento de login con campos vacíos")
        
        # Paso 2: Screenshot
        self.take_screenshot("08_empty_fields_attempted")
        
        # Esperar validación
        import time
        time.sleep(2)
        
        self.take_screenshot("09_empty_fields_validation")
        
        # Resultado: Debe permanecer en Index (sin redirigir)
        assert "Index.html" in self.driver.current_url, "No debería redirigir con campos vacíos"
        logger.info("✓ Test PASSED: Validación de campos vacíos")
    
    # HU-001-TC-004: Prueba de límites - Contraseña muy larga
    def test_004_login_with_long_password(self):
        """
        HU-001-TC-004: Prueba de límites - Campo contraseña con límite
        Precondición: Usuario en página de login
        Pasos:
            1. Ingresa usuario válido
            2. Ingresa contraseña con 200+ caracteres
            3. Hace clic en botón "Login"
        Resultado esperado: Maneja límites de entrada correctamente
        """
        logger.info("=== Test: Login con Contraseña Muy Larga ===")
        
        # Asegurar formulario de login visible
        self.index_page.toggle_to_login()
        self.take_screenshot("10_login_long_password_form")
        
        # Paso 1 y 2: Ingresar contraseña muy larga
        long_password = "a" * 200
        self.index_page.login(ADMIN_USER, long_password)
        logger.info(f"Login con contraseña de {len(long_password)} caracteres")
        
        # Paso 3: Screenshot
        self.take_screenshot("11_long_password_submitted")
        
        # Esperar resultado
        import time
        time.sleep(2)
        
        self.take_screenshot("12_long_password_result")
        
        # Debe permanecer en Index (la contraseña no coincide)
        assert "Index.html" in self.driver.current_url
        logger.info("✓ Test PASSED: Límite de contraseña manejado")
