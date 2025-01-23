from models import Favorites
from users.crud import update_location, get_location, add_location
from utils.schemas import UserLocation

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import InterfaceError

async def add_new_location(
    location_info: UserLocation, session: AsyncSession, target: str
):
    """
    Function. Handling adding new location to database.
    :param location_info: location information
    :param session: AsyncSession
    :param target: target of the operation (table name)
    :return: location info or an error on adding new location
    """
    location_added: UserLocation | InterfaceError = await add_location(
        location_info, session, target
    )

    return location_added


async def update_user_location(location_info: UserLocation, session: AsyncSession):
    """
    Function. Handling updating user location
    :param location_info: new location information
    :param session: AsyncSession
    :return: new location info or an error on updating new location
    """
    location: Favorites | InterfaceError  = await get_location(
        session, acc_id=location_info.acc_id
    )

    if type(location) is Favorites:
        location.loc_id = location_info.loc_id
        location.loc_name = location_info.loc_name
        location.loc_region = location_info.loc_region
        location.loc_country = location_info.loc_country
        await update_location(location, session)

    return location