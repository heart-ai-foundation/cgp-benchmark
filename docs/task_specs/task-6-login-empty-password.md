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
