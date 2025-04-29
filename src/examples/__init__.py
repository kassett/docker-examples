import logging
from typing import Literal

from pydantic_settings import BaseSettings

VERSION = "0.0.1"

from examples.cli import Config, get_settings

class LogLevel(BaseSettings):
    log_level: Literal["INFO", "DEBUG", "EXCEPTION"] = "INFO"

def get_logger(name: str = "__main__") -> logging.Logger:
    logger = logging.Logger(name)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(LogLevel().log_level)
    return logger

__all__ = ["Config", "get_settings"]