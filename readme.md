# Pick Regno Service
REST API-сервис для запуска ML-модели, определяющей вероятность корректного распознавания автомобильного номера на основе данных с камеры и нейросети. Сервис разработан с использованием FastAPI и CatBoost, ориентирован на работу в высоконагруженной системе (до 500 RPS).

# Состав проекта
main.py — точка входа, FastAPI-сервис

pick_regno.py — функция pick_regno, реализующая ML-логику

micromodel.cbm — файл модели CatBoost (предоставлен ML-специалистом)

test_data.csv — тестовый датасет

test_client.py — скрипт для локального тестирования REST API

# Запуск
## 1. Разверните контейнеры с приложением
docker-compose up -d
  - По умолчанию: развернется 2 контейнера с выделением 3х ядер на каждый контейнер.
  - Отредактируйте число ядер под Ваше устройство, в app/Dockerfile

### Пример запроса:
POST /predict
json
{
  "regno_recognize": "А939НО196",
  "afts_regno_ai": "А939НО190",
  "recognition_accuracy": 6.4,
  "afts_regno_ai_score": 0.8689,
  "afts_regno_ai_char_scores": "[0.99, 0.99, 0.87]",
  "afts_regno_ai_length_scores": "[1.0, 0.9, 0.85]",
  "camera_type": "Стационарная",
  "camera_class": "Астра-Трафик",
  "time_check": "2021-08-01 09:02:59",
  "direction": "0"
}
### Ответ:
json
{
  "result": [[0.9833, 0.0166]]
}


# Тестирование:
python test_client.py

## Этот скрипт:

загружает test_data.csv

построчно делает POST-запросы к /predict

выводит статус ответа и вероятности
 - Настройте число workers согласно тестируемого приложения, по умолчанию max_workers = 6

# Особенности реализации
REST API принимает по одному объекту за запрос.
NGINX позволяет горизонтально масштабировать сервис

Данная архитектура выбрана, для распараллеливания нагрузки на синхронный сервис.

# Структура проекта
.
app_
|   ├── main.py                # FastAPI-сервис
|   ├── Dockerfile             
|   ├── pick_regno.py          # Модель CatBoost
|   ├── micromodel.cbm         # ML-логика
|   └── requirements.txt       # Зависимости
test
|   ├── test_client.py         # Скрипт для тестирования REST API
|   └── test_data.csv          # CSV с тестовыми примерами
nginx
|   └── nginx.conf             # конфигурационный файл nginx
├─README.md                    # Этот файл
└─docker-compose.yml            