import pytest
from sql_injection_demo import safe_login

def test_safe_login_with_correct_password():
    """Корректные данные должны проходить"""
    assert safe_login("admin", "SuperSecret123") is True

def test_safe_login_blocks_sql_injection():
    """SQL-инъекция НЕ должна проходить (система защищена)"""
    assert safe_login("admin", "' OR '1'='1") is False, "Безопасная функция пропустила инъекцию! Защита сломана."
