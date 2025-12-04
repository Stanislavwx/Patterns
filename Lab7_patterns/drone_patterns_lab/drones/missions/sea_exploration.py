from __future__ import annotations

from drones.template.base import DroneMission
class SeaExplorationMission(DroneMission):
    def perform_payload_action(self) -> None:
        self.telemetry.push("payload", action="sonar_sweep")
        # невелика корекція курсу як імітація сканування
        self.controller.adjust_course((0, 1.5, 0))

    def collect_and_store_data(self) -> dict:
        reading = self.environment.sample()
        data = {"mission": self.config.mission_id, "wave_height": reading.get("wave_height", 0)}
        self.persistence.store(self.config.mission_id, data)
        self.telemetry.push("collect", data=data)
        return data
