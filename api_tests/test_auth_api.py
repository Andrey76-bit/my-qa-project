import pytest
import requests
import json

class RestfulBookerClient:
    BASE_URL = "https://restful-booker.herokuapp.com"

    def get_token(self, username="admin", password="password123"):
        """Получаем токен-пропуск на КПП"""
        url = f"{self.BASE_URL}/auth"
        headers = {"Content-Type": "application/json"}
        body = {
            "username": username,
            "password": password
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        return response

    def create_booking(self, token):
        """Создаём бронь, предъявив токен"""
        url = f"{self.BASE_URL}/booking"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"  # Предъявляем пропуск
        }
        body = {
            "firstname": "Андрей",
            "lastname": "Тестировщик",
            "totalprice": 777,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-08-10",
                "checkout": "2026-08-13"
            },
            "additionalneeds": "Бойцовский настрой"
        }
        response = requests.post(url, headers=headers, json=body)
        return response

@pytest.fixture
def client():
    return RestfulBookerClient()

def test_get_token(client):
    """Тест 1: Проверяем, что токен получается корректно"""
    response = client.get_token()
    assert response.status_code == 200, f"Не смогли получить токен: {response.status_code}"
    data = response.json()
    assert "token" in data, "В ответе нет поля 'token'"
    print(f"✅ Токен получен: {data['token'][:15]}...")

def test_create_booking_with_auth(client):
    """Тест 2: Получаем токен и создаём бронь"""
    # Шаг 1: Забираем пропуск
    token_response = client.get_token()
    token = token_response.json()["token"]

    # Шаг 2: Действуем
    booking_response = client.create_booking(token)
    assert booking_response.status_code == 200, f"Не смогли создать бронь: {booking_response.status_code}"
    booking_data = booking_response.json()
    assert "bookingid" in booking_data, "В ответе нет ID брони"
    assert booking_data["booking"]["firstname"] == "Андрей"
    print(f"✅ Бронь создана! ID: {booking_data['bookingid']}, Гость: {booking_data['booking']['firstname']}")
