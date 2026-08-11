import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    page.click_start()
    finish_text = page.get_finish_text()
    assert "Hello World!" in finish_text, f"Ожидался 'Hello World!', а получен '{finish_text}'"
    print("✅ Динамическая загрузка пройдена! Текст:", finish_text)

def test_start_button_disappears_after_click(browser):
    """Проверяем, что после нажатия Start кнопка исчезает (защита от двойного нажатия)"""
    page = DynamicLoadingPage(browser)
    page.go_to()
    page.click_start()
    # Ждём, пока кнопка Start исчезнет
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located(page.start_button)
    )
    print("✅ Кнопка Start исчезла после нажатия — защита от двойного клика работает!")
