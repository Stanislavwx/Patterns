from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from drones.bridge.controller import DroneController
from drones.config.mission_config import MissionConfig
from drones.environment.base import Environment
from drones.strategy.base import ReactionStrategy
from drones.cor.base import FailSafeHandler
from drones.utils.telemetry import Telemetry
from drones.utils.persistence import Persistence


class DroneMission(ABC):
    """Template Method base class."""

    def __init__(
        self,
        config: MissionConfig,
        controller: DroneController,
        environment: Environment,
        reaction_strategy: ReactionStrategy,
        fail_safe: FailSafeHandler,
        persistence: Persistence,
        telemetry: Telemetry | None = None,
    ) -> None:
        self.config = config
        self.controller = controller
        self.environment = environment
        self.reaction_strategy = reaction_strategy
        self.fail_safe = fail_safe
        self.persistence = persistence
        self.telemetry = telemetry or Telemetry()
        self.observed_events: list = []
        self._remaining_reactions = int(self.config.behavior_params.get("reaction_cycles", 1))

    def execute_mission(self) -> Dict[str, Any]:
        self.load_config()
        self.setup_event_subscriptions()
        self.analyze_environment()
        self.preflight_check()
        self.navigate_to_area()
        self.perform_payload_action()
        while self.environment_requires_reaction():
            reading = self.environment.sample()
            self.react_to_environment(reading)
            self._remaining_reactions -= 1
        collected = self.collect_and_store_data()
        self.return_to_base()
        result = self.postprocess_results(collected)
        return result

    def load_config(self) -> None:
        self.telemetry.push("load_config", mission=self.config.mission_id)

    def setup_event_subscriptions(self) -> None:
        def on_event(event) -> None:
            self.observed_events.append(event)
            self.telemetry.push("event", name=event.name, reading=event.reading)

        self.environment.subscribe(on_event)
        self.telemetry.push("subscriptions_ready")

    def analyze_environment(self) -> None:
        event = self.environment.start()
        self.telemetry.push("analyzed_environment", reading=event.reading)

    def preflight_check(self) -> None:
        self.telemetry.push("preflight")
        self.controller.takeoff()

    def navigate_to_area(self) -> None:
        self.telemetry.push("navigate", target=vars(self.config.target_area))
        self.controller.goto(self.config.target_area.to_tuple())

    @abstractmethod
    def perform_payload_action(self) -> None:  # pragma: no cover - abstract
        ...

    def environment_requires_reaction(self) -> bool:
        return self._remaining_reactions > 0

    def react_to_environment(self, reading: dict) -> str:
        self.telemetry.push("react", reading=reading)
        return self.reaction_strategy.react(self, reading)

    def collect_and_store_data(self) -> Dict[str, Any]:
        data = {"mission": self.config.mission_id, "events": len(self.observed_events)}
        self.persistence.store(self.config.mission_id, data)
        self.telemetry.push("collect", data=data)
        return data

    def return_to_base(self) -> None:
        self.telemetry.push("return", base=vars(self.config.base_area))
        self.controller.goto(self.config.base_area.to_tuple())
        self.controller.land()

    def postprocess_results(self, collected: Dict[str, Any]) -> Dict[str, Any]:
        summary = {
            "mission_id": self.config.mission_id,
            "collected": collected,
            "steps": [rec.step for rec in self.telemetry.records],
        }
        self.telemetry.push("postprocess", summary=summary)
        return summary
