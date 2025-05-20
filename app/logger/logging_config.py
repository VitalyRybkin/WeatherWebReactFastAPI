from typing import Dict, Any


def get_logging_config() -> Dict[str, Any]:
    dict_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(levelname)s] %(asctime)s | %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "filters": {},
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "loggers": {
            "root": {
                "handlers": ["stdout"],
                "level": "INFO",
            }
        },
    }
    return dict_config
