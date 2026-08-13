import pickle
import json
import hmac
import hashlib

SECRET_KEY = b"supersecretkey"

class User:
    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin

def serialize_user_vulnerable(user):
    """УЯЗВИМАЯ сериализация: используем pickle (небезопасно)"""
    return pickle.dumps(user)

def deserialize_user_vulnerable(payload):
    """УЯЗВИМАЯ десериализация: доверяем любым данным, которые нам пришли"""
    print("[УЯЗВИМО] Десериализуем pickle...")
    return pickle.loads(payload)

def serialize_user_safe(user):
    """БЕЗОПАСНАЯ сериализация: используем JSON и добавляем HMAC-подпись"""
    data = json.dumps({"username": user.username, "is_admin": user.is_admin}).encode()
    signature = hmac.new(SECRET_KEY, data, hashlib.sha256).hexdigest()
    return data, signature

def deserialize_user_safe(data, signature):
    """БЕЗОПАСНАЯ десериализация: проверяем подпись перед использованием"""
    expected_signature = hmac.new(SECRET_KEY, data, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_signature, signature):
        print("[БЕЗОПАСНО] Подпись не совпала! Данные могли быть изменены.")
        return None
    print("[БЕЗОПАСНО] Подпись верна, загружаем данные...")
    user_dict = json.loads(data.decode())
    return User(user_dict["username"], user_dict["is_admin"])

if __name__ == "__main__":
    print("=== Атака на уязвимую сериализацию ===")
    # Злоумышленник создаёт поддельный payload, используя pickle
    admin_user = User("hacker", is_admin=True)
    malicious_payload = pickle.dumps(admin_user)
    # Уязвимая функция без проверки загрузит поддельного админа
    loaded_vulnerable = deserialize_user_vulnerable(malicious_payload)
    print(f"Получен пользователь: {loaded_vulnerable.username}, is_admin={loaded_vulnerable.is_admin}")

    print("\n=== Защита через подпись ===")
    # Безопасная сериализация обычного пользователя
    normal_user = User("andrey", is_admin=False)
    data, sig = serialize_user_safe(normal_user)
    print(f"Отправляем данные: {data.decode()}, подпись: {sig}")

    # Злоумышленник пытается подменить JSON на is_admin=True, не зная SECRET_KEY
    forged_data = b'{"username": "hacker", "is_admin": true}'
    # Безопасная функция отвергнет подделку
    loaded_safe_forged = deserialize_user_safe(forged_data, sig)  # подпись от нормального пользователя не совпадёт
    if loaded_safe_forged is None:
        print("Подделка не удалась: подпись не совпадает.")
    else:
        print(f"Подделка прошла! {loaded_safe_forged.username}, is_admin={loaded_safe_forged.is_admin}")

    # А если подпись правильная?
    loaded_safe_valid = deserialize_user_safe(data, sig)
    print(f"Валидные данные: {loaded_safe_valid.username}, is_admin={loaded_safe_valid.is_admin}")
