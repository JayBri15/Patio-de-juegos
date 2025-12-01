"""
Test Suite - Pruebas de Carrito de Compras
Historias de Usuario: HU-006 (Carrito)

Casos de prueba:
- HU-006-TC-001: Camino feliz - Agregar producto al carrito
- HU-006-TC-002: Prueba negativa - Carrito vacío
- HU-006-TC-003: Prueba de límites - Múltiples productos en carrito
"""
import pytest
import logging
import os
import time
from pages.index_page import IndexPage
from pages.lista_page import ListaPage
from pages.carrito_page import CarritoPage
from config.config import SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


class TestCarrito:
    """Suite de pruebas para carrito de compras"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup - Navega a lista de productos"""
        self.driver = driver
        
        # Navegar a Lista
        self.lista_page = ListaPage(driver)
        self.lista_page.navigate_to()
        time.sleep(2)
        
        self.carrito_page = CarritoPage(driver)
        
        logger.info("Setup completado - Página Lista cargada")
    
    def take_screenshot(self, name):
        """Auxiliar para capturar pantallas"""
        filename = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot guardado: {filename}")
        return filename
    
    # HU-006-TC-001: Camino feliz - Agregar al carrito
    def test_001_add_product_to_cart(self):
        """
        HU-006-TC-001: Camino feliz
        Precondición: Usuario en Lista, hay productos disponibles
        Pasos:
            1. Obtiene cantidad inicial de items en carrito
            2. Agrega primer producto al carrito
            3. Navega a Carrito
        Resultado esperado: Producto aparece en carrito
        """
        logger.info("=== Test: Agregar Producto al Carrito ===")
        
        self.take_screenshot("601_lista_for_cart")
        
        # Paso 1: Verificar cantidad de productos
        product_count = self.lista_page.get_products_count()
        logger.info(f"Productos disponibles: {product_count}")
        
        self.take_screenshot("602_products_available")
        
        if product_count > 0:
            # Paso 2: Agregar al carrito
            self.lista_page.add_to_cart_by_index(0)
            logger.info("Producto agregado al carrito")
            
            self.take_screenshot("603_product_added_to_cart")
            
            time.sleep(2)
            
            # Paso 3: Navegar a carrito
            self.carrito_page.navigate_to()
            time.sleep(2)
            
            self.take_screenshot("604_carrito_page_loaded")
            
            # Resultado: Verificar que el producto está en el carrito
            cart_count = self.carrito_page.get_cart_items_count()
            logger.info(f"Items en carrito: {cart_count}")
            
            self.take_screenshot("605_cart_item_verified")
            
            assert cart_count > 0, "Carrito vacío, producto no se agregó"
            logger.info("✓ Test PASSED: Producto agregado al carrito")
        else:
            logger.warning("No hay productos para agregar al carrito")
            self.take_screenshot("606_no_products_for_cart")
    
    # HU-006-TC-002: Prueba negativa - Carrito vacío
    def test_002_empty_cart_scenario(self):
        """
        HU-006-TC-002: Prueba negativa
        Precondición: Usuario en Carrito sin productos agregados
        Pasos:
            1. Navega a Carrito sin agregar productos
            2. Verifica mensaje de carrito vacío
        Resultado esperado: Muestra mensaje apropiado
        """
        logger.info("=== Test: Carrito Vacío ===")
        
        # Limpiar carrito si existe (en sessionStorage)
        self.driver.execute_script("sessionStorage.removeItem('pdj_cart')")
        logger.info("SessionStorage limpiado")
        
        self.take_screenshot("607_clearing_cart")
        
        # Paso 1: Navegar a carrito vacío
        self.carrito_page.navigate_to()
        time.sleep(2)
        
        self.take_screenshot("608_empty_cart_page")
        
        # Paso 2: Verificar mensaje de carrito vacío
        cart_count = self.carrito_page.get_cart_items_count()
        logger.info(f"Items en carrito vacío: {cart_count}")
        
        self.take_screenshot("609_empty_cart_verified")
        
        # Resultado: Carrito debe estar vacío
        assert cart_count == 0, "El carrito no está vacío"
        logger.info("✓ Test PASSED: Carrito vacío manejado correctamente")
    
    # HU-006-TC-003: Prueba de límites - Múltiples productos
    def test_003_add_multiple_products_to_cart(self):
        """
        HU-006-TC-003: Prueba de límites
        Precondición: Usuario en Lista
        Pasos:
            1. Agrega múltiples productos al carrito
            2. Navega a Carrito
            3. Verifica cantidad
        Resultado esperado: Múltiples productos en carrito
        """
        logger.info("=== Test: Agregar Múltiples Productos al Carrito ===")
        
        # Limpiar carrito
        self.driver.execute_script("sessionStorage.removeItem('pdj_cart')")
        
        self.take_screenshot("610_multi_product_start")
        
        # Recargar lista
        self.lista_page.navigate_to()
        time.sleep(2)
        
        product_count = self.lista_page.get_products_count()
        logger.info(f"Productos disponibles: {product_count}")
        
        self.take_screenshot("611_multi_product_list")
        
        # Agregar múltiples productos (máximo 3)
        added_count = 0
        for i in range(min(3, product_count)):
            try:
                self.lista_page.add_to_cart_by_index(i)
                added_count += 1
                logger.info(f"Producto {i+1} agregado al carrito")
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Error agregando producto {i+1}: {str(e)}")
        
        self.take_screenshot(f"612_added_{added_count}_products")
        
        # Navegar a carrito
        self.carrito_page.navigate_to()
        time.sleep(2)
        
        self.take_screenshot("613_multi_cart_page")
        
        # Verificar cantidad en carrito
        cart_count = self.carrito_page.get_cart_items_count()
        logger.info(f"Items en carrito: {cart_count}")
        
        self.take_screenshot("614_multi_cart_verified")
        
        assert cart_count > 0, "No se agregaron productos al carrito"
        logger.info(f"✓ Test PASSED: {cart_count} productos en carrito")
    
    # HU-006-TC-004: Eliminar producto del carrito
    def test_004_remove_product_from_cart(self):
        """
        HU-006-TC-004: Prueba de límites - Remover
        Precondición: Usuario en Carrito con al menos 1 producto
        Pasos:
            1. Verifica cantidad inicial
            2. Elimina primer producto
            3. Verifica cantidad disminuyó
        Resultado esperado: Producto removido
        """
        logger.info("=== Test: Remover Producto del Carrito ===")
        
        # Agregar un producto primero
        self.lista_page.navigate_to()
        time.sleep(2)
        
        product_count = self.lista_page.get_products_count()
        if product_count > 0:
            self.lista_page.add_to_cart_by_index(0)
            time.sleep(2)
        
        self.take_screenshot("615_remove_from_cart_start")
        
        # Navegar a carrito
        self.carrito_page.navigate_to()
        time.sleep(2)
        
        # Paso 1: Cantidad inicial
        initial_count = self.carrito_page.get_cart_items_count()
        logger.info(f"Items iniciales: {initial_count}")
        
        self.take_screenshot("616_cart_before_remove")
        
        if initial_count > 0:
            # Paso 2: Eliminar primer producto
            self.carrito_page.remove_item_by_index(0)
            logger.info("Producto removido del carrito")
            
            self.take_screenshot("617_remove_initiated")
            
            time.sleep(2)
            
            self.take_screenshot("618_after_remove")
            
            # Paso 3: Verificar cantidad
            final_count = self.carrito_page.get_cart_items_count()
            logger.info(f"Items finales: {final_count}")
            
            assert final_count < initial_count or final_count == initial_count - 1
            logger.info("✓ Test PASSED: Producto removido del carrito")
        else:
            logger.warning("Carrito vacío, no se puede remover")
            self.take_screenshot("619_empty_cart_no_remove")
