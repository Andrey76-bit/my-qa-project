import sqlite3

# Подключаемся к нашей старой знакомой — базе test.db
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Создаём таблицу заказов, если её ещё нет, и добавляем данные
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product TEXT,
        price REAL,
        order_date TEXT
    )
""")

# Вставляем несколько заказов от разных пользователей и с разными датами
sample_data = [
    (1, 1, 'Книга', 500, '2025-01-01'),
    (2, 1, 'Ручка', 10, '2025-01-05'),
    (3, 1, 'Ноутбук', 1500, '2025-02-01'),
    (4, 2, 'Мышь', 700, '2025-01-10'),
    (5, 2, 'Клавиатура', 800, '2025-01-20'),
]
cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", sample_data)
conn.commit()

print("--- Анализ заказов с помощью LAG и LEAD ---")

# Наш SQL-запрос с оконными функциями (работает в SQLite 3.25+)
query = """
SELECT 
    user_id,
    product,
    price,
    order_date,
    LAG(price) OVER (PARTITION BY user_id ORDER BY order_date) AS "Предыдущая цена",
    LEAD(price) OVER (PARTITION BY user_id ORDER BY order_date) AS "Следующая цена"
FROM orders
ORDER BY user_id, order_date;
"""

cursor.execute(query)
rows = cursor.fetchall()

# Выводим результат красиво
print(f"{'User ID':<10} {'Товар':<15} {'Цена':<10} {'Дата':<12} {'Пред. цена':<15} {'След. цена':<15}")
print("-" * 85)
for row in rows:
    user_id, product, price, order_date, prev_price, next_price = row
    print(f"{user_id:<10} {product:<15} {price:<10} {order_date:<12} {str(prev_price):<15} {str(next_price):<15}")

# Автоматическая проверка (тест): для первого заказа пользователя предыдущей цены быть не должно
assert rows[0][4] is None, "Ошибка: у первого заказа должна быть NULL предыдущая цена!"
print("\n✅ Все проверки пройдены! Оконные функции работают как часы.")

conn.close()
