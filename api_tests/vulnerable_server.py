from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import urllib.parse

# Создаём базу данных при запуске
conn = sqlite3.connect("test_vuln.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'SuperSecret123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('andrey', 'MyPass777')")
conn.commit()
conn.close()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        user_id = params.get("id", [None])[0]

        if user_id is not None:
            # УЯЗВИМО: прямая подстановка в SQL-запрос
            query = f"SELECT username, password FROM users WHERE id = {user_id}"
            conn = sqlite3.connect("test_vuln.db")
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.close()
                if rows:
                    response = f"Найдено: {rows}"
                else:
                    response = "Не найдено"
            except Exception as e:
                conn.close()
                response = f"Ошибка SQL: {e}"
        else:
            response = "Укажите параметр id, например: /?id=1"

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
    print("Сервер запущен на http://127.0.0.1:8000")
    print("Пример: http://127.0.0.1:8000/?id=1")
    server.serve_forever()
