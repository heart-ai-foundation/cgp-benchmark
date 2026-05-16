# Task 5 Design Note

## Scope

Implemented the favorite items API surface inside the allowed item route and user model files:

- `favorite_item(user_id: int, item_id: int) -> dict`
- `unfavorite_item(user_id: int, item_id: int) -> dict`
- `list_favorite_items(user_id: int) -> list[dict]`

## Design

Favorite state is stored as `User.favorite_item_ids`, matching the existing in-memory `User.item_ids` ownership model. The item route uses the existing `get_user()` registry lookup and `User.owns_item()` to enforce that favoriting non-owned items fails.

Idempotency is handled by checking membership before appending during favorite and checking membership before removal during unfavorite. Listing returns serialized item dictionaries in the existing `ITEMS` order.

## Verification Snapshot

- `cd benchmark-repo && pytest tests/test_items.py`: passed, 7 tests.
- `cd benchmark-repo && pytest`: passed, 14 tests.
