import pytest
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

@pytest.fixture
def browser():
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    yield driver
    driver.quit()

def test_checkboxes(browser):
    browser.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = browser.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    first_checkbox = checkboxes[0]
    second_checkbox = checkboxes[1]
    assert not first_checkbox.is_selected()
    assert second_checkbox.is_selected()
    first_checkbox.click()
    assert first_checkbox.is_selected()
    print("✅ Чекбоксы пройдены")

def test_dropdown(browser):
    browser.get("https://the-internet.herokuapp.com/dropdown")
    dropdown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(dropdown)
    select.select_by_visible_text("Option 2")
    assert select.first_selected_option.text == "Option 2"
    print("✅ Выпадающий список пройден")

def test_file_upload(browser):
    browser.get("https://the-internet.herokuapp.com/upload")
    upload_input = browser.find_element(By.ID, "file-upload")
    file_path = os.path.join(os.getcwd(), "test_upload.txt")
    upload_input.send_keys(file_path)
    browser.find_element(By.ID, "file-submit").click()
    success = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert "File Uploaded!" in success.text
    print("✅ Загрузка файла пройдена")

def test_alert(browser):
    browser.get("https://the-internet.herokuapp.com/javascript_alerts")
    browser.find_element(By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
    alert = WebDriverWait(browser, 10).until(EC.alert_is_present())
    assert alert.text == "I am a JS Alert"
    alert.accept()
    result = browser.find_element(By.ID, "result")
    assert "You successfully clicked an alert" in result.text
    print("✅ Простой алерт пройден")

def test_confirm_alert(browser):
    browser.get("https://the-internet.herokuapp.com/javascript_alerts")
    browser.find_element(By.CSS_SELECTOR, "button[onclick='jsConfirm()']").click()
    alert = WebDriverWait(browser, 10).until(EC.alert_is_present())
    alert.dismiss()
    result = browser.find_element(By.ID, "result")
    assert "You clicked: Cancel" in result.text
    print("✅ Confirm алерт (Cancel) пройден")

def test_prompt_alert(browser):
    browser.get("https://the-internet.herokuapp.com/javascript_alerts")
    browser.find_element(By.CSS_SELECTOR, "button[onclick='jsPrompt()']").click()
    alert = WebDriverWait(browser, 10).until(EC.alert_is_present())
    alert.send_keys("Брат Андрей")
    alert.accept()
    result = browser.find_element(By.ID, "result")
    assert "You entered: Брат Андрей" in result.text
    print("✅ Prompt алерт пройден")
