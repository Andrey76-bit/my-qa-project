import hashlib

# УЯЗВИМЫЙ способ: храним пароль как обычный текст
def store_password_plain(password):
    return password  # Просто возвращаем строку

def check_password_plain(stored_password, user_password):
    return stored_password == user_password

# БЕЗОПАСНЫЙ способ: храним хеш пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password_hashed(stored_hash, user_password):
    return stored_hash == hash_password(user_password)

if __name__ == "__main__":
    password = "SuperSecret123"

    print("=== Уязвимое хранение пароля ===")
    stored_plain = store_password_plain(password)
    print("Хранится в базе:", stored_plain)
    print("Проверка входа:", check_password_plain(stored_plain, "SuperSecret123"))

    print("\n=== Безопасное хранение (хеш) ===")
    stored_hash = hash_password(password)
    print("Хранится в базе (хеш):", stored_hash)
    print("Проверка входа (верный пароль):", check_password_hashed(stored_hash, "SuperSecret123"))
    print("Проверка входа (неверный пароль):", check_password_hashed(stored_hash, "WrongPass"))
