from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Создаём "водителя" для Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Задача: открыть сайт
driver.get("https://www.google.com")

# Проверяем, что заголовок страницы содержит слово "Google"
assert "Google" in driver.title

print("✅ Боевая задача 'Hello, Браузер!' выполнена успешно!")
print(f"Заголовок страницы: '{driver.title}'")

# Закрываем браузер
driver.quit()
