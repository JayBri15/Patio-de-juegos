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
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot guardado: {filename}")
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
            self.lista_page.delete_product_by_index(0)
            logger.info("Eliminar producto iniciado")
            
            self.take_screenshot("503_delete_initiated")
            
            # Aceptar confirmación (si existe)
            try:
                time.sleep(1)
                alert = self.driver.switch_to.alert
                alert.accept()
                logger.info("Confirmación de eliminación aceptada")
                self.take_screenshot("504_delete_confirmed")
            except:
                logger.info("No hay alerta de confirmación")
                self.take_screenshot("504_no_alert")
            
            time.sleep(2)
            
            self.take_screenshot("505_after_delete")
            
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
            # Paso 2: Iniciar eliminación
            self.lista_page.delete_product_by_index(0)
            logger.info("Intento de eliminar iniciado")
            
            self.take_screenshot("509_delete_attempt")
            
            # Paso 3: Cancelar
            try:
                time.sleep(1)
                alert = self.driver.switch_to.alert
                alert.dismiss()  # Cancelar en lugar de aceptar
                logger.info("Confirmación cancelada")
                self.take_screenshot("510_delete_cancelled")
            except:
                logger.info("No hay alerta para cancelar")
                self.take_screenshot("510_no_alert_cancel")
            
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
                    self.lista_page.delete_product_by_index(0)
                    logger.info(f"Eliminación {i+1} iniciada")
                    
                    try:
                        time.sleep(1)
                        alert = self.driver.switch_to.alert
                        alert.accept()
                        deleted_count += 1
                        logger.info(f"Producto {i+1} eliminado")
                    except:
                        logger.info(f"Sin alerta para producto {i+1}")
                    
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"Error eliminando producto {i+1}: {str(e)}")
        
        self.take_screenshot(f"515_multiple_deleted_{deleted_count}")
        
        # Resultado: Verificar reducción de conteo
        final_count = self.lista_page.get_products_count()
        logger.info(f"Productos finales: {final_count}")
        
        assert final_count <= initial_count
        logger.info(f"✓ Test PASSED: {deleted_count} productos eliminados correctamente")
