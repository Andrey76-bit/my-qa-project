# access_control_demo.py - демонстрация Broken Access Control (IDOR)

# База данных пользователей (для простоты словарь)
users_db = {
    123: {"name": "Андрей", "balance": 1000},
    124: {"name": "Злоумышленник", "balance": 999999},
}

def get_user_profile_vulnerable(user_id):
    """
    УЯЗВИМАЯ функция: просто возвращает данные по ID, не проверяя,
    имеет ли текущий пользователь право на них.
    """
    if user_id in users_db:
        return users_db[user_id]
    return None

def get_user_profile_safe(current_user_id, requested_user_id):
    """
    БЕЗОПАСНАЯ функция: проверяет, что запрашиваемый ID совпадает
    с ID текущего пользователя.
    """
    if current_user_id == requested_user_id and requested_user_id in users_db:
        return users_db[requested_user_id]
    return None

if __name__ == "__main__":
    print("=== Уязвимый доступ (злоумышленник лезет к чужому профилю) ===")
    profile = get_user_profile_vulnerable(124)
    print("Доступ получен к:", profile)

    print("\n=== Безопасный доступ ===")
    # Андрей (текущий пользователь) пытается запросить чужой профиль
    profile_safe = get_user_profile_safe(current_user_id=123, requested_user_id=124)
    print("Доступ отклонён:", profile_safe)
    # Андрей запрашивает свой профиль
    profile_ok = get_user_profile_safe(current_user_id=123, requested_user_id=123)
    print("Доступ к своему профилю:", profile_ok)
