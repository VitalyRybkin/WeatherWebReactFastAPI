from typing import Any

from celery_tasks.tasks import location_by_name
from utils.setting_schemas import LocationPublic


def get_location(location_name: str = None, location_id: int = None) -> list[dict[str, Any]] | None:
    if location_name:
        result = location_by_name.apply_async(args=[location_name])

        locations_list: list[dict[str, Any]] = []
        for location in result.get():
            locations_list.append(LocationPublic(**location).model_dump())
        return locations_list