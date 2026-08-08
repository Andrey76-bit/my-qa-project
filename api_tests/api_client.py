import requests

class JSONPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_user(self, user_id):
        url = f"{self.BASE_URL}/users/{user_id}"
        response = requests.get(url)
        return response

    def get_all_users(self):
        url = f"{self.BASE_URL}/users"
        response = requests.get(url)
        return response
