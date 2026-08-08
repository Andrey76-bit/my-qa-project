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
    assert "name" in user
    assert "email" in user
    assert "address" in user
    assert user["name"] == "Leanne Graham"

def test_create_user():
    """Проверяем создание нового пользователя (POST)"""
    new_user_data = {
        "name": "Андрей",
        "username": "andrey76",
        "email": "andrey@example.com"
    }
    response = client.create_user(new_user_data)
    assert response.status_code == 201  # 201 Created
    created_user = response.json()
    assert created_user["name"] == "Андрей"
    assert created_user["email"] == "andrey@example.com"
    assert "id" in created_user  # сервер должен присвоить ID

def test_update_user():
    """Проверяем полное обновление пользователя (PUT)"""
    updated_data = {
        "name": "Андрей Обновлённый",
        "username": "andrey_new",
        "email": "andrey_new@example.com"
    }
    response = client.update_user(1, updated_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Андрей Обновлённый"
    assert updated_user["id"] == 1  # ID не должен измениться

def test_delete_user():
    """Проверяем удаление пользователя (DELETE)"""
    response = client.delete_user(1)
    assert response.status_code == 200
    # Обычно DELETE возвращает пустое тело или подтверждение
