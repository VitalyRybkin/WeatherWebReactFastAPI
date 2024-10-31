from utils.schemas import User


def create_user(register_new_user: User) -> dict:
    user = register_new_user.model_dump()
    return {
        "success": True,
        "user": user,
    }