"""
Utilidades generales para pruebas
"""
import time
import logging

logger = logging.getLogger(__name__)


def wait_for_element_to_disappear(driver, locator, timeout=10):
    """Espera a que un elemento desaparezca del DOM"""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.invisibility_of_element_located(locator))
    logger.info(f"Elemento desapareció: {locator}")


def verify_page_title(driver, expected_title):
    """Verifica el título de la página"""
    current_title = driver.title
    assert current_title == expected_title, f"Título esperado: {expected_title}, pero obtuve: {current_title}"
    logger.info(f"Título verificado: {current_title}")


def verify_url_contains(driver, expected_url_part):
    """Verifica que la URL actual contiene un texto específico"""
    current_url = driver.current_url
    assert expected_url_part in current_url, f"URL esperada contener: {expected_url_part}, pero obtuve: {current_url}"
    logger.info(f"URL verificada: {current_url}")


def get_alert_text(driver):
    """Obtiene el texto de una alerta"""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(driver, 10)
    alert = wait.until(EC.alert_is_present())
    text = alert.text
    logger.info(f"Texto de alerta: {text}")
    return text


def sleep(seconds):
    """Pausa la ejecución (usar solo si es necesario)"""
    logger.warning(f"Esperando {seconds} segundos...")
    time.sleep(seconds)
