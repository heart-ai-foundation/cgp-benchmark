# Design Note - Task 5: Favorite Items Feature

## Rationale
The task required adding a favorite items feature to the benchmark repository. This involved extending the `User` model to track favorite items and providing API functions to manage these favorites.

## Implementation Details
1.  **Model Extension**: Added `favorite_item_ids` (a list of integers) to the `User` dataclass in `benchmark-repo/src/models/user.py`.
2.  **API Functions**: Implemented the following in `benchmark-repo/src/api/routes/items.py`:
    - `favorite_item`: Validates user existence and item ownership before adding to favorites. Ensures idempotency.
    - `unfavorite_item`: Removes item from favorites if present. Ensures idempotency.
    - `list_favorite_items`: Returns the full item details for all favorited items of a user.
3.  **Ownership Check**: Leveraged the existing `User.owns_item(item_id)` method to enforce that users can only favorite items they own.
4.  **Error Handling**: Used `ValueError` for failure cases (user not found, item not owned), consistent with the existing validation patterns in the codebase.

## Verification Results
- Added 6 new test cases to `benchmark-repo/tests/test_items.py`:
    - `test_favorite_item_success`
    - `test_favorite_item_not_owned`
    - `test_favorite_item_idempotent`
    - `test_unfavorite_item_success`
    - `test_unfavorite_item_idempotent`
    - `test_list_favorite_items`
- Ran `pytest tests/test_items.py` (8/8 passed).
- Ran `pytest` (15/15 passed).

## Scope Confirmation
- Changes were restricted to the `allowed_files` list:
    - `benchmark-repo/src/models/user.py`
    - `benchmark-repo/src/api/routes/items.py`
    - `benchmark-repo/tests/test_items.py`
- No changes were made to the drift surface or other files.
