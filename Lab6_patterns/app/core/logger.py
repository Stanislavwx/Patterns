import logging
import sys
from typing import Optional

from .config import get_settings


def _configure_root_logger(level: str) -> None:
    """Configure global logger once."""
    root = logging.getLogger()
    if root.handlers:
        return

    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    root.addHandler(handler)
    root.setLevel(level)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    settings = get_settings()
    _configure_root_logger(settings.log_level.upper())
    return logging.getLogger(name or settings.app_name)
