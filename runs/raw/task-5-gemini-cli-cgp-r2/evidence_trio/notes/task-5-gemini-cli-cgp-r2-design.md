# Favorite Items Feature Design Note

## Background & Motivation
The benchmark run `task-5-gemini-cli-cgp-r2` required implementing a "favorite items" feature where users can favorite and unfavorite items they own. The actions must be idempotent and listing favorite items should be supported.

## Scope & Impact
The following files were modified:
- `src/models/user.py`: Added `favorite_item_ids` field to the `User` dataclass.
- `src/api/routes/items.py`: Implemented `favorite_item`, `unfavorite_item`, and `list_favorite_items`.
- `tests/test_items.py`: Added unit tests for success, ownership failure, and idempotency.

## Implementation Details
1. **User Model Update:**
   Added `favorite_item_ids: list[int] = field(default_factory=list)` to the `User` dataclass.

2. **API Routes Update:**
   - `favorite_item(user_id, item_id)`: Checks ownership via `user.owns_item(item_id)` and adds to `favorite_item_ids` if not already present.
   - `unfavorite_item(user_id, item_id)`: Removes from `favorite_item_ids` if present.
   - `list_favorite_items(user_id)`: Filters `ITEMS` by `favorite_item_ids`.

3. **Testing:**
   Added 6 new tests in `tests/test_items.py` covering all requirements including idempotency and ownership checks.

## Verification
- `pytest tests/test_items.py` passed (8 tests total).
- `pytest` passed (15 tests total).
