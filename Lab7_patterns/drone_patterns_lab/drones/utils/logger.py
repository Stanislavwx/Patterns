import logging
from typing import Optional


def get_logger(name: str, level: int = logging.INFO, fmt: Optional[str] = None) -> logging.Logger:
    if fmt is None:
        fmt = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
