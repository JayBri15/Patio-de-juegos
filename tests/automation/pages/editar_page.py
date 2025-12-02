"""
Page Object Model - Página de Editar Productos
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import EDITAR_URL


class EditarPage(BasePage):
    """Página para editar productos existentes"""
    
    def __init__(self, driver):
        super().__init__(driver, EDITAR_URL)
    
    # Localizadores
    PRODUCT_NAME = (By.ID, "editName")
    PRODUCT_PRICE = (By.ID, "editPrice")
    PRODUCT_DESCRIPTION = (By.ID, "editDesc")
    PRODUCT_STOCK = (By.ID, "editStock")
    PRODUCT_IMAGE = (By.ID, "editImage")
    SAVE_BUTTON = (By.CSS_SELECTOR, "form#editForm button[type='submit']")
    CANCEL_BUTTON = (By.ID, "cancelEdit")
    
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    
    def get_product_name(self):
        """Obtiene el nombre del producto actual"""
        return self.find_element(self.PRODUCT_NAME).get_attribute("value")
    
    def get_product_price(self):
        """Obtiene el precio del producto actual"""
        return self.find_element(self.PRODUCT_PRICE).get_attribute("value")
    
    def get_product_description(self):
        """Obtiene la descripción del producto actual"""
        return self.find_element(self.PRODUCT_DESCRIPTION).get_attribute("value")
    
    def update_product_name(self, new_name):
        """Actualiza el nombre del producto"""
        self.send_keys(self.PRODUCT_NAME, new_name)
    
    def update_product_price(self, new_price):
        """Actualiza el precio del producto"""
        self.send_keys(self.PRODUCT_PRICE, new_price)
    
    def update_product_description(self, new_description):
        """Actualiza la descripción del producto"""
        self.send_keys(self.PRODUCT_DESCRIPTION, new_description)
    
    def update_product_category(self, new_category):
        """Actualiza la categoría del producto"""
        # No hay selección de categoría en la versión actual; ignorar
        return
    
    def save_product(self):
        """Guarda los cambios del producto"""
        self.click_element(self.SAVE_BUTTON)
    
    def cancel(self):
        """Cancela la edición"""
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
