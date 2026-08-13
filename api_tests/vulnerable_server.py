from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import urllib.parse
from http import cookies

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
        "title": "Тестовый сервер",
        "choose_language": "Выберите язык:",
        "russian": "Русский",
        "english": "English",
        "found": "Найдено: {}",
        "not_found": "Не найдено",
        "specify_id": "Укажите параметр id, например: /?id=1",
        "error": "Ошибка SQL: {}",
    },
    "en": {
        "title": "Test Server",
        "choose_language": "Choose language:",
        "russian": "Russian",
        "english": "English",
        "found": "Found: {}",
        "not_found": "Not found",
        "specify_id": "Specify id parameter, e.g., /?id=1",
        "error": "SQL Error: {}",
    }
}

DEFAULT_LANG = "ru"

class RequestHandler(BaseHTTPRequestHandler):
    def _get_lang_from_cookie(self):
        """Читаем язык из cookie"""
        if 'Cookie' in self.headers:
            cookie = cookies.SimpleCookie()
            cookie.load(self.headers['Cookie'])
            if 'lang' in cookie:
                lang = cookie['lang'].value
                if lang in MESSAGES:
                    return lang
        return DEFAULT_LANG

    def _set_lang_cookie(self, lang):
        """Устанавливаем cookie с выбранным языком"""
        self.send_header('Set-Cookie', f'lang={lang}; Path=/')

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        # Проверяем, не пришёл ли запрос на смену языка
        if 'set_lang' in params:
            new_lang = params['set_lang'][0]
            if new_lang in MESSAGES:
                self._set_lang_cookie(new_lang)
                lang = new_lang
            else:
                lang = DEFAULT_LANG
        else:
            lang = self._get_lang_from_cookie()

        msg = MESSAGES[lang]

        # Получаем user_id из параметров
        user_id = params.get("id", [None])[0]
        if user_id is not None:
            # УЯЗВИМО: прямая подстановка в SQL-запрос (для демонстрации)
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

        # Строим HTML-страницу с выбором языка
        html = f"""<html>
<head><title>{msg['title']}</title></head>
<body>
    <h1>{msg['title']}</h1>
    <p>{msg['choose_language']} <a href="/?set_lang=ru">{msg['russian']}</a> | <a href="/?set_lang=en">{msg['english']}</a></p>
    <hr>
    <p>{response}</p>
    <p>Текущий язык: {lang}</p>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
    print("Сервер запущен на http://127.0.0.1:8000")
    print("Для выбора языка используйте ссылки на странице или ?set_lang=ru / ?set_lang=en")
    server.serve_forever()
