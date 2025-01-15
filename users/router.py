from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from models import Users
from users import user_controller
from users.user_controller import user_logging, linking_accounts
from utils.db_engine import db_engine
from utils.schemas import UserCreate, UserLogin, UserAccountsLink

router = APIRouter(prefix="/users")


@router.post("/registration/", summary="Register a new user")
async def create_user(
    new_user: UserCreate, session: AsyncSession = Depends(db_engine.session_dependency)
) -> JSONResponse:
    """
    Function (POST-request). Creates a new user.
    :param new_user: login (an email address), password, bot_id, bot_name
    :param session: AsyncSession
    :return: whether the user was successfully created or not (HTTP error)
    """

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

    if type(user_created) is IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User could not be created. User already exists.",
        )

    if type(user_created) is InterfaceError:
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
    """
    Function (GET-request). Logs a user in.
    :param user_login: user login (an email address)
    :param user_password: user password
    :param session: AsyncSession
    :return: whether the user was successfully logged in or not (HTTP error)
    """

    user_logging_in: UserLogin = UserLogin(login=user_login, password=user_password)

    user_logged_in: Users | None = await user_logging(
        user=user_logging_in, session=session
    )

    if user_logged_in:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User logged in",
                "user": {
                    "id": user_logged_in.id,
                    "login": user_logged_in.login,
                },
            },
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password.",
    )


@router.patch("/link/", summary="Login with e-mail and password")
async def link_account(
    user_link_info: UserAccountsLink,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    """
    Function (PATCH-request). Links web and telegram accounts.
    :param user_link_info: login (an email address) and bot_name
    :param session: AsyncSession
    :return: whether the user's accounts were successfully linked or not (HTTP error)
    """

    account_linked: bool = await linking_accounts(user=user_link_info, session=session)

    if account_linked:
        return JSONResponse(content={"success": True, "detail": "Accounts linked."})
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="Account could not be linked. Bot user not found.",
    )
