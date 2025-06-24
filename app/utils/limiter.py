from math import ceil

from fastapi import Request, Response

from app.utils.exception_handler import TooManyRequestsError


async def error_callback(request: Request, response: Response, expire: int):
    """
    default callback when too many requests
    :param request:
    :param expire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(expire / 1000)

    raise TooManyRequestsError(
        "Too Many Requests",
        {"Retry-After": str(expire)},
    )
