"""
Module. Logger handler.
"""

import logging

import logging.config
from datetime import datetime

from app.logger.logging_config import get_logging_config, Loggers


class NoTracebackFormatter(logging.Formatter):
    def format(self, record):
        return f"{record.levelname:<10}|{datetime.fromtimestamp(record.created)} | {record.name} - {record.getMessage()} | {record.exc_info}"

    def formatStack(self, stack_info):
        return ""


def get_logger(name) -> logging.Logger:
    """
    Function. Creates a logger instance.
    :return: logger instance
    """

    logger = logging.getLogger(name)
    logger_config = get_logging_config()
    logging.config.dictConfig(logger_config)
    handler = logging.getHandlerByName("file_rotating")
    handler.setFormatter(NoTracebackFormatter())

    return logger


basic_logger = get_logger(Loggers.basic)
database_logger = get_logger(Loggers.database_err)
