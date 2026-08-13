from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import urllib.parse
from http import cookies

# Создаём базу данных
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
        "mode_label": "Режим безопасности:",
        "vulnerable_mode": "Уязвимый режим",
        "secure_mode": "Защищённый режим",
        "admin_page": "Перейти на /admin",
        "admin_title": "Секретная страница администратора",
        "admin_secret": "Секретные данные: доступ разрешён!",
        "admin_access_denied": "Доступ запрещён. Вы не администратор.",
        "admin_instruction": "Введите id администратора (или используйте SQL-инъекцию в уязвимом режиме)",
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
        "mode_label": "Security mode:",
        "vulnerable_mode": "Vulnerable mode",
        "secure_mode": "Secure mode",
        "admin_page": "Go to /admin",
        "admin_title": "Admin Secret Page",
        "admin_secret": "Secret data: access granted!",
        "admin_access_denied": "Access denied. You are not admin.",
        "admin_instruction": "Enter admin id (or use SQL injection in vulnerable mode)",
    }
}

DEFAULT_LANG = "ru"
DEFAULT_PROTECTION = "off"

CSS = """
body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 40px; color: #333; }
.container { max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
h1 { color: #2c3e50; }
a { color: #3498db; text-decoration: none; margin: 0 5px; }
a:hover { text-decoration: underline; }
label { display: block; margin-top: 15px; font-weight: bold; }
input[type="text"] { width: 70%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; }
button { padding: 8px 15px; margin-left: 5px; background-color: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:hover { background-color: #2980b9; }
.result { margin-top: 20px; padding: 10px; background: #ecf0f1; border-radius: 5px; }
.mode { background: #f9e79f; padding: 10px; border-radius: 5px; margin: 10px 0; }
.secret { background: #f5b7b1; padding: 10px; border-radius: 5px; margin: 10px 0; }
"""

class RequestHandler(BaseHTTPRequestHandler):
    def _get_cookie_dict(self):
        c = cookies.SimpleCookie()
        if 'Cookie' in self.headers:
            c.load(self.headers['Cookie'])
        return c

    def _get_lang(self):
        c = self._get_cookie_dict()
        if 'lang' in c:
            lang = c['lang'].value
            if lang in MESSAGES:
                return lang
        return DEFAULT_LANG

    def _get_protection(self):
        c = self._get_cookie_dict()
        if 'protection' in c:
            prot = c['protection'].value
            if prot in ("on", "off"):
                return prot
        return DEFAULT_PROTECTION

    def _set_cookie(self, name, value):
        self.send_header('Set-Cookie', f'{name}={value}; Path=/')

    def _render_page(self, lang, protection, user_id=None, path="/", is_admin_page=False):
        msg = MESSAGES[lang]
        rows = []  # Инициализируем, чтобы избежать UnboundLocalError

        if user_id is not None:
            if protection == "off":
                query = f"SELECT username, password FROM users WHERE id = {user_id}"
                conn = sqlite3.connect("test_vuln.db")
                cur = conn.cursor()
                try:
                    cur.execute(query)
                    rows = cur.fetchall()
                    conn.close()
                    if rows:
                        response = msg["found"].format(rows)
                    else:
                        response = msg["not_found"]
                except Exception as e:
                    conn.close()
                    response = msg["error"].format(e)
            else:
                query = "SELECT username, password FROM users WHERE id = ?"
                conn = sqlite3.connect("test_vuln.db")
                cur = conn.cursor()
                try:
                    cur.execute(query, (user_id,))
                    rows = cur.fetchall()
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

        # Строим секретное сообщение только если есть запрос
        secret_html = ""
        if is_admin_page:
            if user_id:
                if protection == "off" and rows and "admin" in str(rows):
                    secret_html = f'<div class="secret">{msg["admin_secret"]}</div>'
                else:
                    secret_html = f'<div class="secret">{msg["admin_access_denied"]}</div>'
            else:
                secret_html = f'<div class="secret">{msg["admin_instruction"]}</div>'

        if is_admin_page:
            page_title = msg["admin_title"]
            form_action = "/admin"
        else:
            page_title = msg["title"]
            form_action = "/"

        html = f"""<html>
<head><title>{page_title}</title><style>{CSS}</style></head>
<body>
<div class="container">
    <h1>{page_title}</h1>
    <p>{msg['choose_language']} <a href="/?set_lang=ru">{msg['russian']}</a> | <a href="/?set_lang=en">{msg['english']}</a></p>
    <div class="mode">{msg['mode_label']} <a href="/?set_protection=off">{msg['vulnerable_mode']}</a> | <a href="/?set_protection=on">{msg['secure_mode']}</a> | Текущий: {protection}</div>
    <hr>
    <form action="{form_action}" method="get">
        <label for="id">{msg['enter_id']}</label>
        <input type="text" id="id" name="id" placeholder="1">
        <button type="submit">{msg['search']}</button>
    </form>
    <div class="result">{response}</div>
    {secret_html}
    <p><a href="/admin">{msg['admin_page']}</a></p>
    <p>{msg['current_lang']} {lang}</p>
</div>
</body>
</html>"""
        return html

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if 'set_lang' in params:
            new_lang = params['set_lang'][0]
            if new_lang in MESSAGES:
                self._set_cookie('lang', new_lang)
        if 'set_protection' in params:
            new_prot = params['set_protection'][0]
            if new_prot in ("on", "off"):
                self._set_cookie('protection', new_prot)

        lang = self._get_lang()
        protection = self._get_protection()
        user_id = params.get("id", [None])[0]
        is_admin = (path == "/admin")

        html = self._render_page(lang, protection, user_id, path, is_admin)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
    print("Сервер запущен на http://127.0.0.1:8000")
    print("Уязвимый/защищённый режим переключается ссылками или ?set_protection=on/off")
    print("Страница /admin доступна по адресу http://127.0.0.1:8000/admin")
    server.serve_forever()
