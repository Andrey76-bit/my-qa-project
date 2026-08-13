import pytest
from command_injection_demo import ping_host_safe, ping_host_vulnerable

def test_vulnerable_allows_command_injection():
    """Уязвимая функция должна выполнить инъекцию (для демонстрации)"""
    output = ping_host_vulnerable("127.0.0.1; echo INJECTED")
    assert "INJECTED" in output, "Инъекция не сработала, проверьте окружение"

def test_safe_blocks_command_injection():
    """Безопасная функция не должна выполнить инъекцию"""
    output = ping_host_safe("127.0.0.1; echo INJECTED")
    assert "INJECTED" not in output, "Безопасная функция пропустила командную инъекцию!"
    assert "Недопустимый хост" in output

def test_safe_allows_normal_ping():
    """Безопасная функция должна пропускать валидный хост"""
    output = ping_host_safe("127.0.0.1")
    # Просто проверяем, что не вернула отказ
    assert "Недопустимый хост" not in output
