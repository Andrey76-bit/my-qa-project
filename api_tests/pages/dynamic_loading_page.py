from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DynamicLoadingPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://the-internet.herokuapp.com/dynamic_loading/1"
        self.start_button = (By.CSS_SELECTOR, "#start button")
        self.finish_text = (By.ID, "finish")

    def go_to(self):
        """Открывает страницу с динамической загрузкой"""
        self.driver.get(self.url)

    def click_start(self):
        """Нажимает кнопку Start для запуска загрузки"""
        self.driver.find_element(*self.start_button).click()

    def get_finish_text(self, timeout=10):
        """Ждёт появления финишного элемента и возвращает его текст"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.finish_text)
        )
        return element.text
