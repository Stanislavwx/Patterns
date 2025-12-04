from drones.factory.mission_factory import MissionFactory


def main() -> None:
    factory = MissionFactory()
    cfg = {
        "mission_id": "demo-run",
        "mission_type": "sea_exploration",
        "environment_type": "sea",
        "platform_type": "sea",
        "mode": "single",
        "target_area": {"x": 2, "y": 2, "z": 0},
        "base_area": {"x": 0, "y": 0, "z": 0},
        "thresholds": {"max_wave": 3},
        "behavior_params": {"reaction_cycles": 1, "seed": 3},
    }
    mission = factory.create_from_dict(cfg)
    result = mission.execute_mission()
    print("Mission executed:", result)


if __name__ == "__main__":
    main()
