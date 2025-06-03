"""
Module. Logger configuration.
"""

import logging
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Loggers:
    basic: str = "BASIC_LOGGER"
    database_err: str = "DATABASE_LOGGER"


class LevelFileHandler(logging.Handler):
    def __init__(self, mode="a"):
        super().__init__()
        self.mode = mode

    def emit(self, record):
        with open(f"DB_{record.levelname}.log", self.mode) as f:
            msg = self.format(record)
            f.write(msg + "\n")


def get_logging_config() -> Dict[str, Any]:
    """
    Function. Get logging configuration.
    :return: logging configuration dictionary.
    """
    dict_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": f"{'[%(levelname)s]':<10} %(asctime)s | %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "filters": {},
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "db_err_file": {
                "()": LevelFileHandler,
                "formatter": "default",
                "mode": "a",
            },
            "time_rotating": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "backupCount": 5,
                "formatter": "default",
                "filename": "db_err.log",
                "when": "D",
                "interval": 1,
                "delay": True,
            },
        },
        "loggers": {
            f"{Loggers.basic}": {
                "handlers": ["stdout"],
                "level": "INFO",
            },
            f"{Loggers.database_err}": {
                "handlers": ["db_err_file"],
                "level": "ERROR",
            },
            f"{Loggers.database_err}.utils": {
                "handlers": ["time_rotating"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }
    return dict_config
