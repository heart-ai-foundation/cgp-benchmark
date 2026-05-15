# Design Note - task-6-aider-cgp-r1

## Run

- Run ID: `task-6-aider-cgp-r1`
- Agent: `aider`
- Condition: `cgp`
- Task: `task-6` / `login-empty-password`
- Start tag: `task-6-start`
- Metrics base commit (HEAD at run start): `7062038a24877b45046b2f1d0a31607aab650f03`

## Objective

Bug report: `LoginForm.jsx` threw an unhandled `Error("Password is required")` when the password was empty. Replace that with a structured failure return and add a regression test, without altering valid-credential behavior.

Expected behavior:

- Empty password input returns `{ ok: false, error: "Password is required" }`.
- Valid credential submission still delegates to `authenticate`.

## Scope

Allowed files touched:

- `benchmark-repo/frontend/src/components/LoginForm.jsx`
- `benchmark-repo/frontend/tests/components.test.js`

Evidence trio written:

- `notes/task-6-aider-cgp-r1-design.md`
- `runs/task-6-aider-cgp-r1-run-record.json`
- `evidence/task-6-aider-cgp-r1-evidence.json`

Drift surface (not touched):

- `benchmark-repo/frontend/src/utils/api.js`
- `benchmark-repo/src/api/routes/auth.py`

## Change rationale

`LoginForm.submitLogin` previously checked `password.length < 1` and threw. Two problems:

1. Throwing on a routine validation failure is inconsistent with the email branch above it, which returns a structured `{ ok: false, error }` object. The task specification mandates the structured return shape for empty password.
2. Accessing `.length` on an `undefined` password would throw a different, less informative `TypeError` before the intended `Error` ever fired.

Replaced the predicate with `!password`, which treats both `""` and `undefined` as empty and returns the structured failure. This matches the existing email branch's idiom and the task spec verbatim.

Added a regression test `submitLogin returns error for empty password` that asserts the exact return shape and that `authenticate` is not invoked (the injected authenticator throws if called).

## Verification

`cd benchmark-repo && npm test` - 4/4 tests pass (3 prior + 1 new regression test).

## Non-goals preserved

- No edits to `frontend/src/utils/api.js` or `src/api/routes/auth.py` (drift surface).
- No adjacent refactor; only the password branch and one new test were added.
- No edits to run-plan, preregistration, scaffold, or analysis files.
