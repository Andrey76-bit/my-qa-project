import pytest
from api_client import JSONPlaceholderClient

# Это фикстура — она создаёт клиент и отдаёт его тестам
@pytest.fixture
def client():
    return JSONPlaceholderClient()

# Теперь каждый тест может "попросить" client, и pytest передаст его
@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_get_single_user(client, user_id):
    """Проверяем структуру данных для каждого пользователя из списка"""
    response = client.get_user(user_id)
    assert response.status_code == 200, f"Пользователь {user_id} не найден (статус {response.status_code})"
    user = response.json()
    assert "name" in user, f"У пользователя {user_id} нет поля name"
    assert "email" in user, f"У пользователя {user_id} нет поля email"
    assert user["id"] == user_id, f"Ожидался id={user_id}, а получен {user['id']}"

def test_get_all_users(client):
    """Проверяем, что список пользователей не пустой и содержит 10 элементов"""
    response = client.get_all_users()
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 10, f"Ожидалось 10 пользователей, а получено {len(users)}"

def test_create_user(client):
    """Проверяем создание нового пользователя (POST)"""
    new_user_data = {
        "name": "Андрей",
        "username": "andrey76",
        "email": "andrey@example.com"
    }
    response = client.create_user(new_user_data)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["name"] == "Андрей"
    assert created_user["email"] == "andrey@example.com"
    assert "id" in created_user

def test_update_user(client):
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
    assert updated_user["id"] == 1

def test_delete_user(client):
    """Проверяем удаление пользователя (DELETE)"""
    response = client.delete_user(1)
    assert response.status_code == 200
