# insecure_design_demo.py - демонстрация Insecure Design (нет ограничения попыток)

class LoginSystemVulnerable:
    """УЯЗВИМЫЙ дизайн: позволяет неограниченные попытки входа"""
    def __init__(self):
        self.password = "SuperSecret123"
        self.attempts = 0

    def try_login(self, password):
        self.attempts += 1
        if password == self.password:
            return True
        return False

class LoginSystemSafe:
    """БЕЗОПАСНЫЙ дизайн: блокирует после 5 неудачных попыток"""
    def __init__(self):
        self.password = "SuperSecret123"
        self.attempts = 0
        self.max_attempts = 5
        self.locked = False

    def try_login(self, password):
        if self.locked:
            return "LOCKED"
        self.attempts += 1
        if password == self.password:
            return True
        if self.attempts >= self.max_attempts:
            self.locked = True
        return False

if __name__ == "__main__":
    print("=== Уязвимый дизайн (можно перебирать бесконечно) ===")
    vuln = LoginSystemVulnerable()
    for i in range(6):
        result = vuln.try_login(f"wrong{i}")
        print(f"Попытка {i+1}: {result}")
    # Пробуем верный пароль после 6 неверных
    print("Попытка с верным паролем:", vuln.try_login("SuperSecret123"))

    print("\n=== Безопасный дизайн (блокировка после 5 попыток) ===")
    safe = LoginSystemSafe()
    for i in range(6):
        result = safe.try_login(f"wrong{i}")
        print(f"Попытка {i+1}: {result}")
    # Пробуем верный пароль после блокировки
    print("Попытка с верным паролем:", safe.try_login("SuperSecret123"))
