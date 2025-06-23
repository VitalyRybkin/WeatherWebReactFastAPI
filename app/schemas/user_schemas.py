"""
Module. User pydentic models.
"""

from typing import Annotated, List, Dict

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict

from app.schemas.setting_schemas import SettingsPublic, FavoriteLocation


class UserBase(BaseModel):
    """
    Base pydentic model for user
    Attributes
    ----------
    login: EmailStr
        user's email as a unique login
    """

    login: EmailStr | None = None


class UserPassword(BaseModel):
    """
    Base pydentic model for user's password
    Attributes
    ---------
    password: str
        string password to be hashed
    """

    password: Annotated[str, MinLen(5), MaxLen(15)] | None = None


class UserTelegram(BaseModel):
    """
    Base pydentic model for user Telegram registration
    Attributes
    ----------
    bot_id: int
        bot id of the telegram user
    bot_name: str
        name of the telegram user
    """

    bot_id: int | None = None
    bot_name: str | None = None


class UserPublic(UserBase, UserTelegram):
    """
    Pydentic model for user registration information
    Attributes
    ----------
    id: int
        user account ID
    """

    model_config = ConfigDict()
    id: int | None = None


class UserCreate(UserBase, UserPassword, UserTelegram):
    """
    Pydentic model for user creation
    """


class UserLogin(UserBase, UserPassword):
    """
    Pydentic model for user login
    """

    model_config = ConfigDict()


class UserAccountsLink(UserBase, UserTelegram):
    """
    Pydentic model for user accounts link
    """


class UserChangePassword(UserBase, UserPassword):
    """
    Pydentic model for user change password.
    Attributes
    --------
    login: EmailStr
        user's email as a unique login
    password: str | None
        user account password
    new_password: str | None
        user new account password
    """

    new_password: Annotated[str, MinLen(5), MaxLen(15)] | None = None


class LocationPublic(BaseModel):
    """
    Pydentic model for user location response
    Attributes
    --------
    loc_id: int
        location's id
    loc_name: str
        location's name
    loc_region: str
        location's region
    loc_country: str
        location's country
    """

    loc_id: int
    loc_name: str
    loc_region: str
    loc_country: str


class UserFullInfoPublic(BaseModel):
    """
    Pydentic model for user creation response
    Attributes
    ---------
    user_info: UserPublic
        user info pydantic model
    user_settings: SettingsPublic
        user settings pydantic model
    """

    model_config = ConfigDict()
    user_info: UserPublic
    user_settings: SettingsPublic


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class LoggedUserPublic(UserFullInfoPublic):
    """
    Pydentic model for user login response
    Attributes
    --------
    favorite: FavoriteLocation | Dict
        user's favorite location pydentic model
    wishlist: List[FavoriteLocation] | List
        user's wishlist pydentic model
    """

    # user_info: UserPublic
    # user_settings: SettingsPublic
    favorite: FavoriteLocation | Dict
    wishlist: List[FavoriteLocation] | List
    # token: TokenInfo
