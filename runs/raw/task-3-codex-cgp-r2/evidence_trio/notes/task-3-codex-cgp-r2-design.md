# Design Note: task-3-codex-cgp-r2

## Scope

Implemented the Task 3 user-items route-equivalent callable in `benchmark-repo/src/api/routes/users.py` and added focused coverage in `benchmark-repo/tests/test_users.py`.

## Design

- Added `list_user_items(user_id)` to represent `GET /users/{user_id}/items`.
- Reused the existing `get_user` lookup and `User.owns_item()` ownership helper.
- Reused the existing route-level `ITEMS` in `src.api.routes.items` and returned each item through `Item.as_dict()` so response shape matches existing item route behavior.
- Returned `None` when the user is unknown, matching the repository's existing `get_user` / `get_item` not-found style.
- Added `get_user_items` as a route-name alias for compatibility with the endpoint wording while keeping `list_user_items` as the primary collection-style function.

## Verification Snapshot

- `cd benchmark-repo && pytest tests/test_users.py`: passed, 4 tests.
- `cd benchmark-repo && pytest`: passed, 11 tests.

## Scope Control

Edited only allowed implementation/test files and the required evidence trio paths.
