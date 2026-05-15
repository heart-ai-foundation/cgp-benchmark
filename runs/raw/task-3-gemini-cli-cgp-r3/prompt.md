# Benchmark Run Prompt

Run ID: `task-3-gemini-cli-cgp-r3`
Agent: `gemini-cli`
Condition: `cgp`
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

# CGP Prompt Template

Use this template for CGP condition runs.

```text
You are executing a Continuity-Governed Prompting run using the Next-Prompt Protocol scaffold.

Before acting, read these files in order:

1. next-prompt-protocols/.slice-lock.json
2. next-prompt-protocols/manifest.json
3. next-prompt-protocols/role-context.md
4. next-prompt-protocols/phases/phase-1/README.md
5. next-prompt-protocols/active/task-3-gemini-cli-cgp-r3.md
6. The task specification at docs/task_specs/task-3-user-items-endpoint.md

Execute only the active slice. Stay inside allowed files. Preserve non-goals. Run the named verification commands before declaring completion. If the manifest, lock, active protocol, task spec, or repository state disagree on a load-bearing detail, stop and report rather than improvising.

Before declaring completion, write the evidence trio named in the active protocol:

1. Design note
2. Run record
3. Evidence JSON

Task:
Add a `GET /users/{user_id}/items` equivalent route function to `src/api/routes/users.py` that returns the items belonging to a specific user. Add tests in `tests/test_users.py`.

Because the benchmark app does not depend on a web framework, the route is represented as a callable function with route-equivalent behavior.
```

The CGP condition must include the same task content as Baseline while adding the operational scaffold: manifest, slice lock, role context, active protocol, explicit scope, verification, stop condition, and evidence requirements.
