from typing import Any

from locust import HttpUser, constant_pacing, task

from config import cfg


class DBUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    @task
    def login_user(self):
        form: dict[str, Any] = {
            "login": f"{cfg.user_login}",
            "password": f"{cfg.user_password}",
        }
        headers: dict[str, Any] = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        with self.client.post(
            url="/users/login/",
            data=form,
            headers=headers,
            catch_response=True,
            name=self.login_user.__name__,
        ) as request:
            if request.status_code != 200:
                request.failure(request.text)
