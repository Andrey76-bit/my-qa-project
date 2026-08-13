# logging_demo.py - демонстрация A09: Security Logging and Monitoring Failures

class VulnerableSystem:
    """УЯЗВИМАЯ система: не ведёт логи, поэтому атаку не видно."""
    def __init__(self):
        self.password = "Secret123"
        self.attempts = 0

    def login(self, password):
        # Просто проверяем пароль, ничего не записывая
        if password == self.password:
            return "Вход выполнен"
        else:
            self.attempts += 1
            return "Неверный пароль"

class SecureSystem:
    """БЕЗОПАСНАЯ система: пишет лог о каждой попытке и предупреждает о подозрительной активности."""
    def __init__(self):
        self.password = "Secret123"
        self.attempts = 0
        self.log = []

    def login(self, password):
        # Логируем все попытки
        self.log.append(f"Попытка входа с паролем '{password}'")
        if password == self.password:
            return "Вход выполнен"
        else:
            self.attempts += 1
            # Если неудачных попыток 5 или больше, бьём тревогу
            if self.attempts >= 5:
                self.log.append("⚠️ ОБНАРУЖЕНА АТАКА ПЕРЕБОРОМ: 5 неудачных попыток!")
            return "Неверный пароль"

    def get_log(self):
        return "\n".join(self.log)

if __name__ == "__main__":
    print("=== Уязвимая система (нет логов) ===")
    vuln = VulnerableSystem()
    for i in range(6):
        vuln.login(f"wrong{i}")
    print("Логи: (пусто)")
    print("Система понятия не имеет, что её атаковали!")

    print("\n=== Безопасная система (ведёт логи) ===")
    secure = SecureSystem()
    for i in range(6):
        secure.login(f"wrong{i}")
    print(secure.get_log())
