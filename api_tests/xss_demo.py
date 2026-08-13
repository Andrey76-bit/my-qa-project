# xss_demo.py - демонстрация уязвимости XSS

def render_message(user_input):
    """
    УЯЗВИМАЯ функция: вставляет пользовательский ввод в HTML без экранирования.
    """
    html = f"<div>Сообщение: {user_input}</div>"
    print(f"[УЯЗВИМЫЙ HTML] {html}")
    return html

def render_message_safe(user_input):
    """
    БЕЗОПАСНАЯ функция: экранирует спецсимволы, чтобы тег <script> не сработал.
    """
    import html as html_module
    safe_input = html_module.escape(user_input)
    html = f"<div>Сообщение: {safe_input}</div>"
    print(f"[БЕЗОПАСНЫЙ HTML] {html}")
    return html

if __name__ == "__main__":
    print("=== Обычное сообщение ===")
    render_message("Привет, брат!")
    print()

    print("=== Атака XSS ===")
    render_message("<script>alert('XSS')</script>")
    print()

    print("=== Защита от XSS ===")
    render_message_safe("<script>alert('XSS')</script>")
