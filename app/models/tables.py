"""
Module. Table names storage.
"""

# from dataclasses import dataclass
from enum import StrEnum


# @dataclass
class Tables(StrEnum):
    """
    Class. Table names storage.
    """

    USERS = "users"
    WISHLIST = "wishlist"
    SETTINGS = "settings"
    HOURLY = "hourly"
    CURRENT = "current"
    DAILY = "daily"
    FAVORITES = "favorites"
