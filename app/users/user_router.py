"""
Module. User operations (registration, login, change password etc.) API routes.
"""

from typing import Any, List, Dict

from fastapi import APIRouter, status, Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app import utils
from app.logger.logging_handler import info_logger
from app.models import Users
from app.schemas.error_response_schemas import (
    DBErrorMessage,
    ConflictErrorMessage,
    UnauthorizedErrorMessage,
    NotFoundErrorMessage,
    Ok,
)
from app.schemas.setting_schemas import SettingsPublic, FavoriteLocation
from app.schemas.user_schemas import (
    UserCreate,
    UserAccountsLink,
    UserChangePassword,
    UserPublic,
    UserFullInfoPublic,
    LoggedUserPublic,
    TokenInfo,
)
from app.users import user_controller
from app.users.user_controller import (
    user_logging,
    linking_accounts,
    change_password,
)
from app.utils import to_json
from app.utils.auth import user_auth
from app.utils.db_engine import db_engine
from app.utils.exception_handler import (
    DatabaseInterfaceError,
    UnauthorizedError,
    DatabaseIntegrityError,
    NotFoundError,
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/registration/",
    summary="Register a new user",
    response_model=UserFullInfoPublic,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ConflictErrorMessage,
            "description": "User already exists.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": DBErrorMessage,
            "description": "Database connection error.",
        },
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

    if isinstance(new_user, IntegrityError):
        raise DatabaseIntegrityError("User already exists.")

    if isinstance(new_user, InterfaceError):
        raise DatabaseInterfaceError("User could not be created.")

    user_settings = await get_settings_dict(new_user)
    user_settings_response: SettingsPublic = SettingsPublic(**user_settings)
    user_info: UserPublic = UserPublic(**to_json(new_user))

    # TODO add email notification

    info_logger.info(msg=user_info)

    return UserFullInfoPublic(user_info=user_info, user_settings=user_settings_response)


@user_router.post(
    "/login/",
    summary="User login with e-mail and password",
    response_model=LoggedUserPublic,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": UnauthorizedErrorMessage,
            "description": "Incorrect username or password.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": DBErrorMessage,
            "description": "Database connection error.",
        },
    },
)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse | LoggedUserPublic:
    """
    Function. Logs a user in.
    :return: Whether the user was successfully logged in or not (HTTP error)
    """
    logged_user: Users | None | type[InterfaceError] = await user_logging(
        form_data.username, form_data.password, session
    )

    if isinstance(logged_user, InterfaceError):
        raise DatabaseInterfaceError("User could not be logged in.")

    if not logged_user:
        raise UnauthorizedError("Incorrect username or password.")

    user_token: TokenInfo = TokenInfo(
        access_token=utils.auth.encode_jwt(
            {
                "sub": logged_user.id,
                "login": logged_user.login,
            }
        ),
    )

    response.headers["Authorization"] = (
        f"{user_token.token_type} {user_token.access_token}"
    )

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
        # token=user_token,
    )


async def get_settings_dict(logged_user) -> dict[str, Any]:
    """
    Function. User settings dict parsed from DB response.
    :param logged_user: logged user data
    :return: user settings as dict
    """
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
    dependencies=[Depends(user_auth)],
    response_model=Ok,
    responses={
        # status.HTTP_200_OK: {"model": Success, "description": "Accounts linked."},
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundErrorMessage,
            "description": "Record not found error.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": DBErrorMessage,
            "description": "Database connection error.",
        },
    },
)
async def link_account(
    user_link_info: UserAccountsLink,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> Ok:
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
        raise DatabaseInterfaceError("Accounts could not be linked.")

    if account_linked is None:
        raise NotFoundError(
            "Bot user not found.",
            {"X-Error-Code": "USER_NOT_FOUND"},
        )

    return Ok(success=True, message="Accounts linked.")


@user_router.put(
    "/change_password/",
    summary="Change user password",
    dependencies=[Depends(user_auth)],
    response_model=Ok,
    responses={
        # status.HTTP_200_OK: {"model": Success, "description": "APassword changed."},
        status.HTTP_401_UNAUTHORIZED: {
            "model": DBErrorMessage,
            "description": "Incorrect password.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": DBErrorMessage,
            "description": "Database connection error.",
        },
    },
    description="Changes user password with login, password, new password",
)
async def update_user_password(
    user: UserChangePassword,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> Ok:
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
        raise UnauthorizedError("Incorrect password.")

    if isinstance(user_password_changed, InterfaceError):
        raise DatabaseInterfaceError(message="Accounts could not be linked.")

    return Ok(success=True, message="Password changed.")
