import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path="/usr/bin/google-chrome")
        page = browser.new_page()
        yield page
        browser.close()

def test_title(browser):
    browser.goto("https://example.com")
    assert "Example Domain" in browser.title()
