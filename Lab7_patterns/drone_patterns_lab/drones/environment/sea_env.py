import random

from drones.environment.base import Environment


class SeaEnvironment(Environment):
    def sample(self) -> dict:
        return {
            "wave_height": random.uniform(0, 5),
            "current_speed": random.uniform(0, 3),
            "salinity": random.uniform(30, 35),
        }
