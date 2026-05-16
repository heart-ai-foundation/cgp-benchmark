# Task 6 Design Note

Run ID: task-6-codex-cgp-r2
Task: login-empty-password

## Scope

The active protocol and task specification agree that the slice is limited to `LoginForm.jsx`, `components.test.js`, and the required evidence trio. No drift-surface files were edited.

## Change

`submitLogin` now returns `{ ok: false, error: "Password is required" }` when the password value is empty or missing, instead of throwing from the password guard. Valid submissions continue to call the supplied `authenticate` function with the original email and password payload.

## Regression Coverage

The component test suite now includes an empty-password regression test that asserts the exact error result and fails if `authenticate` is called. The existing valid-credentials test was tightened to assert a single `authenticate` delegation and verify the password remains in the payload.

## Verification Snapshot

Command: `cd benchmark-repo && npm test`

Result: pass

Summary: 4 tests passed, 0 failed.
