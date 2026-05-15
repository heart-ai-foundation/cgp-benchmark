# Design Note - Task 3: User Items Endpoint

## Rationale
The goal is to provide an endpoint equivalent that retrieves all items belonging to a specific user. 
In this benchmark app, "routes" are represented as callable functions.
The `User` model has `item_ids`, and the `Item` model has `owner_id`. 
The existing `ITEMS` list in `src/api/routes/items.py` contains the item data.
To implement `get_user_items(user_id)`, I will filter the `ITEMS` list for items where `owner_id == user_id`.

## Planned Changes

### `src/api/routes/users.py`
- Import `ITEMS` from `src.api.routes.items`.
- Implement `get_user_items(user_id: int) -> list[dict]`.

### `tests/test_users.py`
- Add a test case `test_get_user_items_returns_items_for_user` to verify that the function returns the correct items for a valid user.
- Add a test case `test_get_user_items_returns_empty_list_for_nonexistent_user` to verify behavior for a user with no items or a non-existent user.

## Verification Snapshot
- `pytest tests/test_users.py`
- `pytest`
