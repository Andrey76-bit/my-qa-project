import random
import string
import pytest

def generate_random_password():
    """Генерирует абсолютно случайную строку, которая может быть плохим паролем"""
    length = random.randint(4, 12)  # Длина от 4 до 12 (многие будут короткими)
    # В наборе буквы, цифры и немного спецсимволов
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def validate_password(pwd):
    """Проверяет пароль на соответствие правилам. Возвращает список ошибок."""
    errors = []
    if len(pwd) < 8:
        errors.append(f"Слишком короткий (длина {len(pwd)})")
    if not any(c.isupper() for c in pwd):
        errors.append("Нет заглавной буквы")
    if not any(c.isdigit() for c in pwd):
        errors.append("Нет цифры")
    if not any(c in "!@#$%^&*()" for c in pwd):
        errors.append("Нет спецсимвола")
    return errors

@pytest.mark.parametrize("test_number", range(1000))  # Запускаем тест 1000 раз
def test_random_password_security(test_number):
    """Проверяем 1000 случайных паролей"""
    pwd = generate_random_password()
    errors = validate_password(pwd)
    # assert с понятным сообщением — если ошибки есть, тест упадёт
    assert len(errors) == 0, f"Пароль '{pwd}' не прошёл проверку: {', '.join(errors)}"
