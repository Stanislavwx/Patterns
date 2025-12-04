from drones.bridge.air import AirPlatform
from drones.bridge.controller import DroneController
from drones.cor.adjust_altitude_handler import AdjustAltitudeHandler
from drones.cor.emergency_land_handler import EmergencyLandHandler
from drones.cor.reroute_handler import ReRouteHandler
from drones.cor.swarm_reassign_handler import SwarmReassignHandler


def build_chain():
    return ReRouteHandler(AdjustAltitudeHandler(SwarmReassignHandler(EmergencyLandHandler())))


def test_chain_handles_wind_issue():
    chain = build_chain()
    controller = DroneController(AirPlatform())
    result = chain.handle({"type": "wind", "strength": 3}, {"controller": controller})
    assert result == "altitude_adjusted"
    actions = [a for a, _ in controller.impl.history]
    assert "adjust_air_course" in actions


def test_chain_falls_back_to_emergency_land():
    chain = build_chain()
    controller = DroneController(AirPlatform())
    result = chain.handle({"type": "unknown"}, {"controller": controller})
    assert result == "emergency_land"
    actions = [a for a, _ in controller.impl.history]
    assert actions[-1] == "land"
