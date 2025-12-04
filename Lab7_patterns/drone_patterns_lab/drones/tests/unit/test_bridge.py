from drones.bridge.air import AirPlatform
from drones.bridge.controller import DroneController


def test_controller_delegates_to_implementor():
    impl = AirPlatform()
    controller = DroneController(impl)

    controller.takeoff()
    controller.goto((1, 2, 3))
    controller.adjust_course((0.1, 0, 0))
    controller.set_swarm()
    controller.broadcast({"msg": "hi"})
    controller.hold_position()
    controller.land()

    actions = [action for action, _ in impl.history]
    assert actions[0] == "takeoff"
    assert "fly_to" in actions
    assert "adjust_air_course" in actions
    assert actions[-1] == "land"
