from src.api.validators import require_non_empty
from src.models.user import User


def login(user: User, password: str) -> dict:
    require_non_empty(password, "password")
    if not user.can_login():
        return {"ok": False, "reason": "inactive"}
    return {"ok": True, "user_id": user.id}
