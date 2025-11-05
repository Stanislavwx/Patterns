from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class Route:
    method: str
    template: str

    def build_path(self, **params) -> str:
        try:
            return self.template.format(**params)
        except KeyError as e:
            raise ValueError(f"Missing route param: {e} for template {self.template}")

DEFAULT_ROUTES: Dict[str, Route] = {
    "power":          Route(method="POST", template="/power/{state}"),
    "set_volume":     Route(method="POST", template="/volume/{level}"),
    "set_brightness": Route(method="POST", template="/brightness/{level}"),
    "position":       Route(method="POST", template="/position/{value}"),
}

def make_route(action: str, registry: Dict[str, Route] = DEFAULT_ROUTES) -> Route:
    try:
        return registry[action]
    except KeyError:
        raise ValueError(f"Unknown action: {action}")
