from src.models.user import User


USERS = [
    User(id=1, email="ada@example.com", name="Ada", item_ids=[1, 2]),
    User(id=2, email="grace@example.com", name="Grace", item_ids=[3]),
]


def list_users(active_only: bool = True) -> list[dict]:
    return [
        {"id": user.id, "email": user.email, "name": user.name}
        for user in USERS
        if user.active or not active_only
    ]


def get_user(user_id: int) -> User | None:
    for user in USERS:
        if user.id == user_id:
            return user
    return None
