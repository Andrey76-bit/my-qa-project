import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path="/usr/bin/google-chrome")
        page = browser.new_page()
        yield page
        browser.close()

def test_checkboxes(browser):
    browser.goto("https://the-internet.herokuapp.com/checkboxes")

    # Находим чекбоксы по CSS-селектору
    first_checkbox = browser.locator("input[type='checkbox']").nth(0)

    # Проверяем, что первый чекбокс не отмечен
    assert first_checkbox.is_checked() is False

    # Кликаем по первому чекбоксу
    first_checkbox.click()

    # Проверяем, что после клика он стал отмечен
    assert first_checkbox.is_checked() is True

    print("✅ Playwright: тест чекбоксов пройден")
