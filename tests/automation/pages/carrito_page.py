"""
Page Object Model - Página de Carrito
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import CARRITO_URL


class CarritoPage(BasePage):
    """Página del carrito de compras"""
    
    def __init__(self, driver):
        super().__init__(driver, CARRITO_URL)
    
    # Localizadores
    CART_TABLE = (By.ID, "cartTable")
    CART_ITEMS = (By.XPATH, "//table[@id='cartTable']/tbody/tr")
    EMPTY_CART_MESSAGE = (By.CLASS_NAME, "empty-cart")
    
    REMOVE_BUTTON = (By.XPATH, "//button[contains(@onclick, 'removeFromCart')]")
    UPDATE_QUANTITY_INPUT = (By.XPATH, "//input[@name='quantity']")
    UPDATE_BUTTON = (By.XPATH, "//button[contains(@onclick, 'updateQuantity')]")
    
    CHECKOUT_BUTTON = (By.ID, "checkoutBtn")
    CONTINUE_SHOPPING = (By.ID, "continueShoppingBtn")
    
    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    
    def get_cart_items_count(self):
        """Obtiene la cantidad de items en el carrito"""
        try:
            items = self.find_elements(self.CART_ITEMS)
            return len(items)
        except:
            return 0
    
    def get_cart_item_names(self):
        """Obtiene la lista de nombres de productos en el carrito"""
        items = self.find_elements(self.CART_ITEMS)
        names = []
        for item in items:
            name = item.find_element(By.XPATH, ".//td[1]").text
            names.append(name)
        return names
    
    def remove_item_by_index(self, index):
        """Elimina un item del carrito por su índice"""
        items = self.find_elements(self.CART_ITEMS)
        if index < len(items):
            remove_btn = items[index].find_element(By.XPATH, ".//button[contains(@onclick, 'removeFromCart')]")
            self.driver.execute_script("arguments[0].click();", remove_btn)
    
    def update_quantity(self, index, quantity):
        """Actualiza la cantidad de un item"""
        items = self.find_elements(self.CART_ITEMS)
        if index < len(items):
            quantity_input = items[index].find_element(By.XPATH, ".//input[@name='quantity']")
            self.send_keys((By.XPATH, f"({self.UPDATE_QUANTITY_INPUT[1]})[{index+1}]"), str(quantity))
    
    def checkout(self):
        """Realiza el checkout"""
        self.click_element(self.CHECKOUT_BUTTON)
    
    def continue_shopping(self):
        """Continúa comprando"""
        self.click_element(self.CONTINUE_SHOPPING)
    
    def is_empty_cart_message_visible(self):
        """Verifica si el carrito está vacío"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def logout(self):
        """Cierra sesión"""
        self.click_element(self.LOGOUT_BUTTON)
