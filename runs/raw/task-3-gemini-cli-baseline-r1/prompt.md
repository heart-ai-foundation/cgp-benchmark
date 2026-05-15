# Benchmark Run Prompt

Run ID: `task-3-gemini-cli-baseline-r1`
Agent: `gemini-cli`
Condition: `baseline`
Task: `task-3` / `user-items-endpoint`
Start tag: `task-3-start`

## Task Specification

# Task 3: User Items Endpoint

## Description

Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` that returns the items belonging to a specific user. Add tests in `tests/test_users.py`.

Because the benchmark app does not depend on a web framework, the route is represented as a callable function with route-equivalent behavior.

## Allowed Files

- `src/api/routes/users.py`
- `tests/test_users.py`

## Drift Surface

- `src/api/routes/items.py`
- `src/models/user.py`
- `src/api/middleware.py`

## Verification

- `pytest tests/test_users.py`
- `pytest`

## Condition Template

# Baseline Prompt Template

Use this template for Baseline condition runs.

```text
You are working in a small Python + JavaScript hybrid project. The backend code lives under src/, backend tests live under tests/, and frontend code lives under frontend/.

Task:
Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` that returns the items belonging to a specific user. Add tests in `tests/test_users.py`.

Because the benchmark app does not depend on a web framework, the route is represented as a callable function with route-equivalent behavior.

Relevant files:
- `src/api/routes/users.py`
- `tests/test_users.py`

Suggested verification:
- `pytest tests/test_users.py`
- `pytest`

Please complete the task and run the relevant tests when you are done.
```

The baseline condition may mention relevant files and tests, but it must not include the Next-Prompt Protocol scaffold, manifest, slice lock, evidence trio requirement, or explicit stop-condition machinery.
