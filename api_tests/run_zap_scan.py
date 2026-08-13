import time
import sys
from zapv2 import ZAPv2

# Адрес ZAP daemon (мы запускали на порту 8090)
zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

def main():
    target = "http://127.0.0.1:8000"
    print(f"Начинаем сканирование цели: {target}")
    
    # 1. Открываем цель через ZAP
    zap.urlopen(target)
    time.sleep(2)
    
    # 2. Запускаем паука (Spider)
    print("Запускаем Spider...")
    scan_id = zap.spider.scan(target)
    while int(zap.spider.status(scan_id)) < 100:
        print(f"Spider progress: {zap.spider.status(scan_id)}%")
        time.sleep(2)
    print("Spider завершён.")
    
    # 3. Запускаем активное сканирование (Active Scan)
    print("Запускаем Active Scan...")
    scan_id = zap.ascan.scan(target)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"Active Scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(5)
    print("Active Scan завершён.")
    
    # 4. Получаем алерты
    alerts = zap.core.alerts(baseurl=target)
    print(f"Найдено алертов: {len(alerts)}")
    for alert in alerts:
        print(f"[{alert['risk']}] {alert['alert']} - {alert['url']}")
    
    # 5. Генерируем HTML-отчёт
    report = zap.core.htmlreport()
    with open("zap_report.html", "w") as f:
        f.write(report)
    print("Отчёт сохранён в zap_report.html")

if __name__ == "__main__":
    main()
