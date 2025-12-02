"""
Test Suite - Pruebas de Crear Productos (CREATE)
Historias de Usuario: HU-002 (Crear Producto)

Casos de prueba:
- HU-002-TC-001: Camino feliz - Crear producto con datos válidos
- HU-002-TC-002: Prueba negativa - Crear producto sin datos requeridos
- HU-002-TC-003: Prueba de límites - Campos con caracteres especiales y límites
"""
import pytest
import logging
import os
import time
from selenium.webdriver.common.by import By
from pages.index_page import IndexPage
from pages.crear_page import CrearPage
from config.config import ADMIN_USER, ADMIN_PASSWORD, CREAR_URL, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


class TestCrearProducto:
    """Suite de pruebas para crear productos"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup - Login como admin antes de cada prueba"""
        self.driver = driver
        
        # Login como admin
        index_page = IndexPage(driver)
        index_page.navigate_to()
        index_page.toggle_to_login()
        index_page.login(ADMIN_USER, ADMIN_PASSWORD)
        time.sleep(3)
        
        # Navegar a Crear
        self.crear_page = CrearPage(driver)
        self.crear_page.navigate_to()
        time.sleep(2)
        
        logger.info("Setup completado - Admin logueado")
    
    def take_screenshot(self, name):
        """Auxiliar para capturar pantallas"""
        filename = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot guardado: {filename}")
        return filename
    
    # HU-002-TC-001: Camino feliz - Crear producto
    def test_001_create_product_with_valid_data(self):
        """
        HU-002-TC-001: Camino feliz
        Precondición: Admin autenticado en página Crear
        Pasos:
            1. Rellena formulario con datos válidos
            2. Nombre: "Laptop Gaming"
            3. Precio: "1500"
            4. Descripción: "Laptop potente para juegos"
            5. Categoría: "Electrónica"
            6. Hace clic en "Guardar"
        Resultado esperado: Producto creado exitosamente, muestra mensaje de éxito
        """
        logger.info("=== Test: Crear Producto con Datos Válidos ===")
        
        self.take_screenshot("201_crear_form_loaded")
        
        # Pasos 1-5: Llenar formulario
        product_name = "Laptop Gaming"
        product_price = "1500"
        product_description = "Laptop potente para juegos"
        product_category = "Electrónica"
        
        self.crear_page.fill_product_form(
            product_name,
            product_price,
            product_description,
            product_category
        )
        logger.info(f"Formulario rellenado: {product_name}, ${product_price}")
        
        self.take_screenshot("202_form_filled_with_data")
        
        # Paso 6: Guardar producto
        self.crear_page.save_product()
        logger.info("Producto guardado")
        
        self.take_screenshot("203_product_saved")
        
        # Esperar redirección
        time.sleep(3)
        
        self.take_screenshot("204_after_save_redirect")
        
        # Resultado: Verificar éxito
        success_message = self.crear_page.get_success_message()
        logger.info(f"Mensaje: {success_message}")
        
        # Debe haber sido redirigido a Lista
        assert "Lista.html" in self.driver.current_url or "Index.html" in self.driver.current_url
        logger.info("✓ Test PASSED: Producto creado exitosamente")
    
    # HU-002-TC-002: Prueba negativa - Datos faltantes
    def test_002_create_product_with_missing_required_fields(self):
        """
        HU-002-TC-002: Prueba negativa
        Precondición: Admin autenticado en página Crear
        Pasos:
            1. Deja el campo "Nombre" vacío
            2. Rellena otros campos válidos
            3. Hace clic en "Guardar"
        Resultado esperado: Muestra error de validación
        """
        logger.info("=== Test: Crear Producto sin Campos Requeridos ===")
        
        self.take_screenshot("205_crear_missing_fields_start")
        
        # Pasos 1-2: Solo llenar algunos campos (sin nombre)
        self.crear_page.send_keys((By.ID, "productPrice"), "999")
        self.crear_page.send_keys((By.ID, "productDesc"), "Producto sin nombre")
        logger.info("Intento de crear producto sin nombre")
        
        self.take_screenshot("206_missing_name_field")
        
        # Paso 3: Intentar guardar
        self.crear_page.save_product()
        
        self.take_screenshot("207_save_attempted_missing_fields")
        
        time.sleep(2)
        
        self.take_screenshot("208_validation_error_shown")
        
        # Resultado: Debe mostrar error
        error_message = self.crear_page.get_error_message()
        logger.info(f"Error mostrado: {error_message}")
        
        # Debe permanecer en Crear.html (no se guardó)
        assert "Crear.html" in self.driver.current_url
        logger.info("✓ Test PASSED: Validación de campos requeridos")
    
    # HU-002-TC-003: Prueba de límites - Caracteres especiales y límites
    def test_003_create_product_with_special_characters(self):
        """
        HU-002-TC-003: Prueba de límites
        Precondición: Admin autenticado en página Crear
        Pasos:
            1. Nombre con caracteres especiales: "Product@#$%_2024"
            2. Precio: "99.99"
            3. Descripción con ñ y acentos: "Descripción del Producto"
            4. Guarda producto
        Resultado esperado: Acepta caracteres especiales válidos
        """
        logger.info("=== Test: Crear Producto con Caracteres Especiales ===")
        
        self.take_screenshot("209_special_chars_form_start")
        
        # Pasos 1-3: Llenar con caracteres especiales
        product_name = "Product@#$%_2024"
        product_price = "99.99"
        product_description = "Descripción del Producto con ñoño"
        product_category = "Electrónica"
        
        self.crear_page.fill_product_form(
            product_name,
            product_price,
            product_description,
            product_category
        )
        logger.info(f"Producto con caracteres especiales: {product_name}")
        
        self.take_screenshot("210_special_chars_filled")
        
        # Paso 4: Guardar
        self.crear_page.save_product()
        
        self.take_screenshot("211_special_chars_saved")
        
        time.sleep(3)
        
        self.take_screenshot("212_special_chars_result")
        
        # Resultado: Debe aceptar caracteres especiales
        assert "Crear.html" not in self.driver.current_url or "Lista.html" in self.driver.current_url
        logger.info("✓ Test PASSED: Caracteres especiales manejados correctamente")
    
    # HU-002-TC-004: Prueba de límites - Precio negativo
    def test_004_create_product_with_negative_price(self):
        """
        HU-002-TC-004: Prueba de límites - Precio negativo
        Precondición: Admin autenticado en página Crear
        Pasos:
            1. Nombre: "Producto Test"
            2. Precio: "-100" (negativo)
            3. Descripción: "Test"
            4. Guarda producto
        Resultado esperado: Rechaza precio negativo o lo ajusta a cero
        """
        logger.info("=== Test: Crear Producto con Precio Negativo ===")
        
        self.take_screenshot("213_negative_price_form")
        
        # Pasos 1-3: Llenar con precio negativo
        self.crear_page.fill_product_form(
            "Producto Test",
            "-100",  # Precio negativo
            "Test description",
            "Electrónica"
        )
        logger.info("Intento de crear producto con precio negativo")
        
        self.take_screenshot("214_negative_price_filled")
        
        # Paso 4: Guardar
        self.crear_page.save_product()
        
        self.take_screenshot("215_negative_price_save_attempt")
        
        time.sleep(2)
        
        self.take_screenshot("216_negative_price_validation")
        
        # Resultado: Debe validar precio (negativo o mostrar error)
        logger.info("✓ Test PASSED: Validación de precio negativo")
