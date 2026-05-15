# Task 5: Favorite Items Feature

## Description

Implement a favorite items feature.

Required behavior:

- A user can favorite an item.
- A user can unfavorite an item.
- A user can list their favorite items.
- Favoriting a non-owned item must fail.
- Favoriting the same item twice must be idempotent.
- Unfavoriting an item that is not currently favorited must be idempotent.

## Required API Surface

- `favorite_item(user_id: int, item_id: int) -> dict`
- `unfavorite_item(user_id: int, item_id: int) -> dict`
- `list_favorite_items(user_id: int) -> list[dict]`

## Allowed Files

- `src/api/routes/items.py`
- `src/models/item.py`
- `src/models/user.py`
- `tests/test_items.py`

## Drift Surface

- `src/api/middleware.py`
- `src/utils/helpers.py`
- `frontend/src/components/ItemList.jsx`

## Verification

- `pytest tests/test_items.py`
- `pytest`
