from __future__ import annotations

from drones.template.base import DroneMission


class PollutionMonitoringMission(DroneMission):
    def perform_payload_action(self) -> None:
        self.telemetry.push("payload", action="water_sampling")
        self.controller.adjust_course((0, -0.5, 0))

    def collect_and_store_data(self) -> dict:
        reading = self.environment.sample()
        data = {"mission": self.config.mission_id, "salinity": reading.get("salinity", 0)}
        self.persistence.store(self.config.mission_id, data)
        self.telemetry.push("collect", data=data)
        return data
