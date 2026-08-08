sudo apt install fonts-noto-color-emoji -y
sudo apt install ttf-mscorefonts-installer fonts-noto fonts-symbola -y
sudo fc-cache -fv
python3 --version
print("Hello, брат!")
nano hello.py
python3 hello.py
nano hello.py
python3 hello.py
echo 'name = input("Привет, воин! Как тебя зовут? ")
print("Здравствуй, " + name + "! Добро пожаловать в мир Linux и Python, мой брат!")' > hello_andrey.py
python3 hello_andrey.py
nano check_number.py
python3 check_number.py
7
0
nano check_number.py
nano test_calc.py
python3 test_calc.py
nano test_calc.py
python3 test_calc.py
python3 hello.py
# Тест 3: проверка с отрицательным числом
result = summa(-5, 5)
if result == 0:;     print("Тест 3: PASSED (-5 + 5 = " + str(result) + ")")
else:
[200~# Тест 3: проверка с отрицательным числом
result = summa(-5, 5)
if result == 0:;     print("Тест 3: PASSED (-5 + 5 = " + str(result) + ")")
else:
nano test_calc.py
python3 test_calc.py
nano test_division.py
python3 test_division.py
nano sqlite_test.py
python3 sqlite_test.py
nano sqlite_test.py
sudo apt update && sudo apt install sqlite3 python3-pip -y
cd ~
python3 sqlite_test.py
echo 'import sqlite3
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
print("Готово.")' > sqlite_debug.py
python3 sqlite_debug.py
python3 sqlite_debug.pyecho 'import sqlite3

# Подключаемся к базе (если её нет, она создастся)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Создаем таблицу и добавляем Ивана, если его ещё нет
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (1, \"Иван\", 25)")
conn.commit()

# Наш первый АВТОМАТИЧЕСКИЙ ТЕСТ!
cursor.execute("SELECT age FROM users WHERE name = \"Иван\"")
result = cursor.fetchone()
expected_age = 25

if result and result[0] == expected_age:
    print("ТЕСТ ПРОЙДЕН! Возраст Ивана = " + str(result[0]) + ", как и ожидалось.")
else:
    print("БАГ! Что-то пошло не так. Ожидался " + str(expected_age) + ", а в базе что-то другое.")

conn.close()' > test_db.pypython3 test_db.py
rm test.db
python3 test_db.py
cd ~
echo 'import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (1, \"Иван\", 25)")
conn.commit()

cursor.execute("SELECT age FROM users WHERE name = \"Иван\"")
result = cursor.fetchone()
expected_age = 25

if result and result[0] == expected_age:
    print("ТЕСТ ПРОЙДЕН! Возраст Ивана = " + str(result[0]) + ", как и ожидалось.")
else:
    print("БАГ! Что-то пошло не так. Ожидался " + str(expected_age) + ", а в базе что-то другое.")

conn.close()' > test_db.pycd ~
rm -f test.db
echo 'import sqlite3

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

conn.close()' > test_db.py
python3 test_db.py
ntecho 'import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Подготавливаем таблицу (как раньше, но теперь добавим второго Ивана для наглядности)
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, \"Иван\", 25)")
cursor.execute("INSERT INTO users VALUES (2, \"Анна\", 30)")
cursor.execute("INSERT INTO users VALUES (3, \"Иван\", 25)")  # <-- дубликат!
conn.commit()

# ======== ТЕСТ 1: возраст Ивана = 25 ========
print("--- Тест 1: Проверка возраста Ивана ---")
cursor.execute("SELECT age FROM users WHERE name = \"Иван\" LIMIT 1")
row = cursor.fetchone()
expected = 25
if row and row[0] == expected:
    print("PASSED: возраст первого Ивана =", row[0])
else:
    print("FAILED: ожидалось", expected, "получено", row)

# ======== ТЕСТ 2: нет дубликатов по имени ========
print("--- Тест 2: Проверка на дубликаты ---")
cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
if duplicates:
    print("FAILED! Найдены дубликаты:")
    for name, cnt in duplicates:
        print("  -", name, "встречается", cnt, "раз(а)")
else:
    print("PASSED: дубликатов имён нет.")

conn.close()' > test_users.py
echo 'import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Подготавливаем таблицу (как раньше, но теперь добавим второго Ивана для наглядности)
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, \"Иван\", 25)")
cursor.execute("INSERT INTO users VALUES (2, \"Анна\", 30)")
cursor.execute("INSERT INTO users VALUES (3, \"Иван\", 25)")  # <-- дубликат!
conn.commit()

# ======== ТЕСТ 1: возраст Ивана = 25 ========
print("--- Тест 1: Проверка возраста Ивана ---")
cursor.execute("SELECT age FROM users WHERE name = \"Иван\" LIMIT 1")
row = cursor.fetchone()
expected = 25
if row and row[0] == expected:
    print("PASSED: возраст первого Ивана =", row[0])
else:
    print("FAILED: ожидалось", expected, "получено", row)

# ======== ТЕСТ 2: нет дубликатов по имени ========
print("--- Тест 2: Проверка на дубликаты ---")
cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
if duplicates:
    print("FAILED! Найдены дубликаты:")
    for name, cnt in duplicates:
        print("  -", name, "встречается", cnt, "раз(а)")
else:
    print("PASSED: дубликатов имён нет.")

conn.close()' > test_users.pypython3 test_users.py
cd ~
echo 'import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, \"Иван\", 25)")
cursor.execute("INSERT INTO users VALUES (2, \"Анна\", 30)")
cursor.execute("INSERT INTO users VALUES (3, \"Иван\", 25)")
conn.commit()

print("--- Тест 1: Проверка возраста Ивана ---")
cursor.execute("SELECT age FROM users WHERE name = \"Иван\" LIMIT 1")
row = cursor.fetchone()
expected = 25
if row and row[0] == expected:
    print("PASSED: возраст первого Ивана =", row[0])
else:
    print("FAILED: ожидалось", expected, "получено", row)

print("--- Тест 2: Проверка на дубликаты ---")
cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
if duplicates:
    print("FAILED! Найдены дубликаты:")
    for name, cnt in duplicates:
        print("  -", name, "встречается", cnt, "раз(а)")
else:
    print("PASSED: дубликатов имён нет.")

conn.close()' > test_users.py
python3 test_users.py
echo 'import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Подготавливаем таблицу и данные (тот же "грязный" набор)
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, \"Иван\", 25)")
cursor.execute("INSERT INTO users VALUES (2, \"Анна\", 30)")
cursor.execute("INSERT INTO users VALUES (3, \"Иван\", 25)")
conn.commit()

# ======== ТЕСТ 1: возраст Ивана = 25 ========
print("--- Тест 1: Проверка возраста Ивана ---")
cursor.execute("SELECT age FROM users WHERE name = \"Иван\" LIMIT 1")
row = cursor.fetchone()
expected = 25
if row and row[0] == expected:
    print("PASSED: возраст первого Ивана =", row[0])
else:
    print("FAILED: ожидалось", expected, "получено", row)

# ======== ТЕСТ 2: поиск дубликатов (до исправления) ========
print("--- Тест 2: Проверка на дубликаты (до исправления) ---")
cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
if duplicates:
    print("FAILED! Найдены дубликаты:")
    for name, cnt in duplicates:
        print("  -", name, "встречается", cnt, "раз(а)")
    # Тут мы "чиним" баг: удаляем второго Ивана
    cursor.execute("DELETE FROM users WHERE id = 3")
    conn.commit()
    print(">>> Баг исправлен: дубликат удалён. Запускаем проверку заново...")
else:
    print("PASSED: дубликатов имён нет.")

# ======== ТЕСТ 2 (повторно, после исправления) ========
print("--- Тест 2: Проверка на дубликаты (после исправления) ---")
cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
if duplicates:
    print("FAILED! Остались дубликаты:")
    for name, cnt in duplicates:
        print("  -", name, "встречается", cnt, "раз(а)")
else:
    print("PASSED: дубликатов имён нет.")

conn.close()' > test_fix.pypython3 test_fix.py
python3 test_fix.py
cat > test_fix.py << 'EOF'
import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, \"Иван\", 25)")
cursor.execute("INSERT INTO users VALUES (2, \"Анна\", 30)")
cursor.execute("INSERT INTO users VALUES (3, \"Иван\", 25)")
conn.commit()

print("--- Тест 1: Проверка возраста Ивана ---")
cursor.execute("SELECT age FROM users WHERE name = \"Иван\" LIMIT 1")
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


cat > test_fix.py << 'EOF'
import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, \"Иван\", 25)")
cursor.execute("INSERT INTO users VALUES (2, \"Анна\", 30)")
cursor.execute("INSERT INTO users VALUES (3, \"Иван\", 25)")
conn.commit()

print("--- Тест 1: Проверка возраста Ивана ---")
cursor.execute("SELECT age FROM users WHERE name = \"Иван\" LIMIT 1")
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



EOF

python3 test_fix.py
sudo apt install python3-pytest -y
python3 -m pytest test_with_pytest.py -v
pwd
ls -l test*.py
mv 'Несохранённый документ 1' test_with_pytest.py
ls -l test_with_pytest.py
ls -l
rm -rf test_with_pytest.py
cat > test_with_pytest.py << 'EOF'
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
    cursor.execute("SELECT name, COUNT(*) FROM users GROUP BY name HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    assert len(duplicates) == 0, f"Найдены дубликаты: {duplicates}"
    conn.close()
EOF

python3 -m pytest test_with_pytest.py -v
cat > test_with_pytest.py << 'EOF'
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
EOF

python3 -m pytest test_with_pytest.py -v
cat > test_random_math.py << 'EOF'
import random
import pytest

def test_addition_identity():
    """Проверяем, что для 100 случайных чисел х+0 всегда равно х"""
    for i in range(100):          # Повторить 100 раз
        x = random.randint(-1000, 1000)   # Случайное число от -1000 до 1000
        assert x + 0 == x, f"ОШИБКА: {x} + 0 != {x} (итерация {i})"

def test_multiplication_identity():
    """Проверяем, что для 100 случайных чисел х*1 всегда равно х"""
    for i in range(100):
        x = random.randint(-1000, 1000)
        assert x * 1 == x, f"ОШИБКА: {x} * 1 != {x} (итерация {i})"
EOF

python3 -m pytest test_random_math.py -v
cat > test_password_police.py << 'EOF'
import random
import string
import pytest

def generate_random_password():
    """Генерирует абсолютно случайную строку, которая может быть плохим паролем"""
    length = random.randint(4, 12)  # Длина от 4 до 12 (многие будут короткими)
    # В наборе буквы, цифры и немного спецсимволов
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def validate_password(pwd):
    """Проверяет пароль на соответствие правилам. Возвращает список ошибок."""
    errors = []
    if len(pwd) < 8:
        errors.append(f"Слишком короткий (длина {len(pwd)})")
    if not any(c.isupper() for c in pwd):
        errors.append("Нет заглавной буквы")
    if not any(c.isdigit() for c in pwd):
        errors.append("Нет цифры")
    if not any(c in "!@#$%^&*()" for c in pwd):
        errors.append("Нет спецсимвола")
    return errors

@pytest.mark.parametrize("test_number", range(1000))  # Запускаем тест 1000 раз
def test_random_password_security(test_number):
    """Проверяем 1000 случайных паролей"""
    pwd = generate_random_password()
    errors = validate_password(pwd)
    # assert с понятным сообщением — если ошибки есть, тест упадёт
    assert len(errors) == 0, f"Пароль '{pwd}' не прошёл проверку: {', '.join(errors)}"
EOF

python3 -m pytest test_password_police.py -v
curl https://jsonplaceholder.typicode.com/users
curl https://jsonplaceholder.typicode.com/users/1
sudo apt install python3-requests -y
cat > test_api.py << 'EOF'
import requests

def test_get_user():
    url = "https://jsonplaceholder.typicode.com/users/1"
    response = requests.get(url)   # Отправляем GET-запрос
    assert response.status_code == 200, f"Сервер не ответил 200, ответил {response.status_code}"
    data = response.json()         # Превращаем JSON в словарь
    assert data['name'] == "Leanne Graham", f"Имя не совпадает, получили {data['name']}"
    print("API Test PASSED: пользователь найден, имя Leanne Graham.")
EOFcat > test_api.py << 'EOF'
import requests

def test_get_user():
    url = "https://jsonplaceholder.typicode.com/users/1"
    response = requests.get(url)   # Отправляем GET-запрос
    assert response.status_code == 200, f"Сервер не ответил 200, ответил {response.status_code}"
    data = response.json()         # Превращаем JSON в словарь
    assert data['name'] == "Leanne Graham", f"Имя не совпадает, получили {data['name']}"
    print("API Test PASSED: пользователь найден, имя Leanne Graham.")
EOFpython3 test_api.py

python3 test_api.py
nano test_api.py
python3 test_api.py
nano test_api.py
python3 test_api.py
rm test_api.py
echo "import requests" > test_api.py
echo "" >> test_api.py
echo "def test_get_user():" >> test_api.py
echo "    url = \"https://jsonplaceholder.typicode.com/users/1\"" >> test_api.pyecho "    response = requests.get(url)" >> test_api.py
echo "    data = response.json()" >> test_api.py
echo "    assert data['name'] == \"Leanne Graham\", f\"Имя не совпадает, получили {data['name']}\"" >> test_api.py
echo "    print(\"API Test PASSED: пользователь найден, имя Leanne Graham.\")" >> test_api.py
cat test_api.py
rm test_api.py
python3 test_api.py
echo "aW1wb3J0IHJlcXVlc3RzCgpkZWYgdGVzdF9nZXRfdXNlcigpOgogICAgdXJsID0gImh0dHBzOi8vanNvbnBsYWNlaG9sZGVyLnR5cGljb2RlLmNvbS91c2Vycy8xIgogICAgcmVzcG9uc2UgPSByZXF1ZXN0cy5nZXQodXJsKQogICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgZiJTZXJ2ZXIgbm90IHJlc3BvbmRlZCAyMDAsIHJlc3BvbmRlZCB7cmVzcG9uc2Uuc3RhdHVzX2NvZGV9IgogICAgZGF0YSA9IHJlc3BvbnNlLmpzb24oKQogICAgYXNzZXJ0IGRhdGFbJ25hbWUnXSA9PSAiTGVhbm5lIEdyYWhhbSIsIGYiSW1hIG5lIHNvdnBhZGFldCwgcG9sdWNoZW5vIHtkYXRhWyduYW1lJ119IgogICAgcHJpbnQoIkFQSSBUZXN0IFBBU1NFRDogcG9sa3pvdmF0ZWwgZm91bmQsIGltamEgTGVhbm5lIEdyYWhhbS4iKQ==" | base64 -d > test_api.py
cat test_api.py
python3 test_api.py
python3 -m pytest test_api.py -v
sudo apt install fonts-noto-color-emoji -y
sudo fc-cache -fv
