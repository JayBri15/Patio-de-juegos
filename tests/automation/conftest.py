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


@pytest.fixture(scope="function")
def driver():
    """
    Inicializa y retorna un WebDriver según la configuración.
    Se ejecuta antes de cada test y se cierra después.
    """
    if BROWSER.lower() == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    elif BROWSER.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
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
