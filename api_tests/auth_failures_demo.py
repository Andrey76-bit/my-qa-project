# auth_failures_demo.py - демонстрация A07: Identification and Authentication Failures

# База пользователей (для примера)
USERS = {
    "andrey@example.com": {"password": "StrongPass123", "name": "Андрей"},
    "admin@example.com": {"password": "AdminSecret456", "name": "Админ"},
}

def login_vulnerable(email, password):
    """УЯЗВИМАЯ функция: раскрывает, зарегистрирован ли email, и не ограничивает попытки"""
    if email not in USERS:
        return "Ошибка: пользователь с таким email не найден"
    if USERS[email]["password"] == password:
        return "Вход выполнен"
    else:
        return "Ошибка: неверный пароль"

def login_safe(email, password, attempts_tracker=None):
    """БЕЗОПАСНАЯ функция: не раскрывает, что именно неверно, и блокирует после 5 попыток"""
    if attempts_tracker is None:
        attempts_tracker = {}
    # Проверяем блокировку
    if attempts_tracker.get(email, 0) >= 5:
        return "Аккаунт временно заблокирован из-за множества попыток"
    
    # Единое сообщение об ошибке для любого неверного ввода
    if email in USERS and USERS[email]["password"] == password:
        return "Вход выполнен"
    else:
        # Увеличиваем счётчик неудач
        attempts_tracker[email] = attempts_tracker.get(email, 0) + 1
        return "Ошибка: неверный email или пароль"

if __name__ == "__main__":
    print("=== Уязвимая аутентификация ===")
    print(login_vulnerable("notfound@example.com", "any"))
    print(login_vulnerable("andrey@example.com", "wrongpass"))
    
    print("\n=== Безопасная аутентификация ===")
    tracker = {}
    print(login_safe("notfound@example.com", "any", tracker))
    print(login_safe("andrey@example.com", "wrongpass", tracker))
    # Покажем блокировку после 5 неверных попыток
    for i in range(5):
        print(login_safe("andrey@example.com", f"wrong{i}", tracker))
    print(login_safe("andrey@example.com", "StrongPass123", tracker))
