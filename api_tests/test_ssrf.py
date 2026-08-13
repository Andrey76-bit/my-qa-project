import pytest
from ssrf_demo import fetch_url_safe, fetch_url_vulnerable

def test_vulnerable_allows_internal_access():
    """Уязвимая функция должна обращаться к внутренним ресурсам (демонстрация)"""
    result = fetch_url_vulnerable("http://localhost/admin")
    assert "Внутренний ресурс" in result, "Уязвимая функция не получила доступ к localhost"

def test_safe_blocks_localhost():
    """Безопасная функция должна блокировать localhost"""
    result = fetch_url_safe("http://localhost/admin")
    assert "Доступ запрещён" in result, "Безопасная функция пропустила localhost!"

def test_safe_blocks_private_ips():
    """Безопасная функция должна блокировать приватные IP"""
    result = fetch_url_safe("http://192.168.1.1/secret")
    assert "Доступ запрещён" in result, "Безопасная функция пропустила приватный IP!"

def test_safe_allows_external_urls():
    """Безопасная функция должна разрешать внешние URL"""
    result = fetch_url_safe("https://example.com/image.jpg")
    assert "Загружен внешний ресурс" in result, "Безопасная функция ошибочно заблокировала внешний URL"
