from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://the-internet.herokuapp.com/login"

        # Локаторы (сюда мы выносим все селекторы)
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button.radius")
        self.flash_message = (By.CSS_SELECTOR, ".flash")

    def go_to(self):
        """Открывает страницу логина"""
        self.driver.get(self.url)

    def enter_username(self, username):
        """Вводит имя пользователя"""
        self.driver.find_element(*self.username_field).send_keys(username)

    def enter_password(self, password):
        """Вводит пароль"""
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        """Нажимает кнопку Login"""
        self.driver.find_element(*self.login_button).click()

    def get_flash_message_text(self):
        """Ждёт появления flash-сообщения и возвращает его текст"""
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.flash_message)
        )
        return message.text

    def login_as(self, username, password):
        """Выполняет полный сценарий входа: открыть страницу, ввести данные, нажать Login"""
        self.go_to()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
