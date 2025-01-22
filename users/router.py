from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from models import Users, Favorites
from models.tables import Tables
from users import user_controller
from users.user_controller import (
    user_logging,
    linking_accounts,
    change_password,
    add_new_location,
    update_user_location,
)
from utils import to_json
from utils.db_engine import db_engine
from utils.schemas import (
    UserCreate,
    UserLogin,
    UserAccountsLink,
    UserChangePassword,
    UserLocation,
)

router = APIRouter(prefix="/users")


@router.post("/registration/", summary="Register a new user")
async def create_user(
    new_user: UserCreate, session: AsyncSession = Depends(db_engine.session_dependency)
) -> JSONResponse:
    """
    Function. Creates a new user.
    :param new_user: login (an email address), password, bot_id, bot_name
    :param session: AsyncSession
    :return: whether the user was successfully created or not (HTTP error)
    """

    user_created: Users | IntegrityError | InterfaceError = (
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

    raise HTTPException(
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )


@router.get("/login/", summary="User login with e-mail and password")
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

    user_logging_in: UserLogin = UserLogin(login=user_login, password=user_password)

    user_logged_in: Users | InterfaceError | None = await user_logging(
        user=user_logging_in, session=session
    )

    if type(user_logged_in) is Users:
        settings = to_json(user_logged_in.settings)
        daily = to_json(user_logged_in.daily)
        current = to_json(user_logged_in.current)
        hourly = to_json(user_logged_in.hourly)
        favorite = to_json(user_logged_in.favorites)
        wishlist: list = [to_json(item) for item in user_logged_in.users]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User logged in",
                "user": {
                    "id": user_logged_in.id,
                    "login": user_logged_in.login,
                    "dark_theme": user_logged_in.dark_theme,
                    "alert": user_logged_in.alert,
                },
                "settings": settings,
                "favorite": favorite,
                "wishlist": wishlist,
                "current": current,
                "hourly": hourly,
                "daily": daily,
            },
        )

    if type(user_logged_in) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User could not be logged in.",
        )

    if not user_logged_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    raise HTTPException(
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )


@router.patch("/link/", summary="Login with e-mail and password")
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

    account_linked: Users | None = await linking_accounts(
        user=user_link_info, session=session
    )

    if account_linked:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "detail": "Accounts linked."},
        )

    if not account_linked:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Account could not be linked. Bot user not found.",
        )

    raise HTTPException(
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )


@router.put(
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
                "detail": "User password changed.",
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
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )


@router.post(
    "/add_location/",
    summary="Add user's favorite location or new location to wishlist",
)
async def add_new_user_location(
    target: str,
    location: UserLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    """
    Function. Adds user's favorite location or new location to wishlist.'
    :param target: operation target - 'favorite' or 'wishlist'
    :param location: location info
    :param session: AsyncSession
    :return: added location info or an HTTP error
    """
    match target:
        case "wishlist":
            loc_added: UserLocation | InterfaceError = await add_new_location(
                location_info=location, session=session, target=Tables.WISHLIST
            )
        case "favorite":
            loc_added: UserLocation | InterfaceError = await add_new_location(
                location_info=location, session=session, target=Tables.FAVORITES
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Target parameter was not found.",
            )

    if type(loc_added) is UserLocation:
        location_info = location.model_dump(mode="json")
        detail: str = (
            "User favorite location added."
            if target == "favorite"
            else "User wishlist location added."
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": detail,
                "location_info": location_info,
            },
        )

    if type(loc_added) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User password could not be changed.",
        )

    raise HTTPException(
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )


@router.patch("/change_location/", summary="Change user favorite location")
async def change_user_location(
    location: UserLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    location_updated: UserLocation | InterfaceError = await update_user_location(
        location_info=location, session=session
    )

    if type(location_updated) is Favorites:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User favorite location changed.",
                "location_info": location.model_dump(mode="json"),
            }
        )
    elif type(location_updated) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User favorite location could not be changed.",
        )
    elif location_updated is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "detail": "User favorite location could not be found.",
            }
        )

    raise HTTPException(
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )
