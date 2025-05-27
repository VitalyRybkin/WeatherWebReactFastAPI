"""
Module. Logger handler.
"""

import logging

import logging.config
from app.logger.logging_config import get_logging_config, Loggers


def get_logger(name) -> logging.Logger:
    """
    Function. Creates a logger instance.
    :param name: logger name
    :return: logger instance
    """

    logger = logging.getLogger(name)
    logger_config = get_logging_config()
    logging.config.dictConfig(logger_config)

    return logger


basic_logger = get_logger(Loggers.basic)
database_logger = get_logger(Loggers.database_err)
