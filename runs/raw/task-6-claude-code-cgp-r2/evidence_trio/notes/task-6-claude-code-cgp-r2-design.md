# Design Note - task-6-claude-code-cgp-r2

## Run

- Run ID: `task-6-claude-code-cgp-r2`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-6` / `login-empty-password`
- Phase: `phase-1`
- HEAD at execution: `eebfef0d42f375daecc81b7e0d65d4beb54a9f5b`

## Problem

`benchmark-repo/frontend/src/components/LoginForm.jsx` threw an unhandled
`Error("Password is required")` when `password` was empty. Spec requires the
function instead return `{ ok: false, error: "Password is required" }` and
continue to delegate valid credentials to `authenticate`.

## Change

In `LoginForm.jsx`, replaced the `throw` branch with a structured return:

```js
if (!password) {
  return { ok: false, error: "Password is required" };
}
```

The truthiness check covers both empty string and `undefined`/`null` password
inputs, which is consistent with the existing `!email` guard one block above.

## Regression Test

Added `submitLogin returns error for empty password` to
`benchmark-repo/frontend/tests/components.test.js`. It asserts:

1. `result.ok === false`
2. `result.error === "Password is required"`
3. `authenticate` is not invoked when the password is missing.

The pre-existing `submitLogin delegates valid credentials` test continues to
cover the success path.

## Scope discipline

Edits limited to the allowed-files set:

- `benchmark-repo/frontend/src/components/LoginForm.jsx`
- `benchmark-repo/frontend/tests/components.test.js`
- `notes/task-6-claude-code-cgp-r2-design.md`
- `runs/task-6-claude-code-cgp-r2-run-record.json`
- `evidence/task-6-claude-code-cgp-r2-evidence.json`

No edits to drift surface (`frontend/src/utils/api.js`,
`src/api/routes/auth.py`) or to scaffold, run-plan, preregistration, or
analysis files.

## Verification

`cd benchmark-repo && npm test` - 4 tests, 4 pass, 0 fail.
