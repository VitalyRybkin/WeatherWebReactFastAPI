from datetime import timedelta, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Coroutine

import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from requests import Response, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .settings import settings


def encode_jwt(
    payload: dict[str, Any],
    private_key_path: Path = settings.jwt_authentication.private_key_path.read_text(),
    algorithm: str = settings.jwt_authentication.algorithm,
    expires_in: int = settings.jwt_authentication.access_token_expires_in,
    expire_in_timedelta: timedelta | None = None,
) -> str:
    """
    Function. Encode JWT
    :param payload: payload
    :param private_key_path: path to private key file
    :param algorithm: encryption algorithm
    :param expires_in: set token expiration time in minutes
    :param expire_in_timedelta: passed token expiration time in minutes
    :return: encoded jwt
    """

    extend_payload = payload.copy()
    now = datetime.now(timezone.utc)

    token_expire: datetime = (
        now + expire_in_timedelta
        if expire_in_timedelta
        else now + timedelta(minutes=expires_in)
    )

    extend_payload.update({"exp": token_expire})
    return jwt.encode(extend_payload, private_key_path, algorithm=algorithm)


def decode_jwt(
    token: str | bytes,
    public_key_path: Path = settings.jwt_authentication.public_key_path.read_text(),
    algorithm: str = settings.jwt_authentication.algorithm,
) -> str:
    """
    Function. Decode JWT
    :param token: encoded jwt
    :param public_key_path: path to public key file
    :param algorithm: decryption algorithm
    :return: decoded jwt
    """
    return jwt.decode(
        token,
        public_key_path,
        algorithms=[algorithm],
    )


class JWTAuthentication(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())

    async def dispatch(self, request: Request, call_next: Callable) -> str | Any:
        try:
            decode_jwt(token=self.credentials.credentials)
            return await call_next(request)
        except jwt.exceptions.ExpiredSignatureError:
            return await call_next(request)
        except jwt.exceptions.InvalidTokenError:
            return await call_next(request)
