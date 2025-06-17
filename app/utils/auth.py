from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from starlette.responses import JSONResponse

from .settings import settings

http_bearer: HTTPBearer = HTTPBearer()


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
):
    try:
        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authorization scheme"
            )
        decode_jwt(token=credentials.credentials)
        return None
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
