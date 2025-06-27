"""
Module. Logger handler.
"""

import logging

import logging.config
from datetime import datetime
from logging import Handler

from app.logger.logging_config import get_logging_config
from app.utils.settings import settings


class NoTracebackFormatter(logging.Formatter):
    def format(self, record):
        return f"[{record.levelname + ']':<10}|{datetime.fromtimestamp(record.created)} | {record.name} - {record.getMessage():<40} | {record.exc_info}"

    def formatStack(self, stack_info):
        return ""


class StandardDebugFormatter(logging.Formatter):
    def format(self, record):
        return f"[{record.levelname + ']':<10}|{datetime.fromtimestamp(record.created)} | {record.name} - {record.getMessage()}"


def get_logger(name) -> logging.Logger:
    """
    Function. Creates a logger instance.
    :return: logger instance
    """

    logger = logging.getLogger(name)
    logger_config = get_logging_config()
    logging.config.dictConfig(logger_config)

    handler: Handler = logging.getHandlerByName(settings.handlers.DB_HANDLER)
    handler.setFormatter(NoTracebackFormatter())

    handler = logging.getHandlerByName(settings.handlers.STDOUT_HANDLER)
    handler.setFormatter(StandardDebugFormatter())

    return logger


info_logger = get_logger(settings.loggers.INFO_LOGGER)
database_logger = get_logger(settings.loggers.DB_LOGGER)
