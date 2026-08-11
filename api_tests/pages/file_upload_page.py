import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FileUploadPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://the-internet.herokuapp.com/upload"
        self.file_input = (By.ID, "file-upload")
        self.submit_button = (By.ID, "file-submit")
        self.success_message = (By.TAG_NAME, "h3")

    def go_to(self):
        self.driver.get(self.url)

    def upload_file(self, file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        self.driver.find_element(*self.file_input).send_keys(file_path)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def get_success_message_text(self):
        message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.success_message)
        )
        return message.text
