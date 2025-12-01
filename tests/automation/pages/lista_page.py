"""
Page Object Model - Página de Listar Productos
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import LISTA_URL


class ListaPage(BasePage):
    """Página para listar productos"""
    
    def __init__(self, driver):
        super().__init__(driver, LISTA_URL)
    
    # Localizadores
    PRODUCT_TABLE = (By.ID, "productTable")
    PRODUCT_ROWS = (By.XPATH, "//table[@id='productTable']/tbody/tr")
    NO_PRODUCTS_MESSAGE = (By.CLASS_NAME, "no-products")
    
    EDIT_BUTTON = (By.XPATH, "//a[contains(@onclick, 'editProduct')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(@onclick, 'deleteProduct')]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@onclick, 'addToCart')]")
    
    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    GO_TO_CARRITO = (By.ID, "goToCarritoBtn")
    
    SEARCH_BOX = (By.ID, "searchBox")
    SEARCH_BUTTON = (By.ID, "searchBtn")
    
    def get_products_count(self):
        """Obtiene la cantidad de productos en la tabla"""
        products = self.find_elements(self.PRODUCT_ROWS)
        return len(products)
    
    def get_product_names(self):
        """Obtiene la lista de nombres de productos"""
        products = self.find_elements(self.PRODUCT_ROWS)
        names = []
        for product in products:
            name = product.find_element(By.XPATH, ".//td[1]").text
            names.append(name)
        return names
    
    def edit_product_by_index(self, index):
        """Edita un producto por su índice"""
        products = self.find_elements(self.PRODUCT_ROWS)
        if index < len(products):
            edit_btn = products[index].find_element(By.XPATH, ".//a[contains(@onclick, 'editProduct')]")
            self.driver.execute_script("arguments[0].click();", edit_btn)
    
    def delete_product_by_index(self, index):
        """Elimina un producto por su índice"""
        products = self.find_elements(self.PRODUCT_ROWS)
        if index < len(products):
            delete_btn = products[index].find_element(By.XPATH, ".//button[contains(@onclick, 'deleteProduct')]")
            self.driver.execute_script("arguments[0].click();", delete_btn)
    
    def add_to_cart_by_index(self, index):
        """Agrega un producto al carrito por su índice"""
        products = self.find_elements(self.PRODUCT_ROWS)
        if index < len(products):
            cart_btn = products[index].find_element(By.XPATH, ".//button[contains(@onclick, 'addToCart')]")
            self.driver.execute_script("arguments[0].click();", cart_btn)
    
    def search_product(self, product_name):
        """Busca un producto por nombre"""
        self.send_keys(self.SEARCH_BOX, product_name)
        self.click_element(self.SEARCH_BUTTON)
    
    def is_no_products_message_visible(self):
        """Verifica si se muestra el mensaje de sin productos"""
        return self.is_element_visible(self.NO_PRODUCTS_MESSAGE)
    
    def logout(self):
        """Cierra sesión"""
        self.click_element(self.LOGOUT_BUTTON)
    
    def go_to_cart(self):
        """Va al carrito"""
        self.click_element(self.GO_TO_CARRITO)
