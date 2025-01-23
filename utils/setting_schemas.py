from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class FavoriteLocation(BaseModel):
    """
    Pydentic model for user location information
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    acc_id: int
    loc_id: int
    loc_name: Annotated[str, MaxLen(100)]
    loc_region: Annotated[str, MaxLen(100)]
    loc_country: Annotated[str, MaxLen(100)]