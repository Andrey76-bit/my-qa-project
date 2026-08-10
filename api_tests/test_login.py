import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    yield driver
    driver.quit()

# --- Негативный тест (уже был) ---
def test_login_with_invalid_password(browser):
    browser.get("https://the-internet.herokuapp.com/login")
    username_field = browser.find_element(By.ID, "username")
    password_field = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.CSS_SELECTOR, "button.radius")
    username_field.send_keys("tomsmith")
    password_field.send_keys("WrongPassword!")
    login_button.click()
    flash_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )
    assert "Your password is invalid!" in flash_message.text
    print("✅ Негативный тест пройден!")

# --- Позитивный тест (НОВЫЙ) ---
def test_login_with_valid_credentials(browser):
    browser.get("https://the-internet.herokuapp.com/login")
    username_field = browser.find_element(By.ID, "username")
    password_field = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.CSS_SELECTOR, "button.radius")
    username_field.send_keys("tomsmith")
    password_field.send_keys("SuperSecretPassword!")  # правильный пароль
    login_button.click()

    # Ждём появления элемента на странице, куда мы попадаем после логина (Secure Area)
    success_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )
    assert "You logged into a secure area!" in success_message.text
    print("✅ Позитивный тест пройден!")
