class VulnerableSystem:
    def __init__(self):
        self.password = "Secret123"
        self.attempts = 0

    def login(self, password):
        if password == self.password:
            return "Вход выполнен"
        else:
            self.attempts += 1
            return "Неверный пароль"

class SecureSystem:
    def __init__(self):
        self.password = "Secret123"
        self.attempts = 0
        self.log = []

    def login(self, password):
        self.log.append(f"Попытка входа с паролем '{password}'")
        if password == self.password:
            return "Вход выполнен"
        else:
            self.attempts += 1
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

    print("\n=== Безопасная система (ведёт логи) ===")
    secure = SecureSystem()
    for i in range(6):
        secure.login(f"wrong{i}")
    print(secure.get_log())
