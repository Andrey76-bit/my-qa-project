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

print("--- Полный набор оконных функций: COUNT, MIN, MAX ---")

# Наш запрос из full_analytics.sql
query = """
SELECT 
    user_id,
    product,
    price,
    order_date,
    COUNT(*) OVER (PARTITION BY user_id ORDER BY order_date) AS "Заказов всего",
    MIN(price) OVER (PARTITION BY user_id ORDER BY order_date) AS "Мин. чек",
    MAX(price) OVER (PARTITION BY user_id ORDER BY order_date) AS "Макс. чек"
FROM orders
WHERE price IS NOT NULL
ORDER BY user_id, order_date;
"""

cursor.execute(query)
rows = cursor.fetchall()

# Красивая таблица
print(f"{'User':<6} {'Товар':<15} {'Цена':<8} {'Дата':<12} {'Всего заказов':<16} {'Мин. чек':<10} {'Макс. чек':<10}")
print("-" * 80)
for row in rows:
    user_id, product, price, order_date, cnt, min_price, max_price = row
    print(f"{user_id:<6} {product:<15} {price:<8} {order_date:<12} {cnt:<16} {min_price:<10} {max_price:<10}")

# Автотест: для первого заказа пользователя количество=1, мин.чек=цена, макс.чек=цена
first_order = rows[0]
assert first_order[4] == 1, f"Ошибка: у первого заказа количество должно быть 1, а не {first_order[4]}"
assert first_order[5] == first_order[2], f"Ошибка: мин. чек первого заказа должен быть {first_order[2]}, а не {first_order[5]}"
assert first_order[6] == first_order[2], f"Ошибка: макс. чек первого заказа должен быть {first_order[2]}, а не {first_order[6]}"
print("\n✅ Автотест пройден! COUNT, MIN, MAX OVER работают как часы.")

conn.close()
