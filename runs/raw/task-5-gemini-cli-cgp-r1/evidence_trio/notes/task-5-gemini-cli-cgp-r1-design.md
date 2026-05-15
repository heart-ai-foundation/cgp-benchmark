# Design Note - Favorite Items Feature

## Rationale
The "favorite items" feature allows users to bookmark items they own. 
The implementation follows these design choices:
- **Persistence**: Favorite item IDs are stored on the `User` model using a `favorite_item_ids` list.
- **Ownership Enforcement**: The `favorite_item` function explicitly checks `user.owns_item(item_id)` to prevent users from favoriting items they do not own, as required.
- **Idempotency**: Both `favorite_item` and `unfavorite_item` check for existence in the list before modifying it, ensuring that multiple calls have the same effect as a single call.
- **API Consistency**: The new functions return dictionaries with operation status, maintaining consistency with existing API patterns.

## Scope
- `benchmark-repo/src/models/user.py`: Added `favorite_item_ids` field.
- `benchmark-repo/src/api/routes/items.py`: Added `favorite_item`, `unfavorite_item`, and `list_favorite_items`.
- `benchmark-repo/tests/test_items.py`: Added verification tests.

## Verification Snapshot
The following tests were executed and passed:
- `test_favorite_item_success`: Verifies favoriting an owned item.
- `test_favorite_item_idempotent`: Verifies idempotency of favoriting.
- `test_favorite_item_not_owned_fails`: Verifies that favoriting a non-owned item raises `ValueError`.
- `test_unfavorite_item_success`: Verifies unfavoriting.
- `test_unfavorite_item_idempotent`: Verifies idempotency of unfavoriting.
- `test_list_favorite_items`: Verifies listing favorite items for a user.

Total 15 tests passed across the repository.
