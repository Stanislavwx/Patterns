from __future__ import annotations

from drones.template.base import DroneMission


class DefectsDetectionMission(DroneMission):
    def perform_payload_action(self) -> None:
        self.telemetry.push("payload", action="thermal_scan")
        self.controller.hold_position()

    def collect_and_store_data(self) -> dict:
        reading = self.environment.sample()
        defects = reading.get("crack_density", 0)
        data = {"mission": self.config.mission_id, "defects": defects}
        self.persistence.store(self.config.mission_id, data)
        self.telemetry.push("collect", data=data)
        return data
