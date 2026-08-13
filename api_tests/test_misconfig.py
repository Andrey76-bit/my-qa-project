import pytest
from misconfig_demo import App

def test_debug_mode_reveals_secrets():
    """Уязвимая конфигурация: DEBUG=True раскрывает внутренние данные"""
    app = App(debug=True)
    result = app.handle_error()
    assert "SUPER_SECRET_TOKEN_12345" in result, "Отладочный режим должен показать секрет"

def test_production_mode_hides_secrets():
    """Безопасная конфигурация: DEBUG=False скрывает детали"""
    app = App(debug=False)
    result = app.handle_error()
    assert "SUPER_SECRET_TOKEN_12345" not in result, "Продакшн-режим не должен раскрывать секреты!"
    assert "Произошла ошибка" in result
