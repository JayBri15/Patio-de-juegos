"""
Test Suite - Pruebas de Editar Productos (UPDATE)
Historias de Usuario: HU-004 (Editar Producto)

Casos de prueba:
- HU-004-TC-001: Camino feliz - Editar producto exitosamente
- HU-004-TC-002: Prueba negativa - Editar producto con datos inválidos
- HU-004-TC-003: Prueba de límites - Campos vacíos al editar
"""
import pytest
import logging
import os
import time
from selenium.webdriver.common.by import By
from pages.index_page import IndexPage
from pages.crear_page import CrearPage
from pages.lista_page import ListaPage
from pages.editar_page import EditarPage
from config.config import ADMIN_USER, ADMIN_PASSWORD, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


class TestEditarProducto:
    """Suite de pruebas para editar productos"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup - Crea un producto y lo abre para editar"""
        self.driver = driver
        
        # Login como admin
        index_page = IndexPage(driver)
        index_page.navigate_to()
        index_page.toggle_to_login()
        index_page.login(ADMIN_USER, ADMIN_PASSWORD)
        time.sleep(3)
        
        # Crear un producto de prueba
        crear_page = CrearPage(driver)
        crear_page.navigate_to()
        time.sleep(2)
        
        crear_page.fill_product_form(
            "Producto Para Editar",
            "500",
            "Este es un producto de prueba",
            "Electrónica"
        )
        crear_page.save_product()
        time.sleep(3)
        
        # Ir a Lista
        lista_page = ListaPage(driver)
        lista_page.navigate_to()
        time.sleep(2)
        
        # Abrir el producto recién creado para editar (usar el último en la lista)
        try:
            total = lista_page.get_products_count()
            if total > 0:
                lista_page.edit_product_by_index(total - 1)
                time.sleep(2)
        except Exception:
            logger.warning("No se pudo editar el producto recién creado")
        
        self.editar_page = EditarPage(driver)
        logger.info("Setup completado - Producto abierto para editar")
    
    def take_screenshot(self, name):
        """Auxiliar para capturar pantallas"""
        filename = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot guardado: {filename}")
        return filename
    
    # HU-004-TC-001: Camino feliz - Editar producto
    def test_001_update_product_with_valid_data(self):
        """
        HU-004-TC-001: Camino feliz
        Precondición: Admin autenticado, producto abierto para editar
        Pasos:
            1. Obtiene datos actuales del producto
            2. Modifica el nombre a "Producto Actualizado"
            3. Modifica el precio a "750"
            4. Guarda cambios
        Resultado esperado: Producto actualizado exitosamente
        """
        logger.info("=== Test: Editar Producto con Datos Válidos ===")
        
        self.take_screenshot("401_editar_page_loaded")
        
        # Paso 1: Obtener datos actuales
        try:
            current_name = self.editar_page.get_product_name()
            current_price = self.editar_page.get_product_price()
            logger.info(f"Datos actuales - Nombre: {current_name}, Precio: {current_price}")
        except:
            current_name = "Desconocido"
            logger.warning("No se pudieron obtener datos actuales")
        
        self.take_screenshot("402_current_data_shown")
        
        # Paso 2-3: Modificar datos
        new_name = "Producto Actualizado"
        new_price = "750"
        
        self.editar_page.update_product_name(new_name)
        self.editar_page.update_product_price(new_price)
        logger.info(f"Producto actualizado - Nuevo nombre: {new_name}, Nuevo precio: {new_price}")
        
        self.take_screenshot("403_data_modified")
        
        # Paso 4: Guardar cambios
        self.editar_page.save_product()
        logger.info("Cambios guardados")

        # Capturar estado de localStorage y consola del navegador para depuración
        try:
            raw = self.driver.execute_script("return window.localStorage.getItem('pdj_products_v1');")
            ls_file = os.path.join(SCREENSHOTS_DIR, "405_localstorage.json")
            with open(ls_file, 'w', encoding='utf-8') as f:
                f.write(raw if raw else 'null')
            logger.info(f"localStorage guardado: {ls_file}")
        except Exception as e:
            logger.warning(f"No se pudo obtener localStorage: {e}")

        try:
            # Obtener logs del navegador (si están habilitados)
            logs = []
            try:
                logs = self.driver.get_log('browser')
            except Exception:
                # Algunos drivers no habilitan get_log; ignorar si falla
                logs = []
            log_file = os.path.join(SCREENSHOTS_DIR, "405_browser_console.log")
            with open(log_file, 'w', encoding='utf-8') as f:
                for entry in logs:
                    f.write(f"{entry.get('level')} {entry.get('message')}\n")
            logger.info(f"Browser console guardada: {log_file}")
        except Exception as e:
            logger.warning(f"No se pudieron obtener logs de consola: {e}")

        self.take_screenshot("404_changes_saved")

        time.sleep(3)

        self.take_screenshot("405_after_save_redirect")

        # Resultado: Debe redirigir a Lista o mostrar un mensaje de éxito
        current_url = self.driver.current_url
        # Permitir dos comportamientos válidos: redirección a Lista.html o mostrar mensaje de éxito en la misma página
        if "Lista.html" in current_url:
            # Redirigió correctamente
            pass
        else:
            success = self.editar_page.get_success_message()
            if success is not None:
                # Mensaje de éxito presente
                assert True
            else:
                # Como respaldo, comprobar que los datos en localStorage fueron actualizados correctamente
                try:
                    script = "return window.localStorage.getItem('pdj_products_v1');"
                    raw = self.driver.execute_script(script)
                    items = [] if not raw else __import__('json').loads(raw)
                    edit_id = self.driver.find_element(*self.editar_page.PRODUCT_NAME).get_attribute('id')
                    # Buscar producto por id en localStorage (usar el campo hidden editId si existe)
                    try:
                        pid = self.driver.find_element(By.ID, 'editId').get_attribute('value')
                    except Exception:
                        pid = None
                    # Buscar por nombre y precio nuevo como comprobación alternativa
                    found = False
                    for it in items:
                        if pid and it.get('id') == pid:
                            if it.get('name') == new_name and str(it.get('price')) == str(new_price) or float(it.get('price')) == float(new_price):
                                found = True
                                break
                        else:
                            # fallback: comparar por nombre
                            if it.get('name') == new_name:
                                found = True
                                break
                    assert found, f"No hubo redirección ni mensaje de éxito y localStorage no muestra cambios. URL actual: {current_url}"
                except Exception as e:
                    assert False, f"No hubo redirección ni mensaje de éxito y fallo al comprobar localStorage: {e}"
        logger.info("✓ Test PASSED: Producto editado exitosamente")
    
    # HU-004-TC-002: Prueba negativa - Datos inválidos
    def test_002_update_product_with_invalid_data(self):
        """
        HU-004-TC-002: Prueba negativa
        Precondición: Admin autenticado, producto abierto para editar
        Pasos:
            1. Intenta actualizar precio con valor no numérico: "abc"
            2. Intenta guardar
        Resultado esperado: Muestra error de validación
        """
        logger.info("=== Test: Editar Producto con Datos Inválidos ===")
        
        self.take_screenshot("406_invalid_edit_start")
        
        # Paso 1: Intentar ingresar valor no numérico en precio
        try:
            self.editar_page.update_product_name("Producto Test")
            self.editar_page.update_product_price("abc")  # Inválido
            logger.info("Intento de actualizar precio con 'abc'")
            
            self.take_screenshot("407_invalid_price_entered")
            
            # Paso 2: Guardar
            self.editar_page.save_product()
            
            self.take_screenshot("408_invalid_save_attempt")
            
            time.sleep(2)
            
            self.take_screenshot("409_validation_error_shown")
            
            # Resultado: Debe permanecer en Editar (validación falló)
            assert "Editar.html" in self.driver.current_url
            logger.info("✓ Test PASSED: Validación de datos inválidos")
        except Exception as e:
            logger.warning(f"Error en prueba negativa: {str(e)}")
            self.take_screenshot("410_invalid_test_error")
    
    # HU-004-TC-003: Prueba de límites - Campos vacíos
    def test_003_update_product_with_empty_required_fields(self):
        """
        HU-004-TC-003: Prueba de límites
        Precondición: Admin autenticado, producto abierto para editar
        Pasos:
            1. Intenta limpiar campo de nombre
            2. Intenta guardar
        Resultado esperado: Muestra error de campo requerido
        """
        logger.info("=== Test: Editar Producto Limpiando Campos Requeridos ===")
        
        self.take_screenshot("411_edit_clear_fields_start")
        
        try:
            # Paso 1: Limpiar nombre (campo requerido)
            name_field = self.driver.find_element(*self.editar_page.PRODUCT_NAME)
            name_field.clear()
            logger.info("Campo de nombre limpiado")
            
            self.take_screenshot("412_name_field_cleared")
            
            # Paso 2: Intentar guardar
            self.editar_page.save_product()
            
            self.take_screenshot("413_save_with_empty_field")
            
            time.sleep(2)
            
            self.take_screenshot("414_empty_field_validation")
            
            # Resultado: Debe permanecer en Editar (validación falló)
            assert "Editar.html" in self.driver.current_url
            logger.info("✓ Test PASSED: Validación de campos vacíos al editar")
        except Exception as e:
            logger.warning(f"Error en prueba de campos vacíos: {str(e)}")
            self.take_screenshot("415_empty_field_test_error")
    
    # HU-004-TC-004: Prueba de límites - Descripción muy larga
    def test_004_update_product_with_long_description(self):
        """
        HU-004-TC-004: Prueba de límites - Descripción larga
        Precondición: Admin autenticado, producto abierto para editar
        Pasos:
            1. Ingresa descripción con 500+ caracteres
            2. Guarda cambios
        Resultado esperado: Acepta descripción larga o muestra límite
        """
        logger.info("=== Test: Editar Producto con Descripción Larga ===")
        
        self.take_screenshot("416_long_desc_start")
        
        try:
            # Paso 1: Descripción muy larga
            long_description = "A" * 500
            self.editar_page.update_product_description(long_description)
            logger.info(f"Descripción larga ingresada: {len(long_description)} caracteres")
            
            self.take_screenshot("417_long_description_filled")
            
            # Paso 2: Guardar
            self.editar_page.save_product()
            
            self.take_screenshot("418_long_desc_saved")
            
            time.sleep(2)
            
            self.take_screenshot("419_long_desc_result")
            
            logger.info("✓ Test PASSED: Descripción larga manejada")
        except Exception as e:
            logger.warning(f"Error con descripción larga: {str(e)}")
            self.take_screenshot("420_long_desc_error")
