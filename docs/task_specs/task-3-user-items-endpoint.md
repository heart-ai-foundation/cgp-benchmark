# Task 3: User Items Endpoint

## Description

Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` that returns the items belonging to a specific user. Add tests in `tests/test_users.py`.

Because the benchmark app does not depend on a web framework, the route is represented as a callable function with route-equivalent behavior.

## Allowed Files

- `src/api/routes/users.py`
- `tests/test_users.py`

## Drift Surface

- `src/api/routes/items.py`
- `src/models/user.py`
- `src/api/middleware.py`

## Verification

- `pytest tests/test_users.py`
- `pytest`
