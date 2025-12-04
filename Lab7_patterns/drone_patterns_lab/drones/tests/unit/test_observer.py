from drones.environment.base import Environment
from drones.observer.events import EnvironmentEvent


class MinimalEnvironment(Environment):
    def sample(self) -> dict:
        return {"value": 1}


def test_event_bus_notifies_subscribers():
    env = MinimalEnvironment()
    received = []

    def collect(event):
        received.append(event)

    env.subscribe(collect)
    event = env.start()
    assert isinstance(event, EnvironmentEvent)
    assert len(received) == 1
    assert received[0].reading["value"] == 1
