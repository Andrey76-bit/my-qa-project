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
        "enter_id": "Введите ID пользователя:",
        "search": "Найти",
        "current_lang": "Текущий язык:",
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
        "enter_id": "Enter user ID:",
        "search": "Search",
        "current_lang": "Current language:",
    }
}

DEFAULT_LANG = "ru"

CSS = """
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    margin: 40px;
    color: #333;
}
.container {
    max-width: 600px;
    margin: auto;
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
h1 {
    color: #2c3e50;
}
a {
    color: #3498db;
    text-decoration: none;
    margin: 0 5px;
}
a:hover {
    text-decoration: underline;
}
label {
    display: block;
    margin-top: 15px;
    font-weight: bold;
}
input[type="text"] {
    width: 80%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
button {
    padding: 8px 15px;
    margin-left: 5px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
button:hover {
    background-color: #2980b9;
}
.result {
    margin-top: 20px;
    padding: 10px;
    background: #ecf0f1;
    border-radius: 5px;
}
"""
class RequestHandler(BaseHTTPRequestHandler):
    def _get_lang_from_cookie(self):
        if 'Cookie' in self.headers:
            cookie = cookies.SimpleCookie()
            cookie.load(self.headers['Cookie'])
            if 'lang' in cookie:
                lang = cookie['lang'].value
                if lang in MESSAGES:
                    return lang
        return DEFAULT_LANG

    def _set_lang_cookie(self, lang):
        self.send_header('Set-Cookie', f'lang={lang}; Path=/')

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

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
                    response = msg["found"].format(rows)
                else:
                    response = msg["not_found"]
            except Exception as e:
                conn.close()
                response = msg["error"].format(e)
        else:
            response = msg["specify_id"]

        html = f"""<html>
<head><title>{msg['title']}</title><style>{CSS}</style></head>
<body>
<div class="container">
    <h1>{msg['title']}</h1>
    <p>{msg['choose_language']} <a href="/?set_lang=ru">{msg['russian']}</a> | <a href="/?set_lang=en">{msg['english']}</a></p>
    <hr>
    <form action="/" method="get">
        <label for="id">{msg['enter_id']}</label>
        <input type="text" id="id" name="id" placeholder="1">
        <button type="submit">{msg['search']}</button>
    </form>
    <div class="result">{response}</div>
    <p>{msg['current_lang']} {lang}</p>
</div>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
    print("Сервер запущен на http://127.0.0.1:8000")
    print("Для выбора языка используйте ссылки или форму")
    server.serve_forever()
