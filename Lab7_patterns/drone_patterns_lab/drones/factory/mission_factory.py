from __future__ import annotations

from pathlib import Path
from typing import Dict, Type

from drones.bridge.air import AirPlatform
from drones.bridge.controller import DroneController
from drones.bridge.sea import SeaPlatform
from drones.bridge.surface import SurfacePlatform
from drones.config.mission_config import MissionConfig
from drones.cor.adjust_altitude_handler import AdjustAltitudeHandler
from drones.cor.emergency_land_handler import EmergencyLandHandler
from drones.cor.reroute_handler import ReRouteHandler
from drones.cor.swarm_reassign_handler import SwarmReassignHandler
from drones.environment.air_env import AirEnvironment
from drones.environment.sea_env import SeaEnvironment
from drones.environment.surface_env import SurfaceEnvironment
from drones.factory.config_loader import ConfigLoader
from drones.missions.agriculture import AgricultureMission
from drones.missions.defects_detection import DefectsDetectionMission
from drones.missions.pollution_monitoring import PollutionMonitoringMission
from drones.missions.rescue import RescueMission
from drones.missions.sea_exploration import SeaExplorationMission
from drones.strategy.crack_reaction import CrackReaction
from drones.strategy.wave_reaction import WaveReaction
from drones.strategy.wind_reaction import WindReaction
from drones.template.base import DroneMission
from drones.utils.persistence import Persistence
from drones.utils.telemetry import Telemetry


class MissionFactory:
    def __init__(self, persistence: Persistence | None = None) -> None:
        self.persistence = persistence or Persistence(Path("data"))

    def create_from_dict(self, payload: Dict) -> DroneMission:
        config = ConfigLoader.from_dict(payload)
        return self.create(config)

    def create(self, config: MissionConfig) -> DroneMission:
        env = self._build_environment(config)
        implementor = self._build_platform(config)
        controller = DroneController(implementor)
        strategy = self._build_strategy(config)
        fail_safe = self._build_failsafe_chain()
        mission_cls = self._mission_mapping()[config.mission_type]
        telemetry = Telemetry()
        mission = mission_cls(
            config=config,
            controller=controller,
            environment=env,
            reaction_strategy=strategy,
            fail_safe=fail_safe,
            persistence=self.persistence,
            telemetry=telemetry,
        )
        if config.mode == "swarm":
            controller.set_swarm()
        return mission

    def _build_environment(self, config: MissionConfig):
        env_map = {
            "air": AirEnvironment,
            "sea": SeaEnvironment,
            "surface": SurfaceEnvironment,
        }
        env_cls = env_map.get(config.environment_type)
        if not env_cls:
            raise ValueError(f"Unknown environment {config.environment_type}")
        return env_cls(seed=config.behavior_params.get("seed"))

    def _build_platform(self, config: MissionConfig):
        platform_map = {
            "air": AirPlatform,
            "sea": SeaPlatform,
            "surface": SurfacePlatform,
        }
        platform_cls = platform_map.get(config.platform_type)
        if not platform_cls:
            raise ValueError(f"Unknown platform {config.platform_type}")
        return platform_cls()

    def _build_strategy(self, config: MissionConfig):
        if config.environment_type == "air":
            return WindReaction()
        if config.environment_type == "sea":
            return WaveReaction()
        return CrackReaction()

    def _build_failsafe_chain(self):
        return ReRouteHandler(
            AdjustAltitudeHandler(SwarmReassignHandler(EmergencyLandHandler())),
        )

    def _mission_mapping(self) -> Dict[str, Type[DroneMission]]:
        return {
            "sea_exploration": SeaExplorationMission,
            "agriculture": AgricultureMission,
            "defects_detection": DefectsDetectionMission,
            "rescue": RescueMission,
            "pollution_monitoring": PollutionMonitoringMission,
        }
