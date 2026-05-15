# Benchmark Run Prompt

Run ID: `task-5-claude-code-cgp-r1`
Agent: `claude-code`
Condition: `cgp`
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

# CGP Prompt Template

Use this template for CGP condition runs.

```text
You are executing a Continuity-Governed Prompting run using the Next-Prompt Protocol scaffold.

Before acting, read these files in order:

1. next-prompt-protocols/.slice-lock.json
2. next-prompt-protocols/manifest.json
3. next-prompt-protocols/role-context.md
4. next-prompt-protocols/phases/phase-1/README.md
5. next-prompt-protocols/active/task-5-claude-code-cgp-r1.md
6. The task specification at docs/task_specs/task-5-favorite-items.md

Execute only the active slice. Stay inside allowed files. Preserve non-goals. Run the named verification commands before declaring completion. If the manifest, lock, active protocol, task spec, or repository state disagree on a load-bearing detail, stop and report rather than improvising.

Before declaring completion, write the evidence trio named in the active protocol:

1. Design note
2. Run record
3. Evidence JSON

Task:
Implement a favorite items feature.

Required behavior:

- A user can favorite an item.
- A user can unfavorite an item.
- A user can list their favorite items.
- Favoriting a non-owned item must fail.
- Favoriting the same item twice must be idempotent.
- Unfavoriting an item that is not currently favorited must be idempotent.
```

The CGP condition must include the same task content as Baseline while adding the operational scaffold: manifest, slice lock, role context, active protocol, explicit scope, verification, stop condition, and evidence requirements.
