# Benchmark Run Prompt

Run ID: `task-6-codex-cgp-r3`
Agent: `codex`
Condition: `cgp`
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

# CGP Prompt Template

Use this template for CGP condition runs.

```text
You are executing a Continuity-Governed Prompting run using the Next-Prompt Protocol scaffold.

Before acting, read these files in order:

1. next-prompt-protocols/.slice-lock.json
2. next-prompt-protocols/manifest.json
3. next-prompt-protocols/role-context.md
4. next-prompt-protocols/phases/phase-1/README.md
5. next-prompt-protocols/active/task-6-codex-cgp-r3.md
6. The task specification at docs/task_specs/task-6-login-empty-password.md

Execute only the active slice. Stay inside allowed files. Preserve non-goals. Run the named verification commands before declaring completion. If the manifest, lock, active protocol, task spec, or repository state disagree on a load-bearing detail, stop and report rather than improvising.

Before declaring completion, write the evidence trio named in the active protocol:

1. Design note
2. Run record
3. Evidence JSON

Task:
Bug report: `LoginForm.jsx` fails to handle empty password inputs gracefully, throwing an unhandled exception. Fix the bug and add a regression test.

Expected behavior:

- Empty password input returns `{ ok: false, error: "Password is required" }`.
- Valid credential submission still delegates to `authenticate`.
```

The CGP condition must include the same task content as Baseline while adding the operational scaffold: manifest, slice lock, role context, active protocol, explicit scope, verification, stop condition, and evidence requirements.
