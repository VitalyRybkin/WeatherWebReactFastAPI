import time
from functools import wraps

import celery
from celery.exceptions import MaxRetriesExceededError, TimeoutError
from fastapi import HTTPException
from kombu.exceptions import OperationalError

from app.logger.logging_handler import info_logger
from app.utils.settings import settings


class APIRetryHandler:
    """
    Class. API retry handler. Attempts to retry the request if an error occurs.
    Attributes:
        max_retries (int): The maximum number of retries.
        delay(int): The delay in seconds between retries.
    """

    def __init__(
        self,
        max_retries: int = settings.retry.LIMIT,
        delay: int = settings.retry.DELAY_SEC,
    ):
        self.max_retries = max_retries
        self.delay = delay

    def __call__(self, fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            attempts: int = 1
            while attempts <= self.max_retries:
                print(
                    f"Trying {fn.__name__.upper()!r}... [attempts: {attempts}/{self.max_retries}]"
                )
                try:
                    return fn(*args, **kwargs)
                except ConnectionError as e:
                    info_logger.info(f"Retrying {fn}, exception: {e}")
                except Exception as e:
                    info_logger.info(f"Retrying {fn}, exception: {e}")

                attempts += 1
                time.sleep(self.delay)

            raise HTTPException(status_code=502, detail="Too many retries.")

        return wrapper


class RetryTask(celery.Task):
    """
    Class. Inheritor of celery.Task class. Sets retry options.
    """

    autoretry_for = (
        Exception,
        ConnectionError,
        MaxRetriesExceededError,
        TimeoutError,
        OperationalError,
    )
    retry_kwargs = {"max_retries": 5}
    retry_backoff = 1
    retry_jitter = True
