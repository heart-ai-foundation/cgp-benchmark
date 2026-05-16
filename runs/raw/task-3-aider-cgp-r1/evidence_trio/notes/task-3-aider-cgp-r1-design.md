# Design Note: task-3-aider-cgp-r1

## Objective
Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` that returns the items belonging to a specific user.

## Implementation Approach
1. Added `get_user_items(user_id: int) -> list[dict]` function to `users.py`
2. Function imports ITEMS from `items.py` to access item data
3. Uses existing `get_user()` function to validate user exists
4. Filters items by `owner_id` matching the requested `user_id`
5. Returns list of item dictionaries using `item.as_dict()`

## Design Decisions
- Returns empty list for non-existent users (graceful degradation)
- Leverages existing `get_user()` for user validation
- Follows established pattern of returning dictionaries from route functions
- Uses `item.as_dict()` for consistent serialization

## Test Coverage
- Test successful retrieval of multiple items for user 1
- Test single item retrieval for user 2  
- Test empty list return for non-existent user
- Verify correct owner_id filtering

## Verification
- All existing tests continue to pass
- New functionality tested comprehensively
