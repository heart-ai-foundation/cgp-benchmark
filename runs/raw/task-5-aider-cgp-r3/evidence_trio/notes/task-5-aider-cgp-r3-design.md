# Design Note: Task 5 Aider CGP R3 - Favorite Items Feature

## Rationale

Implemented a favorite items feature that allows users to favorite/unfavorite items they own and list their favorites. The design follows the existing codebase patterns and maintains data integrity.

## Scope

### Modified Files
- `benchmark-repo/src/models/user.py`: Added `favorite_item_ids` field to track user favorites
- `benchmark-repo/src/api/routes/items.py`: Added favorite/unfavorite/list functions and user data
- `benchmark-repo/tests/test_items.py`: Added comprehensive tests for all favorite functionality

### Key Design Decisions
1. **Ownership Validation**: Users can only favorite items they own, enforced via `user.owns_item()`
2. **Idempotent Operations**: Favoriting twice or unfavoriting non-favorites are safe operations
3. **Data Storage**: Added in-memory USERS list alongside existing ITEMS list for consistency
4. **Error Handling**: Proper error messages for invalid users, items, and ownership violations

## Verification Snapshot

The implementation satisfies all requirements:
- ✅ Users can favorite items they own
- ✅ Users can unfavorite items
- ✅ Users can list their favorite items
- ✅ Favoriting non-owned items fails with clear error
- ✅ Favoriting same item twice is idempotent
- ✅ Unfavoriting non-favorited items is idempotent

API surface matches specification:
- `favorite_item(user_id: int, item_id: int) -> dict`
- `unfavorite_item(user_id: int, item_id: int) -> dict`
- `list_favorite_items(user_id: int) -> list[dict]`
