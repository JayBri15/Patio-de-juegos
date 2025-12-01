"""
Page Object Model - Página de Crear Productos
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import CREAR_URL


class CrearPage(BasePage):
    """Página para crear nuevos productos"""
    
    def __init__(self, driver):
        super().__init__(driver, CREAR_URL)
    
    # Localizadores
    PRODUCT_NAME = (By.ID, "productName")
    PRODUCT_PRICE = (By.ID, "productPrice")
    PRODUCT_DESCRIPTION = (By.ID, "productDescription")
    PRODUCT_CATEGORY = (By.ID, "productCategory")
    PRODUCT_IMAGE = (By.ID, "productImage")
    SAVE_BUTTON = (By.ID, "saveProductBtn")
    CANCEL_BUTTON = (By.ID, "cancelBtn")
    
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    
    def fill_product_form(self, name, price, description, category):
        """Llena el formulario de producto"""
        self.send_keys(self.PRODUCT_NAME, name)
        self.send_keys(self.PRODUCT_PRICE, price)
        self.send_keys(self.PRODUCT_DESCRIPTION, description)
        
        # Seleccionar categoría
        self.click_element(self.PRODUCT_CATEGORY)
        category_option = (By.XPATH, f"//select[@id='productCategory']/option[text()='{category}']")
        self.click_element(category_option)
    
    def save_product(self):
        """Guarda el producto"""
        self.click_element(self.SAVE_BUTTON)
    
    def cancel(self):
        """Cancela la creación de producto"""
        self.click_element(self.CANCEL_BUTTON)
    
    def get_success_message(self):
        """Obtiene el mensaje de éxito"""
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def get_error_message(self):
        """Obtiene el mensaje de error"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def logout(self):
        """Cierra sesión"""
        self.click_element(self.LOGOUT_BUTTON)
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        self.find_element(self.PRODUCT_NAME).clear()
        self.find_element(self.PRODUCT_PRICE).clear()
        self.find_element(self.PRODUCT_DESCRIPTION).clear()
