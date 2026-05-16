# Design Note: task-3-aider-cgp-r2

## Objective
Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` that returns the items belonging to a specific user.

## Implementation Approach
1. Added `get_user_items(user_id: int) -> list[dict]` function to `users.py`
2. Function leverages existing `get_user()` to find the user
3. Filters items from `ITEMS` list based on user's `item_ids` field
4. Returns items in dictionary format using `item.as_dict()`
5. Returns empty list for non-existent users

## Design Rationale
- Reuses existing `get_user()` function for consistency
- Follows same pattern as `get_item()` in returning dict format
- Handles edge case of non-existent user gracefully
- Imports `ITEMS` from items module to access item data

## Test Coverage
- Tests successful retrieval of user items
- Tests handling of non-existent user
- Tests correct filtering for different users
- Verifies item names and counts match expectations

## Scope
Changes limited to allowed files:
- `src/api/routes/users.py` - added function and import
- `tests/test_users.py` - added comprehensive tests
