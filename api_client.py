import requests

class JSONPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_user(self, user_id):
        """Получить одного пользователя по ID"""
        url = f"{self.BASE_URL}/users/{user_id}"
        response = requests.get(url)
        return response

    def get_all_users(self):
        """Получить список всех пользователей"""
        url = f"{self.BASE_URL}/users"
        response = requests.get(url)
        return response

    def create_user(self, user_data):
        """Создать нового пользователя (POST)"""
        url = f"{self.BASE_URL}/users"
        response = requests.post(url, json=user_data)
        return response

    def update_user(self, user_id, user_data):
        """Полностью обновить пользователя (PUT)"""
        url = f"{self.BASE_URL}/users/{user_id}"
        response = requests.put(url, json=user_data)
        return response

    def delete_user(self, user_id):
        """Удалить пользователя (DELETE)"""
        url = f"{self.BASE_URL}/users/{user_id}"
        response = requests.delete(url)
        return response
