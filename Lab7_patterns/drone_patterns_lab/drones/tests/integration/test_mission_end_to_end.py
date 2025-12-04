from drones.factory.mission_factory import MissionFactory


def test_full_mission_execution_stores_results():
    factory = MissionFactory()
    cfg = {
        "mission_id": "integration-1",
        "mission_type": "agriculture",
        "environment_type": "air",
        "platform_type": "air",
        "mode": "single",
        "target_area": {"x": 1, "y": 1, "z": 1},
        "base_area": {"x": 0, "y": 0, "z": 0},
        "thresholds": {"max_wind": 20},
        "behavior_params": {"reaction_cycles": 1, "seed": 1},
    }
    mission = factory.create_from_dict(cfg)
    result = mission.execute_mission()
    assert result["mission_id"] == "integration-1"
    stored = factory.persistence.load("integration-1")
    assert stored["mission"] == "integration-1"
