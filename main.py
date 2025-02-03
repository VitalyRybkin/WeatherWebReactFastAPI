from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1.views import location_router
from models import AbstractBaseModel
from users.user_router import user_router
from users.settings_router import settings_router
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


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
