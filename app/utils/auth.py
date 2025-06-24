"""
Module. User authentication functions and classes.
"""

from datetime import timedelta, datetime, timezone
from typing import Any, Optional

import jwt
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .settings import settings
from ..schemas.user_schemas import TokenInfo


class Bearer(HTTPBearer):
    """
    Class. Overrides HTTPBearer behaviour - auto_error true on location_id endpoint.
    """

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:

        if (
            request.url.path
            == f"/app/api_v1/id/{request.path_params.get('location_id')}/"
        ):
            self.auto_error = False
        await super().__call__(request)


http_bearer: HTTPBearer = Bearer()


def encode_jwt(
    payload: dict[str, Any],
    private_key_path: str = settings.jwt_authentication.private_key_path.read_text(),
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
    public_key_path: str = settings.jwt_authentication.public_key_path.read_text(),
    algorithm: str = settings.jwt_authentication.algorithm,
):
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


async def user_auth(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> HTTPAuthorizationCredentials | None:
    """
    Function. User authentication handler.
    :param credentials: user credentials
    :return: auth token or none
    """
    if credentials:
        try:
            if credentials.scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authorization scheme"
                )
            payload = decode_jwt(token=credentials.credentials)
            return payload
        except jwt.ExpiredSignatureError as exc:
            raise HTTPException(status_code=401, detail="Token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise HTTPException(status_code=401, detail="Invalid token") from exc
    return None


class AuthResponseMiddleware(BaseHTTPMiddleware):
    """
    Class. Middleware to handle auth response header.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        auth_header = request.headers.get("Authorization")

        if auth_header:
            token: str = auth_header.split("Bearer ")[1]
            payload = decode_jwt(token=token)
            user_token: TokenInfo = TokenInfo(
                access_token=encode_jwt(
                    {
                        "sub": payload["sub"],
                        "login": payload["login"],
                    }
                ),
            )
            response.headers["Authorization"] = (
                f"{user_token.token_type} {user_token.access_token}"
            )

        return response
