import re

def fetch_url_vulnerable(url):
    """УЯЗВИМАЯ функция: обращается по любому URL без проверки"""
    print(f"[УЯЗВИМО] Запрашиваю {url}")
    # В реальности здесь был бы requests.get(url) или что-то подобное
    # Для демонстрации просто возвращаем результат, будто запрос выполнен
    if "localhost" in url or "127.0.0.1" in url:
        return "Внутренний ресурс доступен: секретная информация!"
    return "Загружен внешний ресурс"

def fetch_url_safe(url):
    """БЕЗОПАСНАЯ функция: запрещает доступ к внутренним адресам"""
    print(f"[БЕЗОПАСНО] Проверяю {url}")
    # Запрещаем localhost и приватные IP
    if re.search(r'(localhost|127\.0\.0\.1|192\.168\.|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)', url):
        return "Доступ запрещён: запрос к внутренним ресурсам"
    return "Загружен внешний ресурс"

if __name__ == "__main__":
    print("=== Атака SSRF (уязвимая функция) ===")
    print(fetch_url_vulnerable("http://localhost/admin"))
    print(fetch_url_vulnerable("http://192.168.1.1/secret"))

    print("\n=== Защита от SSRF (безопасная функция) ===")
    print(fetch_url_safe("http://localhost/admin"))
    print(fetch_url_safe("http://192.168.1.1/secret"))
    print(fetch_url_safe("https://example.com/image.jpg"))
