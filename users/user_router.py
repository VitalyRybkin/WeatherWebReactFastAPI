from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from models import Users
from users import user_controller
from users.user_controller import (
    user_logging,
    linking_accounts,
    change_password,
)
from utils import to_json
from utils.db_engine import db_engine
from schemas.user_schemas import (
    UserCreate,
    UserLogin,
    UserAccountsLink,
    UserChangePassword,
)

user_router = APIRouter(prefix="/users")


@user_router.post("/registration/", summary="Register a new user")
async def create_user(
    new_user: UserCreate, session: AsyncSession = Depends(db_engine.session_dependency)
) -> JSONResponse:
    """
    Function. Creates a new user.
    :param new_user: login (an email address), password, bot_id, bot_name
    :param session: AsyncSession
    :return: whether the user was successfully created or not (HTTP error)
    """

    new_user: Users | IntegrityError | InterfaceError = (
        await user_controller.create_user(session=session, new_user=new_user)
    )

    if type(new_user) is Users:
        user_settings: dict = {}
        user_settings.update(
            {new_user.settings.__tablename__: to_json(new_user.settings)}
        )
        user_settings.update(
            {new_user.current.__tablename__: to_json(new_user.current)}
        )
        user_settings.update({new_user.daily.__tablename__: to_json(new_user.daily)})
        user_settings.update({new_user.hourly.__tablename__: to_json(new_user.hourly)})

        # TODO add email notification

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "detail": "User created.",
                "user": {
                    "id": new_user.id,
                    "login": new_user.login,
                    "bot_id": new_user.bot_id,
                    "bot_name": new_user.bot_name,
                    "alert": new_user.alert,
                    # "email_confirmed": new_user.email_confirmed
                },
                "user_settings": user_settings,
            },
        )

    if type(new_user) is IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User could not be created. User already exists.",
        )

    if type(new_user) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User could not be created.",
        )

    # TODO move default exception to decorator
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )


@user_router.get("/login/", summary="User login with e-mail and password")
async def login(
    user_login: EmailStr,
    user_password: str,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    """
    Function. Logs a user in.
    :param user_login: user login (an email address)
    :param user_password: user password
    :param session: AsyncSession
    :return: whether the user was successfully logged in or not (HTTP error)
    """

    user_to_log_in: UserLogin = UserLogin(login=user_login, password=user_password)

    logged_user: Users | InterfaceError | None = await user_logging(
        user=user_to_log_in, session=session
    )

    # TODO move user_settings dict to controller
    if type(logged_user) is Users:
        user_settings: dict = {}
        user_settings.update(
            {logged_user.settings.__tablename__: to_json(logged_user.settings)}
        )
        user_settings.update(
            {logged_user.current.__tablename__: to_json(logged_user.current)}
        )
        user_settings.update(
            {logged_user.daily.__tablename__: to_json(logged_user.daily)}
        )
        user_settings.update(
            {logged_user.hourly.__tablename__: to_json(logged_user.hourly)}
        )

        if logged_user.favorites:
            user_settings.update(
                {logged_user.favorites.__tablename__: to_json(logged_user.favorites)}
            )

        if logged_user.wishlist:
            wishlist: list = [to_json(item) for item in logged_user.wishlist]
            user_settings.update({"wishlist": wishlist})

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User logged in",
                "user": {
                    "id": logged_user.id,
                    "login": logged_user.login,
                    "dark_theme": logged_user.dark_theme,
                    "alert": logged_user.alert,
                },
                "user_settings": user_settings,
            },
        )

    if type(logged_user) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User could not be logged in.",
        )

    if not logged_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )


@user_router.patch("/link/", summary="Link web and telegram accounts")
async def link_account(
    user_link_info: UserAccountsLink,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    """
    Function. Links web and telegram accounts.
    :param user_link_info: login (an email address) and bot_name
    :param session: AsyncSession
    :return: whether the user's accounts were successfully linked or not (HTTP error)
    """

    # TODO what if already linked
    # TODO verify bot account to be linked
    account_linked: Users | None = await linking_accounts(
        user=user_link_info, session=session
    )

    if account_linked is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. Accounts could not be linked.",
        )

    if account_linked:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "detail": "Accounts linked."},
        )

    if account_linked is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account could not be linked. Bot user not found.",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )


@user_router.put(
    "/change_password/",
    summary="Change user password",
    description="Changes user password with login, password, new password",
)
async def update_user_password(
    user: UserChangePassword,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    """
    Function. Changes user password.
    :param user: login, password, new password
    :param session: SQLAlchemy session
    :return: whether the user password was successfully updated or not (HTTP error)
    """
    user_password_changed: Users | InterfaceError | None = await change_password(
        user=user, session=session
    )

    if type(user_password_changed) is Users:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User password has changed.",
            },
        )

    if user_password_changed is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Incorrect password."},
        )

    if type(user_password_changed) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User password could not be changed.",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )
