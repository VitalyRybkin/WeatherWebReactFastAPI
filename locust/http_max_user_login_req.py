from typing import Any

from locust import HttpUser, constant_pacing, task

from config import cfg


class DBUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    @task
    def login_user(self):
        body: dict[str, Any] = {
            "user_login": f"{cfg.user_login}",
            "user_password": f"{cfg.user_password}",
        }
        with self.client.get(
            f"/users/login/?user_login={cfg.user_login}&user_password={cfg.user_password}",
            catch_response=True,
            name=self.login_user.__name__,
        ) as request:
            if request.status_code != 200:
                request.failure(request.text)
