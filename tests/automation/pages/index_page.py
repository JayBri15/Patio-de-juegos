"""
Page Object Model - Página de Index (Login/Registro)
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import INDEX_URL


class IndexPage(BasePage):
    """Página de inicio con login y registro"""
    
    def __init__(self, driver):
        super().__init__(driver, INDEX_URL)
    
    # Localizadores (ajustados a la versión actual de `docs/HTML/Index.html`)
    LOGIN_FORM = (By.ID, "loginForm")
    REGISTER_FORM = (By.ID, "registerForm")
    LOGIN_TOGGLE = (By.ID, "tabLogin")
    REGISTER_TOGGLE = (By.ID, "tabRegister")

    # Elementos de Login
    LOGIN_USERNAME = (By.ID, "loginName")
    LOGIN_PASSWORD = (By.ID, "loginPassword")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "form#loginForm button[type='submit']")
    LOGIN_ERROR = (By.CLASS_NAME, "error-message")

    # Elementos de Registro
    REGISTER_USERNAME = (By.ID, "regName")
    REGISTER_EMAIL = (By.ID, "regEmail")
    REGISTER_PASSWORD = (By.ID, "regPassword")
    REGISTER_CONFIRM_PASSWORD = (By.ID, "regPassword2")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "form#registerForm button[type='submit']")
    REGISTER_ERROR = (By.CLASS_NAME, "error-message")

    # Mensajes de éxito
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    
    def toggle_to_login(self):
        """Cambia a formulario de login"""
        self.click_element(self.LOGIN_TOGGLE)
    
    def toggle_to_register(self):
        """Cambia a formulario de registro"""
        self.click_element(self.REGISTER_TOGGLE)
    
    def login(self, username, password):
        """Realiza login con usuario y contraseña"""
        self.send_keys(self.LOGIN_USERNAME, username)
        self.send_keys(self.LOGIN_PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def register(self, username, password, confirm_password):
        """Realiza registro de nuevo usuario"""
        self.send_keys(self.REGISTER_USERNAME, username)
        # El formulario de registro actual usa email + contraseña
        # si se requiere ajustar, se asigna también REGISTER_EMAIL
        self.send_keys(self.REGISTER_PASSWORD, password)
        self.send_keys(self.REGISTER_CONFIRM_PASSWORD, confirm_password)
        self.click_element(self.REGISTER_BUTTON)
    
    def get_login_error_message(self):
        """Obtiene el mensaje de error en el login"""
        if self.is_element_visible(self.LOGIN_ERROR):
            return self.get_text(self.LOGIN_ERROR)
        return None
    
    def get_register_error_message(self):
        """Obtiene el mensaje de error en el registro"""
        if self.is_element_visible(self.REGISTER_ERROR):
            return self.get_text(self.REGISTER_ERROR)
        return None
    
    def get_success_message(self):
        """Obtiene el mensaje de éxito"""
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def is_login_form_visible(self):
        """Verifica si el formulario de login es visible"""
        return self.is_element_visible(self.LOGIN_FORM)
    
    def is_register_form_visible(self):
        """Verifica si el formulario de registro es visible"""
        return self.is_element_visible(self.REGISTER_FORM)
