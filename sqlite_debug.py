import sqlite3
import os

print("Скрипт запущен...")
print("Текущая папка:", os.getcwd())

# Создаем файл БД
conn = sqlite3.connect("test.db")
print("База данных создана/подключена.")

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, \"Иван\")")
conn.commit()
print("Данные добавлены.")

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Найдено строк:", len(rows))
for row in rows:
    print("Пользователь:", row)

conn.close()
print("Готово.")
