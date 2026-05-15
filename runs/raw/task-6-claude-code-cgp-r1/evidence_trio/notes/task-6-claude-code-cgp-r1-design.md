# Design Note - task-6-claude-code-cgp-r1

## Run

- Run ID: `task-6-claude-code-cgp-r1`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-6` / `login-empty-password`
- Metrics base commit: `7f75a360f508fb3f485cb8c4b5e79873d1648ecd`

## Problem

`submitLogin` in `frontend/src/components/LoginForm.jsx` threw an unhandled
`Error("Password is required")` when the password was empty, and would also
have thrown a `TypeError` if `password` were missing entirely (because the
guard read `password.length`). The expected behavior, per the task
specification, is a structured failure result:
`{ ok: false, error: "Password is required" }`.

## Change

In `LoginForm.jsx`, replace the throwing branch with a returned error object,
using a falsy check so both `""` and `undefined`/`null` are handled without
ever evaluating `.length` on a missing value:

```js
if (!password) {
  return { ok: false, error: "Password is required" };
}
```

The valid-credential path is untouched and still delegates to `authenticate`.

In `frontend/tests/components.test.js`, add a regression test
`"submitLogin returns error for empty password"` that calls `submitLogin`
with `password: ""` and an `authenticate` stub that throws if invoked. The
test asserts the exact shape `{ ok: false, error: "Password is required" }`,
guaranteeing both the new return contract and that `authenticate` is not
called for an empty password.

## Scope discipline

Edits limited to the two allowed task files plus the evidence trio:

- `benchmark-repo/frontend/src/components/LoginForm.jsx`
- `benchmark-repo/frontend/tests/components.test.js`
- `notes/task-6-claude-code-cgp-r1-design.md`
- `runs/task-6-claude-code-cgp-r1-run-record.json`
- `evidence/task-6-claude-code-cgp-r1-evidence.json`

Drift-surface files (`frontend/src/utils/api.js`, `src/api/routes/auth.py`)
were not opened or modified. No adjacent refactors were performed.

## Verification snapshot

`cd benchmark-repo && npm test` -> 4 passed, 0 failed (added regression
test `submitLogin returns error for empty password` plus the three
pre-existing tests).
