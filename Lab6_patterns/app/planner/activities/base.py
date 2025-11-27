from dataclasses import dataclass

from app.db.models import Activity


@dataclass
class BaseActivity:
    name: str
    type: str
    priority: int = 1

    def to_activity(self) -> Activity:
        return Activity(name=self.name, type=self.type, priority=self.priority)
