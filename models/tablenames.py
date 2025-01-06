from dataclasses import dataclass


@dataclass
class TableNames:
    USERS: str = "users"
    WISHLIST: str = "wishlist"
    SETTINGS: str = "settings"
    HOURLY: str = "hourly"
    CURRENT: str = "current"
    DAILY: str = "daily"
    FAVORITES: str = "favorites"

