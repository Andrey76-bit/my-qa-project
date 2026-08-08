import requests

def test_get_user():
    url = "https://jsonplaceholder.typicode.com/users/1"
    response = requests.get(url)
    assert response.status_code == 200, f"Сервер не ответил 200, ответил {response.status_code}"
    data = response.json()
    assert data['name'] == "Leanne Graham", f"Имя не совпадает, получили {data['name']}"
    print("API Test PASSED: пользователь найден, имя Leanne Graham.")
