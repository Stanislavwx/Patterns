import random

from drones.environment.base import Environment


class SurfaceEnvironment(Environment):
    def sample(self) -> dict:
        return {
            "terrain_roughness": random.uniform(0, 1),
            "obstacle_density": random.uniform(0, 0.5),
            "crack_density": random.uniform(0, 1),
        }
