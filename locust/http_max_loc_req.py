import random
from typing import Any

from locust import HttpUser, constant_pacing, task

from config import cfg


class APIUser(HttpUser):
    """
    Class. Load test for API endpoints.
    """

    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    @task
    def get_location_name(self) -> None:
        location_name: str = random.choice(cfg.location_name)

        with self.client.get(
            f"/api_v1/{location_name}",
            catch_response=True,
            name=self.get_location_name.__name__,
        ) as request:
            if request.status_code != 200:
                request.failure(request.text)

            if request.json()[0]:
                location_id: int = request.json()[0]["id"]
                self.get_location_forecast(location_id)

    @task
    def get_location_forecast(self, location_id: int) -> None:
        body: dict[str, Any] = {
            "settings": {
                "current": True,
                "daily": 3,
                "hourly": 8,
                "units": "F",
                "dark_theme": False,
                "alerts": False,
                "notifications": {},
            },
            "current": {
                "visibility": True,
                "humidity": True,
                "wind_extended": True,
                "pressure": True,
            },
            "hourly": {
                "visibility": True,
                "humidity": True,
                "wind_extended": True,
                "pressure": True,
            },
            "daily": {
                "visibility": True,
                "humidity": True,
                "astro": True,
            },
        }
        with self.client.get(
            f"/api_v1/{location_id}",
            catch_response=True,
            json=body,
            name=self.get_location_forecast.__name__,
        ) as request:
            if request.status_code != 200:
                request.failure(request.text)
