# misconfig_demo.py - демонстрация Security Misconfiguration

class App:
    def __init__(self, debug):
        self.debug = debug
        self.secret = "SUPER_SECRET_TOKEN_12345"

    def handle_error(self):
        if self.debug:
            # УЯЗВИМАЯ конфигурация: отладочный режим раскрывает секреты
            return f"ERROR: Database connection failed. Token = {self.secret}, Path = /var/www/app, Version = 1.2.3"
        else:
            # БЕЗОПАСНАЯ конфигурация: пользователь видит только общее сообщение
            return "Произошла ошибка. Пожалуйста, попробуйте позже."

if __name__ == "__main__":
    print("=== Небезопасная конфигурация (DEBUG=True) ===")
    app_debug = App(debug=True)
    print(app_debug.handle_error())

    print("\n=== Безопасная конфигурация (DEBUG=False) ===")
    app_prod = App(debug=False)
    print(app_prod.handle_error())
