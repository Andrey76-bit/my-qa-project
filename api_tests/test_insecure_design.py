import pytest
from insecure_design_demo import LoginSystemSafe, LoginSystemVulnerable

def test_vulnerable_system_allows_unlimited_attempts():
    """Уязвимая система не блокирует после многих попыток (демонстрация)"""
    vuln = LoginSystemVulnerable()
    for i in range(10):
        vuln.try_login(f"wrong{i}")
    # После 10 неудачных всё ещё можно войти с верным паролем
    assert vuln.try_login("SuperSecret123") is True, "Уязвимая система должна пропустить вход после перебора"

def test_safe_system_locks_after_five_attempts():
    """Безопасная система блокируется после 5 неудачных попыток"""
    safe = LoginSystemSafe()
    for i in range(5):
        safe.try_login(f"wrong{i}")
    # Теперь даже верный пароль не должен пройти
    assert safe.try_login("SuperSecret123") == "LOCKED", "Система не заблокировалась после 5 попыток!"

def test_safe_system_allows_login_before_lock():
    """Безопасная система должна позволять войти до блокировки"""
    safe = LoginSystemSafe()
    # 4 неудачные попытки
    for i in range(4):
        safe.try_login(f"wrong{i}")
    # На 5-й попытке вводим верный пароль
    assert safe.try_login("SuperSecret123") is True, "Система должна разрешить вход до блокировки"
