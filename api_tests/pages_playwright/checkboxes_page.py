from playwright.sync_api import Page

class CheckboxesPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://the-internet.herokuapp.com/checkboxes"
        self.checkboxes = page.locator("input[type='checkbox']")

    def goto(self):
        self.page.goto(self.url)

    def get_checkbox(self, index: int):
        return self.checkboxes.nth(index)

    def is_checked(self, index: int) -> bool:
        return self.get_checkbox(index).is_checked()

    def click_checkbox(self, index: int):
        self.get_checkbox(index).click()
