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
