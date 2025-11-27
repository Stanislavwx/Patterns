# Smart Day Planner (Strategy + Observer)

Веб-сервіс будує щоденний план залежно від погоди та вподобань користувача. Реалізовані патерни Strategy (підбір активностей під тип погоди) та Observer (планувальник реагує на оновлення погоди від метеостанції).

## Можливості
- FastAPI бекенд з MongoDB для збереження планів, погоди та вподобань.
- Інтеграція з OpenWeatherMap (є мок-режим без ключа).
- Періодичний фоновий запит погоди, автоматичне оновлення плану.
- REST API для планів та вподобань, простий HTML/CSS фронтенд.
- Логи для ключових подій (погода, БД, оновлення плану).

## Швидкий старт (локально)
1. Встановіть залежності:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Сконфігуруйте `.env` (можна почати з `.env.example`). Мінімум потрібні:
   ```
   OPENWEATHER_API_KEY=<ваш ключ або change-me>
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB=smart_planner
   DEFAULT_CITY=Kyiv
   WEATHER_POLL_INTERVAL=900
   ```
   Якщо ключ не задано, сервіс працюватиме з мок-погодою без зовнішніх запитів.
3. Запустіть MongoDB (локально або через docker-compose, див. нижче).
4. Стартуйте API:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Відкрийте http://127.0.0.1:8000/ для простого UI або http://127.0.0.1:8000/docs для Swagger.

## Запуск через Docker Compose
```bash
cp .env.example .env  # за потреби відредагуйте
docker compose up --build
```
Сервіси (порт `8800` проброшений на хост):
- `app`: FastAPI (`http://localhost:8800`)
- `mongo`: MongoDB з volume `mongo-data`
- `mongo-express` (опціонально, порт 8081)

> На Fedora з podman/composer корисно вказати повні образи `docker.io/library/...` (вже прописано в compose). Якщо немає Docker, можна ставити `podman-docker` і користуватись тими ж командами `docker compose ...`.

> Детальний опис патернів, архітектури та сценарію захисту шукайте у файлі `LAB_REPORT.txt`.

## Основні ендпоінти
- `GET /health` — перевірка стану.
- `GET /plan?user_id=default` — поточний план (створить новий, якщо відсутній).
- `POST /plan/refresh?user_id=default&city=Kyiv` — форс-оновлення погоди та плану.
- `GET /preferences/{user_id}` — отримати вподобання.
- `PUT /preferences/{user_id}` — оновити вподобання (тіло: `UserPreferences`).
- `GET /plans?limit=10&user_id=default` — останні плани.

### Приклад запитів
```bash
curl -X POST "http://localhost:8000/plan/refresh?user_id=default&city=Kyiv"

curl -X PUT "http://localhost:8000/preferences/ivan" \\
  -H "Content-Type: application/json" \\
  -d '{"preferred_types":["outdoor","productive"],"avoid_types":["sport"],"working_hours_start":9,"working_hours_end":17,"weekend_mode":true,"prefers_outdoor":true}'
```

## Структура проєкту
```
app/
├── api/routes.py            # REST + фронтовий маршрут
├── core/config.py           # Налаштування (BaseSettings)
├── core/logger.py           # Глобальний логер
├── db/mongodb.py            # Підключення Mongo
├── db/models.py             # Pydantic-моделі
├── planner/day_planner.py   # Observer, робота зі стратегіями/БД
├── planner/strategies/      # WeatherStrategy + конкретні стратегії
├── planner/activities/      # Опис активностей
├── weather/weather_api.py   # Обгортка OpenWeatherMap
├── weather/weather_station.py# Subject (observable)
├── tasks/scheduler.py       # Простий asyncio-шедулер
├── main.py                  # Точка входу FastAPI
templates/index.html         # Простий UI
static/styles.css            # Стилі UI
docker-compose.yaml, Dockerfile, requirements.txt, README.md
```

## Коротко про патерни
- **Strategy**: `WeatherStrategy` + `Sunny/Rainy/Cloudy/Snowy` формують список активностей з урахуванням вподобань.
- **Observer**: `WeatherStation` (Subject) інформує `DayPlanner` (Observer) при зміні погоди.

## Примітки
- Без валідного `OPENWEATHER_API_KEY` використовується мок-погода (немає зовнішніх запитів).
- План зберігається в Mongo разом з погодою та вподобаннями користувача.
