# Task 3 Design Note

Run ID: `task-3-codex-cgp-r3`

## Scope

Implemented the route-equivalent callable for `GET /users/{user_id}/items` in `benchmark-repo/src/api/routes/users.py` and added focused coverage in `benchmark-repo/tests/test_users.py`.

## Design

The new `list_user_items(user_id)` function follows the existing in-memory route style:

- resolves the user with the existing `get_user` helper
- returns `None` when no matching user exists, matching the repository's nullable single-resource route convention
- returns item dictionaries by reusing each item's `as_dict()` serializer
- uses `User.owns_item()` so the endpoint reflects the user model's item ownership contract

No drift-surface files were edited.

## Verification

- `cd benchmark-repo && pytest tests/test_users.py` passed with 4 tests.
- `cd benchmark-repo && pytest` passed with 11 tests.
