import random
import pytest

def test_addition_identity():
    """Проверяем, что для 100 случайных чисел х+0 всегда равно х"""
    for i in range(100):          # Повторить 100 раз
        x = random.randint(-1000, 1000)   # Случайное число от -1000 до 1000
        assert x + 0 == x, f"ОШИБКА: {x} + 0 != {x} (итерация {i})"

def test_multiplication_identity():
    """Проверяем, что для 100 случайных чисел х*1 всегда равно х"""
    for i in range(100):
        x = random.randint(-1000, 1000)
        assert x * 1 == x, f"ОШИБКА: {x} * 1 != {x} (итерация {i})"
