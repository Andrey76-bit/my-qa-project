import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, 'Иван', 25)")
cursor.execute("INSERT INTO users VALUES (2, 'Анна', 30)")
cursor.execute("INSERT INTO users VALUES (3, 'Иван', 25)")
conn.commit()

print("--- Тест 1: Проверка возраста Ивана ---")
cursor.execute("SELECT age FROM users WHERE name = 'Иван' LIMIT 1")
row = cursor.fetchone()
expected = 25
if row and row[0] == expected:
    print("PASSED: возраст первого Ивана =", row[0])
else:
    print("FAILED: ожидалось", expected, "получено", row)

print("--- Тест 2: Проверка на дубликаты (до исправления) ---")
cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
if duplicates:
    print("FAILED! Найдены дубликаты:")
    for name, cnt in duplicates:
        print("  -", name, "встречается", cnt, "раз(а)")
    cursor.execute("DELETE FROM users WHERE id = 3")
    conn.commit()
    print(">>> Баг исправлен: дубликат удалён. Запускаем проверку заново...")
else:
    print("PASSED: дубликатов имён нет.")

print("--- Тест 2: Проверка на дубликаты (после исправления) ---")
cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
if duplicates:
    print("FAILED! Остались дубликаты:")
    for name, cnt in duplicates:
        print("  -", name, "встречается", cnt, "раз(а)")
else:
    print("PASSED: дубликатов имён нет.")

conn.close()
