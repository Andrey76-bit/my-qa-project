import pytest
from crypto_demo import hash_password, check_password_hashed, check_password_plain, store_password_plain

def test_plain_storage_reveals_password():
    """Уязвимое хранение: пароль виден невооружённым глазом (это плохо)"""
    stored = store_password_plain("SuperSecret123")
    assert stored == "SuperSecret123", "Пароль должен лежать в открытом виде (демонстрация уязвимости)"

def test_hashed_password_is_not_plaintext():
    """Безопасное хранение: хеш не должен быть равен паролю"""
    stored = hash_password("SuperSecret123")
    assert stored != "SuperSecret123", "Хеш не должен совпадать с исходным паролем!"

def test_hashed_password_verification_works():
    """Проверка входа должна работать с хешем"""
    stored = hash_password("SuperSecret123")
    assert check_password_hashed(stored, "SuperSecret123") is True
    assert check_password_hashed(stored, "WrongPass") is False
