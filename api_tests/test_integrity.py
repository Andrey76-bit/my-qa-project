import pytest
import pickle
from integrity_demo import User, serialize_user_safe, deserialize_user_safe, deserialize_user_vulnerable, serialize_user_vulnerable

def test_vulnerable_deserialization_allows_admin_forgery():
    """Уязвимая десериализация позволяет подделать is_admin=True (без проверки)"""
    # Злоумышленник создаёт поддельного пользователя-админа
    malicious_payload = pickle.dumps(User("hacker", is_admin=True))
    loaded = deserialize_user_vulnerable(malicious_payload)
    assert loaded.is_admin is True, "Уязвимая функция должна загрузить поддельного админа"

def test_safe_deserialization_rejects_forged_data():
    """Безопасная десериализация отвергает данные с неверной подписью"""
    # Получаем валидные данные и подпись для обычного пользователя
    normal_user = User("andrey", is_admin=False)
    data, sig = serialize_user_safe(normal_user)
    # Злоумышленник подменяет JSON, но не может подделать подпись
    forged_data = b'{"username": "hacker", "is_admin": true}'
    loaded = deserialize_user_safe(forged_data, sig)
    assert loaded is None, "Безопасная функция не должна принять поддельные данные"

def test_safe_deserialization_accepts_valid_data():
    """Безопасная десериализация принимает валидные данные с правильной подписью"""
    normal_user = User("andrey", is_admin=False)
    data, sig = serialize_user_safe(normal_user)
    loaded = deserialize_user_safe(data, sig)
    assert loaded is not None
    assert loaded.username == "andrey"
    assert loaded.is_admin is False
