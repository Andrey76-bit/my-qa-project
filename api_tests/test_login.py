import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page import LoginPage  # импортируем наш класс страницы

@pytest.fixture
def browser():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_login_with_invalid_password(browser):
    # Создаём объект страницы
    login_page = LoginPage(browser)
    # Используем готовый метод
    login_page.login_as("tomsmith", "WrongPassword!")
    # Проверяем сообщение
    assert "Your password is invalid!" in login_page.get_flash_message_text()
    print("✅ Негативный тест пройден (POM)!")

def test_login_with_valid_credentials(browser):
    login_page = LoginPage(browser)
    login_page.login_as("tomsmith", "SuperSecretPassword!")
    assert "You logged into a secure area!" in login_page.get_flash_message_text()
    print("✅ Позитивный тест пройден (POM)!")
