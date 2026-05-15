# Design Note — task-5-claude-code-cgp-r2

## Run
- Run ID: `task-5-claude-code-cgp-r2`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-5` / `favorite-items`
- Metrics base commit (scaffold HEAD): `134139d89c33ca1a455af06ec19b29d7b425ec29`
- Task-start anchor (`current_commit` in lock/manifest): `2614dd699ae0c27e2d63ae30b18d349951c7a4c5`

## Objective
Implement a favorite items feature with the API surface
`favorite_item`, `unfavorite_item`, `list_favorite_items`, satisfying the six
behavioral requirements in the task spec.

## Scope
Stayed strictly within the allowed-files set declared in
`next-prompt-protocols/.slice-lock.json`:

- `benchmark-repo/src/api/routes/items.py`
- `benchmark-repo/src/models/user.py`
- `benchmark-repo/tests/test_items.py`
- evidence trio under `notes/`, `runs/`, `evidence/`

`benchmark-repo/src/models/item.py` was in the allowed set but did not require
modification: the favorite relation is per-user, so the `User` model carries
the foreign keys.

No drift-surface file (`middleware.py`, `helpers.py`, `ItemList.jsx`) was
touched.

## Design
- Store favorites on `User` as `favorite_item_ids: list[int]`, mirroring the
  existing `item_ids` pattern. This avoids introducing a new global table or
  collection and matches the codebase's in-module list-store style
  (`USERS`, `ITEMS`).
- `favorite_item` validates user existence, item existence, and ownership,
  then idempotently appends. Returns a status dict
  (`{"ok": bool, "user_id", "item_id", "favorited"}` or
  `{"ok": False, "error": ...}`).
- `unfavorite_item` idempotently removes. Returns success even when the item
  was not previously favorited (idempotent per spec).
- `list_favorite_items` returns full item dicts (via `Item.as_dict()`) for the
  user's favorite ids, preserving the dict shape already used by
  `list_items` / `get_item`.
- `User.has_favorited` added as a small convenience predicate paralleling
  `owns_item`.

## Non-owned item handling
Spec says "favoriting a non-owned item must fail." The chosen failure mode is
returning `{"ok": False, "error": "item_not_owned"}` rather than raising,
because the existing module-level functions return data structures, not
exceptions. This is consistent with the codebase's style and lets callers
discriminate without try/except. The user's favorites list is not mutated on
failure (verified by test).

## Verification snapshot
- `cd benchmark-repo && pytest tests/test_items.py` → 8 passed
- `cd benchmark-repo && pytest` → 15 passed (no regressions in auth, users,
  validators)

## Stop-condition check
Lock, manifest, role-context, active protocol, and task spec all agree on:
- task id (`task-5`), run id (`task-5-claude-code-cgp-r2`)
- allowed files
- verification commands
No disagreement encountered; no stop-and-report condition triggered.
