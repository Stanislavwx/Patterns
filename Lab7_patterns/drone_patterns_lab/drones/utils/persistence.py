from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class Persistence:
    """Very small persistence layer that stores mission results in memory and disk."""

    def __init__(self, base_path: str | Path | None = None) -> None:
        self._memory: Dict[str, Any] = {}
        self.base_path = Path(base_path) if base_path else None

    def store(self, mission_id: str, result: Any) -> None:
        self._memory[mission_id] = result
        if self.base_path:
            self.base_path.mkdir(parents=True, exist_ok=True)
            target = self.base_path / f"{mission_id}.json"
            target.write_text(json.dumps(result, indent=2))

    def load(self, mission_id: str) -> Any:
        if mission_id in self._memory:
            return self._memory[mission_id]
        if self.base_path:
            target = self.base_path / f"{mission_id}.json"
            if target.exists():
                return json.loads(target.read_text())
        raise KeyError(f"mission {mission_id} not found")
