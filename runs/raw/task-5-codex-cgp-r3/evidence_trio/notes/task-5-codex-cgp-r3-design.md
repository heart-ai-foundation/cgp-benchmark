# Task 5 Design Note

Run ID: `task-5-codex-cgp-r3`

## Scope

Implemented the favorite items feature inside the allowed files:

- `benchmark-repo/src/api/routes/items.py`
- `benchmark-repo/src/models/user.py`
- `benchmark-repo/tests/test_items.py`

`benchmark-repo/src/models/item.py` did not require changes.

## Design

Favorite state is stored on each `User` as `favorite_item_ids`, matching the existing in-memory ownership model where users already hold `item_ids`.

The public item route API now includes:

- `favorite_item(user_id: int, item_id: int) -> dict`
- `unfavorite_item(user_id: int, item_id: int) -> dict`
- `list_favorite_items(user_id: int) -> list[dict]`

Favoriting and unfavoriting both validate that the user exists, the item exists, and the item is owned by that user. A non-owned item raises `ValueError`, so the operation fails without mutating favorite state.

Idempotency is handled in the `User` model:

- Favoriting an already favorited item does not duplicate it.
- Unfavoriting a non-favorited item leaves state unchanged.

## Verification Snapshot

- `cd benchmark-repo && pytest tests/test_items.py`: passed, 7 tests.
- `cd benchmark-repo && pytest`: passed, 14 tests.
