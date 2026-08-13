import pytest
from logging_demo import SecureSystem, VulnerableSystem

def test_vulnerable_system_does_not_log_attempts():
    vuln = VulnerableSystem()
    vuln.login("wrong1")
    vuln.login("wrong2")
    assert vuln.attempts == 2

def test_secure_system_logs_every_attempt():
    secure = SecureSystem()
    secure.login("wrong1")
    log = secure.get_log()
    assert "Попытка входа" in log

def test_secure_system_detects_bruteforce():
    secure = SecureSystem()
    for i in range(5):
        secure.login(f"wrong{i}")
    log = secure.get_log()
    assert "ОБНАРУЖЕНА АТАКА ПЕРЕБОРОМ" in log
