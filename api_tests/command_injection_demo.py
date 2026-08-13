import subprocess
import re

def ping_host_vulnerable(host):
    """УЯЗВИМАЯ функция: конкатенирует строку и запускает через shell"""
    command = f"ping -c 1 {host}"
    print(f"[УЯЗВИМАЯ КОМАНДА] {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=3)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def ping_host_safe(host):
    """БЕЗОПАСНАЯ функция: проверяет ввод и не использует shell"""
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return "Недопустимый хост"
    command = ["ping", "-c", "1", host]
    print(f"[БЕЗОПАСНАЯ КОМАНДА] {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=3)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print("=== Обычный пинг ===")
    print(ping_host_vulnerable("127.0.0.1"))
    print("\n=== Атака Command Injection ===")
    # Вводим хост с инъекцией, чтобы сервер выполнил echo
    malicious_input = "127.0.0.1; echo INJECTED"
    print("Уязвимая функция (атака сработает):")
    output = ping_host_vulnerable(malicious_input)
    print(output)
    print("Безопасная функция (атака заблокируется):")
    print(ping_host_safe(malicious_input))
