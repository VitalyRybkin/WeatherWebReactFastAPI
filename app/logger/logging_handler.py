import logging

from app.logger.logging_config import get_logging_config, Loggers
import logging.config


def get_logger(name):

    logger = logging.getLogger(name)
    logger_config = get_logging_config()
    logging.config.dictConfig(logger_config)

    return logger


basic_logger = get_logger(Loggers.basic)
database_logger = get_logger(Loggers.database_err)
