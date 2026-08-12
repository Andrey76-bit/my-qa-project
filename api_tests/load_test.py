import requests
import concurrent.futures
import time

URL = "https://jsonplaceholder.typicode.com/posts"
NUM_USERS = 20  # Наша "толпа" виртуальных пользователей

def send_request(user_id):
    """Один виртуальный пользователь отправляет запрос"""
    start = time.time()
    try:
        response = requests.get(URL)
        elapsed = round(time.time() - start, 3)
        return {"user": user_id, "status": response.status_code, "time": elapsed}
    except Exception as e:
        elapsed = round(time.time() - start, 3)
        return {"user": user_id, "status": "ERROR", "time": elapsed, "error": str(e)}

def main():
    print(f"🚀 Запускаем нагрузочный тест: {NUM_USERS} пользователей -> {URL}")
    print("=" * 60)

    # Запускаем всех пользователей одновременно
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_USERS) as executor:
        results = list(executor.map(send_request, range(1, NUM_USERS + 1)))

    # Считаем статистику
    success = [r for r in results if r["status"] == 200]
    errors = [r for r in results if r["status"] != 200]
    times = [r["time"] for r in results]

    print(f"✅ Успешных запросов: {len(success)}")
    print(f"❌ Ошибочных запросов: {len(errors)}")
    if times:
        print(f"⏱️ Среднее время ответа: {round(sum(times)/len(times), 3)} сек")
        print(f"⚡ Максимальное время ответа: {max(times)} сек")

    # Выводим первые 10 результатов для наглядности
    print("\n--- Первые 10 результатов ---")
    for r in results[:10]:
        print(f"Пользователь {r['user']}: статус={r['status']}, время={r['time']} сек")

if __name__ == "__main__":
    main()
