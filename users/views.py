from fastapi import APIRouter

from users import user_controller
from utils.schemas import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user: User):
    return user_controller.create_user(register_new_user=user)
