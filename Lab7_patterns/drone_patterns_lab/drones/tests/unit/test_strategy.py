from drones.config.mission_config import Coord, MissionConfig
from drones.strategy.wind_reaction import WindReaction
from drones.bridge.controller import DroneController
from drones.bridge.air import AirPlatform
from drones.cor.base import FailSafeHandler
from drones.template.base import DroneMission
from drones.environment.base import Environment
from drones.utils.persistence import Persistence


class AcceptAllHandler(FailSafeHandler):
    def __init__(self) -> None:
        super().__init__(None)
        self.handled = False

    def _process(self, issue: dict, context: dict) -> str:
        self.handled = True
        return "handled"


class NullMission(DroneMission):
    def perform_payload_action(self) -> None:  # pragma: no cover - not used
        return None


class FixedEnvironment(Environment):
    def sample(self) -> dict:
        return {"wind_speed": 12}


def test_wind_strategy_triggers_failsafe_when_threshold_exceeded():
    handler = AcceptAllHandler()
    cfg = MissionConfig(
        mission_id="windy",
        mission_type="agriculture",
        environment_type="air",
        platform_type="air",
        mode="single",
        target_area=Coord(0, 0, 0),
        base_area=Coord(0, 0, 0),
        thresholds={"max_wind": 5},
        behavior_params={"reaction_cycles": 0},
    )
    mission = NullMission(
        config=cfg,
        controller=DroneController(AirPlatform()),
        environment=FixedEnvironment(),
        reaction_strategy=WindReaction(),
        fail_safe=handler,
        persistence=Persistence(),
    )
    outcome = mission.react_to_environment({"wind_speed": 10})
    assert outcome == "handled"
    assert handler.handled is True
