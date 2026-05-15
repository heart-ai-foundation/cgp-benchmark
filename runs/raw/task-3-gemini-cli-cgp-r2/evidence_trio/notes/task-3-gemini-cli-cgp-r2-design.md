# Design Note: User Items Endpoint (task-3-gemini-cli-cgp-r2)

## Rationale
The task required adding a function equivalent to a `GET /users/{user_id}/items` route. This function needs to return items belonging to a specific user. 

I implemented `get_user_items(user_id: int)` in `src/api/routes/users.py`. 
- It first validates the user exists using the existing `get_user` function.
- It then filters the `ITEMS` list (imported from `src.api.routes.items`) for items where `owner_id` matches the `user_id`.
- Items are returned as dictionaries using `item.as_dict()` to maintain consistency with other route functions like `list_items` and `get_item`.

## Scope
- `benchmark-repo/src/api/routes/users.py`: Added `get_user_items`.
- `benchmark-repo/tests/test_users.py`: Added `test_get_user_items_returns_items_for_user` and `test_get_user_items_returns_none_for_missing_user`.

## Verification Snapshot
Ran `pytest` in `benchmark-repo/`:
- `tests/test_users.py` passed (4 tests: 2 existing, 2 new).
- Full suite passed (11 tests).

```
tests/test_auth.py ..                                                    [ 18%]
tests/test_items.py ..                                                   [ 36%]
tests/test_users.py ....                                                 [ 72%]
tests/test_validators.py ...                                             [100%]

============================== 11 passed in 0.02s ==============================
```