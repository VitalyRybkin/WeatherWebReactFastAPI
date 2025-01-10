from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from users import user_controller
from users.user_controller import user_logging
from utils.schemas import User, UserOut, UserLogin
from utils.db_engine import db_engine

router = APIRouter(prefix="/users")


@router.post("/registration/", summary="Register a new user")
async def create_user(
    new_user: User, session: AsyncSession = Depends(db_engine.session_dependency)
) -> JSONResponse:
    user_created: UserOut | None = await user_controller.create_user(
        session=session, new_user=new_user
    )

    if user_created:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "detail": "User created",
                "user": user_created.model_dump(),
            },
        )

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User could not be created. User already exists",
    )


@router.get("/login/", summary="User login with e-mail and password")
async def login(
    user_login: EmailStr,
    user_password: str,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    user: UserLogin = UserLogin(email=user_login, password=user_password)
    user_logged_in: bool = await user_logging(user=user, session=session)

    if user_logged_in:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User logged in",
            },
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
