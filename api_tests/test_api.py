import pytest
from api_client import JSONPlaceholderClient

client = JSONPlaceholderClient()

def test_get_all_users():
    """Проверяем, что список пользователей не пустой и содержит 10 элементов"""
    response = client.get_all_users()
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 10, f"Ожидалось 10 пользователей, а получено {len(users)}"

def test_get_single_user():
    """Проверяем структуру данных одного пользователя"""
    response = client.get_user(1)
    assert response.status_code == 200
    user = response.json()
    # Проверяем, что у пользователя есть обязательные поля
    assert "name" in user
    assert "email" in user
    assert "address" in user
    assert user["name"] == "Leanne Graham"
