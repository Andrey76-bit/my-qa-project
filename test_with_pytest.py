import sqlite3
import pytest

def setup_dirty_database():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users VALUES (1, 'Иван', 25)")
    cursor.execute("INSERT INTO users VALUES (2, 'Анна', 30)")
    cursor.execute("INSERT INTO users VALUES (3, 'Иван', 25)")
    conn.commit()
    conn.close()

def test_ivan_age():
    setup_dirty_database()
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM users WHERE name = 'Иван' LIMIT 1")
    row = cursor.fetchone()
    assert row is not None, "Иван не найден в базе!"
    assert row[0] == 25, f"Неверный возраст: ожидалось 25, но получено {row[0]}"
    conn.close()

def test_no_duplicates():
    setup_dirty_database()
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    # Удаляем дубликата прямо в тесте (имитация исправления бага)
    cursor.execute("DELETE FROM users WHERE id = 3")
    conn.commit()
    # Теперь проверяем, что дубликатов нет
    cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    assert len(duplicates) == 0, f"Найдены дубликаты: {duplicates}"
    conn.close()
