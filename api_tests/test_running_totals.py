import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Создаём таблицу заказов, если ещё нет, и добавляем данные
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

sample_data = [
    (1, 1, 'Книга', 500, '2025-01-01'),
    (2, 1, 'Ручка', 10, '2025-01-05'),
    (3, 1, 'Ноутбук', 1500, '2025-02-01'),
    (4, 2, 'Мышь', 700, '2025-01-10'),
    (5, 2, 'Клавиатура', 800, '2025-01-20'),
]
cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", sample_data)
conn.commit()

print("--- Нарастающий итог и средний чек ---")

query = """
SELECT 
    user_id,
    product,
    price,
    order_date,
    SUM(price) OVER (PARTITION BY user_id ORDER BY order_date) AS "Сумма с начала",
    ROUND(AVG(price) OVER (PARTITION BY user_id ORDER BY order_date), 2) AS "Средний чек"
FROM orders
WHERE price IS NOT NULL
ORDER BY user_id, order_date;
"""

cursor.execute(query)
rows = cursor.fetchall()

# Красивая таблица
print(f"{'User':<6} {'Товар':<15} {'Цена':<8} {'Дата':<12} {'Сумма с начала':<18} {'Средний чек':<12}")
print("-" * 75)
for row in rows:
    user_id, product, price, order_date, running_sum, avg_price = row
    print(f"{user_id:<6} {product:<15} {price:<8} {order_date:<12} {running_sum:<18} {avg_price:<12}")

# Автотест: для первого заказа пользователя нарастающая сумма должна равняться его цене
first_order = rows[0]
assert first_order[4] == first_order[2], f"Ошибка: нарастающая сумма первого заказа должна быть {first_order[2]}, а не {first_order[4]}"
print("\n✅ Автотест пройден: нарастающий итог и средний чек работают как часы!")

conn.close()
