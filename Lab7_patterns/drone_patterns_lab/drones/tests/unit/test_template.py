from drones.config.mission_config import Coord, MissionConfig
from drones.environment.base import Environment
from drones.strategy.wind_reaction import WindReaction
from drones.template.base import DroneMission
from drones.bridge.controller import DroneController
from drones.bridge.air import AirPlatform
from drones.cor.emergency_land_handler import EmergencyLandHandler
from drones.utils.persistence import Persistence


class FakeEnvironment(Environment):
    def sample(self) -> dict:
        return {"wind_speed": 1}


class DummyMission(DroneMission):
    def perform_payload_action(self) -> None:
        self.telemetry.push("payload", action="dummy")


def test_template_executes_steps_in_order():
    cfg = MissionConfig(
        mission_id="demo",
        mission_type="agriculture",
        environment_type="air",
        platform_type="air",
        mode="single",
        target_area=Coord(1, 1, 1),
        base_area=Coord(0, 0, 0),
        thresholds={"max_wind": 5},
        behavior_params={"reaction_cycles": 1},
    )
    mission = DummyMission(
        config=cfg,
        controller=DroneController(AirPlatform()),
        environment=FakeEnvironment(),
        reaction_strategy=WindReaction(),
        fail_safe=EmergencyLandHandler(),
        persistence=Persistence(),
    )
    mission.execute_mission()
    steps = [r.step for r in mission.telemetry.records]
    assert steps[:3] == ["load_config", "subscriptions_ready", "event"]
    assert steps[3:7] == ["analyzed_environment", "preflight", "navigate", "payload"]
    assert "collect" in steps
    assert steps[-1] == "postprocess"
