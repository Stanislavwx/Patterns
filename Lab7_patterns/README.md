# Patterns Lab 7 — Drone Mission Framework

Модульний симулятор місій дронів, який демонструє шаблон Template Method, Bridge, Strategy, Observer, Abstract Factory / Factory Method, Chain of Responsibility та мінімальний HTTP API (FastAPI) для запуску місій.

## Структура
- `drones/api` — FastAPI застосунок та ендпоїнти (`/mission/run`, `/mission/status/{id}`, `/mission/result/{id}`).
- `drones/factory` — `MissionFactory` + `ConfigLoader`.
- `drones/observer` — EventBus і події середовища.
- `drones/cor` — ланцюжок аварійних обробників.
- `drones/strategy` — реакції на середовище.
- `drones/bridge` — контролер та реалізації руху (повітря/море/суходіл).
- `drones/template` — базовий клас місії (Template Method).
- `drones/missions` — конкретні місії: SeaExploration, Agriculture, DefectsDetection, Rescue, PollutionMonitoring.
- `drones/environment` — середовища: Air, Sea, Surface.
- `drones/utils` — логер, телеметрія, персистенція, математика.
- `drones/tests` — юніт та інтеграційні тести.
- `docs/` — design.md та UML.png.

## Приклад конфігурації місії
```json
{
  "mission_id": "demo-1",
  "mission_type": "agriculture",
  "environment_type": "air",
  "platform_type": "air",
  "mode": "single",
  "target_area": {"x": 10, "y": 5, "z": 2},
  "base_area": {"x": 0, "y": 0, "z": 0},
  "thresholds": {"max_wind": 12},
  "behavior_params": {"reaction_cycles": 1, "seed": 42}
}
```

## Запуск API
```bash
uvicorn drones.api.server:app --reload
# POST /mission/run з конфігом вище, потім перевірити статус/результат
```

## Демо скрипт
```bash
python demo.py
```
Він створює місію через фабрику, виконує її та виводить підсумок.

## Тести
```bash
pytest
```

## Основні патерни
- Template Method: `DroneMission.execute_mission`.
- Bridge: `DroneController` + `MovementImplementor` реалізації.
- Strategy: `WindReaction`, `WaveReaction`, `CrackReaction`.
- Observer: `Environment` + `EventBus`.
- Factory: `MissionFactory`.
- Chain of Responsibility: `ReRouteHandler -> AdjustAltitudeHandler -> SwarmReassignHandler -> EmergencyLandHandler`.
