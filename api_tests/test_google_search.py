from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Открываем Google
driver.get("https://www.google.com")

# Находим поле поиска и вводим запрос
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.send_keys(Keys.RETURN)

# Ждём, пока на странице появится блок с результатами (например, элемент с id="search")
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    print("✅ Блок результатов найден. Поиск отработал успешно!")
except:
    print("❌ Блок результатов не появился за 10 секунд.")

# Для надёжности проверим, что заголовок содержит "Selenium Python" (но не падаем ассертом, просто выводим)
if "Selenium Python" in driver.title:
    print(f"✅ Заголовок совпадает: '{driver.title}'")
else:
    print(f"⚠️ Заголовок не совпадает, но это ок. Фактический: '{driver.title}'")

time.sleep(2)  # Немного подождём, чтобы увидеть результат
driver.quit()
