import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path="/usr/bin/google-chrome")
        page = browser.new_page()
        yield page
        browser.close()

def test_login_with_invalid_password(browser):
    browser.goto("https://the-internet.herokuapp.com/login")

    browser.fill("#username", "tomsmith")
    browser.fill("#password", "WrongPassword!")
    browser.click("button.radius")

    # Ждём появления сообщения об ошибке (Playwright сам ждёт)
    error = browser.locator(".flash.error")
    assert "Your password is invalid!" in error.text_content()

    print("✅ Playwright: негативный тест логина пройден")
