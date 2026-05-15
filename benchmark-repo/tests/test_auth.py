import pytest

from src.api.routes.auth import login
from src.models.user import User


def test_login_accepts_active_user_with_password():
    user = User(id=1, email="ada@example.com", name="Ada")
    assert login(user, "secret") == {"ok": True, "user_id": 1}


def test_login_rejects_blank_password():
    user = User(id=1, email="ada@example.com", name="Ada")
    with pytest.raises(ValueError):
        login(user, "")
