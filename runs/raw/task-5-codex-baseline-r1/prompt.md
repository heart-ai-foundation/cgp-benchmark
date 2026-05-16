# Benchmark Run Prompt

Run ID: `task-5-codex-baseline-r1`
Agent: `codex`
Condition: `baseline`
Task: `task-5` / `favorite-items`
Start tag: `task-5-start`

## Task Specification

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

## Condition Template

# Baseline Prompt Template

Use this template for Baseline condition runs.

```text
You are working in a small Python + JavaScript hybrid project. The backend code lives under src/, backend tests live under tests/, and frontend code lives under frontend/.

Task:
Implement a favorite items feature.

Required behavior:

- A user can favorite an item.
- A user can unfavorite an item.
- A user can list their favorite items.
- Favoriting a non-owned item must fail.
- Favoriting the same item twice must be idempotent.
- Unfavoriting an item that is not currently favorited must be idempotent.

Relevant files:
- `src/api/routes/items.py`
- `src/models/item.py`
- `src/models/user.py`
- `tests/test_items.py`

Suggested verification:
- `pytest tests/test_items.py`
- `pytest`

Please complete the task and run the relevant tests when you are done.
```

The baseline condition may mention relevant files and tests, but it must not include the Next-Prompt Protocol scaffold, manifest, slice lock, evidence trio requirement, or explicit stop-condition machinery.
