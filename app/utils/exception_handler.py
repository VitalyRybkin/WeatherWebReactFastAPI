from fastapi import HTTPException

from app.logger.logging_handler import database_logger, info_logger


class BadRequestError(HTTPException):
    def __init__(self):
        super().__init__(400, detail="Server cannot process the request.")


class UnauthorizedError(HTTPException):
    def __init__(self, message: str):
        super().__init__(401, message, headers={"WWW-Authenticate": "Bearer"})


class NotFoundError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            404, message, headers={"X-Custom-Error-Header": "USER_NOT_FOUND"}
        )


class DatabaseIntegrityError(HTTPException):
    def __init__(self, message: str, headers: dict[str, str] = None):
        super().__init__(409, message, headers)
        database_logger.error(message)
        info_logger.error(message)


class UnprocessableEntityError(HTTPException):
    def __init__(self, message: str, headers: dict[str, str] = None):
        super().__init__(422, message, headers)


class TooManyRequestsError(HTTPException):
    def __init__(self, message: str, headers: dict[str, str] = None):
        super().__init__(429, message, headers)


class DatabaseInterfaceError(HTTPException):
    def __init__(self, message: str):
        super().__init__(500, f"Database connection error. {message}")
        database_logger.exception("Database connection error.")
