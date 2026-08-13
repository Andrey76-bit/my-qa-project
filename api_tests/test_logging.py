import pytest
from logging_demo import SecureSystem, VulnerableSystem

def test_vulnerable_system_does_not_log_attempts():
    """Уязвимая система не логирует попытки (атака остаётся незамеченной)"""
    vuln = VulnerableSystem()
    vuln.login("wrong1")
    vuln.login("wrong2")
    # Уязвимая система не имеет метода get_log, поэтому проверим, что attempts не даёт полной картины
    assert vuln.attempts == 2, "Количество попыток должно считаться, но логов нет (уязвимость демонстрируется)"

def test_secure_system_logs_every_attempt():
    """Безопасная система записывает каждую попытку"""
    secure = SecureSystem()
    secure.login("wrong1")
    log = secure.get_log()
    assert "Попытка входа" in log, "Лог должен содержать запись о попытке"

def test_secure_system_detects_bruteforce():
    """Безопасная система обнаруживает атаку перебором после 5 неудачных попыток"""
    secure = SecureSystem()
    for i in range(5):
        secure.login(f"wrong{i}")
    log = secure.get_log()
    assert "ОБНАРУЖЕНА АТАКА ПЕРЕБОРОМ" in log, "Система не предупредила о подозрительной активности!"
