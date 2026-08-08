import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Удаляем таблицу, если она есть, и создаем новую, правильную
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

# Вставляем Ивана с возрастом 25
cursor.execute("INSERT OR REPLACE INTO users (id, name, age) VALUES (1, \"Иван\", 25)")
conn.commit()

# Проверяем
cursor.execute("SELECT age FROM users WHERE name = \"Иван\"")
result = cursor.fetchone()
expected_age = 25

if result and result[0] == expected_age:
    print("ТЕСТ ПРОЙДЕН! Возраст Ивана = " + str(result[0]) + ", как и ожидалось.")
else:
    print("БАГ! Что-то пошло не так. Ожидался " + str(expected_age) + ", а в базе что-то другое.")
    if result:
        print("Реальный возраст в базе:", result[0])
    else:
        print("Иван не найден в базе.")

conn.close()
