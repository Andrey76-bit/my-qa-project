# Функция, которую мы тестируем (наш "калькулятор")
def divide(a, b):
    return a / b

# Тест 1: Проверяем, что обычное деление работает
result = divide(10, 2)
if result == 5:
    print("Тест 1: PASSED (10 / 2 = " + str(result) + ")")
else:
    print("Тест 1: FAILED! Ожидалось 5, получили " + str(result))

# Тест 2: Проверяем, что деление на ноль ВЫЗЫВАЕТ ОШИБКУ
try:
    divide(0, 0)
    print("Тест 2: FAILED! Ожидалась ошибка, но функция не упала.")
except ZeroDivisionError:
    print("Тест 2: PASSED (деление на ноль вызвало ошибку ZeroDivisionError)")
