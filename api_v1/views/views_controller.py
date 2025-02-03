from celery_tasks.tasks import location_by_name


def get_location(location_name: str = None, location_id: int = None) -> list | None:
    if location_name:
        result = location_by_name.apply_async(args=[location_name])
        return result.get()
