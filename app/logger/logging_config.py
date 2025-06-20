"""
Module. Logger configuration.
"""

import logging
from typing import Dict, Any

from app.utils.settings import settings


class LevelFileHandler(logging.Handler):
    def __init__(self, mode="a"):
        super().__init__()
        self.mode = mode

    def emit(self, record):
        with open(f"db_{record.levelname}.log", self.mode) as f:
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
        "formatters": {},
        "filters": {},
        "handlers": {
            settings.handlers.STDOUT_HANDLER: {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            settings.handlers.DB_HANDLER: {
                "class": "logging.handlers.RotatingFileHandler",
                "backupCount": 5,
                # "formatter": "default",
                "filename": "logs/db_err_file.log",
                # "when": "D",
                # "interval": 1,
                "delay": True,
                "maxBytes": 1048576,
            },
        },
        "loggers": {
            settings.loggers.DEBUG_LOGGER: {
                "handlers": [
                    settings.handlers.STDOUT_HANDLER,
                ],
                "level": "INFO",
            },
            settings.loggers.DB_LOGGER: {
                "handlers": [
                    settings.handlers.DB_HANDLER,
                ],
                "level": "ERROR",
            },
        },
    }
    return dict_config
