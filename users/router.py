from typing import Type

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from sqlalchemy.exc import InterfaceError, IntegrityError
from models import Users
from users import user_controller
from users.user_controller import user_logging, linking_accounts
from utils.db_engine import db_engine
from utils.schemas import UserCreate, UserLogin

router = APIRouter(prefix="/users")


@router.post("/registration/", summary="Register a new user")
async def create_user(
    new_user: UserCreate, session: AsyncSession = Depends(db_engine.session_dependency)
) -> JSONResponse:
    user_created: Users | dict[str, IntegrityError | InterfaceError] = (
        await user_controller.create_user(session=session, new_user=new_user)
    )

    if type(user_created) is Users:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "detail": "User created.",
                "user": {
                    "id": user_created.id,
                    "login": user_created.login,
                    "bot_id": user_created.bot_id,
                    "bot_name": user_created.bot_name,
                },
            },
        )

    if type(user_created["error"]) is IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User could not be created. User already exists.",
        )

    if type(user_created["error"]) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User could not be created.",
        )


@router.get("/login/", summary="User login with e-mail and password")
async def login(
    user_login: EmailStr,
    user_password: str,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    user_logging_in: UserLogin = UserLogin(login=user_login, password=user_password)
    user_logged_in: bool = await user_logging(user=user_logging_in, session=session)

    if user_logged_in:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User logged in",
            },
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )


@router.patch("/link/", summary="Login with e-mail and password")
async def link_account(
    user_login: EmailStr,
    bot_name: str,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    account_linked: bool = await linking_accounts(
        user_login=user_login, bot_name=bot_name, session=session
    )
    if account_linked:
        return JSONResponse(content={"success": True, "detail": "Account linked"})
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="Account could not be linked. Bot user not found.",
    )


@router.post("/logout", summary="Logout")
async def logout(
    user: UserCreate, session: AsyncSession = Depends(db_engine.session_dependency)
):
    return user
