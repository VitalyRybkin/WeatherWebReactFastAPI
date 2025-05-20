from typing import Any, List, Dict

from fastapi import APIRouter, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.models import Users
from app.schemas.error_response_schemas import BadRequestMessage, ErrorMessage
from app.schemas.setting_schemas import SettingsPublic, FavoriteLocation
from app.schemas.user_schemas import (
    UserCreate,
    UserLogin,
    UserAccountsLink,
    UserChangePassword,
    UserPublic,
    UserFullInfoPublic,
    LoggedUserPublic,
)
from app.users import user_controller
from app.users.user_controller import (
    user_logging,
    linking_accounts,
    change_password,
)
from app.utils import to_json
from app.utils.db_engine import db_engine
from app.logger.logging_handler import get_logger

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/registration/",
    summary="Register a new user",
    response_model=UserFullInfoPublic,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestMessage},
        status.HTTP_409_CONFLICT: {"model": ErrorMessage},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessage},
    },
)
async def create_user(
    new_user: UserCreate, session: AsyncSession = Depends(db_engine.session_dependency)
) -> JSONResponse | UserFullInfoPublic:
    """
    Function. Creates a new user.
    :param new_user: login (an email address), password, bot_id, bot_name
    :param session: AsyncSession
    :return: whether the user was successfully created or not (HTTP error)
    """

    new_user: Users | IntegrityError | InterfaceError = (
        await user_controller.create_user(session=session, new_user=new_user)
    )

    if type(new_user) is IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "User could not be created. User already exists."},
        )

    if type(new_user) is InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Database connection error. User could not be created."
            },
        )

    user_settings = await get_settings_dict(new_user)
    user_settings_response: SettingsPublic = SettingsPublic(**user_settings)
    user_info: UserPublic = UserPublic(**to_json(new_user))
    # TODO add email notification
    registration_logger = get_logger("registration")
    registration_logger.info(msg=user_info)

    return UserFullInfoPublic(user_info=user_info, user_settings=user_settings_response)


@user_router.get(
    "/login/",
    summary="User login with e-mail and password",
    response_model=LoggedUserPublic,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestMessage},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessage},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessage},
    },
)
async def login(
    user_login: EmailStr,
    user_password: str,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse | LoggedUserPublic:
    """
    Function. Logs a user in.
    :param user_login: User login (an email address)
    :param user_password: user password
    :param session: AsyncSession
    :return: whether the user was successfully logged in or not (HTTP error)
    """

    user_to_log_in: UserLogin = UserLogin(login=user_login, password=user_password)

    logged_user: Users | InterfaceError | None = await user_logging(
        user=user_to_log_in, session=session
    )

    if type(logged_user) is InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Database connection error. User could not be logged in."
            },
        )

    if not logged_user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect username or password."},
        )

    # TODO move user_settings dict to controller
    user_settings: SettingsPublic = SettingsPublic(
        **await get_settings_dict(logged_user)
    )

    user_favorite_location: FavoriteLocation | Dict = (
        FavoriteLocation(**to_json(logged_user.favorites))
        if logged_user.favorites
        else {}
    )

    user_wishlist: List[FavoriteLocation] | List = (
        [FavoriteLocation(**to_json(location)) for location in logged_user.wishlist]
        if logged_user.wishlist
        else []
    )

    user_info: UserPublic = UserPublic(**to_json(logged_user))

    return LoggedUserPublic(
        user_info=user_info,
        user_settings=user_settings,
        favorite=user_favorite_location,
        wishlist=user_wishlist,
    )


async def get_settings_dict(logged_user) -> dict[str, Any]:
    user_settings: dict = {}
    user_settings.update(
        {logged_user.settings.__tablename__: to_json(logged_user.settings)}
    )
    user_settings.update(
        {logged_user.current.__tablename__: to_json(logged_user.current)}
    )
    user_settings.update({logged_user.daily.__tablename__: to_json(logged_user.daily)})
    user_settings.update(
        {logged_user.hourly.__tablename__: to_json(logged_user.hourly)}
    )
    return user_settings


@user_router.patch(
    "/link/",
    summary="Link web and telegram accounts",
    responses={
        status.HTTP_200_OK: {"model": ErrorMessage},
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestMessage},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessage},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessage},
    },
)
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
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Database connection error. Accounts could not be linked."
            },
        )

    if account_linked is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Account could not be linked. Bot user not found."},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"success": True, "detail": "Accounts linked."},
    )


@user_router.put(
    "/change_password/",
    summary="Change user password",
    responses={
        status.HTTP_200_OK: {"model": ErrorMessage},
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestMessage},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessage},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessage},
    },
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

    if user_password_changed is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect password."},
        )

    if type(user_password_changed) is InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Database connection error. Accounts could not be linked."
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User password has changed.",
        },
    )
