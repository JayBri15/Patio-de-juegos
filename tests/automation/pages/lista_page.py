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
    
    # Localizadores (coincidir con `docs/HTML/Lista.html`)
    PRODUCT_TABLE = (By.ID, "usersTable")
    PRODUCT_ROWS = (By.XPATH, "//table[@id='usersTable']/tbody/tr")
    NO_PRODUCTS_MESSAGE = (By.ID, "emptyMessage")

    # Buttons are rendered with classes and data-id attributes (see docs/JS/Lista.js)
    EDIT_BUTTON = (By.XPATH, "//button[contains(@class, 'edit')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(@class, 'delete')]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@class, 'add')]")

    LOGOUT_BUTTON = (By.ID, "logoutBtn")
    GO_TO_CARRITO = (By.ID, "gotoCartBtn")
    GO_TO_MANAGER = (By.ID, "gotoManagerBtn")

    SEARCH_BOX = (By.ID, "search")
    
    def get_products_count(self):
        """Obtiene la cantidad de productos en la tabla"""
        products = self.find_elements(self.PRODUCT_ROWS)
        return len(products)
    
    def get_product_names(self):
        """Obtiene la lista de nombres de productos"""
        products = self.find_elements(self.PRODUCT_ROWS)
        names = []
        for product in products:
            # table columns: img, name, desc, price, actions
            name = product.find_element(By.XPATH, ".//td[2]").text
            names.append(name)
        return names
    
    def edit_product_by_index(self, index):
        """Edita un producto por su índice"""
        products = self.find_elements(self.PRODUCT_ROWS)
        if index < len(products):
            edit_btn = products[index].find_element(By.XPATH, ".//button[contains(@class, 'edit')]")
            self.driver.execute_script("arguments[0].click();", edit_btn)
    
    def delete_product_by_index(self, index):
        """Elimina un producto por su índice"""
        products = self.find_elements(self.PRODUCT_ROWS)
        if index < len(products):
            delete_btn = products[index].find_element(By.XPATH, ".//button[contains(@class, 'delete')]")
            # Usar click nativo para que WebDriver gestione correctamente el modal de confirmación
            # NOTA: No intentar consultar el DOM aquí, ya que el `confirm()` puede estar abierto
            # y provocar `unexpected alert open` cuando Selenium intente interactuar con la página.
            # El test llamante es responsable de aceptar/dismiss la alerta y luego verificar el DOM.
            delete_btn.click()
    
    def add_to_cart_by_index(self, index):
        """Agrega un producto al carrito por su índice"""
        products = self.find_elements(self.PRODUCT_ROWS)
        if index < len(products):
            # buttons rendered as <button class="btn add" data-id="...">Agregar al carrito</button>
            # Buscar por clase 'add' dentro de la fila
            cart_btn = products[index].find_element(By.XPATH, ".//button[contains(@class, 'add')]")
            self.driver.execute_script("arguments[0].click();", cart_btn)
    
    def search_product(self, product_name):
        """Busca un producto por nombre"""
        # El listado actual escucha el evento 'input', enviar keys debería filtrar
        self.send_keys(self.SEARCH_BOX, product_name)
    
    def is_no_products_message_visible(self):
        """Verifica si se muestra el mensaje de sin productos"""
        return self.is_element_visible(self.NO_PRODUCTS_MESSAGE)
    
    def logout(self):
        """Cierra sesión"""
        self.click_element(self.LOGOUT_BUTTON)
    
    def go_to_cart(self):
        """Va al carrito"""
        self.click_element(self.GO_TO_CARRITO)
