import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pages.dynamic_loading_page import DynamicLoadingPage

@pytest.fixture
def browser():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_dynamic_loading(browser):
    """Проверяем, что после нажатия Start появляется текст 'Hello World!'"""
    page = DynamicLoadingPage(browser)
    page.go_to()
    
    # Убеждаемся, что финишный элемент ещё не виден (можно проверить, что его нет)
    # Но главное — запускаем загрузку
    page.click_start()
    
    # Ждём появления результата и проверяем его
    finish_text = page.get_finish_text()
    assert "Hello World!" in finish_text, f"Ожидался 'Hello World!', а получен '{finish_text}'"
    print("✅ Динамическая загрузка пройдена! Текст:", finish_text)
