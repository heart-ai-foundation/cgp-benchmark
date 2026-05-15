# Design Note - task-5-claude-code-cgp-r1

## Run

- Run ID: `task-5-claude-code-cgp-r1`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-5` / `favorite-items`
- Start tag: `task-5-start`

## Objective

Implement a favorite items feature satisfying the behaviors in
`docs/task_specs/task-5-favorite-items.md`: favorite, unfavorite, list
favorites, reject favoriting non-owned items, idempotent favorite/unfavorite.

## Scope

Only files listed in the active protocol were modified:

- `benchmark-repo/src/api/routes/items.py` - added `favorite_item`,
  `unfavorite_item`, `list_favorite_items`, and a private `_find_item` helper.
- `benchmark-repo/src/models/user.py` - added `favorite_item_ids: list[int]`
  field defaulting to an empty list.
- `benchmark-repo/tests/test_items.py` - added tests for all required
  behaviors (favorite, unfavorite, idempotency in both directions,
  rejection of non-owned items, list-favorites) plus an autouse fixture
  that snapshots and restores per-user favorites to keep tests isolated
  given the module-level in-memory `USERS` store.

`benchmark-repo/src/models/item.py` was listed as allowed but not edited;
no change to the `Item` schema was required since favorites are owned by
the `User`.

## Design rationale

- Favorites live on `User.favorite_item_ids` rather than on `Item`. The
  spec ties favorites to a specific user; storing the relation on the
  user keeps the `Item` model agnostic of viewer state and mirrors the
  existing `item_ids` ownership list.
- Ownership is the gate for favoriting. The spec says "Favoriting a
  non-owned item must fail", so we raise `ValueError` when the user does
  not own the item. The signature returns `dict` on success.
- Idempotency: `favorite_item` appends only if the id is not already in
  the list; `unfavorite_item` removes only if present. Both return a
  consistent result dict either way.
- `list_favorite_items` resolves each favorite id against the in-memory
  `ITEMS` list and returns the item's `as_dict()` payload. Missing items
  are skipped defensively (cannot happen with the current seed data, but
  guards against stale references if items are later removed).
- The route module imports `get_user` from `src.api.routes.users`. That
  module is read-only for this task; only its API was used.

## Non-goals respected

- No edits outside the allowed-files set. `src/api/routes/users.py`,
  `src/api/middleware.py`, `src/utils/helpers.py`, and
  `frontend/src/components/ItemList.jsx` were not modified.
- No adjacent refactors. No changes to run plan, preregistration,
  scaffold, or analysis files.

## Verification snapshot

- `cd benchmark-repo && pytest tests/test_items.py` - 9 passed.
- `cd benchmark-repo && pytest` - 16 passed.
