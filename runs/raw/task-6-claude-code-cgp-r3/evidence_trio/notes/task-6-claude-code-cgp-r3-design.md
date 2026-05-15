# Design Note - task-6-claude-code-cgp-r3

## Run

- Run ID: `task-6-claude-code-cgp-r3`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-6` / `login-empty-password`
- Phase: `phase-1`

## Problem

`submitLogin` in `frontend/src/components/LoginForm.jsx` raised
`new Error("Password is required")` when the password was empty. The
specification requires returning `{ ok: false, error: "Password is required" }`
in that branch, matching the existing email-missing branch.

## Fix

Replaced the `throw` branch with a structured return mirroring the email-missing
branch. The check `if (!password)` covers empty string and any other falsy
input that previously would have thrown when accessing `password.length`. Valid
credentials still flow through to `authenticate`.

## Scope

Only the two files in the task spec's allowed-file set were modified:

- `benchmark-repo/frontend/src/components/LoginForm.jsx` - swap throw for return.
- `benchmark-repo/frontend/tests/components.test.js` - add regression test.

No edits to drift-surface files (`frontend/src/utils/api.js`,
`src/api/routes/auth.py`) and no adjacent refactors.

## Verification

`cd benchmark-repo && npm test` - 4 tests pass, including the new
`submitLogin rejects empty password without throwing` regression test which
asserts the structured return and that `authenticate` is not called.
