"""
Fixture para inicializar WebDriver de Selenium
"""
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import BROWSER, HEADLESS, SCREENSHOTS_DIR
from config.config import LISTA_URL
import json


@pytest.fixture(scope="function")
def driver():
    """
    Inicializa y retorna un WebDriver según la configuración.
    Se ejecuta antes de cada test y se cierra después.
    """
    if BROWSER.lower() == "chrome":
        options = webdriver.ChromeOptions()
        # Establecer el binario de Google Chrome estable
        options.binary_location = "/usr/bin/google-chrome-stable"
        if HEADLESS:
            options.add_argument("--headless")
        # Habilitar captura de logs de navegador (console) para Chrome
        try:
            options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        except Exception:
            # Silencioso si la versión de selenium no soporta set_capability
            pass
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        # No maximizar en headless
        if not HEADLESS:
            options.add_argument("--start-maximized")
        try:
            # Usar el chromedriver instalado en /usr/local/bin
            driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
        except:
            # Si falla, dejar que Selenium intente encontrarlo
            driver = webdriver.Chrome(options=options)
        # Asegurar que el directorio de screenshots exista (por si no se cargó config en tiempo)
        try:
            from config.config import SCREENSHOTS_DIR
            import os
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        except Exception:
            pass
        # Seed localStorage with sample products so Lista/Carrito have data
        try:
            sample_products = [
                {"id": "p1", "name": "Pelota", "desc": "Pelota de fútbol", "price": 9.99, "image": ""},
                {"id": "p2", "name": "Aro", "desc": "Aro para jugar", "price": 5.5, "image": ""},
                {"id": "p3", "name": "Cometa", "desc": "Cometa colorida", "price": 12.0, "image": ""}
            ]
            # Navegar brevemente a la página lista para establecer localStorage
            driver.get(LISTA_URL)
            driver.execute_script("localStorage.setItem('pdj_products_v1', arguments[0]);", json.dumps(sample_products))
            # asegurarse que sessionStorage carrito esté vacío
            driver.execute_script("sessionStorage.removeItem('pdj_cart');")
        except Exception:
            # No bloquear si el seed falla (ej: sin servidor en http://localhost:8000)
            pass
    elif BROWSER.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Firefox(options=options)
    elif BROWSER.lower() == "edge":
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Navegador no soportado: {BROWSER}")
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def take_screenshot(driver):
    """
    Fixture para capturar pantallas durante las pruebas
    """
    def _screenshot(name):
        filename = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
        driver.save_screenshot(filename)
        return filename
    
    return _screenshot
