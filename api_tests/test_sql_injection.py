import pytest
from sql_injection_demo import vulnerable_login

def test_normal_login():
    assert vulnerable_login("admin", "SuperSecret123") is True

def test_sql_injection_attack():
    assert vulnerable_login("admin", "' OR '1'='1") is True, "Система пропустила инъекцию (это плохо)"
