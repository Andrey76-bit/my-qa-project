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

# Словари переводов
MESSAGES = {
    "ru": {
        "found": "Найдено: {}",
        "not_found": "Не найдено",
        "specify_id": "Укажите параметр id, например: /?id=1",
        "error": "Ошибка SQL: {}",
        "title": "Тестовый сервер",
    },
    "en": {
        "found": "Found: {}",
        "not_found": "Not found",
        "specify_id": "Specify id parameter, e.g., /?id=1",
        "error": "SQL Error: {}",
        "title": "Test Server",
    }
}

DEFAULT_LANG = "ru"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        user_id = params.get("id", [None])[0]
        lang = params.get("lang", [DEFAULT_LANG])[0]
        if lang not in MESSAGES:
            lang = DEFAULT_LANG
        msg = MESSAGES[lang]

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
                    response = msg["found"].format(rows)
                else:
                    response = msg["not_found"]
            except Exception as e:
                conn.close()
                response = msg["error"].format(e)
        else:
            response = msg["specify_id"]

        # Отправляем HTML с заголовком на нужном языке
        html = f"<html><head><title>{msg['title']}</title></head><body>{response}</body></html>"
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
    print("Сервер запущен на http://127.0.0.1:8000")
    print("Пример: http://127.0.0.1:8000/?id=1&lang=ru")
    print("Пример: http://127.0.0.1:8000/?id=1&lang=en")
    server.serve_forever()
