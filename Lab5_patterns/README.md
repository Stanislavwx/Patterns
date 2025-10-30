# SmartApp IoT Microservices (Dockerized)

Три мікросервіси FastAPI (колонка, світло, штори) + головний веб-додаток. Працює локально або через Docker Compose.

## Локальний запуск (venv)
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
python -m devices.smart_speaker
python -m devices.smart_light
python -m devices.smart_curtains
python -m main
```

## Запуск через Docker Compose
```bash
docker compose build
docker compose up -d
docker compose ps
```
АБО
```bash
podman-compose up -d --build
podman-compose ps
```

- Дашборд: http://127.0.0.1:8010  
- Swagger: http://127.0.0.1:8001/docs, :8002/docs, :8003/docs

Зупинка і видалення:
```bash
docker compose down
```
АБО
```bash
podman-compose down
```


## Патерни
- Controller: `controller/app_controller.py`
- Facade: `controller/iot_facade.py`
- Decorator: `devices/base_device.py` (LoggingDeviceDecorator)
- Microservice: `devices/`

## Нотатки
- У Docker мережі головний сервіс звертається до `speaker:8001`, `light:8002`, `curtains:8003` через змінні середовища.
- Всередині контейнерів всі сервіси слухають `0.0.0.0`, тому порти проброшені назовні.
