# Task 3 Design Note

Run ID: `task-3-codex-cgp-r1`

## Scope

Implemented the route-equivalent callable for `GET /users/{user_id}/items` in `benchmark-repo/src/api/routes/users.py` and added focused tests in `benchmark-repo/tests/test_users.py`.

## Design

- Added `list_user_items(user_id: int) -> list[dict]`.
- Reused the existing in-memory `ITEMS` fixture and each item's `as_dict()` serializer so the response shape matches the existing item route payloads.
- Reused `get_user()` and `User.owns_item()` while also checking `item.owner_id`, keeping the result constrained to items that belong to the requested user.
- Returned an empty list for an unknown user because this route-equivalent callable returns a collection and the task did not define a framework-level 404 response.

## Verification Snapshot

- `cd benchmark-repo && pytest tests/test_users.py`: passed, 5 tests.
- `cd benchmark-repo && pytest`: passed, 12 tests.
