"""
Page Object Model - Clase base para todas las páginas
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import EXPLICIT_WAIT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:
    """Clase base con funcionalidades comunes para todas las páginas"""
    
    def __init__(self, driver, url=None):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def navigate_to(self):
        """Navega a la URL de la página"""
        if self.url:
            logger.info(f"Navegando a: {self.url}")
            self.driver.get(self.url)
    
    def find_element(self, locator):
        """Encuentra un elemento y espera hasta que sea visible"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Elemento encontrado: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Timeout esperando elemento: {locator}")
            raise
    
    def find_elements(self, locator):
        """Encuentra múltiples elementos"""
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.info(f"Elementos encontrados ({len(elements)}): {locator}")
            return elements
        except TimeoutException:
            # Si no se encuentran elementos, devolver lista vacía en lugar de romper la ejecución.
            logger.info(f"No se encontraron elementos para {locator}; devolviendo lista vacía")
            return []
    
    def click_element(self, locator):
        """Hace clic en un elemento después de esperarlo"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            logger.info(f"Haciendo clic en: {locator}")
            element.click()
        except TimeoutException:
            logger.error(f"Timeout haciendo clic en: {locator}")
            raise
    
    def send_keys(self, locator, text):
        """Envía texto a un campo de entrada"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Texto enviado a {locator}: {text}")
        except Exception as e:
            logger.error(f"Error enviando texto a {locator}: {str(e)}")
            raise
    
    def get_text(self, locator):
        """Obtiene el texto de un elemento"""
        try:
            element = self.find_element(locator)
            text = element.text
            logger.info(f"Texto obtenido de {locator}: {text}")
            return text
        except Exception as e:
            logger.error(f"Error obteniendo texto de {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator):
        """Verifica si un elemento está visible"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Elemento visible: {locator}")
            return True
        except TimeoutException:
            logger.info(f"Elemento no visible: {locator}")
            return False
    
    def is_element_present(self, locator):
        """Verifica si un elemento está presente en el DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def switch_to_alert_and_accept(self):
        """Cambia a una alerta y la acepta"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            logger.info("Alerta detectada, aceptando...")
            alert.accept()
        except TimeoutException:
            logger.warning("No se detectó alerta")
    
    def get_current_url(self):
        """Obtiene la URL actual"""
        return self.driver.current_url
