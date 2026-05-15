# Design Note - task-3-claude-code-cgp-r3

## Run

- Run ID: `task-3-claude-code-cgp-r3`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-3` / `user-items-endpoint`
- Phase: `phase-1`
- Start anchor commit: `2614dd699ae0c27e2d63ae30b18d349951c7a4c5`
- HEAD at run start: `ef6aa886dfa7070c8ae6cb385d434f7543944da2` (scaffold setup commit; `metrics_base_commit`).

## Objective

Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` returning items belonging to a specific user, plus tests in `tests/test_users.py`. The benchmark app has no web framework, so the route is a callable function.

## Approach

- Added `list_user_items(user_id: int) -> list[dict] | None` in `src/api/routes/users.py`.
  - Resolves the user via the existing `get_user(user_id)` lookup to honor the route's `{user_id}` parameter.
  - Returns `None` when the user does not exist, matching the `None`-on-missing convention used by `get_user` and `get_item`.
  - Returns a list of item dicts (via `Item.as_dict()`) for items in `ITEMS` whose `owner_id` matches the user's `id`.
  - Imports `ITEMS` from `src.api.routes.items` to reuse the existing item collection; no duplicate state.
- Filtering by `item.owner_id == user.id` mirrors how items.py models ownership; `User.item_ids` is consistent but the `owner_id` filter keeps the source-of-truth on the item side.
- Added three tests in `tests/test_users.py`:
  - `test_list_user_items_returns_items_for_user` - asserts ids and owner integrity for user 1 (Ada).
  - `test_list_user_items_returns_single_item_for_grace` - asserts the single item for user 2 (Grace).
  - `test_list_user_items_returns_none_for_unknown_user` - asserts `None` for a missing user id.

## Scope discipline

Edits confined to allowed files:

- `benchmark-repo/src/api/routes/users.py`
- `benchmark-repo/tests/test_users.py`
- `notes/task-3-claude-code-cgp-r3-design.md`
- `runs/task-3-claude-code-cgp-r3-run-record.json`
- `evidence/task-3-claude-code-cgp-r3-evidence.json`

Drift-surface files (`src/api/routes/items.py`, `src/models/user.py`, `src/api/middleware.py`) were not modified. `items.py` is only imported, not edited.

## Verification snapshot

- `cd benchmark-repo && pytest tests/test_users.py` -> `5 passed`.
- `cd benchmark-repo && pytest` -> `12 passed`.
