from dataclasses import dataclass


@dataclass
class Tables:
    """
    Dataclass to store table names
    """
    USERS: str = "users"
    WISHLIST: str = "wishlist"
    SETTINGS: str = "settings"
    HOURLY: str = "hourly"
    CURRENT: str = "current"
    DAILY: str = "daily"
    FAVORITES: str = "favorites"
