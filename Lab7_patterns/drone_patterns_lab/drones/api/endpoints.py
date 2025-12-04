from __future__ import annotations

from typing import Dict

from fastapi import BackgroundTasks, FastAPI, HTTPException

from drones.config.mission_config import MissionConfig
from drones.factory.mission_factory import MissionFactory


class MissionManager:
    def __init__(self, factory: MissionFactory) -> None:
        self.factory = factory
        self.status: Dict[str, str] = {}
        self.results: Dict[str, dict] = {}

    def _run_mission(self, cfg: dict) -> None:
        mission = self.factory.create_from_dict(cfg)
        mission_id = mission.config.mission_id
        self.status[mission_id] = "running"
        result = mission.execute_mission()
        self.status[mission_id] = "completed"
        self.results[mission_id] = result

    def enqueue(self, cfg: dict, background: BackgroundTasks) -> str:
        mission_id = cfg["mission_id"]
        self.status[mission_id] = "queued"
        background.add_task(self._run_mission, cfg)
        return mission_id

    def run_blocking(self, cfg: dict) -> dict:
        self._run_mission(cfg)
        return self.results[cfg["mission_id"]]


def create_app(factory: MissionFactory | None = None) -> FastAPI:
    factory = factory or MissionFactory()
    manager = MissionManager(factory)
    app = FastAPI(title="Drone Patterns Lab API")

    @app.post("/mission/run")
    def run_mission(cfg: dict, background: BackgroundTasks):
        mission_id = cfg.get("mission_id")
        if not mission_id:
            raise HTTPException(status_code=400, detail="mission_id required")
        manager.enqueue(cfg, background)
        return {"mission_id": mission_id, "status": "queued"}

    @app.get("/mission/status/{mission_id}")
    def get_status(mission_id: str):
        status = manager.status.get(mission_id)
        if not status:
            raise HTTPException(status_code=404, detail="unknown mission")
        return {"mission_id": mission_id, "status": status}

    @app.get("/mission/result/{mission_id}")
    def get_result(mission_id: str):
        if mission_id not in manager.results:
            raise HTTPException(status_code=404, detail="result not ready")
        return {"mission_id": mission_id, "result": manager.results[mission_id]}

    return app
