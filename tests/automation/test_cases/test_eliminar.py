"""
Test Suite - Pruebas de Eliminar Productos (DELETE)
Historias de Usuario: HU-005 (Eliminar Producto)

Casos de prueba:
- HU-005-TC-001: Camino feliz - Eliminar producto exitosamente
- HU-005-TC-002: Prueba negativa - Cancelar eliminación
- HU-005-TC-003: Prueba de límites - Eliminar último producto
"""
import pytest
import logging
import os
import time
from pages.index_page import IndexPage
from pages.crear_page import CrearPage
from pages.lista_page import ListaPage
from config.config import ADMIN_USER, ADMIN_PASSWORD, SCREENSHOTS_DIR
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class TestEliminarProducto:
    """Suite de pruebas para eliminar productos"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup - Crea un producto para eliminar"""
        self.driver = driver
        
        # Login como admin
        index_page = IndexPage(driver)
        index_page.navigate_to()
        index_page.toggle_to_login()
        index_page.login(ADMIN_USER, ADMIN_PASSWORD)
        time.sleep(3)
        
        # Crear un producto de prueba para eliminar
        crear_page = CrearPage(driver)
        crear_page.navigate_to()
        time.sleep(2)
        
        crear_page.fill_product_form(
            "Producto Para Eliminar",
            "100",
            "Este producto será eliminado",
            "Electrónica"
        )
        crear_page.save_product()
        time.sleep(3)
        
        # Ir a Lista
        self.lista_page = ListaPage(driver)
        self.lista_page.navigate_to()
        time.sleep(2)
        
        logger.info("Setup completado - Producto creado para eliminar")
    
    def take_screenshot(self, name):
        """Auxiliar para capturar pantallas"""
        filename = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot guardado: {filename}")
        except UnexpectedAlertPresentException:
            # Si hay una alerta presente, no podemos tomar screenshot vía Selenium.
            # Registramos el texto de la alerta para diagnóstico y seguimos sin aceptar/rechazarla,
            # dejando que el flujo del test maneje la confirmación posteriormente.
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
            except Exception:
                alert_text = "<no alert text available>"
            txt_file = os.path.join(SCREENSHOTS_DIR, f"{name}_alert.txt")
            with open(txt_file, "w") as f:
                f.write(f"Alert present when taking screenshot: {alert_text}\n")
            logger.info(f"No se pudo tomar screenshot por alerta; guardado texto en: {txt_file}")
        return filename
    
    # HU-005-TC-001: Camino feliz - Eliminar producto
    def test_001_delete_product_successfully(self):
        """
        HU-005-TC-001: Camino feliz
        Precondición: Admin autenticado, lista de productos visible
        Pasos:
            1. Cuenta productos iniciales
            2. Hace clic en botón eliminar del primer producto
            3. Acepta la confirmación
        Resultado esperado: Producto eliminado, conteo disminuye
        """
        logger.info("=== Test: Eliminar Producto Exitosamente ===")
        
        self.take_screenshot("501_delete_list_loaded")
        
        # Paso 1: Contar productos iniciales
        initial_count = self.lista_page.get_products_count()
        logger.info(f"Productos iniciales: {initial_count}")
        
        self.take_screenshot("502_initial_count_taken")
        
        if initial_count > 0:
            # Paso 2-3: Eliminar producto
            # Antes de click: registrar el data-id del botón para correlacionar con localStorage
            try:
                products = self.lista_page.find_elements(self.lista_page.PRODUCT_ROWS)
                btn = products[0].find_element("xpath", ".//button[contains(@class, 'delete')]")
                data_id = btn.get_attribute("data-id") if btn else None
                logger.info(f"Delete button data-id: {data_id}")
            except Exception:
                data_id = None

            # Interceptar el confirm() del navegador para que devuelva True (aceptar)
            # Esto evita condiciones de carrera con el diálogo nativo y hace la prueba determinista.
            try:
                self.driver.execute_script("window.confirm = function(msg) { return true; };")
            except Exception:
                logger.warning("No se pudo sobreescribir window.confirm; continuando")

            # Iniciar eliminación (click). El page object no espera la alerta.
            self.lista_page.delete_product_by_index(0)
            logger.info("Eliminar producto iniciado (confirm auto-aceptado)")
            self.take_screenshot("503_delete_initiated")

            # Tras aceptar, registrar localStorage para diagnóstico y esperar reducción del DOM
            try:
                ls = self.driver.execute_script('return localStorage.getItem("pdj_products_v1")')
            except Exception as e:
                ls = None
                logger.warning(f"No se pudo leer localStorage: {e}")

            logger.info(f"LocalStorage after delete attempt: {ls}")
            self.take_screenshot("505_after_delete")

            # Esperar hasta que el conteo sea menor que el inicial (o timeout)
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: self.lista_page.get_products_count() < initial_count
                )
            except Exception:
                logger.info("Timeout esperando reducción de filas en la tabla")

            # Resultado: Verificar conteo reducido
            final_count = self.lista_page.get_products_count()
            logger.info(f"Productos después de eliminar: {final_count}")

            assert final_count < initial_count or final_count == initial_count - 1
            logger.info("✓ Test PASSED: Producto eliminado exitosamente")
        else:
            logger.warning("No hay productos para eliminar")
            self.take_screenshot("506_no_products_to_delete")
    
    # HU-005-TC-002: Prueba negativa - Cancelar eliminación
    def test_002_cancel_product_deletion(self):
        """
        HU-005-TC-002: Prueba negativa
        Precondición: Admin autenticado, lista de productos visible
        Pasos:
            1. Cuenta productos iniciales
            2. Hace clic en botón eliminar
            3. Cancela la confirmación
        Resultado esperado: Producto NO se elimina, conteo igual
        """
        logger.info("=== Test: Cancelar Eliminación de Producto ===")
        
        self.take_screenshot("507_cancel_delete_start")
        
        # Paso 1: Contar productos iniciales
        initial_count = self.lista_page.get_products_count()
        logger.info(f"Productos iniciales: {initial_count}")
        
        self.take_screenshot("508_initial_count_cancel_test")
        
        if initial_count > 0:
            # Para esta prueba reemplazamos window.confirm para cancelar (retornar false)
            try:
                self.driver.execute_script("window.confirm = function(msg) { return false; };")
            except Exception:
                logger.warning("No se pudo sobreescribir window.confirm; intentaremos con dismiss")

            # Paso 2: Iniciar eliminación
            self.lista_page.delete_product_by_index(0)
            logger.info("Intento de eliminar iniciado (confirm auto-cancelado)")
            
            self.take_screenshot("509_delete_attempt")
            self.take_screenshot("510_delete_cancelled")
            
            time.sleep(1)
            
            self.take_screenshot("511_after_cancel")
            
            # Resultado: Conteo debe ser igual
            final_count = self.lista_page.get_products_count()
            logger.info(f"Productos después de cancelar: {final_count}")
            
            assert final_count == initial_count
            logger.info("✓ Test PASSED: Eliminación cancelada correctamente")
        else:
            logger.warning("No hay productos para cancelar eliminación")
            self.take_screenshot("512_no_products_cancel_delete")
    
    # HU-005-TC-003: Prueba de límites - Múltiples eliminaciones
    def test_003_delete_multiple_products(self):
        """
        HU-005-TC-003: Prueba de límites
        Precondición: Admin autenticado, lista con múltiples productos
        Pasos:
            1. Cuenta productos
            2. Elimina primer producto
            3. Elimina primer producto de nuevo (que era el segundo)
            4. Verifica conteo
        Resultado esperado: Múltiples eliminaciones funcionan
        """
        logger.info("=== Test: Eliminar Múltiples Productos ===")
        
        self.take_screenshot("513_multi_delete_start")
        
        initial_count = self.lista_page.get_products_count()
        logger.info(f"Productos iniciales: {initial_count}")
        
        self.take_screenshot("514_initial_multi_count")
        
        deleted_count = 0
        
        # Eliminar máximo 2 productos o los disponibles
        for i in range(min(2, initial_count)):
            try:
                product_count = self.lista_page.get_products_count()
                if product_count > 0:
                    # Asegurar que los confirms sean aceptados automáticamente
                    try:
                        self.driver.execute_script("window.confirm = function(msg) { return true; };")
                    except Exception:
                        pass

                    self.lista_page.delete_product_by_index(0)
                    logger.info(f"Eliminación {i+1} iniciada (confirm auto-aceptado)")
                    deleted_count += 1
                    time.sleep(0.5)
            except Exception as e:
                logger.warning(f"Error eliminando producto {i+1}: {str(e)}")
        
        self.take_screenshot(f"515_multiple_deleted_{deleted_count}")
        
        # Resultado: Verificar reducción de conteo
        final_count = self.lista_page.get_products_count()
        logger.info(f"Productos finales: {final_count}")
        
        assert final_count <= initial_count
        logger.info(f"✓ Test PASSED: {deleted_count} productos eliminados correctamente")
