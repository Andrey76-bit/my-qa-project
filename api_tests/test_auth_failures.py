import pytest
from auth_failures_demo import login_safe, login_vulnerable

def test_vulnerable_reveals_user_absence():
    """Уязвимая функция раскрывает, что пользователь не существует"""
    result = login_vulnerable("notfound@example.com", "any")
    assert "не найден" in result, "Уязвимая функция должна сообщать о несуществующем пользователе"

def test_safe_hides_user_absence():
    """Безопасная функция не должна раскрывать, существует ли email"""
    result = login_safe("notfound@example.com", "any")
    assert "не найден" not in result, "Безопасная функция не должна сообщать о несуществующем пользователе"
    assert "неверный email или пароль" in result

def test_safe_locks_after_five_attempts():
    """Безопасная функция должна блокировать аккаунт после 5 неудачных попыток"""
    tracker = {}
    for i in range(5):
        login_safe("andrey@example.com", f"wrong{i}", tracker)
    result = login_safe("andrey@example.com", "StrongPass123", tracker)
    assert "заблокирован" in result, "Аккаунт не заблокировался после 5 попыток"

def test_safe_allows_login_before_lock():
    """Безопасная функция должна разрешать вход до блокировки"""
    tracker = {}
    for i in range(4):
        login_safe("andrey@example.com", f"wrong{i}", tracker)
    result = login_safe("andrey@example.com", "StrongPass123", tracker)
    assert result == "Вход выполнен", "Вход должен быть разрешён до блокировки"
