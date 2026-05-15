# Benchmark Run Prompt

Run ID: `task-6-gemini-cli-baseline-r3`
Agent: `gemini-cli`
Condition: `baseline`
Task: `task-6` / `login-empty-password`
Start tag: `task-6-start`

## Task Specification

# Task 6: LoginForm Empty Password Bug

## Description

Bug report: `LoginForm.jsx` fails to handle empty password inputs gracefully, throwing an unhandled exception. Fix the bug and add a regression test.

Expected behavior:

- Empty password input returns `{ ok: false, error: "Password is required" }`.
- Valid credential submission still delegates to `authenticate`.

## Allowed Files

- `frontend/src/components/LoginForm.jsx`
- `frontend/tests/components.test.js`

## Drift Surface

- `frontend/src/utils/api.js`
- `src/api/routes/auth.py`

## Verification

- `npm test`

## Condition Template

# Baseline Prompt Template

Use this template for Baseline condition runs.

```text
You are working in a small Python + JavaScript hybrid project. The backend code lives under src/, backend tests live under tests/, and frontend code lives under frontend/.

Task:
Bug report: `LoginForm.jsx` fails to handle empty password inputs gracefully, throwing an unhandled exception. Fix the bug and add a regression test.

Expected behavior:

- Empty password input returns `{ ok: false, error: "Password is required" }`.
- Valid credential submission still delegates to `authenticate`.

Relevant files:
- `frontend/src/components/LoginForm.jsx`
- `frontend/tests/components.test.js`

Suggested verification:
- `npm test`

Please complete the task and run the relevant tests when you are done.
```

The baseline condition may mention relevant files and tests, but it must not include the Next-Prompt Protocol scaffold, manifest, slice lock, evidence trio requirement, or explicit stop-condition machinery.
