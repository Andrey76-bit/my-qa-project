import pytest
from playwright.sync_api import sync_playwright
from pages_playwright.checkboxes_page import CheckboxesPage

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path="/usr/bin/google-chrome")
        page = browser.new_page()
        yield page
        browser.close()

def test_checkboxes(browser):
    checkboxes_page = CheckboxesPage(browser)
    checkboxes_page.goto()

    # Проверяем начальное состояние
    assert checkboxes_page.is_checked(0) is False
    assert checkboxes_page.is_checked(1) is True

    # Кликаем по первому чекбоксу
    checkboxes_page.click_checkbox(0)

    # Проверяем, что он стал отмечен
    assert checkboxes_page.is_checked(0) is True

    print("✅ Playwright POM: тест чекбоксов пройден")
