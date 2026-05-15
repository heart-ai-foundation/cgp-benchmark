# Design Note - task-6-aider-cgp-r2

## Run

- Run ID: `task-6-aider-cgp-r2`
- Agent: `aider`
- Condition: `cgp`
- Task: `task-6` / `login-empty-password`
- Start tag: `task-6-start`

## Rationale

`submitLogin` in `benchmark-repo/frontend/src/components/LoginForm.jsx` threw an
unhandled `Error("Password is required")` when password was empty. The
specification requires the function to return
`{ ok: false, error: "Password is required" }` for empty passwords, mirroring
the existing empty-email branch which already returns
`{ ok: false, error: "Email is required" }`.

## Change scope

- `benchmark-repo/frontend/src/components/LoginForm.jsx`
  - Replaced the throwing `password.length < 1` branch with an early return of
    `{ ok: false, error: "Password is required" }`. The check uses `!password`
    so undefined/null and empty-string are all rejected consistently with the
    existing email check.
- `benchmark-repo/frontend/tests/components.test.js`
  - Added regression test `submitLogin returns error for empty password` that
    asserts the new return shape and verifies `authenticate` is not invoked.
  - Pre-existing test `submitLogin delegates valid credentials` is unchanged
    and continues to cover the happy path.

## Files in play

- `benchmark-repo/frontend/src/components/LoginForm.jsx`
- `benchmark-repo/frontend/tests/components.test.js`

## Non-goals honored

- No edits to drift-surface files (`frontend/src/utils/api.js`,
  `src/api/routes/auth.py`).
- No edits to run-plan, preregistration, scaffold, or analysis files.
- No adjacent refactors of `LoginForm.jsx` or `components.test.js`.

## Verification snapshot

- Command: `cd benchmark-repo && npm test`
- Result: 4 tests pass, 0 fail.
