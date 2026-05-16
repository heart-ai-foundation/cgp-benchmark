# Design Note: Task 3 User Items Endpoint

## Objective
Add a `GET /users/{user_id}/items` equivalent route function to return items belonging to a specific user.

## Implementation Approach
1. Added `get_user_items(user_id: int, include_archived: bool = False)` function to `src/api/routes/users.py`
2. Function imports `ITEMS` from `src.api.routes.items` to access item data
3. Uses existing `get_user()` function to validate user existence
4. Filters items by `owner_id` matching the requested `user_id`
5. Respects the `include_archived` parameter to filter archived items by default
6. Returns list of item dictionaries using `item.as_dict()` method

## Design Decisions
- Reused existing patterns from `items.py` for consistency (include_archived parameter, as_dict() usage)
- Returns empty list for non-existent users rather than raising exceptions
- Leveraged existing `get_user()` function for user validation
- Maintained separation of concerns by importing items data rather than duplicating logic

## Test Coverage
- Basic functionality: returns correct items for valid user
- Edge case: returns empty list for non-existent user  
- Archived filtering: tests both default behavior and explicit include_archived=True
- Integration: works with existing user and item data structures

## Verification
Function follows route-equivalent behavior pattern established in the codebase.
