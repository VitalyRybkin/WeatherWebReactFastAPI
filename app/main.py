"""
Main app module - start FastAPI app.
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import ORJSONResponse
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api_v1.views import location_router
from app.users.settings_router import settings_router
from app.users.user_router import user_router
from app.utils.auth import user_auth, AuthResponseMiddleware
from app.utils.db_engine import db_engine


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0613, W0621
    """
    Function. Create database.
    :param app: FastAPI
    :return: None
    """
    # async with db_engine.engine.begin() as conn:
    #     await conn.run_sync(AbstractBaseModel.metadata.drop_all)
    yield
    await db_engine.dispose()


app = FastAPI(lifespan=lifespan, root_path="/app", response_class=ORJSONResponse)
app.include_router(user_router, tags=["users"])
app.include_router(
    settings_router, tags=["settings"], dependencies=[Depends(user_auth)]
)
app.include_router(location_router, tags=["locations"])

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

origins: list[str] = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthResponseMiddleware)


@app.exception_handler(HTTPException)
async def enhanced_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            # "error_code": exc.headers.get("X-Error-Code") if exc.headers else None,
            "headers": exc.headers,
            # "path": request.url.path,
        },
    )


@app.get("/", tags=["root"])
def index():
    """
    Function. Main page - start message.
    :return: string
    """
    return "Wellcome to the weather forecast world!"


Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
