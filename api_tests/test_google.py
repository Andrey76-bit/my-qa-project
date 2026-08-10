import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    yield driver
    driver.quit()

def test_duckduckgo_search(browser):
    browser.get("https://duckduckgo.com/")

    # Ждём и находим поле поиска (у него name="q")
    search_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("Selenium Python")
    
    # Находим кнопку поиска и кликаем (обычно это <button> с текстом или type="submit")
    search_button = browser.find_element(By.CSS_SELECTOR, "button[aria-label='Search']")
    search_button.click()

    # Ждём, пока на странице появится заголовок с текстом "Selenium Python"
    WebDriverWait(browser, 10).until(
        EC.title_contains("Selenium Python")
    )
    print(f"✅ Поиск успешен! Заголовок страницы: '{browser.title}'")
