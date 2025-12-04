import random

from drones.environment.base import Environment


class AirEnvironment(Environment):
    def sample(self) -> dict:
        return {
            "wind_speed": random.uniform(0, 20),
            "visibility": random.uniform(0.5, 1.0),
            "temperature": random.uniform(-5, 35),
        }
