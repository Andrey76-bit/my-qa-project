import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'SuperSecret123')")
conn.commit()

def vulnerable_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[УЯЗВИМЫЙ ЗАПРОС] {query}")
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result is not None

def safe_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"[БЕЗОПАСНЫЙ ЗАПРОС] {query} с параметрами: ({username}, {password})")
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

if __name__ == "__main__":
    print("=== Обычный вход ===")
    print("Уязвимая функция:", vulnerable_login("admin", "SuperSecret123"))
    print("Безопасная функция:", safe_login("admin", "SuperSecret123"))
    print()
    print("=== Атака SQL-инъекцией ===")
    print("Уязвимая функция:", vulnerable_login("admin", "' OR '1'='1"))
    print("Безопасная функция:", safe_login("admin", "' OR '1'='1"))
