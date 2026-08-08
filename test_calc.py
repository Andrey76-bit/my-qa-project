# Это наша функция, которую мы тестируем
def summa(a, b):
    return a + b

# Это наш тест
print("Запускаем тест сложения...")
result = summa(2, 3)
if result == 5:
    print("Тест 1: PASSED (2 + 3 = " + str(result) + ")")
else:
    print("Тест 1: FAILED! Ожидалось 5, получили " + str(result))
# Тест 2: проверка с нулями
result = summa(0, 0)
if result == 0:
    print("Тест 2: PASSED (0 + 0 = " + str(result) + ")")
else:
    print("Тест 2: FAILED! Ожидалось 0, получили " + str(result))# Тест 3: проверка с отрицательным числом
result = summa(-5, 5)
if result == 0:
    print("Тест 3: PASSED (-5 + 5 = " + str(result) + ")")
else:
    print("Тест 3: FAILED! Ожидалось 0, получили " + str(result))
