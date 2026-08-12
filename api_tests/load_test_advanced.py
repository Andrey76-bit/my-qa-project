import requests
import concurrent.futures
import time
import csv
import os
import json
from statistics import mean, median

URL = "https://jsonplaceholder.typicode.com/posts"
NUM_USERS = 1000
LOOP_COUNT = 1
TOTAL_REQUESTS = NUM_USERS * LOOP_COUNT

def send_request(request_id):
    start = time.time()
    try:
        response = requests.get(URL)
        elapsed = round(time.time() - start, 3)
        return {
            "request_id": request_id,
            "status": response.status_code,
            "time": elapsed
        }
    except Exception as e:
        elapsed = round(time.time() - start, 3)
        return {
            "request_id": request_id,
            "status": "ERROR",
            "time": elapsed,
            "error": str(e)
        }

def run_load_test():
    print(f"🚀 Запускаем расширенный нагрузочный тест")
    print(f"👥 Пользователей: {NUM_USERS}")
    print(f"🔁 Повторов на пользователя: {LOOP_COUNT}")
    print(f"📦 Всего запросов: {TOTAL_REQUESTS}")
    print("=" * 60)

    all_results = []
    total_requests_sent = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_USERS) as executor:
        for loop in range(LOOP_COUNT):
            batch_start = total_requests_sent + 1
            batch_end = total_requests_sent + NUM_USERS
            batch_ids = range(batch_start, batch_end + 1)
            results = list(executor.map(send_request, batch_ids))
            all_results.extend(results)
            total_requests_sent += NUM_USERS

    success = [r for r in all_results if r["status"] == 200]
    errors = [r for r in all_results if r["status"] != 200]
    times = [r["time"] for r in success]

    print(f"✅ Успешных запросов: {len(success)}")
    print(f"❌ Ошибочных запросов: {len(errors)}")
    if times:
        print(f"⏱️ Среднее время ответа: {round(mean(times), 3)} сек")
        print(f"⚡ Мин. время: {min(times)} сек")
        print(f"🐢 Макс. время: {max(times)} сек")
        print(f"📊 Медиана: {round(median(times), 3)} сек")

    # Сохраняем CSV
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    csv_path = os.path.join(reports_dir, "load_report.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Request ID", "Status", "Time (sec)"])
        for r in all_results:
            writer.writerow([r["request_id"], r["status"], r["time"]])
    print(f"📄 CSV-отчёт сохранён: {csv_path}")

    # Сохраняем JSON (для истории)
    json_path = os.path.join(reports_dir, "load_report.json")
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"📦 JSON-отчёт сохранён: {json_path}")

    # Генерируем HTML с простым графиком (через Chart.js из интернета)
    html_path = os.path.join(reports_dir, "load_report.html")
    times_str = json.dumps(times)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Load Test Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Отчёт по нагрузочному тестированию</h1>
        <p>Пользователей: {NUM_USERS}, Повторов: {LOOP_COUNT}, Всего запросов: {TOTAL_REQUESTS}</p>
        <p>Успешных: {len(success)}, Ошибок: {len(errors)}</p>
        <p>Среднее время: {round(mean(times), 3) if times else 0} сек</p>
        <canvas id="chart" width="400" height="200"></canvas>
        <script>
            const ctx = document.getElementById('chart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: Array.from({{length: {len(times)}}}, (_, i) => i+1),
                    datasets: [{{
                        label: 'Время ответа (сек)',
                        data: {times_str},
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    scales: {{
                        y: {{ beginAtZero: true }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    with open(html_path, "w") as f:
        f.write(html_content)
    print(f"📊 HTML-отчёт с графиком сохранён: {html_path}")
    print("✅ Расширенный нагрузочный тест завершён!")

if __name__ == "__main__":
    run_load_test()
