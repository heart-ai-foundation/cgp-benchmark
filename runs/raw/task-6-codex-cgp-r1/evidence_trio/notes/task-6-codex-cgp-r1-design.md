# Task 6 Design Note

## Scope

Active slice: `task-6-codex-cgp-r1`.

Allowed implementation files:

- `benchmark-repo/frontend/src/components/LoginForm.jsx`
- `benchmark-repo/frontend/tests/components.test.js`

## Change

`submitLogin` now returns `{ ok: false, error: "Password is required" }` when the supplied password is empty instead of throwing an exception.

The valid credential test now counts calls to the supplied `authenticate` callback to verify that valid submissions still delegate exactly once.

## Regression Coverage

Added a regression test for an empty password that asserts the exact error response and fails if `authenticate` is called.

## Verification

Command:

```sh
cd benchmark-repo && npm test
```

Result: passed. Four tests passed, including the new empty-password regression.
