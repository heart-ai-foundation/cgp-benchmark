from src.api.routes.users import get_user, list_users


def test_list_users_returns_active_users():
    users = list_users()
    assert [user["email"] for user in users] == [
        "ada@example.com",
        "grace@example.com",
    ]


def test_get_user_returns_matching_user():
    user = get_user(1)
    assert user is not None
    assert user.name == "Ada"
