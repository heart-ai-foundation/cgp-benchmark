# Design Note - task-3-claude-code-cgp-r1

## Run

- Run ID: `task-3-claude-code-cgp-r1`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-3` / `user-items-endpoint`
- Start tag: `task-3-start`
- HEAD at execution start: `b97caec2094faf36bb53603ef03a1ac3b5919642`

## Objective

Add a `GET /users/{user_id}/items` equivalent route function to
`src/api/routes/users.py` returning the items belonging to a specific user,
plus tests in `tests/test_users.py`. The benchmark app has no web framework,
so the route is a plain callable with route-equivalent behavior.

## Scope

Allowed files touched:

- `benchmark-repo/src/api/routes/users.py`
- `benchmark-repo/tests/test_users.py`

Drift surface (NOT modified):

- `benchmark-repo/src/api/routes/items.py` (imported as a read-only data source)
- `benchmark-repo/src/models/user.py`
- `benchmark-repo/src/api/middleware.py`

## Design rationale

- Added `get_user_items(user_id, include_archived=False) -> list[dict] | None`.
- Reused the existing `get_user` lookup to mirror the existing handler style
  in this module (single sequential scan over the in-module fixture list).
- Source of items is the existing `ITEMS` list from `src/api/routes/items.py`.
  This avoids duplicating the fixture and matches the established pattern
  where each routes module owns its own fixture and exposes it as a
  module-level constant.
- Filter is `item.owner_id == user.id`, consistent with `Item.owner_id`. The
  `User.item_ids` field was considered but `owner_id` is the canonical
  ownership edge used by `Item` and is what a real `/users/{id}/items`
  endpoint would join on.
- Unknown user returns `None` to mirror a 404 semantic, matching the existing
  `get_user` / `get_item` "missing -> None" convention in this codebase.
- `include_archived` defaults to `False`, matching `list_items` so the
  default view of a user's items hides archived rows.

## Tests added

- Items for user 1 are `["Notebook", "Pen"]` and all carry `owner_id == 1`.
- Items for user 2 are `["Backpack"]`.
- Unknown user id returns `None`.
- Archived items are omitted by default.

## Verification snapshot

- `cd benchmark-repo && pytest tests/test_users.py` -> 6 passed.
- `cd benchmark-repo && pytest` -> 13 passed.

## Stop-condition check

Manifest, slice lock, active protocol, task specification, and repository
state agree on objective, allowed files, and verification. No disagreement
encountered; no stop required.
