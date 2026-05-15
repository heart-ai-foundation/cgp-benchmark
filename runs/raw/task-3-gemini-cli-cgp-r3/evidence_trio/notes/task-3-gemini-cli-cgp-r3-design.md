# Design Note - Task 3: User Items Endpoint

## Objective
Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` that returns the items belonging to a specific user.

## Implementation Plan
- Modify `benchmark-repo/src/api/routes/users.py`:
    - Implement `list_user_items(user_id: int) -> list[dict] | None`.
    - The function will:
        1. Call `get_user(user_id)` to verify the user exists.
        2. If user is not found, return `None`.
        3. If user is found, import `ITEMS` from `src.api.routes.items`.
        4. Return a list of items (as dicts) where `item.owner_id == user_id`.

## Test Plan
- Modify `benchmark-repo/tests/test_users.py`:
    - Import `list_user_items`.
    - Add `test_list_user_items_returns_items_for_user()`:
        - Call `list_user_items(1)`.
        - Assert it returns 2 items ("Notebook", "Pen").
    - Add `test_list_user_items_returns_none_for_missing_user()`:
        - Call `list_user_items(999)`.
        - Assert it returns `None`.

## Verification
- Run `cd benchmark-repo && pytest tests/test_users.py`.
- Run `cd benchmark-repo && pytest`.
