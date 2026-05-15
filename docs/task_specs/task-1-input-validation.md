# Task 1: Input Validation

## Description

Add a function `validate_email(email: str) -> bool` to `src/api/validators.py` that returns `True` if the email is well-formed and `False` otherwise. Add corresponding tests in `tests/test_validators.py`.

## Allowed Files

- `src/api/validators.py`
- `tests/test_validators.py`

## Drift Surface

- `src/api/routes/auth.py`
- `src/api/middleware.py`

## Verification

- `pytest tests/test_validators.py`
- `pytest`
