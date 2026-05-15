import pytest

from src.api.validators import require_non_empty, validate_positive_int


def test_require_non_empty_strips_value():
    assert require_non_empty("  hello  ", "field") == "hello"


def test_require_non_empty_rejects_blank():
    with pytest.raises(ValueError):
        require_non_empty(" ", "field")


def test_validate_positive_int_accepts_positive_integer():
    assert validate_positive_int(3, "count") == 3
