from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from prometheus_client import make_asgi_app, Counter

from api_v1.views import location_router
from models import AbstractBaseModel
from users.settings_router import settings_router
from users.user_router import user_router
from utils.db_engine import db_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_engine.engine.begin() as conn:
        await conn.run_sync(AbstractBaseModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan, root_path="/app")
app.include_router(user_router, tags=["users"])
app.include_router(settings_router, tags=["settings"])
app.include_router(location_router, tags=["locations"])

index_counter = Counter("index_counter", "Description of counter")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
def index():
    index_counter.inc()
    return "Wellcome to the weather forecast world!"


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
