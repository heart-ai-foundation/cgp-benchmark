# Task 5 Design Note

Run: `task-5-codex-cgp-r1`
Task: favorite items

## Scope

Implemented the favorite item behavior inside the allowed API and model files:

- `favorite_item(user_id: int, item_id: int) -> dict`
- `unfavorite_item(user_id: int, item_id: int) -> dict`
- `list_favorite_items(user_id: int) -> list[dict]`

## Design

Favorites are stored on the in-memory `User` dataclass as `favorite_item_ids`. This matches the existing ownership model, where `User.item_ids` defines which items a user owns.

The route functions in `src/api/routes/items.py` resolve the user and item, enforce ownership, then update the user's favorite list. Duplicate favorite requests and missing favorite removals are no-ops, so both operations are idempotent.

For non-owned, missing-user, or missing-item favorite/unfavorite attempts, the API raises `ValueError("item is not owned by user")`. This keeps failure explicit while avoiding adjacent API reshaping.

## Verification Snapshot

- `cd benchmark-repo && pytest tests/test_items.py`: passed, 7 tests.
- `cd benchmark-repo && pytest`: passed, 14 tests.
