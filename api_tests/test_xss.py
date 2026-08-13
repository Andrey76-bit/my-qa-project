import pytest
from xss_demo import render_message_safe

def test_safe_render_escapes_script_tag():
    """Проверяем, что <script> экранируется и не остаётся в исходном виде"""
    result = render_message_safe("<script>alert('XSS')</script>")
    assert "<script>" not in result, "Тег <script> не был экранирован! XSS возможен."
    assert "&lt;script&gt;" in result, "Ожидалось экранирование тега <script>"

def test_safe_render_allows_normal_text():
    """Проверяем, что обычный текст не портится"""
    result = render_message_safe("Привет, брат!")
    assert "Привет, брат!" in result
