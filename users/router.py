from fastapi import APIRouter

from users import user_controller
from utils.schemas import User

router = APIRouter(prefix="/users")


@router.post("/registration/", response_model=User)
def create_user(new_user: User):
    return user_controller.create_new_user(register_new_user=new_user)
