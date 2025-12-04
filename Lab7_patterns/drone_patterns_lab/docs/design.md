# Drone Mission Framework Design

## Goals
- Showcase Template Method, Bridge, Strategy, Observer, Factory, and Chain of Responsibility in a cohesive drone mission workflow.
- Support multiple mission types (sea exploration, agriculture, defects detection, rescue, pollution monitoring) across air/sea/surface platforms.
- Expose a tiny FastAPI interface to orchestrate missions and inspect their status/results.

## Architecture
- **API (FastAPI)**: Entry point; receives mission configs, queues execution, and exposes status/result endpoints.
- **Factory**: `MissionFactory` builds the correct Environment, MovementImplementor, Controller, ReactionStrategy, FailSafe chain, Telemetry, and Mission subclass from a config payload.
- **Template Method**: `DroneMission.execute_mission()` defines the invariant workflow: load config → subscribe to environment → analyze → preflight → navigate → payload action → react loop → collect/store → return → postprocess.
- **Bridge**: `DroneController` (abstraction) delegates all movement to `MovementImplementor` implementations (`AirPlatform`, `SeaPlatform`, `SurfacePlatform`).
- **Observer**: Environments publish `EnvironmentEvent` instances through `EventBus`; missions subscribe during setup.
- **Strategy**: Reaction strategies (`WindReaction`, `WaveReaction`, `CrackReaction`) choose how to respond to environment readings.
- **Chain of Responsibility**: Fail-safe chain (`ReRouteHandler` → `AdjustAltitudeHandler` → `SwarmReassignHandler` → `EmergencyLandHandler`) attempts recovery actions in order.
- **Persistence/Telemetry**: Lightweight helpers capture mission steps and store results in memory (optionally on disk).

## Key Flows
1. **Mission creation**: API → `MissionFactory.create_from_dict` → components composed.
2. **Execution**: `execute_mission` runs the template steps; environment publishes an initial event; strategies react to sampled readings; CoR handles safety issues.
3. **Return**: Data stored via `Persistence`; summary returned to API / callers.

## Testing Approach
- Unit tests cover template order, bridge delegation, strategy trigger logic, observer propagation, and CoR fallbacks.
- Integration test runs a full mission via the factory and asserts data persistence.

## Extensibility
- Add missions by subclassing `DroneMission` and registering them in `MissionFactory._mission_mapping`.
- Introduce new platforms/environments by implementing `MovementImplementor`/`Environment` derivatives.
- Drop-in reaction strategies or fail-safe handlers without changing mission logic thanks to Strategy and CoR.
