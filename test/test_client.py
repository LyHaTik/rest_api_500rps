import csv
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_request(row):
    row['recognition_accuracy'] = float(row['recognition_accuracy'])
    row['afts_regno_ai_score'] = float(row['afts_regno_ai_score'])

    start = time.time()
    try:
        response = requests.post("http://127.0.0.1:80/predict", json=row, timeout=10)
        end = time.time()
        duration_ms = (end - start) * 1000
        return duration_ms, response.status_code, response.json()
    except Exception as e:
        return 0, 'error', str(e)

# Загружаем все строки заранее
rows = []
with open("test_data.csv", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(dict(row))

total_time_requests = 0
count = 0
max_workers = 6

start_all = time.perf_counter()  # Время старта всех запросов

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(send_request, row) for row in rows]
    errors = 0
    for future in as_completed(futures):
        duration, status, result = future.result()
        if status != 'error':
            total_time_requests += duration
            count += 1
        else:
            errors += 1

    print(f"Ошибок: {errors}")

end_all = time.perf_counter()  # Время окончания всех запросов
total_duration_ms = (end_all - start_all) * 1000

print(f"\nmax_workers: {max_workers}")
print(f"Запросов: {count}")
print(f"Сумма индивидуальных запросов: {total_time_requests:.2f} ms")
print(f"Общее время: {total_duration_ms:.2f} ms")

if count:
    print(f"Среднее время на запрос: {total_time_requests / count:.2f} ms")
    print(f"Пропускная способность: {count / ((end_all - start_all) or 1):.2f} req/s")
