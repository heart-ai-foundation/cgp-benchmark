# Benchmark Run Prompt

Run ID: `task-1-codex-cgp-r3`
Agent: `codex`
Condition: `cgp`
Task: `task-1` / `input-validation`
Start tag: `task-1-start`

## Task Specification

# Task 1: Input Validation

## Description

Add a function `validate_email(email: str) -> bool` to `src/api/validators.py` that returns `True` if the email is well-formed and `False` otherwise. Add corresponding tests in `tests/test_validators.py`.

## Allowed Files

- `src/api/validators.py`
- `tests/test_validators.py`

## Drift Surface

- `src/api/routes/auth.py`
- `src/api/middleware.py`

## Verification

- `pytest tests/test_validators.py`
- `pytest`

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
5. next-prompt-protocols/active/task-1-codex-cgp-r3.md
6. The task specification at docs/task_specs/task-1-input-validation.md

Execute only the active slice. Stay inside allowed files. Preserve non-goals. Run the named verification commands before declaring completion. If the manifest, lock, active protocol, task spec, or repository state disagree on a load-bearing detail, stop and report rather than improvising.

Before declaring completion, write the evidence trio named in the active protocol:

1. Design note
2. Run record
3. Evidence JSON

Task:
Add a function `validate_email(email: str) -> bool` to `src/api/validators.py` that returns `True` if the email is well-formed and `False` otherwise. Add corresponding tests in `tests/test_validators.py`.
```

The CGP condition must include the same task content as Baseline while adding the operational scaffold: manifest, slice lock, role context, active protocol, explicit scope, verification, stop condition, and evidence requirements.
