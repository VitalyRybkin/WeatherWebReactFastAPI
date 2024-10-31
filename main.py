from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from users.views import router as users_router
from models import AbstractBaseModel
from utils.db_engine import db_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_engine.engine.begin() as conn:
        await conn.run_sync(AbstractBaseModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
