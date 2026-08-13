# outdated_component_demo.py - демонстрация A06: Vulnerable and Outdated Components

class OldComponent:
    """УЯЗВИМЫЙ КОМПОНЕНТ (старая версия библиотеки).
    Использует eval() без ограничений, что позволяет выполнить произвольный код."""
    def evaluate(self, expression):
        print(f"[СТАРЫЙ КОМПОНЕНТ] eval('{expression}')")
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Ошибка: {e}"

class NewComponent:
    """БЕЗОПАСНЫЙ КОМПОНЕНТ (обновлённая версия).
    Проверяет ввод и использует eval с ограниченным окружением (нет __builtins__)."""
    def evaluate(self, expression):
        print(f"[НОВЫЙ КОМПОНЕНТ] Обработка '{expression}'")
        import re
        # Разрешаем только цифры, пробелы и математические операторы
        if re.match(r'^[\d\s+\-*/().]+$', expression):
            try:
                # eval с пустым __builtins__ блокирует __import__ и другие опасные функции
                result = eval(expression, {"__builtins__": None}, {})
                return str(result)
            except Exception as e:
                return "Недопустимое выражение"
        else:
            return "Недопустимое выражение (возможна инъекция)"

if __name__ == "__main__":
    print("=== Попытка эксплуатации устаревшего компонента ===")
    old = OldComponent()
    malicious = "__import__('os').system('echo HACKED')"
    print("Результат:", old.evaluate(malicious))

    print("\n=== Тот же код на обновлённом компоненте ===")
    new = NewComponent()
    print("Результат:", new.evaluate(malicious))

    print("\n=== Обычное выражение на обновлённом компоненте ===")
    print("Результат:", new.evaluate("2 + 3 * 4"))
