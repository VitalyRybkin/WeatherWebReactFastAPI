from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from users import user_controller
from utils.schemas import User, UserOut
from utils.db_engine import db_engine

router = APIRouter(prefix="/users")


@router.post("/registration/")
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
